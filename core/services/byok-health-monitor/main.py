"""
BYOK Health Monitoring Service
Continuously monitors and validates tenant API keys with automated alerts
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json

import redis.asyncio as redis
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select, update, and_

# Import shared components
from shared.auth.jwt_auth import get_current_user, UserContext
from shared.database.models import Base, Integration, Tenant
from shared.credential_management import get_key_resolution_service
from shared.vault.vault_client import VaultClient

# Import platform API clients for validation
import sys
sys.path.append('../marketing-automation-service')
from platform_apis import GoogleAdsClient, MetaAdsClient, LinkedInAdsClient

logger = logging.getLogger(__name__)

# Database Configuration
DATABASE_URL = "postgresql+asyncpg://admin:securepassword@host.docker.internal:5432/bizosaas"
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Redis Configuration
redis_client = None

# Response Models
class HealthStatus(BaseModel):
    platform: str
    tenant_id: str
    is_healthy: bool
    last_check: datetime
    error_message: Optional[str] = None
    expires_at: Optional[datetime] = None
    api_quota_remaining: Optional[int] = None
    health_score: float  # 0.0 to 1.0

class TenantHealthSummary(BaseModel):
    tenant_id: str
    overall_health_score: float
    healthy_platforms: int
    total_platforms: int
    critical_issues: List[str]
    warnings: List[str]
    last_check: datetime

class AlertConfig(BaseModel):
    tenant_id: str
    platform: str
    enabled: bool = True
    health_threshold: float = 0.8  # Alert if health drops below this
    quota_threshold: int = 1000  # Alert if quota drops below this
    expiry_warning_days: int = 7  # Alert if credentials expire in X days

# Background Tasks
class BYOKHealthMonitor:
    """Background health monitoring service"""
    
    def __init__(self, db_session_factory, redis_client: redis.Redis):
        self.db_session_factory = db_session_factory
        self.redis_client = redis_client
        self.monitoring_active = False
        self.check_interval = 300  # 5 minutes
        self.alert_cooldown = 3600  # 1 hour between alerts
        
    async def start_monitoring(self):
        """Start background health monitoring"""
        self.monitoring_active = True
        logger.info("Starting BYOK health monitoring")
        
        while self.monitoring_active:
            try:
                await self._run_health_checks()
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Health monitoring error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    async def stop_monitoring(self):
        """Stop background health monitoring"""
        self.monitoring_active = False
        logger.info("Stopped BYOK health monitoring")
    
    async def _run_health_checks(self):
        """Run health checks for all tenant integrations"""
        async with self.db_session_factory() as session:
            # Get all active integrations
            stmt = select(Integration).where(Integration.status == "active")
            result = await session.execute(stmt)
            integrations = result.scalars().all()
            
            logger.info(f"Running health checks for {len(integrations)} integrations")
            
            # Process in batches to avoid overwhelming APIs
            batch_size = 10
            for i in range(0, len(integrations), batch_size):
                batch = integrations[i:i + batch_size]
                await asyncio.gather(*[
                    self._check_integration_health(integration, session)
                    for integration in batch
                ], return_exceptions=True)
                
                # Small delay between batches
                await asyncio.sleep(1)
    
    async def _check_integration_health(self, integration: Integration, session: AsyncSession):
        """Check health of a specific integration"""
        try:
            key_service = get_key_resolution_service()
            resolved_creds = await key_service.resolve_credentials(
                tenant_id=integration.tenant_id,
                platform=integration.platform_name
            )
            
            # Validate credentials using appropriate client
            validation_result = await self._validate_platform_credentials(
                integration.platform_name,
                resolved_creds.credentials
            )
            
            # Calculate health score
            health_score = self._calculate_health_score(validation_result)
            
            # Store health status
            await self._store_health_status(
                integration.tenant_id,
                integration.platform_name,
                validation_result,
                health_score
            )
            
            # Check for alerts
            await self._check_alerts(
                integration.tenant_id,
                integration.platform_name,
                validation_result,
                health_score
            )
            
            logger.debug(f"Health check completed for {integration.platform_name} (tenant: {integration.tenant_id}): {health_score:.2f}")
            
        except Exception as e:
            logger.error(f"Failed to check health for {integration.platform_name} (tenant: {integration.tenant_id}): {e}")
            
            # Store error status
            await self._store_error_status(
                integration.tenant_id,
                integration.platform_name,
                str(e)
            )
    
    async def _validate_platform_credentials(self, platform: str, credentials: Dict[str, str]) -> Dict[str, Any]:
        """Validate credentials using platform-specific client"""
        try:
            if platform == "google_ads":
                client = GoogleAdsClient(credentials)
                return await client.validate_credentials()
            elif platform in ["facebook_ads", "meta_ads"]:
                client = MetaAdsClient(credentials)
                return await client.validate_credentials()
            elif platform == "linkedin_ads":
                client = LinkedInAdsClient(credentials)
                return await client.validate_credentials()
            else:
                return {
                    "is_healthy": False,
                    "error_message": f"Unsupported platform: {platform}",
                    "last_checked": datetime.utcnow().isoformat()
                }
        except Exception as e:
            return {
                "is_healthy": False,
                "error_message": str(e),
                "last_checked": datetime.utcnow().isoformat()
            }
    
    def _calculate_health_score(self, validation_result: Dict[str, Any]) -> float:
        """Calculate health score from validation result"""
        if not validation_result.get("is_healthy", False):
            return 0.0
        
        score = 1.0
        
        # Reduce score based on quota remaining
        quota_remaining = validation_result.get("api_quota_remaining", 100000)
        if quota_remaining < 1000:
            score *= 0.3  # Critical quota
        elif quota_remaining < 5000:
            score *= 0.7  # Low quota
        elif quota_remaining < 10000:
            score *= 0.9  # Medium quota
        
        # Reduce score if expiring soon
        expires_at = validation_result.get("expires_at")
        if expires_at:
            try:
                expiry_date = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                days_to_expiry = (expiry_date - datetime.utcnow()).days
                
                if days_to_expiry < 1:
                    score *= 0.1  # Expires today/expired
                elif days_to_expiry < 3:
                    score *= 0.5  # Expires very soon
                elif days_to_expiry < 7:
                    score *= 0.8  # Expires soon
                elif days_to_expiry < 30:
                    score *= 0.95  # Expires within month
            except Exception:
                pass  # Ignore parsing errors
        
        return max(0.0, min(1.0, score))
    
    async def _store_health_status(self, tenant_id: str, platform: str, 
                                 validation_result: Dict[str, Any], health_score: float):
        """Store health status in Redis"""
        health_key = f"byok:health:{tenant_id}:{platform}"
        
        health_data = {
            "tenant_id": tenant_id,
            "platform": platform,
            "is_healthy": validation_result.get("is_healthy", False),
            "health_score": health_score,
            "last_check": datetime.utcnow().isoformat(),
            "error_message": validation_result.get("error_message"),
            "expires_at": validation_result.get("expires_at"),
            "api_quota_remaining": validation_result.get("api_quota_remaining"),
            "validation_details": validation_result
        }
        
        # Store with 24-hour expiration
        await self.redis_client.setex(
            health_key,
            86400,  # 24 hours
            json.dumps(health_data, default=str)
        )
        
        # Also store in tenant summary
        await self._update_tenant_health_summary(tenant_id)
    
    async def _store_error_status(self, tenant_id: str, platform: str, error_message: str):
        """Store error status"""
        health_key = f"byok:health:{tenant_id}:{platform}"
        
        error_data = {
            "tenant_id": tenant_id,
            "platform": platform,
            "is_healthy": False,
            "health_score": 0.0,
            "last_check": datetime.utcnow().isoformat(),
            "error_message": error_message,
            "validation_details": {"error": error_message}
        }
        
        await self.redis_client.setex(
            health_key,
            86400,
            json.dumps(error_data, default=str)
        )
        
        await self._update_tenant_health_summary(tenant_id)
    
    async def _update_tenant_health_summary(self, tenant_id: str):
        """Update overall tenant health summary"""
        # Get all health statuses for this tenant
        pattern = f"byok:health:{tenant_id}:*"
        keys = await self.redis_client.keys(pattern)
        
        if not keys:
            return
        
        health_statuses = []
        for key in keys:
            data = await self.redis_client.get(key)
            if data:
                health_statuses.append(json.loads(data))
        
        # Calculate summary statistics
        total_platforms = len(health_statuses)
        healthy_platforms = sum(1 for status in health_statuses if status.get("is_healthy", False))
        overall_health_score = sum(status.get("health_score", 0) for status in health_statuses) / total_platforms
        
        # Collect issues
        critical_issues = []
        warnings = []
        
        for status in health_statuses:
            if not status.get("is_healthy", False):
                critical_issues.append(f"{status['platform']}: {status.get('error_message', 'Unknown error')}")
            elif status.get("health_score", 1.0) < 0.8:
                warnings.append(f"{status['platform']}: Health score {status['health_score']:.2f}")
        
        # Store summary
        summary_key = f"byok:summary:{tenant_id}"
        summary_data = {
            "tenant_id": tenant_id,
            "overall_health_score": overall_health_score,
            "healthy_platforms": healthy_platforms,
            "total_platforms": total_platforms,
            "critical_issues": critical_issues,
            "warnings": warnings,
            "last_check": datetime.utcnow().isoformat()
        }
        
        await self.redis_client.setex(
            summary_key,
            86400,
            json.dumps(summary_data, default=str)
        )
    
    async def _check_alerts(self, tenant_id: str, platform: str,
                          validation_result: Dict[str, Any], health_score: float):
        """Check if alerts should be sent"""
        alert_key = f"byok:alert:{tenant_id}:{platform}"
        
        # Check if we've recently sent an alert (cooldown)
        last_alert = await self.redis_client.get(alert_key)
        if last_alert:
            last_alert_time = datetime.fromisoformat(last_alert.decode())
            if (datetime.utcnow() - last_alert_time).seconds < self.alert_cooldown:
                return  # Still in cooldown
        
        # Check alert conditions
        should_alert = False
        alert_reason = []
        
        if not validation_result.get("is_healthy", False):
            should_alert = True
            alert_reason.append(f"Platform {platform} is unhealthy: {validation_result.get('error_message', 'Unknown error')}")
        
        if health_score < 0.8:
            should_alert = True
            alert_reason.append(f"Platform {platform} health score dropped to {health_score:.2f}")
        
        quota_remaining = validation_result.get("api_quota_remaining", 100000)
        if quota_remaining < 1000:
            should_alert = True
            alert_reason.append(f"Platform {platform} quota critically low: {quota_remaining} remaining")
        
        # Check expiry warning
        expires_at = validation_result.get("expires_at")
        if expires_at:
            try:
                expiry_date = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                days_to_expiry = (expiry_date - datetime.utcnow()).days
                if days_to_expiry <= 7:
                    should_alert = True
                    alert_reason.append(f"Platform {platform} credentials expire in {days_to_expiry} days")
            except Exception:
                pass
        
        if should_alert:
            await self._send_alert(tenant_id, platform, alert_reason, health_score)
            # Set cooldown
            await self.redis_client.setex(
                alert_key,
                self.alert_cooldown,
                datetime.utcnow().isoformat()
            )
    
    async def _send_alert(self, tenant_id: str, platform: str, 
                        reasons: List[str], health_score: float):
        """Send alert notification"""
        alert_data = {
            "tenant_id": tenant_id,
            "platform": platform,
            "reasons": reasons,
            "health_score": health_score,
            "timestamp": datetime.utcnow().isoformat(),
            "alert_type": "byok_health_warning"
        }
        
        # Store alert in Redis for dashboard display
        alert_key = f"byok:alerts:{tenant_id}"
        await self.redis_client.lpush(
            alert_key,
            json.dumps(alert_data, default=str)
        )
        
        # Keep only last 50 alerts per tenant
        await self.redis_client.ltrim(alert_key, 0, 49)
        
        # In production, also send email/Slack/webhook notifications
        logger.warning(f"BYOK Health Alert for tenant {tenant_id}: {'; '.join(reasons)}")

# Global health monitor instance
health_monitor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    global redis_client, health_monitor
    
    # Initialize Redis connection
    redis_client = redis.Redis(
        host="host.docker.internal",
        port=6379,
        decode_responses=False,
        health_check_interval=30
    )
    
    # Initialize database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Initialize Vault client
    vault_client = VaultClient()
    
    # Initialize health monitor
    health_monitor = BYOKHealthMonitor(SessionLocal, redis_client)
    
    # Start background monitoring
    monitoring_task = asyncio.create_task(health_monitor.start_monitoring())
    
    logger.info("BYOK Health Monitor started")
    yield
    
    # Cleanup
    await health_monitor.stop_monitoring()
    monitoring_task.cancel()
    try:
        await monitoring_task
    except asyncio.CancelledError:
        pass
    
    if redis_client:
        await redis_client.aclose()
    logger.info("BYOK Health Monitor stopped")

app = FastAPI(
    title="BYOK Health Monitor Service",
    description="Continuous monitoring and validation of tenant API keys with automated alerts",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencies
async def get_db_session():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# ============ HEALTH MONITORING ENDPOINTS ============

@app.get("/health/{platform}", response_model=HealthStatus)
async def get_platform_health(
    platform: str,
    current_user: UserContext = Depends(get_current_user)
):
    """Get health status for specific platform"""
    try:
        health_key = f"byok:health:{current_user.tenant_id}:{platform}"
        health_data = await redis_client.get(health_key)
        
        if not health_data:
            raise HTTPException(status_code=404, detail="Health data not found - run health check first")
        
        data = json.loads(health_data)
        return HealthStatus(**data)
        
    except Exception as e:
        logger.error(f"Failed to get platform health: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=TenantHealthSummary)
async def get_tenant_health_summary(
    current_user: UserContext = Depends(get_current_user)
):
    """Get overall tenant health summary"""
    try:
        summary_key = f"byok:summary:{current_user.tenant_id}"
        summary_data = await redis_client.get(summary_key)
        
        if not summary_data:
            # Trigger health check if no data
            await _trigger_tenant_health_check(current_user.tenant_id)
            raise HTTPException(status_code=202, detail="Health check initiated - try again in a few moments")
        
        data = json.loads(summary_data)
        return TenantHealthSummary(**data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get tenant health summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/health/check")
async def trigger_health_check(
    platform: Optional[str] = None,
    current_user: UserContext = Depends(get_current_user),
    background_tasks: BackgroundTasks = None
):
    """Manually trigger health check"""
    try:
        if platform:
            background_tasks.add_task(_check_specific_platform, current_user.tenant_id, platform)
            return {"status": "initiated", "message": f"Health check started for {platform}"}
        else:
            background_tasks.add_task(_trigger_tenant_health_check, current_user.tenant_id)
            return {"status": "initiated", "message": "Health check started for all platforms"}
        
    except Exception as e:
        logger.error(f"Failed to trigger health check: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/alerts")
async def get_alerts(
    limit: int = 20,
    current_user: UserContext = Depends(get_current_user)
):
    """Get recent alerts for tenant"""
    try:
        alert_key = f"byok:alerts:{current_user.tenant_id}"
        alerts_data = await redis_client.lrange(alert_key, 0, limit - 1)
        
        alerts = []
        for alert_data in alerts_data:
            alerts.append(json.loads(alert_data))
        
        return {
            "tenant_id": current_user.tenant_id,
            "alerts": alerts,
            "total": len(alerts)
        }
        
    except Exception as e:
        logger.error(f"Failed to get alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/alerts")
async def clear_alerts(
    current_user: UserContext = Depends(get_current_user)
):
    """Clear all alerts for tenant"""
    try:
        alert_key = f"byok:alerts:{current_user.tenant_id}"
        await redis_client.delete(alert_key)
        
        return {"status": "cleared", "message": "All alerts cleared"}
        
    except Exception as e:
        logger.error(f"Failed to clear alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============ UTILITY FUNCTIONS ============

async def _trigger_tenant_health_check(tenant_id: str):
    """Trigger health check for all tenant integrations"""
    if health_monitor:
        async with SessionLocal() as session:
            stmt = select(Integration).where(
                and_(
                    Integration.tenant_id == tenant_id,
                    Integration.status == "active"
                )
            )
            result = await session.execute(stmt)
            integrations = result.scalars().all()
            
            for integration in integrations:
                await health_monitor._check_integration_health(integration, session)

async def _check_specific_platform(tenant_id: str, platform: str):
    """Check health for specific platform"""
    if health_monitor:
        async with SessionLocal() as session:
            stmt = select(Integration).where(
                and_(
                    Integration.tenant_id == tenant_id,
                    Integration.platform_name == platform,
                    Integration.status == "active"
                )
            )
            result = await session.execute(stmt)
            integration = result.scalar_one_or_none()
            
            if integration:
                await health_monitor._check_integration_health(integration, session)

@app.get("/status")
async def service_health():
    """Service health check endpoint"""
    return {
        "status": "healthy",
        "service": "byok-health-monitor",
        "monitoring_active": health_monitor.monitoring_active if health_monitor else False,
        "check_interval_seconds": health_monitor.check_interval if health_monitor else None,
        "timestamp": datetime.utcnow()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8021)