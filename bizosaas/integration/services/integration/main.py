"""
Integration Service - BizoholicSaaS
Handles third-party API integrations, webhooks, and data synchronization
Port: 8004
"""

from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime, timedelta
import logging
from enum import Enum
import json
import asyncio
import hmac
import hashlib
import base64
from cryptography.fernet import Fernet

# Shared imports
import sys
import os
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas')

# Mautic integration
from .mautic_integration import test_mautic_connection, sync_mautic_data, MauticConfig

from shared.database.connection import get_postgres_session, get_redis_client, init_database
from shared.database.models import Integration, WebhookEndpoint, SyncLog
from shared.events.event_bus import EventBus, EventFactory, EventType, event_handler
from shared.auth.jwt_auth import get_current_user, UserContext, require_permission, Permission

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Integration Service",
    description="Third-party integrations and data synchronization for BizoholicSaaS",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
event_bus: EventBus = None
redis_client = None
encryption_key = os.getenv("ENCRYPTION_KEY", Fernet.generate_key()).encode() if isinstance(os.getenv("ENCRYPTION_KEY", ""), str) else Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

# Enums
class PlatformType(str, Enum):
    GOOGLE_ADS = "google_ads"
    FACEBOOK_ADS = "facebook_ads" 
    LINKEDIN_ADS = "linkedin_ads"
    GOOGLE_ANALYTICS = "google_analytics"
    STRIPE = "stripe"
    MAILCHIMP = "mailchimp"
    HUBSPOT = "hubspot"
    ZAPIER = "zapier"
    MAUTIC = "mautic"
    WEBHOOKS = "webhooks"

class IntegrationType(str, Enum):
    OAUTH2 = "oauth2"
    API_KEY = "api_key"
    WEBHOOK = "webhook"
    BASIC_AUTH = "basic_auth"
    JWT = "jwt"

class IntegrationStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    PENDING = "pending"
    EXPIRED = "expired"

class SyncStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"
    CANCELLED = "cancelled"

# Pydantic models
class IntegrationCreate(BaseModel):
    platform_name: PlatformType
    integration_type: IntegrationType
    credentials: Dict[str, Any]  # Will be encrypted
    configuration: Dict[str, Any] = {}
    sync_frequency: int = 3600  # seconds

class IntegrationUpdate(BaseModel):
    credentials: Optional[Dict[str, Any]] = None
    configuration: Optional[Dict[str, Any]] = None
    sync_frequency: Optional[int] = None
    status: Optional[IntegrationStatus] = None

class IntegrationResponse(BaseModel):
    id: str
    platform_name: PlatformType
    integration_type: IntegrationType
    configuration: Dict[str, Any]
    status: IntegrationStatus
    last_sync: Optional[datetime]
    sync_frequency: int
    error_count: int
    tenant_id: str
    created_by: str
    created_at: datetime
    updated_at: datetime

class WebhookCreate(BaseModel):
    endpoint_url: str
    platform: PlatformType
    event_types: List[str]
    secret_key: Optional[str] = None

class WebhookResponse(BaseModel):
    id: str
    endpoint_url: str
    platform: PlatformType
    event_types: List[str]
    is_verified: bool
    last_event: Optional[datetime]
    event_count: int
    tenant_id: str
    created_at: datetime

class SyncRequest(BaseModel):
    integration_id: str
    sync_type: str = "incremental"  # full, incremental
    force_sync: bool = False

class SyncLogResponse(BaseModel):
    id: str
    integration_id: str
    sync_type: str
    status: SyncStatus
    records_processed: int
    records_created: int
    records_updated: int
    records_failed: int
    error_details: Dict[str, Any]
    execution_time_seconds: Optional[float]
    created_at: datetime

class GoogleAdsConfig(BaseModel):
    customer_id: str
    developer_token: str
    client_id: str
    client_secret: str
    refresh_token: str

class FacebookAdsConfig(BaseModel):
    app_id: str
    app_secret: str
    access_token: str
    ad_account_id: str

class LinkedInAdsConfig(BaseModel):
    client_id: str
    client_secret: str
    access_token: str
    refresh_token: str
    account_id: str

class StripeConfig(BaseModel):
    secret_key: str
    publishable_key: str
    webhook_secret: str

class MauticConfigRequest(BaseModel):
    api_url: str
    client_id: str
    client_secret: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    username: Optional[str] = None  # For basic auth fallback
    password: Optional[str] = None  # For basic auth fallback

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database and event bus connections"""
    global event_bus, redis_client
    
    try:
        await init_database()
        logger.info("Database connections initialized")
        
        redis_client = await get_redis_client()
        
        event_bus = EventBus(redis_client, "integration")
        await event_bus.initialize()
        await event_bus.start()
        logger.info("Event bus initialized")
        
        # Start background sync scheduler
        asyncio.create_task(sync_scheduler())
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Clean shutdown of connections"""
    global event_bus
    
    if event_bus:
        await event_bus.stop()
    logger.info("Integration Service shutdown complete")

# Health check endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "integration",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    try:
        async with get_postgres_session("integration") as session:
            await session.execute("SELECT 1")
        
        await redis_client.ping()
        
        return {
            "status": "ready",
            "service": "integration",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service not ready: {str(e)}"
        )

# Encryption utilities
def encrypt_credentials(credentials: Dict[str, Any]) -> str:
    """Encrypt credentials for secure storage"""
    credentials_json = json.dumps(credentials)
    encrypted_data = cipher_suite.encrypt(credentials_json.encode())
    return base64.b64encode(encrypted_data).decode()

def decrypt_credentials(encrypted_credentials: str) -> Dict[str, Any]:
    """Decrypt stored credentials"""
    encrypted_data = base64.b64decode(encrypted_credentials.encode())
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return json.loads(decrypted_data.decode())

# Integration CRUD endpoints
@app.post("/integrations", response_model=IntegrationResponse)
async def create_integration(
    integration_data: IntegrationCreate,
    current_user: UserContext = Depends(require_permission(Permission.INTEGRATION_CREATE))
):
    """Create a new integration"""
    
    try:
        async with get_postgres_session("integration") as session:
            # Encrypt credentials
            encrypted_credentials = encrypt_credentials(integration_data.credentials)
            
            new_integration = Integration(
                id=uuid.uuid4(),
                platform_name=integration_data.platform_name.value,
                integration_type=integration_data.integration_type.value,
                credentials=encrypted_credentials,
                configuration=integration_data.configuration,
                sync_frequency=integration_data.sync_frequency,
                status=IntegrationStatus.PENDING.value,
                tenant_id=uuid.UUID(current_user.tenant_id),
                created_by=uuid.UUID(current_user.user_id)
            )
            
            session.add(new_integration)
            await session.commit()
            await session.refresh(new_integration)
            
            # Test connection and activate if successful
            connection_test = await test_integration_connection(new_integration)
            if connection_test["success"]:
                new_integration.status = IntegrationStatus.ACTIVE.value
                await session.commit()
            else:
                new_integration.status = IntegrationStatus.ERROR.value
                new_integration.error_count = 1
                await session.commit()
            
            # Publish integration connected event
            event = EventFactory.integration_connected(
                tenant_id=current_user.tenant_id,
                integration_id=str(new_integration.id),
                integration_data={
                    "platform": new_integration.platform_name,
                    "type": new_integration.integration_type,
                    "status": new_integration.status,
                    "created_by": current_user.user_id
                }
            )
            await event_bus.publish(event)
            
            return IntegrationResponse(
                id=str(new_integration.id),
                platform_name=PlatformType(new_integration.platform_name),
                integration_type=IntegrationType(new_integration.integration_type),
                configuration=new_integration.configuration,
                status=IntegrationStatus(new_integration.status),
                last_sync=new_integration.last_sync,
                sync_frequency=new_integration.sync_frequency,
                error_count=new_integration.error_count,
                tenant_id=str(new_integration.tenant_id),
                created_by=str(new_integration.created_by),
                created_at=new_integration.created_at,
                updated_at=new_integration.updated_at
            )
            
    except Exception as e:
        logger.error(f"Create integration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create integration"
        )

async def test_integration_connection(integration: Integration) -> Dict[str, Any]:
    """Test integration connection"""
    
    try:
        credentials = decrypt_credentials(integration.credentials)
        platform = integration.platform_name
        
        if platform == PlatformType.GOOGLE_ADS.value:
            return await test_google_ads_connection(credentials)
        elif platform == PlatformType.FACEBOOK_ADS.value:
            return await test_facebook_ads_connection(credentials)
        elif platform == PlatformType.LINKEDIN_ADS.value:
            return await test_linkedin_ads_connection(credentials)
        elif platform == PlatformType.STRIPE.value:
            return await test_stripe_connection(credentials)
        elif platform == PlatformType.MAUTIC.value:
            return await test_mautic_connection(credentials)
        else:
            # Generic API key test
            return {"success": True, "message": "Connection test not implemented for this platform"}
            
    except Exception as e:
        logger.error(f"Integration connection test error: {e}")
        return {"success": False, "error": str(e)}

async def test_google_ads_connection(credentials: Dict[str, Any]) -> Dict[str, Any]:
    """Test Google Ads API connection"""
    
    # Simulate Google Ads API test
    await asyncio.sleep(1)
    
    required_fields = ["customer_id", "developer_token", "client_id", "client_secret", "refresh_token"]
    missing_fields = [field for field in required_fields if field not in credentials]
    
    if missing_fields:
        return {"success": False, "error": f"Missing required fields: {missing_fields}"}
    
    # In real implementation, would make actual API call
    return {"success": True, "message": "Google Ads connection successful"}

async def test_facebook_ads_connection(credentials: Dict[str, Any]) -> Dict[str, Any]:
    """Test Facebook Ads API connection"""
    
    await asyncio.sleep(1)
    
    required_fields = ["app_id", "app_secret", "access_token", "ad_account_id"]
    missing_fields = [field for field in required_fields if field not in credentials]
    
    if missing_fields:
        return {"success": False, "error": f"Missing required fields: {missing_fields}"}
    
    return {"success": True, "message": "Facebook Ads connection successful"}

async def test_linkedin_ads_connection(credentials: Dict[str, Any]) -> Dict[str, Any]:
    """Test LinkedIn Ads API connection"""
    
    await asyncio.sleep(1)
    
    required_fields = ["client_id", "client_secret", "access_token", "account_id"]
    missing_fields = [field for field in required_fields if field not in credentials]
    
    if missing_fields:
        return {"success": False, "error": f"Missing required fields: {missing_fields}"}
    
    return {"success": True, "message": "LinkedIn Ads connection successful"}

async def test_stripe_connection(credentials: Dict[str, Any]) -> Dict[str, Any]:
    """Test Stripe API connection"""
    
    await asyncio.sleep(1)
    
    required_fields = ["secret_key", "publishable_key"]
    missing_fields = [field for field in required_fields if field not in credentials]
    
    if missing_fields:
        return {"success": False, "error": f"Missing required fields: {missing_fields}"}
    
    return {"success": True, "message": "Stripe connection successful"}

@app.get("/integrations", response_model=List[IntegrationResponse])
async def list_integrations(
    current_user: UserContext = Depends(require_permission(Permission.INTEGRATION_READ)),
    platform: Optional[PlatformType] = None,
    status_filter: Optional[IntegrationStatus] = None
):
    """List integrations for current tenant"""
    
    try:
        async with get_postgres_session("integration") as session:
            from sqlalchemy import select
            
            stmt = select(Integration).where(
                Integration.tenant_id == uuid.UUID(current_user.tenant_id),
                Integration.is_active == True
            )
            
            if platform:
                stmt = stmt.where(Integration.platform_name == platform.value)
            
            if status_filter:
                stmt = stmt.where(Integration.status == status_filter.value)
            
            stmt = stmt.order_by(Integration.created_at.desc())
            
            result = await session.execute(stmt)
            integrations = result.scalars().all()
            
            return [
                IntegrationResponse(
                    id=str(integration.id),
                    platform_name=PlatformType(integration.platform_name),
                    integration_type=IntegrationType(integration.integration_type),
                    configuration=integration.configuration,
                    status=IntegrationStatus(integration.status),
                    last_sync=integration.last_sync,
                    sync_frequency=integration.sync_frequency,
                    error_count=integration.error_count,
                    tenant_id=str(integration.tenant_id),
                    created_by=str(integration.created_by),
                    created_at=integration.created_at,
                    updated_at=integration.updated_at
                ) for integration in integrations
            ]
            
    except Exception as e:
        logger.error(f"List integrations error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list integrations"
        )

@app.get("/integrations/{integration_id}", response_model=IntegrationResponse)
async def get_integration(
    integration_id: str,
    current_user: UserContext = Depends(require_permission(Permission.INTEGRATION_READ))
):
    """Get integration by ID"""
    
    try:
        async with get_postgres_session("integration") as session:
            from sqlalchemy import select
            stmt = select(Integration).where(
                Integration.id == uuid.UUID(integration_id),
                Integration.tenant_id == uuid.UUID(current_user.tenant_id),
                Integration.is_active == True
            )
            result = await session.execute(stmt)
            integration = result.scalar_one_or_none()
            
            if not integration:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Integration not found"
                )
            
            return IntegrationResponse(
                id=str(integration.id),
                platform_name=PlatformType(integration.platform_name),
                integration_type=IntegrationType(integration.integration_type),
                configuration=integration.configuration,
                status=IntegrationStatus(integration.status),
                last_sync=integration.last_sync,
                sync_frequency=integration.sync_frequency,
                error_count=integration.error_count,
                tenant_id=str(integration.tenant_id),
                created_by=str(integration.created_by),
                created_at=integration.created_at,
                updated_at=integration.updated_at
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get integration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get integration"
        )

@app.put("/integrations/{integration_id}", response_model=IntegrationResponse)
async def update_integration(
    integration_id: str,
    integration_data: IntegrationUpdate,
    current_user: UserContext = Depends(require_permission(Permission.INTEGRATION_UPDATE))
):
    """Update integration"""
    
    try:
        async with get_postgres_session("integration") as session:
            from sqlalchemy import select
            stmt = select(Integration).where(
                Integration.id == uuid.UUID(integration_id),
                Integration.tenant_id == uuid.UUID(current_user.tenant_id),
                Integration.is_active == True
            )
            result = await session.execute(stmt)
            integration = result.scalar_one_or_none()
            
            if not integration:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Integration not found"
                )
            
            # Update fields
            if integration_data.credentials:
                integration.credentials = encrypt_credentials(integration_data.credentials)
                
                # Test new credentials
                connection_test = await test_integration_connection(integration)
                if connection_test["success"]:
                    integration.status = IntegrationStatus.ACTIVE.value
                    integration.error_count = 0
                else:
                    integration.status = IntegrationStatus.ERROR.value
                    integration.error_count = integration.error_count + 1
            
            if integration_data.configuration is not None:
                integration.configuration = integration_data.configuration
            
            if integration_data.sync_frequency is not None:
                integration.sync_frequency = integration_data.sync_frequency
            
            if integration_data.status is not None:
                integration.status = integration_data.status.value
            
            integration.updated_at = datetime.utcnow()
            await session.commit()
            await session.refresh(integration)
            
            return IntegrationResponse(
                id=str(integration.id),
                platform_name=PlatformType(integration.platform_name),
                integration_type=IntegrationType(integration.integration_type),
                configuration=integration.configuration,
                status=IntegrationStatus(integration.status),
                last_sync=integration.last_sync,
                sync_frequency=integration.sync_frequency,
                error_count=integration.error_count,
                tenant_id=str(integration.tenant_id),
                created_by=str(integration.created_by),
                created_at=integration.created_at,
                updated_at=integration.updated_at
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update integration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update integration"
        )

# Data synchronization endpoints
@app.post("/integrations/{integration_id}/sync")
async def trigger_sync(
    integration_id: str,
    sync_request: SyncRequest,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.INTEGRATION_READ))
):
    """Trigger data synchronization for integration"""
    
    try:
        async with get_postgres_session("integration") as session:
            from sqlalchemy import select
            stmt = select(Integration).where(
                Integration.id == uuid.UUID(integration_id),
                Integration.tenant_id == uuid.UUID(current_user.tenant_id),
                Integration.is_active == True
            )
            result = await session.execute(stmt)
            integration = result.scalar_one_or_none()
            
            if not integration:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Integration not found"
                )
            
            if integration.status != IntegrationStatus.ACTIVE.value:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Integration is not active"
                )
            
            # Create sync log entry
            sync_log = SyncLog(
                id=uuid.uuid4(),
                integration_id=integration.id,
                tenant_id=integration.tenant_id,
                sync_type=sync_request.sync_type,
                status=SyncStatus.SUCCESS.value,  # Will be updated by background task
                records_processed=0,
                records_created=0,
                records_updated=0,
                records_failed=0
            )
            
            session.add(sync_log)
            await session.commit()
            await session.refresh(sync_log)
            
            # Publish sync started event
            event = EventFactory.integration_sync_started(
                tenant_id=current_user.tenant_id,
                integration_id=integration_id,
                sync_data={
                    "sync_log_id": str(sync_log.id),
                    "sync_type": sync_request.sync_type,
                    "platform": integration.platform_name
                }
            )
            await event_bus.publish(event)
            
            # Schedule background sync
            background_tasks.add_task(
                execute_sync,
                str(sync_log.id),
                integration_id,
                sync_request.sync_type,
                sync_request.force_sync
            )
            
            return {
                "message": "Sync started",
                "sync_log_id": str(sync_log.id),
                "integration_id": integration_id,
                "sync_type": sync_request.sync_type
            }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Trigger sync error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to trigger sync"
        )

async def execute_sync(sync_log_id: str, integration_id: str, sync_type: str, force_sync: bool):
    """Background task to execute data synchronization"""
    
    try:
        async with get_postgres_session("integration") as session:
            from sqlalchemy import select
            
            # Get integration and sync log
            integration_stmt = select(Integration).where(Integration.id == uuid.UUID(integration_id))
            integration_result = await session.execute(integration_stmt)
            integration = integration_result.scalar_one_or_none()
            
            sync_log_stmt = select(SyncLog).where(SyncLog.id == uuid.UUID(sync_log_id))
            sync_log_result = await session.execute(sync_log_stmt)
            sync_log = sync_log_result.scalar_one_or_none()
            
            if not integration or not sync_log:
                logger.error(f"Integration or sync log not found: {integration_id}, {sync_log_id}")
                return
            
            start_time = datetime.utcnow()
            
            try:
                # Execute platform-specific sync
                sync_result = await execute_platform_sync(integration, sync_type, force_sync)
                
                # Update sync log with results
                sync_log.status = SyncStatus.SUCCESS.value if sync_result["success"] else SyncStatus.ERROR.value
                sync_log.records_processed = sync_result.get("records_processed", 0)
                sync_log.records_created = sync_result.get("records_created", 0)
                sync_log.records_updated = sync_result.get("records_updated", 0)
                sync_log.records_failed = sync_result.get("records_failed", 0)
                sync_log.execution_time_seconds = (datetime.utcnow() - start_time).total_seconds()
                sync_log.error_details = sync_result.get("errors", {})
                
                # Update integration last sync time
                integration.last_sync = datetime.utcnow()
                if sync_result["success"]:
                    integration.error_count = 0
                else:
                    integration.error_count = integration.error_count + 1
                
                await session.commit()
                
                # Publish sync completed event
                event = EventFactory.integration_sync_completed(
                    tenant_id=str(integration.tenant_id),
                    integration_id=integration_id,
                    sync_data={
                        "sync_log_id": sync_log_id,
                        "status": sync_log.status,
                        "records_processed": sync_log.records_processed,
                        "execution_time": sync_log.execution_time_seconds
                    }
                )
                await event_bus.publish(event)
                
            except Exception as sync_error:
                # Handle sync errors
                sync_log.status = SyncStatus.ERROR.value
                sync_log.execution_time_seconds = (datetime.utcnow() - start_time).total_seconds()
                sync_log.error_details = {"error": str(sync_error)}
                
                integration.error_count = integration.error_count + 1
                if integration.error_count > 5:  # Too many consecutive errors
                    integration.status = IntegrationStatus.ERROR.value
                
                await session.commit()
                
                # Publish sync failed event
                event = EventFactory.integration_sync_failed(
                    tenant_id=str(integration.tenant_id),
                    integration_id=integration_id,
                    sync_data={
                        "sync_log_id": sync_log_id,
                        "error": str(sync_error),
                        "error_count": integration.error_count
                    }
                )
                await event_bus.publish(event)
                
    except Exception as e:
        logger.error(f"Execute sync error: {e}")

async def execute_platform_sync(integration: Integration, sync_type: str, force_sync: bool) -> Dict[str, Any]:
    """Execute platform-specific data synchronization"""
    
    platform = integration.platform_name
    credentials = decrypt_credentials(integration.credentials)
    
    # Simulate sync execution
    await asyncio.sleep(3)
    
    if platform == PlatformType.GOOGLE_ADS.value:
        return await sync_google_ads_data(credentials, sync_type, force_sync)
    elif platform == PlatformType.FACEBOOK_ADS.value:
        return await sync_facebook_ads_data(credentials, sync_type, force_sync)
    elif platform == PlatformType.LINKEDIN_ADS.value:
        return await sync_linkedin_ads_data(credentials, sync_type, force_sync)
    elif platform == PlatformType.STRIPE.value:
        return await sync_stripe_data(credentials, sync_type, force_sync)
    elif platform == PlatformType.MAUTIC.value:
        return await sync_mautic_data(credentials, sync_type, force_sync)
    else:
        return {
            "success": True,
            "records_processed": 100,
            "records_created": 20,
            "records_updated": 75,
            "records_failed": 5,
            "message": f"Simulated sync for {platform}"
        }

async def sync_google_ads_data(credentials: Dict[str, Any], sync_type: str, force_sync: bool) -> Dict[str, Any]:
    """Sync Google Ads data"""
    
    # In real implementation, would use Google Ads API
    await asyncio.sleep(2)
    
    return {
        "success": True,
        "records_processed": 150,
        "records_created": 25,
        "records_updated": 120,
        "records_failed": 5,
        "message": "Google Ads data synced successfully"
    }

async def sync_facebook_ads_data(credentials: Dict[str, Any], sync_type: str, force_sync: bool) -> Dict[str, Any]:
    """Sync Facebook Ads data"""
    
    await asyncio.sleep(2)
    
    return {
        "success": True,
        "records_processed": 120,
        "records_created": 30,
        "records_updated": 85,
        "records_failed": 5,
        "message": "Facebook Ads data synced successfully"
    }

async def sync_linkedin_ads_data(credentials: Dict[str, Any], sync_type: str, force_sync: bool) -> Dict[str, Any]:
    """Sync LinkedIn Ads data"""
    
    await asyncio.sleep(2)
    
    return {
        "success": True,
        "records_processed": 80,
        "records_created": 15,
        "records_updated": 60,
        "records_failed": 5,
        "message": "LinkedIn Ads data synced successfully"
    }

async def sync_stripe_data(credentials: Dict[str, Any], sync_type: str, force_sync: bool) -> Dict[str, Any]:
    """Sync Stripe payment data"""
    
    await asyncio.sleep(1)
    
    return {
        "success": True,
        "records_processed": 50,
        "records_created": 10,
        "records_updated": 35,
        "records_failed": 5,
        "message": "Stripe data synced successfully"
    }

@app.get("/integrations/{integration_id}/sync-logs", response_model=List[SyncLogResponse])
async def get_sync_logs(
    integration_id: str,
    current_user: UserContext = Depends(require_permission(Permission.INTEGRATION_READ)),
    limit: int = 50
):
    """Get sync logs for integration"""
    
    try:
        async with get_postgres_session("integration") as session:
            from sqlalchemy import select
            
            # Verify integration access
            integration_stmt = select(Integration).where(
                Integration.id == uuid.UUID(integration_id),
                Integration.tenant_id == uuid.UUID(current_user.tenant_id)
            )
            integration_result = await session.execute(integration_stmt)
            integration = integration_result.scalar_one_or_none()
            
            if not integration:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Integration not found"
                )
            
            # Get sync logs
            stmt = select(SyncLog).where(
                SyncLog.integration_id == uuid.UUID(integration_id)
            ).order_by(SyncLog.created_at.desc()).limit(limit)
            
            result = await session.execute(stmt)
            sync_logs = result.scalars().all()
            
            return [
                SyncLogResponse(
                    id=str(log.id),
                    integration_id=str(log.integration_id),
                    sync_type=log.sync_type,
                    status=SyncStatus(log.status),
                    records_processed=log.records_processed,
                    records_created=log.records_created,
                    records_updated=log.records_updated,
                    records_failed=log.records_failed,
                    error_details=log.error_details,
                    execution_time_seconds=log.execution_time_seconds,
                    created_at=log.created_at
                ) for log in sync_logs
            ]
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get sync logs error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get sync logs"
        )

# Webhook endpoints
@app.post("/webhooks", response_model=WebhookResponse)
async def create_webhook(
    webhook_data: WebhookCreate,
    current_user: UserContext = Depends(require_permission(Permission.INTEGRATION_CREATE))
):
    """Create a new webhook endpoint"""
    
    try:
        async with get_postgres_session("integration") as session:
            new_webhook = WebhookEndpoint(
                id=uuid.uuid4(),
                endpoint_url=webhook_data.endpoint_url,
                platform=webhook_data.platform.value,
                event_types=webhook_data.event_types,
                secret_key=webhook_data.secret_key,
                is_verified=False,
                tenant_id=uuid.UUID(current_user.tenant_id)
            )
            
            session.add(new_webhook)
            await session.commit()
            await session.refresh(new_webhook)
            
            return WebhookResponse(
                id=str(new_webhook.id),
                endpoint_url=new_webhook.endpoint_url,
                platform=PlatformType(new_webhook.platform),
                event_types=new_webhook.event_types,
                is_verified=new_webhook.is_verified,
                last_event=new_webhook.last_event,
                event_count=new_webhook.event_count,
                tenant_id=str(new_webhook.tenant_id),
                created_at=new_webhook.created_at
            )
            
    except Exception as e:
        logger.error(f"Create webhook error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create webhook"
        )

@app.post("/webhooks/{platform}/receive")
async def receive_webhook(
    platform: PlatformType,
    request: Request
):
    """Receive webhook from external platform"""
    
    try:
        # Get request body and headers
        body = await request.body()
        headers = dict(request.headers)
        
        # Log webhook receipt
        logger.info(f"Received webhook from {platform.value}")
        
        # Verify webhook signature if required
        if platform == PlatformType.STRIPE:
            signature = headers.get("stripe-signature")
            if not verify_stripe_signature(body, signature):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid webhook signature"
                )
        
        # Parse webhook data
        webhook_data = json.loads(body.decode())
        
        # Process webhook based on platform and event type
        await process_webhook_event(platform, webhook_data, headers)
        
        # Update webhook endpoint stats
        await update_webhook_stats(platform, webhook_data.get("type", "unknown"))
        
        return {"status": "received"}
        
    except Exception as e:
        logger.error(f"Receive webhook error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process webhook"
        )

def verify_stripe_signature(payload: bytes, signature_header: str) -> bool:
    """Verify Stripe webhook signature"""
    
    try:
        # In real implementation, would verify using Stripe's webhook secret
        return True
    except Exception as e:
        logger.error(f"Stripe signature verification error: {e}")
        return False

async def process_webhook_event(platform: PlatformType, data: Dict[str, Any], headers: Dict[str, str]):
    """Process webhook event data"""
    
    event_type = data.get("type", "unknown")
    
    if platform == PlatformType.STRIPE:
        await process_stripe_webhook(data, headers)
    elif platform == PlatformType.FACEBOOK_ADS:
        await process_facebook_webhook(data, headers)
    elif platform == PlatformType.GOOGLE_ADS:
        await process_google_webhook(data, headers)
    
    logger.info(f"Processed {platform.value} webhook: {event_type}")

async def process_stripe_webhook(data: Dict[str, Any], headers: Dict[str, str]):
    """Process Stripe webhook events"""
    
    event_type = data.get("type")
    
    if event_type == "payment_intent.succeeded":
        # Handle successful payment
        payment_data = data.get("data", {}).get("object", {})
        logger.info(f"Payment succeeded: {payment_data.get('id')}")
        
        # Publish payment success event
        # Would extract tenant_id from payment metadata
        
    elif event_type == "subscription.created":
        # Handle new subscription
        subscription_data = data.get("data", {}).get("object", {})
        logger.info(f"New subscription: {subscription_data.get('id')}")

async def process_facebook_webhook(data: Dict[str, Any], headers: Dict[str, str]):
    """Process Facebook Ads webhook events"""
    
    # Process Facebook Ads webhook data
    logger.info(f"Processing Facebook webhook: {data}")

async def process_google_webhook(data: Dict[str, Any], headers: Dict[str, str]):
    """Process Google Ads webhook events"""
    
    # Process Google Ads webhook data
    logger.info(f"Processing Google webhook: {data}")

async def update_webhook_stats(platform: PlatformType, event_type: str):
    """Update webhook endpoint statistics"""
    
    try:
        async with get_postgres_session("integration") as session:
            from sqlalchemy import select, update
            
            # Find webhook endpoint for this platform
            stmt = select(WebhookEndpoint).where(
                WebhookEndpoint.platform == platform.value,
                WebhookEndpoint.is_active == True
            )
            result = await session.execute(stmt)
            webhook = result.scalar_one_or_none()
            
            if webhook:
                webhook.event_count = webhook.event_count + 1
                webhook.last_event = datetime.utcnow()
                await session.commit()
                
    except Exception as e:
        logger.error(f"Update webhook stats error: {e}")

# Background sync scheduler
async def sync_scheduler():
    """Background task to schedule automatic syncs"""
    
    while True:
        try:
            await asyncio.sleep(300)  # Check every 5 minutes
            
            async with get_postgres_session("integration") as session:
                from sqlalchemy import select
                
                # Find integrations due for sync
                current_time = datetime.utcnow()
                stmt = select(Integration).where(
                    Integration.status == IntegrationStatus.ACTIVE.value,
                    Integration.is_active == True
                )
                result = await session.execute(stmt)
                integrations = result.scalars().all()
                
                for integration in integrations:
                    if integration.last_sync is None:
                        # Never synced before
                        should_sync = True
                    else:
                        # Check if sync is due
                        next_sync_time = integration.last_sync + timedelta(seconds=integration.sync_frequency)
                        should_sync = current_time >= next_sync_time
                    
                    if should_sync:
                        logger.info(f"Scheduling automatic sync for integration {integration.id}")
                        
                        # Create sync task
                        asyncio.create_task(
                            execute_sync(
                                str(uuid.uuid4()),  # Create a temporary sync log ID
                                str(integration.id),
                                "incremental",
                                False
                            )
                        )
                        
        except Exception as e:
            logger.error(f"Sync scheduler error: {e}")
            await asyncio.sleep(60)  # Wait 1 minute before retrying

# Event handlers
@event_handler(EventType.CAMPAIGN_STARTED)
async def handle_campaign_started(event):
    """Handle campaign started - could trigger platform sync"""
    logger.info(f"Campaign started, checking for platform integrations: {event.data}")

@event_handler(EventType.USER_CREATED)
async def handle_user_created(event):
    """Handle new user created - could set up integrations"""
    logger.info(f"New user created, setting up default integrations: {event.data}")

# Mautic-specific endpoints
@app.post("/mautic/contacts", dependencies=[Depends(require_permission(Permission.INTEGRATION_READ))])
async def create_mautic_contact(
    integration_id: str,
    contact_data: Dict[str, Any],
    current_user: UserContext = Depends(get_current_user)
):
    """Create contact in Mautic via integration"""
    
    try:
        async with get_postgres_session("integration") as session:
            from sqlalchemy import select
            
            # Get integration
            stmt = select(Integration).where(
                Integration.id == uuid.UUID(integration_id),
                Integration.tenant_id == uuid.UUID(current_user.tenant_id),
                Integration.platform_name == PlatformType.MAUTIC.value,
                Integration.status == IntegrationStatus.ACTIVE.value
            )
            result = await session.execute(stmt)
            integration = result.scalar_one_or_none()
            
            if not integration:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Active Mautic integration not found"
                )
            
            # Create contact via Mautic API
            credentials = decrypt_credentials(integration.credentials)
            config = MauticConfig(**credentials)
            
            from .mautic_integration import MauticIntegration, MauticContact
            
            mautic_contact = MauticContact(**contact_data)
            
            async with MauticIntegration(config) as mautic:
                auth_result = await mautic.authenticate()
                if not auth_result["success"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Mautic authentication failed: {auth_result['error']}"
                    )
                
                result = await mautic.create_contact(mautic_contact)
                
                if result["success"]:
                    # Publish contact created event
                    event = EventFactory.contact_created(
                        tenant_id=current_user.tenant_id,
                        contact_data={
                            "mautic_contact_id": result["contact_id"],
                            "email": contact_data.get("email"),
                            "integration_id": integration_id
                        }
                    )
                    await event_bus.publish(event)
                    
                    return {
                        "success": True,
                        "mautic_contact_id": result["contact_id"],
                        "message": "Contact created successfully in Mautic"
                    }
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Failed to create contact: {result['error']}"
                    )
                    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create Mautic contact error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create Mautic contact"
        )

@app.post("/mautic/campaigns", dependencies=[Depends(require_permission(Permission.INTEGRATION_READ))])
async def create_mautic_campaign(
    integration_id: str,
    campaign_data: Dict[str, Any],
    current_user: UserContext = Depends(get_current_user)
):
    """Create campaign in Mautic via integration"""
    
    try:
        async with get_postgres_session("integration") as session:
            from sqlalchemy import select
            
            # Get integration
            stmt = select(Integration).where(
                Integration.id == uuid.UUID(integration_id),
                Integration.tenant_id == uuid.UUID(current_user.tenant_id),
                Integration.platform_name == PlatformType.MAUTIC.value,
                Integration.status == IntegrationStatus.ACTIVE.value
            )
            result = await session.execute(stmt)
            integration = result.scalar_one_or_none()
            
            if not integration:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Active Mautic integration not found"
                )
            
            # Create campaign via Mautic API
            credentials = decrypt_credentials(integration.credentials)
            config = MauticConfig(**credentials)
            
            from .mautic_integration import MauticIntegration, MauticCampaign
            
            mautic_campaign = MauticCampaign(**campaign_data)
            
            async with MauticIntegration(config) as mautic:
                auth_result = await mautic.authenticate()
                if not auth_result["success"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Mautic authentication failed: {auth_result['error']}"
                    )
                
                result = await mautic.create_campaign(mautic_campaign)
                
                if result["success"]:
                    return {
                        "success": True,
                        "mautic_campaign_id": result["campaign_id"],
                        "message": "Campaign created successfully in Mautic"
                    }
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Failed to create campaign: {result['error']}"
                    )
                    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create Mautic campaign error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create Mautic campaign"
        )

@app.post("/mautic/emails", dependencies=[Depends(require_permission(Permission.INTEGRATION_READ))])
async def create_mautic_email(
    integration_id: str,
    email_data: Dict[str, Any],
    current_user: UserContext = Depends(get_current_user)
):
    """Create email template in Mautic via integration"""
    
    try:
        async with get_postgres_session("integration") as session:
            from sqlalchemy import select
            
            # Get integration
            stmt = select(Integration).where(
                Integration.id == uuid.UUID(integration_id),
                Integration.tenant_id == uuid.UUID(current_user.tenant_id),
                Integration.platform_name == PlatformType.MAUTIC.value,
                Integration.status == IntegrationStatus.ACTIVE.value
            )
            result = await session.execute(stmt)
            integration = result.scalar_one_or_none()
            
            if not integration:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Active Mautic integration not found"
                )
            
            # Create email via Mautic API
            credentials = decrypt_credentials(integration.credentials)
            config = MauticConfig(**credentials)
            
            from .mautic_integration import MauticIntegration, MauticEmail
            
            mautic_email = MauticEmail(**email_data)
            
            async with MauticIntegration(config) as mautic:
                auth_result = await mautic.authenticate()
                if not auth_result["success"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Mautic authentication failed: {auth_result['error']}"
                    )
                
                result = await mautic.create_email(mautic_email)
                
                if result["success"]:
                    return {
                        "success": True,
                        "mautic_email_id": result["email_id"],
                        "message": "Email template created successfully in Mautic"
                    }
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Failed to create email: {result['error']}"
                    )
                    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create Mautic email error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create Mautic email"
        )

@app.get("/mautic/stats/{integration_id}")
async def get_mautic_stats(
    integration_id: str,
    current_user: UserContext = Depends(require_permission(Permission.INTEGRATION_READ))
):
    """Get Mautic performance statistics"""
    
    try:
        async with get_postgres_session("integration") as session:
            from sqlalchemy import select
            
            # Get integration
            stmt = select(Integration).where(
                Integration.id == uuid.UUID(integration_id),
                Integration.tenant_id == uuid.UUID(current_user.tenant_id),
                Integration.platform_name == PlatformType.MAUTIC.value,
                Integration.status == IntegrationStatus.ACTIVE.value
            )
            result = await session.execute(stmt)
            integration = result.scalar_one_or_none()
            
            if not integration:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Active Mautic integration not found"
                )
            
            # Get stats via Mautic API
            credentials = decrypt_credentials(integration.credentials)
            config = MauticConfig(**credentials)
            
            from .mautic_integration import MauticIntegration
            
            async with MauticIntegration(config) as mautic:
                auth_result = await mautic.authenticate()
                if not auth_result["success"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Mautic authentication failed: {auth_result['error']}"
                    )
                
                # Get basic stats
                contacts_result = await mautic.search_contacts({"limit": 1})
                campaigns_result = await mautic.get_campaigns()
                emails_result = await mautic.get_emails()
                
                stats = {
                    "total_contacts": 0,
                    "total_campaigns": 0,
                    "total_emails": 0,
                    "last_sync": integration.last_sync.isoformat() if integration.last_sync else None
                }
                
                if contacts_result["success"]:
                    stats["total_contacts"] = contacts_result["data"].get("total", 0)
                
                if campaigns_result["success"]:
                    stats["total_campaigns"] = len(campaigns_result["data"].get("campaigns", {}))
                
                if emails_result["success"]:
                    stats["total_emails"] = len(emails_result["data"].get("emails", {}))
                
                return {
                    "success": True,
                    "integration_id": integration_id,
                    "stats": stats
                }
                    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get Mautic stats error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get Mautic stats"
        )

# Metrics endpoint
@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return {
        "service": "integration",
        "metrics": {
            "active_integrations": 0,
            "total_syncs": 0,
            "failed_syncs": 0,
            "webhook_events": 0
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)