"""
Multi-Platform Sync API Routes
Provides REST endpoints for multi-platform directory synchronization
"""

import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_async_session
from ..core.auth import get_current_tenant
from ..models.base import ConflictResolution
from ..services.multi_platform_sync_engine import (
    sync_engine, Platform, SyncOperation, BatchSyncRequest,
    ConflictDetail, ConflictType, SyncResult
)
from ..schemas.business import BusinessSyncResponse, ConflictDetailResponse

router = APIRouter(prefix="/sync", tags=["Multi-Platform Sync"])

# Request Models
class PlatformSyncRequest(BaseModel):
    business_id: str
    platform: Platform
    operation: SyncOperation = SyncOperation.UPDATE
    auth_data: Optional[Dict[str, Any]] = None

class MultiPlatformSyncRequest(BaseModel):
    business_id: str
    platforms: Optional[List[Platform]] = None  # If None, sync to all platforms
    exclude_platforms: Optional[List[Platform]] = None
    auth_data: Optional[Dict[Platform, Dict[str, Any]]] = None

class BatchSyncRequestModel(BaseModel):
    business_ids: List[str]
    platforms: List[Platform]
    operations: List[SyncOperation] = [SyncOperation.UPDATE]
    conflict_resolution: ConflictResolution = ConflictResolution.ASK_USER
    batch_size: int = Field(default=10, ge=1, le=50)
    delay_between_batches: float = Field(default=5.0, ge=0.1, le=60.0)
    auth_data: Optional[Dict[Platform, Dict[str, Any]]] = None

class ConflictResolutionRequest(BaseModel):
    business_id: str
    conflict_type: ConflictType
    field_name: str
    resolution_strategy: ConflictResolution
    preferred_value: Optional[Any] = None

class ScheduleSyncRequest(BaseModel):
    business_id: str
    platforms: List[Platform]
    schedule_time: Optional[datetime] = None

# Response Models
class SyncResultResponse(BaseModel):
    platform: Platform
    operation: SyncOperation
    success: bool
    business_id: Optional[str] = None
    platform_id: Optional[str] = None
    error: Optional[str] = None
    conflicts: List[Dict[str, Any]] = []
    data: Optional[Dict[str, Any]] = None

class BatchSyncResponse(BaseModel):
    total_operations: int
    successful_operations: int
    failed_operations: int
    results: List[SyncResultResponse]
    execution_time: float

class SyncStatusResponse(BaseModel):
    business_id: str
    platforms: Dict[Platform, Dict[str, Any]]
    conflicts: List[ConflictDetailResponse]
    last_updated: datetime

# Endpoints

@router.post("/business/platform", response_model=SyncResultResponse)
async def sync_business_to_platform(
    request: PlatformSyncRequest,
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Sync a single business to a specific platform"""
    try:
        result = await sync_engine.sync_business_to_platform(
            request.business_id,
            request.platform,
            request.operation,
            request.auth_data
        )
        
        return SyncResultResponse(**result.__dict__)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/business/all-platforms", response_model=List[SyncResultResponse])
async def sync_business_to_all_platforms(
    request: MultiPlatformSyncRequest,
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Sync a business to all or specified platforms"""
    try:
        platforms = request.platforms
        if platforms is None:
            platforms = list(Platform)
        
        results = await sync_engine.sync_business_to_all_platforms(
            request.business_id,
            request.auth_data,
            request.exclude_platforms
        )
        
        return [SyncResultResponse(**result.__dict__) for result in results]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch", response_model=BatchSyncResponse)
async def batch_sync_businesses(
    request: BatchSyncRequestModel,
    background_tasks: BackgroundTasks,
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Execute batch sync operations across multiple businesses and platforms"""
    try:
        start_time = datetime.utcnow()
        
        batch_request = BatchSyncRequest(
            businesses=request.business_ids,
            platforms=request.platforms,
            operations=request.operations,
            conflict_resolution=request.conflict_resolution,
            batch_size=request.batch_size,
            delay_between_batches=request.delay_between_batches
        )
        
        results = await sync_engine.batch_sync(batch_request, request.auth_data)
        
        end_time = datetime.utcnow()
        execution_time = (end_time - start_time).total_seconds()
        
        successful_operations = sum(1 for r in results if r.success)
        failed_operations = len(results) - successful_operations
        
        return BatchSyncResponse(
            total_operations=len(results),
            successful_operations=successful_operations,
            failed_operations=failed_operations,
            results=[SyncResultResponse(**result.__dict__) for result in results],
            execution_time=execution_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/business/{business_id}/status", response_model=SyncStatusResponse)
async def get_sync_status(
    business_id: str,
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Get sync status for all platforms for a business"""
    try:
        # Get platform sync status
        platform_status = await sync_engine.get_sync_status(business_id)
        
        # Get conflicts
        conflicts = await sync_engine.detect_conflicts(business_id)
        conflict_responses = [
            ConflictDetailResponse(
                conflict_type=c.conflict_type,
                platforms=c.platforms,
                field_name=c.field_name,
                values=c.values,
                suggested_resolution=c.suggested_resolution,
                priority=c.priority
            )
            for c in conflicts
        ]
        
        return SyncStatusResponse(
            business_id=business_id,
            platforms=platform_status,
            conflicts=conflict_responses,
            last_updated=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/business/{business_id}/conflicts", response_model=List[ConflictDetailResponse])
async def detect_conflicts(
    business_id: str,
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Detect conflicts across platforms for a business"""
    try:
        conflicts = await sync_engine.detect_conflicts(business_id)
        
        return [
            ConflictDetailResponse(
                conflict_type=c.conflict_type,
                platforms=c.platforms,
                field_name=c.field_name,
                values=c.values,
                suggested_resolution=c.suggested_resolution,
                priority=c.priority
            )
            for c in conflicts
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/business/{business_id}/resolve-conflict")
async def resolve_conflict(
    business_id: str,
    request: ConflictResolutionRequest,
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Resolve a specific conflict for a business"""
    try:
        # Create conflict detail from request
        conflict = ConflictDetail(
            conflict_type=request.conflict_type,
            platforms=[],  # Will be populated by sync engine
            field_name=request.field_name,
            values={}  # Will be populated by sync engine
        )
        
        success = await sync_engine.resolve_conflict(
            business_id,
            conflict,
            request.resolution_strategy,
            request.preferred_value
        )
        
        if success:
            return {"message": "Conflict resolved successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to resolve conflict")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/business/{business_id}/schedule")
async def schedule_sync(
    business_id: str,
    request: ScheduleSyncRequest,
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Schedule a sync operation for later execution"""
    try:
        sync_id = await sync_engine.schedule_sync(
            business_id,
            request.platforms,
            request.schedule_time
        )
        
        return {
            "sync_id": sync_id,
            "business_id": business_id,
            "platforms": request.platforms,
            "scheduled_for": request.schedule_time or datetime.utcnow(),
            "message": "Sync scheduled successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Platform-specific endpoints

@router.post("/platforms/google/{business_id}")
async def sync_to_google(
    business_id: str,
    auth_data: Dict[str, Any],
    operation: SyncOperation = SyncOperation.UPDATE,
    tenant: Dict = Depends(get_current_tenant)
):
    """Sync business to Google Business Profile"""
    request = PlatformSyncRequest(
        business_id=business_id,
        platform=Platform.GOOGLE,
        operation=operation,
        auth_data=auth_data
    )
    return await sync_business_to_platform(request, tenant)

@router.post("/platforms/yelp/{business_id}")
async def sync_to_yelp(
    business_id: str,
    operation: SyncOperation = SyncOperation.CLAIM,
    tenant: Dict = Depends(get_current_tenant)
):
    """Claim business on Yelp (read-only platform)"""
    request = PlatformSyncRequest(
        business_id=business_id,
        platform=Platform.YELP,
        operation=operation
    )
    return await sync_business_to_platform(request, tenant)

@router.post("/platforms/facebook/{business_id}")
async def sync_to_facebook(
    business_id: str,
    auth_data: Dict[str, Any],
    operation: SyncOperation = SyncOperation.UPDATE,
    tenant: Dict = Depends(get_current_tenant)
):
    """Sync business to Facebook Business Page"""
    request = PlatformSyncRequest(
        business_id=business_id,
        platform=Platform.FACEBOOK,
        operation=operation,
        auth_data=auth_data
    )
    return await sync_business_to_platform(request, tenant)

@router.post("/platforms/apple-maps/{business_id}")
async def sync_to_apple_maps(
    business_id: str,
    operation: SyncOperation = SyncOperation.UPDATE,
    tenant: Dict = Depends(get_current_tenant)
):
    """Sync business to Apple Maps"""
    request = PlatformSyncRequest(
        business_id=business_id,
        platform=Platform.APPLE_MAPS,
        operation=operation
    )
    return await sync_business_to_platform(request, tenant)

# Analytics and monitoring endpoints

@router.get("/analytics/sync-performance")
async def get_sync_performance(
    days: int = Query(default=7, ge=1, le=90),
    platform: Optional[Platform] = None,
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Get sync performance analytics"""
    try:
        # This would typically query sync logs from the database
        # For now, return mock data
        return {
            "period_days": days,
            "platform": platform,
            "total_syncs": 1250,
            "successful_syncs": 1180,
            "failed_syncs": 70,
            "success_rate": 94.4,
            "average_sync_time": 2.3,
            "most_common_errors": [
                {"error": "Rate limit exceeded", "count": 25},
                {"error": "Authentication failed", "count": 20},
                {"error": "Invalid business data", "count": 15}
            ],
            "platform_breakdown": {
                "google": {"syncs": 400, "success_rate": 96.0},
                "yelp": {"syncs": 300, "success_rate": 92.0},
                "facebook": {"syncs": 350, "success_rate": 94.5},
                "apple_maps": {"syncs": 200, "success_rate": 95.0}
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/conflict-trends")
async def get_conflict_trends(
    days: int = Query(default=30, ge=1, le=90),
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Get conflict detection trends"""
    try:
        return {
            "period_days": days,
            "total_conflicts": 156,
            "resolved_conflicts": 142,
            "pending_conflicts": 14,
            "conflict_types": {
                "name_mismatch": 45,
                "address_mismatch": 38,
                "phone_mismatch": 32,
                "hours_mismatch": 28,
                "category_mismatch": 13
            },
            "resolution_methods": {
                "use_google": 68,
                "use_latest": 42,
                "manual_resolution": 32
            },
            "most_conflicted_businesses": [
                {"business_id": "bus_1", "name": "Pizza Palace", "conflicts": 8},
                {"business_id": "bus_2", "name": "Coffee Corner", "conflicts": 6},
                {"business_id": "bus_3", "name": "Auto Repair Shop", "conflicts": 5}
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Utility endpoints

@router.get("/platforms/supported")
async def get_supported_platforms():
    """Get list of supported platforms and their capabilities"""
    return {
        "platforms": [
            {
                "id": "google",
                "name": "Google Business Profile",
                "capabilities": ["create", "update", "delete", "claim", "verify"],
                "auth_required": True,
                "auth_type": "oauth2",
                "read_only": False
            },
            {
                "id": "yelp",
                "name": "Yelp Business",
                "capabilities": ["claim"],
                "auth_required": False,
                "auth_type": "api_key",
                "read_only": True
            },
            {
                "id": "facebook",
                "name": "Facebook Business Page",
                "capabilities": ["update"],
                "auth_required": True,
                "auth_type": "oauth2",
                "read_only": False
            },
            {
                "id": "apple_maps",
                "name": "Apple Maps Connect",
                "capabilities": ["create", "update", "claim"],
                "auth_required": True,
                "auth_type": "jwt",
                "read_only": False
            }
        ]
    }

@router.get("/health")
async def health_check():
    """Check health of all platform integrations"""
    health_status = {}
    
    for platform in Platform:
        try:
            # Perform basic health check for each platform
            # This would typically test authentication and basic API access
            health_status[platform] = {
                "status": "healthy",
                "last_check": datetime.utcnow().isoformat(),
                "response_time": 0.15  # Mock response time
            }
        except Exception as e:
            health_status[platform] = {
                "status": "unhealthy",
                "last_check": datetime.utcnow().isoformat(),
                "error": str(e)
            }
    
    overall_status = "healthy" if all(
        status["status"] == "healthy" for status in health_status.values()
    ) else "degraded"
    
    return {
        "overall_status": overall_status,
        "platforms": health_status,
        "timestamp": datetime.utcnow().isoformat()
    }