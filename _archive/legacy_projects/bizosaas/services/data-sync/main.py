#!/usr/bin/env python3

"""
BizOSaaS Cross-Platform Data Synchronization Service
Real-time data flow automation between Bizoholic, CoreLDove, and BizOSaaS platforms
"""

import os
import asyncio
import logging
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

from fastapi import FastAPI, HTTPException, Depends, Request, APIRouter, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import redis.asyncio as redis
import asyncpg
import httpx
import uvicorn
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===========================================
# ENUMS AND CONSTANTS
# ===========================================

class SyncEventType(str, Enum):
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"
    LEAD_CREATED = "lead_created"
    LEAD_UPDATED = "lead_updated"
    ORDER_CREATED = "order_created"
    ORDER_UPDATED = "order_updated"
    CAMPAIGN_CREATED = "campaign_created"
    CAMPAIGN_UPDATED = "campaign_updated"
    PRODUCT_CREATED = "product_created"
    PRODUCT_UPDATED = "product_updated"
    ANALYTICS_UPDATED = "analytics_updated"

class PlatformType(str, Enum):
    BIZOHOLIC = "bizoholic"
    CORELDOVE = "coreldove"
    BIZOSAAS = "bizosaas"

class SyncStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRY = "retry"

# ===========================================
# PYDANTIC MODELS
# ===========================================

class SyncEvent(BaseModel):
    id: Optional[str] = None
    event_type: SyncEventType
    source_platform: PlatformType
    target_platforms: List[PlatformType]
    data: Dict[str, Any]
    tenant_id: str
    user_id: Optional[str] = None
    priority: int = Field(default=5, ge=1, le=10)
    retry_count: int = Field(default=0)
    max_retries: int = Field(default=3)
    created_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    status: SyncStatus = SyncStatus.PENDING

class SyncResult(BaseModel):
    event_id: str
    status: SyncStatus
    target_platform: PlatformType
    success: bool
    error_message: Optional[str] = None
    processed_at: datetime
    processing_time_ms: int

class CrossPlatformUser(BaseModel):
    user_id: str
    email: str
    name: str
    phone: Optional[str] = None
    profile_data: Dict[str, Any] = {}
    preferences: Dict[str, Any] = {}
    tenant_id: str
    platform_data: Dict[PlatformType, Dict[str, Any]] = {}

class SyncMetrics(BaseModel):
    total_events: int
    events_processed: int
    events_failed: int
    events_pending: int
    average_processing_time_ms: float
    platforms_synced: List[str]
    last_sync_time: Optional[datetime] = None

# ===========================================
# FASTAPI APPLICATION SETUP
# ===========================================

app = FastAPI(
    title="BizOSaaS Data Synchronization Service",
    description="Real-time cross-platform data synchronization for BizOSaaS ecosystem",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================================
# CONFIGURATION
# ===========================================

@dataclass
class Settings:
    def __init__(self):
        # Database and Cache
        self.database_url = os.getenv("DATABASE_URL", "postgresql://admin:securepassword@host.docker.internal:5432/bizosaas")
        self.redis_url = os.getenv("REDIS_URL", "redis://host.docker.internal:6379/6")
        
        # Security
        self.jwt_secret = os.getenv("JWT_SECRET", "dev-secret-key")
        self.environment = os.getenv("ENVIRONMENT", "production")
        
        # Platform Service URLs
        self.bizosaas_brain_url = os.getenv("BIZOSAAS_BRAIN_URL", "http://bizosaas-brain:8001")
        self.bizoholic_frontend_url = os.getenv("BIZOHOLIC_FRONTEND_URL", "http://bizosaas-bizoholic-frontend:3008")
        self.coreldove_frontend_url = os.getenv("CORELDOVE_FRONTEND_URL", "http://bizosaas-coreldove-frontend:3012")
        self.auth_service_url = os.getenv("AUTH_SERVICE_URL", "http://bizosaas-auth-v2:8007")
        self.django_crm_url = os.getenv("DJANGO_CRM_URL", "http://bizosaas-django-crm:8008")
        self.saleor_api_url = os.getenv("SALEOR_API_URL", "http://bizosaas-saleor-api:8024")
        self.wagtail_cms_url = os.getenv("WAGTAIL_CMS_URL", "http://bizosaas-wagtail-cms:8006")
        
        # Sync Configuration
        self.sync_batch_size = int(os.getenv("SYNC_BATCH_SIZE", "100"))
        self.sync_interval_seconds = int(os.getenv("SYNC_INTERVAL_SECONDS", "5"))
        self.max_concurrent_syncs = int(os.getenv("MAX_CONCURRENT_SYNCS", "10"))
        self.event_retention_days = int(os.getenv("EVENT_RETENTION_DAYS", "30"))

settings = Settings()

# ===========================================
# DATABASE AND REDIS CONNECTIONS
# ===========================================

redis_client = None
db_pool = None
websocket_connections = []

async def init_redis():
    """Initialize Redis connection"""
    global redis_client
    try:
        redis_client = redis.from_url(settings.redis_url, decode_responses=True)
        await redis_client.ping()
        logger.info("✅ Redis connection established for data sync")
    except Exception as e:
        logger.error(f"❌ Redis connection failed: {e}")
        redis_client = None

async def init_database():
    """Initialize PostgreSQL connection pool"""
    global db_pool
    try:
        db_pool = await asyncpg.create_pool(settings.database_url)
        logger.info("✅ PostgreSQL connection pool established for data sync")
        await create_sync_tables()
    except Exception as e:
        logger.error(f"❌ PostgreSQL connection failed: {e}")
        db_pool = None

async def create_sync_tables():
    """Create data synchronization tables"""
    try:
        async with db_pool.acquire() as conn:
            # Create sync events table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS sync_events (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    event_type VARCHAR(100) NOT NULL,
                    source_platform VARCHAR(50) NOT NULL,
                    target_platforms TEXT[] NOT NULL,
                    data JSONB NOT NULL,
                    tenant_id UUID NOT NULL,
                    user_id UUID,
                    priority INTEGER DEFAULT 5,
                    retry_count INTEGER DEFAULT 0,
                    max_retries INTEGER DEFAULT 3,
                    status VARCHAR(20) DEFAULT 'pending',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    processed_at TIMESTAMP WITH TIME ZONE,
                    error_message TEXT,
                    processing_time_ms INTEGER
                );
            """)
            
            # Create sync results table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS sync_results (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    event_id UUID NOT NULL REFERENCES sync_events(id),
                    target_platform VARCHAR(50) NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    success BOOLEAN NOT NULL,
                    error_message TEXT,
                    processed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    processing_time_ms INTEGER
                );
            """)
            
            # Create cross platform users table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS cross_platform_users (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    phone VARCHAR(50),
                    profile_data JSONB DEFAULT '{}',
                    preferences JSONB DEFAULT '{}',
                    tenant_id UUID NOT NULL,
                    platform_data JSONB DEFAULT '{}',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    UNIQUE(user_id, tenant_id)
                );
            """)
            
            # Create indexes for performance
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_sync_events_status ON sync_events(status);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_sync_events_tenant ON sync_events(tenant_id);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_sync_events_created ON sync_events(created_at);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_cross_platform_users_email ON cross_platform_users(email);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_cross_platform_users_tenant ON cross_platform_users(tenant_id);")
            
            logger.info("✅ Data synchronization tables created successfully")
    except Exception as e:
        logger.error(f"❌ Failed to create sync tables: {e}")

# ===========================================
# DATA SYNC ENGINE
# ===========================================

class DataSyncEngine:
    def __init__(self, db_pool, redis_client):
        self.db_pool = db_pool
        self.redis_client = redis_client
        self.processing_events = set()
        
    async def publish_event(self, event: SyncEvent) -> str:
        """Publish a new sync event"""
        try:
            # Generate event ID if not provided
            if not event.id:
                event.id = f"sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{event.event_type}_{event.source_platform}"
            
            event.created_at = datetime.now(timezone.utc)
            
            # Store in database
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO sync_events (
                        id, event_type, source_platform, target_platforms, data,
                        tenant_id, user_id, priority, max_retries, status, created_at
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                """, event.id, event.event_type, event.source_platform, 
                event.target_platforms, json.dumps(event.data), event.tenant_id,
                event.user_id, event.priority, event.max_retries, event.status.value,
                event.created_at)
            
            # Publish to Redis for real-time processing
            await self.redis_client.lpush("sync_events_queue", event.id)
            await self.redis_client.publish("sync_events_channel", json.dumps({
                "event_id": event.id,
                "event_type": event.event_type,
                "source_platform": event.source_platform,
                "target_platforms": event.target_platforms
            }))
            
            logger.info(f"✅ Published sync event: {event.id}")
            return event.id
            
        except Exception as e:
            logger.error(f"❌ Failed to publish sync event: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to publish sync event: {str(e)}")
    
    async def process_event(self, event_id: str) -> List[SyncResult]:
        """Process a single sync event"""
        if event_id in self.processing_events:
            logger.warning(f"Event {event_id} already being processed")
            return []
        
        self.processing_events.add(event_id)
        results = []
        
        try:
            # Get event from database
            async with self.db_pool.acquire() as conn:
                event_data = await conn.fetchrow("""
                    SELECT * FROM sync_events WHERE id = $1
                """, event_id)
                
                if not event_data:
                    logger.error(f"Event {event_id} not found")
                    return []
                
                # Update status to processing
                await conn.execute("""
                    UPDATE sync_events SET status = 'processing', processed_at = NOW()
                    WHERE id = $1
                """, event_id)
            
            event = SyncEvent(
                id=event_data['id'],
                event_type=event_data['event_type'],
                source_platform=event_data['source_platform'],
                target_platforms=event_data['target_platforms'],
                data=json.loads(event_data['data']),
                tenant_id=event_data['tenant_id'],
                user_id=event_data['user_id'],
                priority=event_data['priority'],
                retry_count=event_data['retry_count'],
                max_retries=event_data['max_retries'],
                status=SyncStatus(event_data['status'])
            )
            
            # Process for each target platform
            for target_platform in event.target_platforms:
                if target_platform == event.source_platform:
                    continue  # Skip self-sync
                
                start_time = datetime.now()
                try:
                    success = await self._sync_to_platform(event, target_platform)
                    processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
                    
                    result = SyncResult(
                        event_id=event_id,
                        target_platform=target_platform,
                        status=SyncStatus.COMPLETED if success else SyncStatus.FAILED,
                        success=success,
                        processed_at=datetime.now(timezone.utc),
                        processing_time_ms=processing_time
                    )
                    
                    # Store result
                    await self._store_sync_result(result)
                    results.append(result)
                    
                except Exception as e:
                    processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
                    result = SyncResult(
                        event_id=event_id,
                        target_platform=target_platform,
                        status=SyncStatus.FAILED,
                        success=False,
                        error_message=str(e),
                        processed_at=datetime.now(timezone.utc),
                        processing_time_ms=processing_time
                    )
                    await self._store_sync_result(result)
                    results.append(result)
                    logger.error(f"❌ Failed to sync to {target_platform}: {e}")
            
            # Update event status
            all_success = all(result.success for result in results)
            final_status = SyncStatus.COMPLETED if all_success else SyncStatus.FAILED
            
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    UPDATE sync_events SET status = $1 WHERE id = $2
                """, final_status.value, event_id)
            
            # Notify WebSocket connections
            await self._notify_websocket_clients({
                "type": "sync_completed",
                "event_id": event_id,
                "status": final_status.value,
                "results": [result.dict() for result in results]
            })
            
            logger.info(f"✅ Processed sync event {event_id} with status {final_status}")
            
        except Exception as e:
            logger.error(f"❌ Failed to process event {event_id}: {e}")
            
            # Update retry count and status
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    UPDATE sync_events 
                    SET retry_count = retry_count + 1,
                        status = CASE 
                            WHEN retry_count + 1 >= max_retries THEN 'failed'
                            ELSE 'retry'
                        END,
                        error_message = $2
                    WHERE id = $1
                """, event_id, str(e))
            
        finally:
            self.processing_events.discard(event_id)
        
        return results
    
    async def _sync_to_platform(self, event: SyncEvent, target_platform: PlatformType) -> bool:
        """Sync data to specific platform"""
        try:
            platform_url = self._get_platform_url(target_platform)
            endpoint = self._get_sync_endpoint(event.event_type, target_platform)
            
            if not platform_url or not endpoint:
                logger.warning(f"No sync endpoint for {event.event_type} on {target_platform}")
                return True  # Skip if no endpoint
            
            # Transform data for target platform
            transformed_data = await self._transform_data(event.data, event.source_platform, target_platform)
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{platform_url}{endpoint}",
                    json={
                        "event_type": event.event_type,
                        "source_platform": event.source_platform,
                        "data": transformed_data,
                        "tenant_id": event.tenant_id,
                        "user_id": event.user_id
                    },
                    headers={"Authorization": f"Bearer {settings.jwt_secret}"},
                    timeout=30.0
                )
                
                if response.status_code in [200, 201, 202]:
                    logger.info(f"✅ Successfully synced to {target_platform}")
                    return True
                else:
                    logger.error(f"❌ Sync failed to {target_platform}: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Exception syncing to {target_platform}: {e}")
            return False
    
    def _get_platform_url(self, platform: PlatformType) -> str:
        """Get platform base URL"""
        urls = {
            PlatformType.BIZOHOLIC: settings.bizoholic_frontend_url,
            PlatformType.CORELDOVE: settings.coreldove_frontend_url,
            PlatformType.BIZOSAAS: settings.bizosaas_brain_url
        }
        return urls.get(platform, "")
    
    def _get_sync_endpoint(self, event_type: SyncEventType, platform: PlatformType) -> str:
        """Get sync endpoint for event type and platform"""
        endpoints = {
            SyncEventType.USER_CREATED: "/api/sync/user/create",
            SyncEventType.USER_UPDATED: "/api/sync/user/update",
            SyncEventType.LEAD_CREATED: "/api/sync/lead/create",
            SyncEventType.LEAD_UPDATED: "/api/sync/lead/update",
            SyncEventType.ORDER_CREATED: "/api/sync/order/create",
            SyncEventType.ORDER_UPDATED: "/api/sync/order/update",
            SyncEventType.CAMPAIGN_CREATED: "/api/sync/campaign/create",
            SyncEventType.CAMPAIGN_UPDATED: "/api/sync/campaign/update",
            SyncEventType.PRODUCT_CREATED: "/api/sync/product/create",
            SyncEventType.PRODUCT_UPDATED: "/api/sync/product/update",
            SyncEventType.ANALYTICS_UPDATED: "/api/sync/analytics/update"
        }
        return endpoints.get(event_type, "")
    
    async def _transform_data(self, data: Dict[str, Any], source: PlatformType, target: PlatformType) -> Dict[str, Any]:
        """Transform data between platforms"""
        # Basic transformation - can be extended for platform-specific needs
        transformed = data.copy()
        
        # Add platform context
        transformed["_sync_metadata"] = {
            "source_platform": source,
            "target_platform": target,
            "transformed_at": datetime.now().isoformat()
        }
        
        # Platform-specific transformations
        if target == PlatformType.CORELDOVE and "price" in data:
            # Convert USD to INR for CoreLDove
            transformed["price_inr"] = data.get("price", 0) * 83  # Approximate conversion
        
        return transformed
    
    async def _store_sync_result(self, result: SyncResult):
        """Store sync result in database"""
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO sync_results (
                        event_id, target_platform, status, success, 
                        error_message, processed_at, processing_time_ms
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                """, result.event_id, result.target_platform, result.status.value,
                result.success, result.error_message, result.processed_at,
                result.processing_time_ms)
        except Exception as e:
            logger.error(f"❌ Failed to store sync result: {e}")
    
    async def _notify_websocket_clients(self, message: Dict[str, Any]):
        """Notify WebSocket clients of sync updates"""
        if not websocket_connections:
            return
        
        disconnected = []
        for websocket in websocket_connections:
            try:
                await websocket.send_text(json.dumps(message))
            except:
                disconnected.append(websocket)
        
        # Remove disconnected clients
        for ws in disconnected:
            websocket_connections.remove(ws)

# Global sync engine instance
sync_engine = None

# ===========================================
# API ENDPOINTS
# ===========================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    services_status = {}
    
    # Check Redis
    try:
        if redis_client:
            await redis_client.ping()
            services_status["redis"] = "healthy"
        else:
            services_status["redis"] = "disconnected"
    except:
        services_status["redis"] = "unhealthy"
    
    # Check PostgreSQL
    try:
        if db_pool:
            async with db_pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            services_status["postgresql"] = "healthy"
        else:
            services_status["postgresql"] = "disconnected"
    except:
        services_status["postgresql"] = "unhealthy"
    
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "environment": settings.environment,
        "services": services_status
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "BizOSaaS Data Synchronization Service",
        "version": "1.0.0",
        "environment": settings.environment,
        "docs": "/docs"
    }

# ===========================================
# SYNC EVENT MANAGEMENT ENDPOINTS
# ===========================================

@app.post("/sync/events", response_model=Dict[str, str])
async def create_sync_event(event: SyncEvent):
    """Create a new sync event"""
    if not sync_engine:
        raise HTTPException(status_code=503, detail="Sync engine not initialized")
    
    event_id = await sync_engine.publish_event(event)
    return {"event_id": event_id, "status": "created"}

@app.get("/sync/events/{event_id}")
async def get_sync_event(event_id: str):
    """Get sync event status and results"""
    try:
        async with db_pool.acquire() as conn:
            event = await conn.fetchrow("""
                SELECT * FROM sync_events WHERE id = $1
            """, event_id)
            
            if not event:
                raise HTTPException(status_code=404, detail="Event not found")
            
            results = await conn.fetch("""
                SELECT * FROM sync_results WHERE event_id = $1
            """, event_id)
            
            return {
                "event": dict(event),
                "results": [dict(result) for result in results]
            }
    except Exception as e:
        logger.error(f"Error fetching sync event: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sync/events")
async def list_sync_events(
    limit: int = 50,
    offset: int = 0,
    status: Optional[SyncStatus] = None,
    tenant_id: Optional[str] = None
):
    """List sync events with filtering"""
    try:
        conditions = []
        params = [limit, offset]
        param_count = 2
        
        if status:
            param_count += 1
            conditions.append(f"status = ${param_count}")
            params.append(status.value)
        
        if tenant_id:
            param_count += 1
            conditions.append(f"tenant_id = ${param_count}")
            params.append(tenant_id)
        
        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
        
        async with db_pool.acquire() as conn:
            events = await conn.fetch(f"""
                SELECT * FROM sync_events 
                {where_clause}
                ORDER BY created_at DESC
                LIMIT $1 OFFSET $2
            """, *params)
            
            total = await conn.fetchval(f"""
                SELECT COUNT(*) FROM sync_events {where_clause}
            """, *params[2:])
            
            return {
                "events": [dict(event) for event in events],
                "total": total,
                "limit": limit,
                "offset": offset
            }
    except Exception as e:
        logger.error(f"Error listing sync events: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sync/events/{event_id}/retry")
async def retry_sync_event(event_id: str):
    """Retry a failed sync event"""
    if not sync_engine:
        raise HTTPException(status_code=503, detail="Sync engine not initialized")
    
    try:
        async with db_pool.acquire() as conn:
            # Check if event exists and can be retried
            event = await conn.fetchrow("""
                SELECT * FROM sync_events 
                WHERE id = $1 AND status IN ('failed', 'retry')
                AND retry_count < max_retries
            """, event_id)
            
            if not event:
                raise HTTPException(status_code=400, detail="Event cannot be retried")
            
            # Reset status to pending
            await conn.execute("""
                UPDATE sync_events SET status = 'pending' WHERE id = $1
            """, event_id)
            
            # Re-queue for processing
            await redis_client.lpush("sync_events_queue", event_id)
            
            return {"message": "Event queued for retry", "event_id": event_id}
    except Exception as e:
        logger.error(f"Error retrying sync event: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===========================================
# CROSS-PLATFORM USER MANAGEMENT
# ===========================================

@app.post("/sync/users", response_model=Dict[str, str])
async def create_cross_platform_user(user: CrossPlatformUser):
    """Create or update cross-platform user"""
    try:
        async with db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO cross_platform_users (
                    user_id, email, name, phone, profile_data, 
                    preferences, tenant_id, platform_data
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                ON CONFLICT (user_id, tenant_id) 
                DO UPDATE SET
                    email = EXCLUDED.email,
                    name = EXCLUDED.name,
                    phone = EXCLUDED.phone,
                    profile_data = EXCLUDED.profile_data,
                    preferences = EXCLUDED.preferences,
                    platform_data = EXCLUDED.platform_data,
                    updated_at = NOW()
            """, user.user_id, user.email, user.name, user.phone,
            json.dumps(user.profile_data), json.dumps(user.preferences),
            user.tenant_id, json.dumps(user.platform_data))
            
            # Create sync event for user update
            if sync_engine:
                event = SyncEvent(
                    event_type=SyncEventType.USER_UPDATED,
                    source_platform=PlatformType.BIZOSAAS,
                    target_platforms=[PlatformType.BIZOHOLIC, PlatformType.CORELDOVE],
                    data=user.dict(),
                    tenant_id=user.tenant_id,
                    user_id=user.user_id
                )
                await sync_engine.publish_event(event)
            
            return {"message": "User synchronized", "user_id": user.user_id}
    except Exception as e:
        logger.error(f"Error creating cross-platform user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sync/users/{user_id}")
async def get_cross_platform_user(user_id: str, tenant_id: str):
    """Get cross-platform user data"""
    try:
        async with db_pool.acquire() as conn:
            user = await conn.fetchrow("""
                SELECT * FROM cross_platform_users 
                WHERE user_id = $1 AND tenant_id = $2
            """, user_id, tenant_id)
            
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            return dict(user)
    except Exception as e:
        logger.error(f"Error fetching cross-platform user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===========================================
# SYNC METRICS AND MONITORING
# ===========================================

@app.get("/sync/metrics", response_model=SyncMetrics)
async def get_sync_metrics(
    tenant_id: Optional[str] = None,
    hours: int = 24
):
    """Get synchronization metrics"""
    try:
        conditions = ["created_at >= NOW() - INTERVAL '%s hours'" % hours]
        params = []
        
        if tenant_id:
            conditions.append("tenant_id = $1")
            params.append(tenant_id)
        
        where_clause = "WHERE " + " AND ".join(conditions)
        
        async with db_pool.acquire() as conn:
            metrics = await conn.fetchrow(f"""
                SELECT 
                    COUNT(*) as total_events,
                    COUNT(CASE WHEN status = 'completed' THEN 1 END) as events_processed,
                    COUNT(CASE WHEN status = 'failed' THEN 1 END) as events_failed,
                    COUNT(CASE WHEN status = 'pending' THEN 1 END) as events_pending,
                    AVG(processing_time_ms) as avg_processing_time_ms,
                    MAX(processed_at) as last_sync_time
                FROM sync_events 
                {where_clause}
            """, *params)
            
            platforms = await conn.fetch(f"""
                SELECT DISTINCT target_platform, COUNT(*) 
                FROM sync_results sr
                JOIN sync_events se ON sr.event_id = se.id
                {where_clause}
                GROUP BY target_platform
            """, *params)
            
            return SyncMetrics(
                total_events=metrics['total_events'] or 0,
                events_processed=metrics['events_processed'] or 0,
                events_failed=metrics['events_failed'] or 0,
                events_pending=metrics['events_pending'] or 0,
                average_processing_time_ms=float(metrics['avg_processing_time_ms'] or 0),
                platforms_synced=[p['target_platform'] for p in platforms],
                last_sync_time=metrics['last_sync_time']
            )
    except Exception as e:
        logger.error(f"Error fetching sync metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sync/status")
async def get_sync_status():
    """Get overall synchronization status"""
    try:
        queue_size = await redis_client.llen("sync_events_queue") if redis_client else 0
        
        async with db_pool.acquire() as conn:
            status = await conn.fetchrow("""
                SELECT 
                    COUNT(CASE WHEN status = 'processing' THEN 1 END) as processing,
                    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending,
                    COUNT(CASE WHEN status = 'retry' THEN 1 END) as retry
                FROM sync_events
                WHERE created_at >= NOW() - INTERVAL '1 hour'
            """)
            
            return {
                "queue_size": queue_size,
                "processing": status['processing'] or 0,
                "pending": status['pending'] or 0,
                "retry": status['retry'] or 0,
                "sync_engine_active": sync_engine is not None,
                "timestamp": datetime.now()
            }
    except Exception as e:
        logger.error(f"Error fetching sync status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===========================================
# WEBSOCKET REAL-TIME UPDATES
# ===========================================

@app.websocket("/ws/sync")
async def websocket_sync_updates(websocket: WebSocket):
    """WebSocket endpoint for real-time sync updates"""
    await websocket.accept()
    websocket_connections.append(websocket)
    
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_connections.remove(websocket)

# ===========================================
# BACKGROUND TASK WORKER
# ===========================================

async def sync_worker():
    """Background worker to process sync events"""
    logger.info("🚀 Starting sync worker...")
    
    while True:
        try:
            if not redis_client or not sync_engine:
                await asyncio.sleep(5)
                continue
            
            # Get next event from queue
            event_id = await redis_client.brpop("sync_events_queue", timeout=5)
            
            if event_id:
                event_id = event_id[1]  # brpop returns (key, value)
                logger.info(f"Processing sync event: {event_id}")
                await sync_engine.process_event(event_id)
            
        except Exception as e:
            logger.error(f"Sync worker error: {e}")
            await asyncio.sleep(1)

# ===========================================
# STARTUP AND SHUTDOWN EVENTS
# ===========================================

@app.on_event("startup")
async def startup_event():
    """Initialize connections and start background workers"""
    global sync_engine
    
    logger.info("🚀 Starting BizOSaaS Data Synchronization Service...")
    await init_redis()
    await init_database()
    
    if db_pool and redis_client:
        sync_engine = DataSyncEngine(db_pool, redis_client)
        
        # Start background worker
        asyncio.create_task(sync_worker())
        
        logger.info("✅ Data Synchronization Service started successfully")
    else:
        logger.error("❌ Failed to initialize connections")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up connections on shutdown"""
    logger.info("🔄 Shutting down Data Synchronization Service...")
    if redis_client:
        await redis_client.close()
    if db_pool:
        await db_pool.close()
    logger.info("✅ Data Synchronization Service shutdown complete")

# ===========================================
# ERROR HANDLERS
# ===========================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

# ===========================================
# MAIN ENTRY POINT
# ===========================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8025,
        reload=True if settings.environment == "development" else False,
        log_level="info"
    )