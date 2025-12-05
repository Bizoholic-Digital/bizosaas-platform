"""
Marketing Automation Service - Consolidated DDD Implementation
Combines campaign management, CRM, and analytics into proper bounded contexts
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional

import redis.asyncio as redis
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select

# Import shared components
from shared.auth.jwt_auth import get_current_user, UserContext, require_campaign_execute
from shared.database.models import Base, Campaign, Integration, Metric
from shared.events.domain_events import (
    CampaignCreated, CampaignLaunched, CampaignMetricsUpdated,
    LeadCaptured, LeadQualified, LeadConverted
)
from shared.events.event_store import EventStore, EventPublisher, EventProcessor

# Domain Models and Services
from domains.campaign import CampaignDomain
from domains.lead import LeadDomain
from domains.analytics import AnalyticsDomain

# Event Handlers
from event_handlers import (
    CampaignEventHandler, LeadEventHandler, 
    TenantEventHandler, NotificationEventHandler
)

# BYOK Integration
from shared.credential_management import (
    KeyResolutionService, CredentialStrategy, 
    initialize_key_resolution_service, get_key_resolution_service
)
from shared.billing import BYOKBillingService, UsageType, get_byok_billing_service
from shared.vault.vault_client import VaultClient

logger = logging.getLogger(__name__)

# Database Configuration
DATABASE_URL = "postgresql+asyncpg://admin:securepassword@host.docker.internal:5432/bizosaas"
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Redis Configuration
redis_client = None
event_publisher = None

# Request/Response Models
class CampaignCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    campaign_type: str
    budget: float
    target_audience: dict = {}
    creative_assets: List[dict] = []

class CampaignResponse(BaseModel):
    id: str
    name: str
    status: str
    campaign_type: str
    budget: float
    created_at: datetime

class LeadCaptureRequest(BaseModel):
    source: str
    contact_info: dict
    campaign_id: Optional[str] = None

class LeadResponse(BaseModel):
    id: str
    source: str
    contact_info: dict
    score: Optional[float] = None
    status: str
    created_at: datetime

class MetricsResponse(BaseModel):
    campaign_metrics: List[dict]
    lead_metrics: List[dict]
    performance_summary: dict

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    global redis_client, event_publisher
    
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
    
    # Initialize event system
    async with SessionLocal() as session:
        event_store = EventStore(redis_client, session)
        await event_store.initialize()
        event_publisher = EventPublisher(event_store)
        await event_publisher.start_background_publisher()
        
        # Initialize BYOK key resolution service
        initialize_key_resolution_service(vault_client, session)
        
        # Initialize event processor with handlers
        event_processor = EventProcessor(event_store)
        
        # Register event handlers
        campaign_handler = CampaignEventHandler(session)
        lead_handler = LeadEventHandler(session)
        tenant_handler = TenantEventHandler(session)
        notification_handler = NotificationEventHandler(session)
        
        event_processor.register_handler(campaign_handler)
        event_processor.register_handler(lead_handler)
        event_processor.register_handler(tenant_handler)
        event_processor.register_handler(notification_handler)
        
        # Start event processing
        await event_processor.start_processing()
    
    logger.info("Marketing Automation Service started")
    yield
    
    # Cleanup
    if event_publisher:
        await event_publisher.stop_background_publisher()
    if 'event_processor' in locals():
        await event_processor.stop_processing()
    if redis_client:
        await redis_client.aclose()
    logger.info("Marketing Automation Service stopped")

app = FastAPI(
    title="Marketing Automation Service",
    description="Consolidated marketing automation with campaign management, CRM, and analytics",
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

async def get_event_publisher():
    return event_publisher

# ============ CAMPAIGN MANAGEMENT BOUNDED CONTEXT ============

@app.post("/campaigns", response_model=CampaignResponse)
async def create_campaign(
    request: CampaignCreateRequest,
    current_user: UserContext = Depends(require_campaign_execute),
    db: AsyncSession = Depends(get_db_session),
    publisher: EventPublisher = Depends(get_event_publisher)
):
    """Create new marketing campaign"""
    try:
        # Use domain service
        campaign_domain = CampaignDomain(db, publisher, current_user.tenant_id)
        campaign = await campaign_domain.create_campaign(
            name=request.name,
            description=request.description,
            campaign_type=request.campaign_type,
            budget=request.budget,
            target_audience=request.target_audience,
            creative_assets=request.creative_assets,
            created_by=current_user.user_id
        )
        
        return CampaignResponse(
            id=str(campaign.id),
            name=campaign.name,
            status=campaign.status,
            campaign_type=campaign.campaign_type,
            budget=campaign.budget,
            created_at=campaign.created_at
        )
        
    except Exception as e:
        logger.error(f"Failed to create campaign: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/campaigns", response_model=List[CampaignResponse])
async def list_campaigns(
    current_user: UserContext = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """List campaigns for current tenant"""
    try:
        stmt = select(Campaign).where(Campaign.tenant_id == current_user.tenant_id)
        result = await db.execute(stmt)
        campaigns = result.scalars().all()
        
        return [
            CampaignResponse(
                id=str(campaign.id),
                name=campaign.name,
                status=campaign.status,
                campaign_type=campaign.campaign_type,
                budget=campaign.budget,
                created_at=campaign.created_at
            )
            for campaign in campaigns
        ]
        
    except Exception as e:
        logger.error(f"Failed to list campaigns: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/campaigns/{campaign_id}/launch")
async def launch_campaign(
    campaign_id: str,
    platform: str,
    config: dict,
    current_user: UserContext = Depends(require_campaign_execute),
    db: AsyncSession = Depends(get_db_session),
    publisher: EventPublisher = Depends(get_event_publisher)
):
    """Launch campaign to advertising platform"""
    try:
        campaign_domain = CampaignDomain(db, publisher, current_user.tenant_id)
        platform_campaign_id = await campaign_domain.launch_campaign(
            campaign_id=campaign_id,
            platform=platform,
            config=config
        )
        
        return {"platform_campaign_id": platform_campaign_id, "status": "launched"}
        
    except Exception as e:
        logger.error(f"Failed to launch campaign: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============ LEAD MANAGEMENT BOUNDED CONTEXT ============

@app.post("/leads", response_model=LeadResponse)
async def capture_lead(
    request: LeadCaptureRequest,
    current_user: UserContext = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
    publisher: EventPublisher = Depends(get_event_publisher)
):
    """Capture new lead"""
    try:
        lead_domain = LeadDomain(db, publisher, current_user.tenant_id)
        lead = await lead_domain.capture_lead(
            source=request.source,
            contact_info=request.contact_info,
            campaign_id=request.campaign_id
        )
        
        return LeadResponse(
            id=str(lead.id),
            source=lead.source,
            contact_info=lead.contact_info,
            score=lead.score,
            status=lead.status,
            created_at=lead.created_at
        )
        
    except Exception as e:
        logger.error(f"Failed to capture lead: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/leads/{lead_id}/qualify")
async def qualify_lead(
    lead_id: str,
    score: float,
    qualification_reason: str,
    current_user: UserContext = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
    publisher: EventPublisher = Depends(get_event_publisher)
):
    """Qualify lead with AI or manual scoring"""
    try:
        lead_domain = LeadDomain(db, publisher, current_user.tenant_id)
        await lead_domain.qualify_lead(
            lead_id=lead_id,
            score=score,
            qualification_reason=qualification_reason,
            qualified_by=current_user.user_id
        )
        
        return {"status": "qualified", "score": score}
        
    except Exception as e:
        logger.error(f"Failed to qualify lead: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============ ANALYTICS BOUNDED CONTEXT ============

@app.get("/analytics/dashboard", response_model=MetricsResponse)
async def get_dashboard_metrics(
    current_user: UserContext = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Get dashboard analytics"""
    try:
        analytics_domain = AnalyticsDomain(db, current_user.tenant_id)
        
        campaign_metrics = await analytics_domain.get_campaign_metrics()
        lead_metrics = await analytics_domain.get_lead_metrics()
        performance_summary = await analytics_domain.get_performance_summary()
        
        return MetricsResponse(
            campaign_metrics=campaign_metrics,
            lead_metrics=lead_metrics,
            performance_summary=performance_summary
        )
        
    except Exception as e:
        logger.error(f"Failed to get dashboard metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analytics/metrics")
async def record_metrics(
    entity_type: str,
    entity_id: str,
    metrics: dict,
    current_user: UserContext = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
    publisher: EventPublisher = Depends(get_event_publisher)
):
    """Record performance metrics"""
    try:
        analytics_domain = AnalyticsDomain(db, current_user.tenant_id)
        await analytics_domain.record_metrics(
            entity_type=entity_type,
            entity_id=entity_id,
            metrics=metrics
        )
        
        # Publish metrics updated event
        if entity_type == "campaign":
            event = CampaignMetricsUpdated(
                tenant_id=current_user.tenant_id,
                campaign_id=entity_id,
                platform="system",
                metrics=metrics
            )
            await publisher.publish(event)
        
        return {"status": "recorded"}
        
    except Exception as e:
        logger.error(f"Failed to record metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============ BYOK MANAGEMENT ENDPOINTS ============

@app.get("/byok/credentials/{platform}")
async def get_resolved_credentials(
    platform: str,
    current_user: UserContext = Depends(get_current_user)
):
    """Get resolved credentials for a platform using BYOK logic"""
    try:
        key_service = get_key_resolution_service()
        resolved = await key_service.resolve_credentials(
            tenant_id=current_user.tenant_id,
            platform=platform
        )
        
        # Don't return actual credentials, just metadata
        return {
            "platform": platform,
            "strategy_used": resolved.strategy_used.value,
            "source": resolved.source,
            "health_status": resolved.health_status,
            "billing_model": resolved.usage_cost_model.value,
            "last_validated": resolved.last_validated.isoformat() if resolved.last_validated else None,
            "expires_at": resolved.expires_at.isoformat() if resolved.expires_at else None
        }
        
    except Exception as e:
        logger.error(f"Failed to resolve credentials: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/byok/health")
async def validate_tenant_credentials(
    current_user: UserContext = Depends(get_current_user)
):
    """Validate health of all tenant's credentials"""
    try:
        key_service = get_key_resolution_service()
        health_statuses = await key_service.validate_all_tenant_credentials(current_user.tenant_id)
        
        return {
            "tenant_id": current_user.tenant_id,
            "total_integrations": len(health_statuses),
            "healthy_count": sum(1 for status in health_statuses if status.is_healthy),
            "health_statuses": [
                {
                    "platform": status.platform,
                    "is_healthy": status.is_healthy,
                    "last_check": status.last_check.isoformat(),
                    "error_message": status.error_message,
                    "expires_at": status.expires_at.isoformat() if status.expires_at else None,
                    "usage_quota_remaining": status.usage_quota_remaining
                }
                for status in health_statuses
            ]
        }
        
    except Exception as e:
        logger.error(f"Failed to validate tenant credentials: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/byok/migrate")
async def migrate_credential_strategy(
    new_strategy: str,
    platforms: Optional[List[str]] = None,
    current_user: UserContext = Depends(require_admin),
    db: AsyncSession = Depends(get_db_session)
):
    """Migrate tenant to different credential strategy"""
    try:
        # Validate strategy
        try:
            strategy_enum = CredentialStrategy(new_strategy)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid strategy: {new_strategy}")
        
        key_service = get_key_resolution_service()
        results = await key_service.migrate_tenant_strategy(
            tenant_id=current_user.tenant_id,
            new_strategy=strategy_enum,
            platforms=platforms
        )
        
        return {
            "tenant_id": current_user.tenant_id,
            "new_strategy": new_strategy,
            "migration_results": results,
            "successful_platforms": [p for p, success in results.items() if success],
            "failed_platforms": [p for p, success in results.items() if not success]
        }
        
    except Exception as e:
        logger.error(f"Failed to migrate credential strategy: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/byok/billing/estimate")
async def estimate_billing_changes(
    proposed_strategy: str,
    current_user: UserContext = Depends(get_current_user)
):
    """Estimate cost changes from switching credential strategy"""
    try:
        # Validate strategy
        try:
            proposed_strategy_enum = CredentialStrategy(proposed_strategy)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid strategy: {proposed_strategy}")
        
        # Get tenant's current strategy (mock for now)
        current_strategy_enum = CredentialStrategy.BYOK  # In real implementation, get from tenant settings
        
        # Mock projected usage (in real implementation, calculate from historical data)
        projected_usage = {
            UsageType.API_CALL: 15000,
            UsageType.CAMPAIGN_EXECUTION: 75,
            UsageType.LEAD_PROCESSING: 1500,
            UsageType.REPORT_GENERATION: 50,
            UsageType.STORAGE_GB: 8,
            UsageType.BANDWIDTH_GB: 120
        }
        
        billing_service = get_byok_billing_service()
        estimate = billing_service.estimate_cost_savings(
            tenant_id=current_user.tenant_id,
            current_strategy=current_strategy_enum,
            proposed_strategy=proposed_strategy_enum,
            projected_usage=projected_usage
        )
        
        return estimate
        
    except Exception as e:
        logger.error(f"Failed to estimate billing changes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/byok/billing/tiers")
async def get_billing_tier_comparison():
    """Get comparison of all billing tiers"""
    try:
        billing_service = get_byok_billing_service()
        return billing_service.get_billing_tier_comparison()
        
    except Exception as e:
        logger.error(f"Failed to get billing tier comparison: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============ PLATFORM API MANAGEMENT ENDPOINTS ============

@app.get("/platforms/validate/{platform}")
async def validate_platform_credentials(
    platform: str,
    current_user: UserContext = Depends(get_current_user)
):
    """Validate platform API credentials using BYOK resolution"""
    try:
        key_service = get_key_resolution_service()
        resolved_creds = await key_service.resolve_credentials(
            tenant_id=current_user.tenant_id,
            platform=platform
        )
        
        if resolved_creds.health_status != "healthy":
            return {
                "platform": platform,
                "is_valid": False,
                "error": f"Credentials are not healthy: {resolved_creds.health_status}",
                "strategy_used": resolved_creds.strategy_used.value,
                "last_validated": resolved_creds.last_validated.isoformat() if resolved_creds.last_validated else None
            }
        
        # Import platform clients dynamically
        from platform_apis import GoogleAdsClient, MetaAdsClient, LinkedInAdsClient
        
        # Validate using appropriate client
        if platform == "google_ads":
            client = GoogleAdsClient(resolved_creds.credentials)
            validation_result = await client.validate_credentials()
        elif platform in ["facebook_ads", "meta_ads"]:
            client = MetaAdsClient(resolved_creds.credentials)
            validation_result = await client.validate_credentials()
        elif platform == "linkedin_ads":
            client = LinkedInAdsClient(resolved_creds.credentials)
            validation_result = await client.validate_credentials()
        else:
            return {
                "platform": platform,
                "is_valid": False,
                "error": f"Unsupported platform: {platform}",
                "supported_platforms": ["google_ads", "meta_ads", "linkedin_ads"]
            }
        
        return {
            "platform": platform,
            "is_valid": validation_result.get("is_healthy", False),
            "strategy_used": resolved_creds.strategy_used.value,
            "validation_result": validation_result
        }
        
    except Exception as e:
        logger.error(f"Failed to validate platform credentials: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/campaigns/{campaign_id}/performance/{platform}")
async def get_platform_campaign_performance(
    campaign_id: str,
    platform: str,
    date_range: int = 30,
    current_user: UserContext = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Get performance metrics from platform APIs"""
    try:
        # Get campaign execution record
        from shared.database.models import CampaignExecution
        stmt = select(CampaignExecution).where(
            CampaignExecution.campaign_id == campaign_id,
            CampaignExecution.tenant_id == current_user.tenant_id,
            CampaignExecution.platform == platform
        )
        result = await db.execute(stmt)
        execution = result.scalar_one_or_none()
        
        if not execution:
            raise HTTPException(status_code=404, detail="Campaign execution not found")
        
        # Resolve credentials and get performance data
        key_service = get_key_resolution_service()
        resolved_creds = await key_service.resolve_credentials(
            tenant_id=current_user.tenant_id,
            platform=platform
        )
        
        # Import platform clients dynamically
        from platform_apis import GoogleAdsClient, MetaAdsClient, LinkedInAdsClient
        
        # Get performance using appropriate client
        if platform == "google_ads":
            client = GoogleAdsClient(resolved_creds.credentials)
            performance_data = await client.get_campaign_performance(
                execution.platform_campaign_id, date_range
            )
        elif platform in ["facebook_ads", "meta_ads"]:
            client = MetaAdsClient(resolved_creds.credentials)
            performance_data = await client.get_campaign_performance(
                execution.platform_campaign_id, date_range
            )
        elif platform == "linkedin_ads":
            client = LinkedInAdsClient(resolved_creds.credentials)
            performance_data = await client.get_campaign_performance(
                execution.platform_campaign_id, date_range
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported platform: {platform}")
        
        return performance_data
        
    except Exception as e:
        logger.error(f"Failed to get platform performance: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/campaigns/{campaign_id}/pause/{platform}")
async def pause_platform_campaign(
    campaign_id: str,
    platform: str,
    current_user: UserContext = Depends(require_campaign_execute),
    db: AsyncSession = Depends(get_db_session)
):
    """Pause campaign on platform"""
    try:
        # Get campaign execution record
        from shared.database.models import CampaignExecution
        stmt = select(CampaignExecution).where(
            CampaignExecution.campaign_id == campaign_id,
            CampaignExecution.tenant_id == current_user.tenant_id,
            CampaignExecution.platform == platform
        )
        result = await db.execute(stmt)
        execution = result.scalar_one_or_none()
        
        if not execution:
            raise HTTPException(status_code=404, detail="Campaign execution not found")
        
        # Resolve credentials
        key_service = get_key_resolution_service()
        resolved_creds = await key_service.resolve_credentials(
            tenant_id=current_user.tenant_id,
            platform=platform
        )
        
        # Import platform clients dynamically
        from platform_apis import GoogleAdsClient, MetaAdsClient, LinkedInAdsClient
        
        # Pause using appropriate client
        success = False
        if platform == "google_ads":
            client = GoogleAdsClient(resolved_creds.credentials)
            success = await client.pause_campaign(execution.platform_campaign_id)
        elif platform in ["facebook_ads", "meta_ads"]:
            client = MetaAdsClient(resolved_creds.credentials)
            success = await client.pause_campaign(execution.platform_campaign_id)
        elif platform == "linkedin_ads":
            client = LinkedInAdsClient(resolved_creds.credentials)
            success = await client.pause_campaign(execution.platform_campaign_id)
        
        if success:
            execution.execution_status = "paused"
            await db.commit()
        
        return {"success": success, "status": "paused" if success else "error"}
        
    except Exception as e:
        logger.error(f"Failed to pause platform campaign: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/campaigns/{campaign_id}/resume/{platform}")
async def resume_platform_campaign(
    campaign_id: str,
    platform: str,
    current_user: UserContext = Depends(require_campaign_execute),
    db: AsyncSession = Depends(get_db_session)
):
    """Resume campaign on platform"""
    try:
        # Similar implementation to pause but with resume
        from shared.database.models import CampaignExecution
        stmt = select(CampaignExecution).where(
            CampaignExecution.campaign_id == campaign_id,
            CampaignExecution.tenant_id == current_user.tenant_id,
            CampaignExecution.platform == platform
        )
        result = await db.execute(stmt)
        execution = result.scalar_one_or_none()
        
        if not execution:
            raise HTTPException(status_code=404, detail="Campaign execution not found")
        
        key_service = get_key_resolution_service()
        resolved_creds = await key_service.resolve_credentials(
            tenant_id=current_user.tenant_id,
            platform=platform
        )
        
        from platform_apis import GoogleAdsClient, MetaAdsClient, LinkedInAdsClient
        
        success = False
        if platform == "google_ads":
            client = GoogleAdsClient(resolved_creds.credentials)
            success = await client.resume_campaign(execution.platform_campaign_id)
        elif platform in ["facebook_ads", "meta_ads"]:
            client = MetaAdsClient(resolved_creds.credentials)
            success = await client.resume_campaign(execution.platform_campaign_id)
        elif platform == "linkedin_ads":
            client = LinkedInAdsClient(resolved_creds.credentials)
            success = await client.resume_campaign(execution.platform_campaign_id)
        
        if success:
            execution.execution_status = "active"
            await db.commit()
        
        return {"success": success, "status": "active" if success else "error"}
        
    except Exception as e:
        logger.error(f"Failed to resume platform campaign: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============ INTEGRATION ENDPOINTS ============

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "marketing-automation-service",
        "byok_enabled": True,
        "supported_platforms": ["google_ads", "meta_ads", "linkedin_ads"],
        "platform_apis_available": True,
        "timestamp": datetime.utcnow()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8020)