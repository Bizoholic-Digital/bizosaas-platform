"""
Multi-Platform Directory Sync API
Comprehensive API endpoints for managing 15+ platform integrations
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from pydantic import BaseModel, Field
from enum import Enum

from ..services.sync.advanced_multi_platform_orchestrator import (
    AdvancedMultiPlatformOrchestrator, SyncRequest, SyncStrategy, SyncPriority,
    advanced_orchestrator
)
from ..services.platform_abstraction.platform_factory import get_platform_factory
from ..services.platform_abstraction.platform_registry import get_platform_registry
from ..services.platform_abstraction.base_platform_client import AuthCredentials, SyncOperation
from ..core.database import get_async_session
from ..core.auth import get_current_user

logger = logging.getLogger(__name__)

# Pydantic Models for API

class SyncStrategyEnum(str, Enum):
    AGGRESSIVE = "aggressive"
    CONSERVATIVE = "conservative"
    SELECTIVE = "selective"
    CUSTOM = "custom"

class SyncPriorityEnum(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class SyncOperationEnum(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    CLAIM = "claim"
    VERIFY = "verify"
    SEARCH = "search"

class PlatformCredentials(BaseModel):
    platform: str
    credentials: Dict[str, Any]
    expires_at: Optional[datetime] = None

class MultiPlatformSyncRequest(BaseModel):
    business_id: str
    strategy: SyncStrategyEnum = SyncStrategyEnum.CONSERVATIVE
    operations: List[SyncOperationEnum] = Field(default_factory=lambda: [SyncOperationEnum.UPDATE])
    platforms: Optional[List[str]] = None
    priority: SyncPriorityEnum = SyncPriorityEnum.MEDIUM
    max_concurrent: int = Field(default=3, ge=1, le=10)
    retry_failed: bool = True
    notify_on_completion: bool = True

class PlatformStatusResponse(BaseModel):
    platform_name: str
    client_available: bool
    last_health_check: Optional[bool]
    metadata: Optional[Dict[str, Any]]
    capabilities: Optional[Dict[str, Any]]

class SyncResultResponse(BaseModel):
    business_id: str
    request_id: str
    overall_success: bool
    total_platforms: int
    successful_platforms: int
    failed_platforms: int
    execution_time: float
    recommendations: List[str]
    platform_results: Dict[str, Dict[str, Any]]

class AnalyticsResponse(BaseModel):
    total_syncs: int
    success_rate: float
    avg_execution_time: float
    platform_performance: Dict[str, Dict[str, Any]]
    recommendations: List[str]

# Router setup
router = APIRouter(
    prefix="/api/brain/business-directory/multi-platform",
    tags=["Multi-Platform Sync"],
    responses={404: {"description": "Not found"}}
)

@router.get("/platforms", response_model=List[PlatformStatusResponse])
async def list_all_platforms():
    """
    Get comprehensive status of all registered platforms
    """
    try:
        factory = get_platform_factory()
        platform_statuses = factory.get_all_platform_status()
        
        response = []
        for status in platform_statuses:
            response.append(PlatformStatusResponse(**status))
        
        return response
        
    except Exception as e:
        logger.error(f"Failed to get platform list: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/platforms/tier/{tier}")
async def get_platforms_by_tier(tier: str):
    """
    Get platforms filtered by tier (tier_1, tier_2, tier_3)
    """
    try:
        factory = get_platform_factory()
        clients = factory.get_clients_for_tier(tier)
        
        return {
            "tier": tier,
            "platforms": [client.platform_name for client in clients],
            "count": len(clients)
        }
        
    except Exception as e:
        logger.error(f"Failed to get tier {tier} platforms: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/platforms/capabilities/{capability}")
async def get_platforms_by_capability(capability: str):
    """
    Get platforms that support a specific capability
    """
    try:
        factory = get_platform_factory()
        clients = factory.get_clients_with_capability(capability)
        
        return {
            "capability": capability,
            "platforms": [client.platform_name for client in clients],
            "count": len(clients)
        }
        
    except Exception as e:
        logger.error(f"Failed to get platforms with capability {capability}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/platforms/health-check")
async def test_all_platform_connections():
    """
    Test connectivity to all registered platforms
    """
    try:
        factory = get_platform_factory()
        results = await factory.test_all_platforms()
        
        healthy_count = sum(1 for status in results.values() if status)
        total_count = len(results)
        
        return {
            "total_platforms": total_count,
            "healthy_platforms": healthy_count,
            "overall_health": healthy_count / total_count if total_count > 0 else 0,
            "platform_status": results
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync", response_model=SyncResultResponse)
async def sync_business_multi_platform(
    request: MultiPlatformSyncRequest,
    background_tasks: BackgroundTasks,
    credentials: List[PlatformCredentials] = None,
    current_user=Depends(get_current_user)
):
    """
    Sync a business across multiple platforms with intelligent orchestration
    """
    try:
        # Convert credentials to expected format
        auth_data = {}
        if credentials:
            for cred in credentials:
                auth_data[cred.platform] = AuthCredentials(
                    platform=cred.platform,
                    credentials=cred.credentials,
                    expires_at=cred.expires_at
                )
        
        # Convert Pydantic model to orchestrator model
        sync_request = SyncRequest(
            business_id=request.business_id,
            strategy=SyncStrategy(request.strategy),
            operations=[SyncOperation(op) for op in request.operations],
            platforms=request.platforms,
            priority=SyncPriority(request.priority),
            max_concurrent=request.max_concurrent,
            retry_failed=request.retry_failed,
            notify_on_completion=request.notify_on_completion
        )
        
        # Execute sync
        result = await advanced_orchestrator.sync_business_intelligent(
            sync_request, auth_data
        )
        
        # Convert platform results to serializable format
        platform_results_dict = {}
        for platform, response in result.platform_results.items():
            platform_results_dict[platform] = {
                "success": response.success,
                "operation": response.operation,
                "error": response.error,
                "status_code": response.status_code,
                "platform_id": response.platform_id,
                "from_cache": response.from_cache
            }
        
        response = SyncResultResponse(
            business_id=result.business_id,
            request_id=result.request_id,
            overall_success=result.overall_success,
            total_platforms=result.total_platforms,
            successful_platforms=result.successful_platforms,
            failed_platforms=result.failed_platforms,
            execution_time=result.execution_time,
            recommendations=result.recommendations,
            platform_results=platform_results_dict
        )
        
        # Log the operation
        logger.info(
            f"Multi-platform sync completed for business {request.business_id}: "
            f"{result.successful_platforms}/{result.total_platforms} successful"
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Multi-platform sync failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/business/{business_id}/recommendations")
async def get_platform_recommendations(business_id: str):
    """
    Get AI-powered platform recommendations for a specific business
    """
    try:
        # This would integrate with the business data to provide recommendations
        factory = get_platform_factory()
        
        # For now, return general recommendations
        # In a full implementation, this would analyze the business data
        recommendations = []
        
        # Get business data and generate recommendations
        # business_data = await get_business_data(business_id)
        # recommendations = factory.get_recommended_platforms_for_business(business_data)
        
        # Placeholder recommendations
        tier_1_platforms = ["google_business", "google_maps", "yelp", "facebook", "apple_maps"]
        
        for platform in tier_1_platforms:
            recommendations.append({
                "platform": platform,
                "priority": "high",
                "rationale": f"Tier 1 platform with high market reach",
                "expected_roi": 0.8,
                "estimated_setup_time": 15
            })
        
        return {
            "business_id": business_id,
            "recommendations": recommendations,
            "total_recommended": len(recommendations)
        }
        
    except Exception as e:
        logger.error(f"Failed to get recommendations for business {business_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics", response_model=AnalyticsResponse)
async def get_sync_analytics(
    business_id: Optional[str] = Query(None),
    timeframe_days: int = Query(30, ge=1, le=365)
):
    """
    Get comprehensive sync analytics and performance metrics
    """
    try:
        analytics = await advanced_orchestrator.get_sync_analytics(
            business_id=business_id,
            timeframe_days=timeframe_days
        )
        
        return AnalyticsResponse(**analytics)
        
    except Exception as e:
        logger.error(f"Failed to get sync analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/registry/summary")
async def get_platform_registry_summary():
    """
    Get comprehensive platform registry summary
    """
    try:
        registry = get_platform_registry()
        summary = registry.get_platform_summary()
        
        # Add validation info
        validation_issues = registry.validate_platform_configuration()
        
        return {
            **summary,
            "validation_issues": validation_issues,
            "system_health": {
                "total_issues": sum(len(issues) for issues in validation_issues.values()),
                "critical_missing": len(validation_issues.get("missing_tier_1", [])),
                "configuration_errors": len(validation_issues.get("configuration_errors", []))
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get registry summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/credentials/validate")
async def validate_platform_credentials(credentials: List[PlatformCredentials]):
    """
    Validate authentication credentials for multiple platforms
    """
    try:
        factory = get_platform_factory()
        validation_results = {}
        
        for cred in credentials:
            auth_credentials = AuthCredentials(
                platform=cred.platform,
                credentials=cred.credentials,
                expires_at=cred.expires_at
            )
            
            is_valid = await factory.validate_credentials(cred.platform, auth_credentials)
            validation_results[cred.platform] = {
                "valid": is_valid,
                "expires_at": cred.expires_at.isoformat() if cred.expires_at else None
            }
        
        valid_count = sum(1 for result in validation_results.values() if result["valid"])
        total_count = len(validation_results)
        
        return {
            "total_platforms": total_count,
            "valid_credentials": valid_count,
            "validation_rate": valid_count / total_count if total_count > 0 else 0,
            "results": validation_results
        }
        
    except Exception as e:
        logger.error(f"Credential validation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/business/{business_id}/sync-status")
async def get_business_sync_status(business_id: str):
    """
    Get sync status across all platforms for a specific business
    """
    try:
        # This would query the database for sync status
        # For now, return a placeholder structure
        
        platforms = ["google_business", "google_maps", "yelp", "facebook", "apple_maps", 
                    "bing_maps", "bing_places", "tripadvisor"]
        
        status = {}
        for platform in platforms:
            status[platform] = {
                "platform_id": f"{platform}_{business_id}",
                "last_synced": datetime.utcnow().isoformat(),
                "sync_status": "success",
                "is_verified": True,
                "is_claimed": platform in ["google_business", "yelp"]
            }
        
        return {
            "business_id": business_id,
            "total_platforms": len(status),
            "synced_platforms": len([p for p, s in status.items() if s["sync_status"] == "success"]),
            "verified_platforms": len([p for p, s in status.items() if s["is_verified"]]),
            "claimed_platforms": len([p for p, s in status.items() if s["is_claimed"]]),
            "platform_status": status
        }
        
    except Exception as e:
        logger.error(f"Failed to get sync status for business {business_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch-sync")
async def batch_sync_multiple_businesses(
    business_ids: List[str],
    strategy: SyncStrategyEnum = SyncStrategyEnum.CONSERVATIVE,
    platforms: Optional[List[str]] = None,
    max_concurrent_businesses: int = Query(5, ge=1, le=20)
):
    """
    Sync multiple businesses in batch with intelligent orchestration
    """
    try:
        if len(business_ids) > 100:
            raise HTTPException(
                status_code=400,
                detail="Maximum 100 businesses allowed per batch request"
            )
        
        # Process in batches
        batch_results = []
        semaphore = asyncio.Semaphore(max_concurrent_businesses)
        
        async def sync_single_business(business_id: str):
            async with semaphore:
                request = SyncRequest(
                    business_id=business_id,
                    strategy=SyncStrategy(strategy),
                    operations=[SyncOperation.UPDATE],
                    platforms=platforms,
                    priority=SyncPriority.MEDIUM
                )
                
                result = await advanced_orchestrator.sync_business_intelligent(request)
                return {
                    "business_id": business_id,
                    "success": result.overall_success,
                    "platforms_synced": result.successful_platforms,
                    "total_platforms": result.total_platforms,
                    "execution_time": result.execution_time
                }
        
        # Execute all business syncs
        tasks = [sync_single_business(business_id) for business_id in business_ids]
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        successful_businesses = []
        failed_businesses = []
        
        for result in batch_results:
            if isinstance(result, Exception):
                failed_businesses.append(str(result))
            elif result["success"]:
                successful_businesses.append(result)
            else:
                failed_businesses.append(result)
        
        total_execution_time = sum(
            r["execution_time"] for r in successful_businesses + failed_businesses
            if isinstance(r, dict) and "execution_time" in r
        )
        
        return {
            "total_businesses": len(business_ids),
            "successful_businesses": len(successful_businesses),
            "failed_businesses": len(failed_businesses),
            "success_rate": len(successful_businesses) / len(business_ids),
            "total_execution_time": total_execution_time,
            "results": batch_results
        }
        
    except Exception as e:
        logger.error(f"Batch sync failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Add the router to your main application
# app.include_router(router)