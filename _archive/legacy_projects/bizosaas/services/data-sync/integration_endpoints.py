#!/usr/bin/env python3

"""
BizOSaaS Data Synchronization - Integration Endpoints
Integration endpoints for the Brain API Gateway
"""

import logging
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
import httpx

logger = logging.getLogger(__name__)

# Integration models
class SyncEventRequest(BaseModel):
    event_type: str
    source_platform: str
    target_platforms: List[str]
    data: Dict[str, Any]
    tenant_id: str
    user_id: Optional[str] = None
    priority: int = 5

class SyncStatusResponse(BaseModel):
    event_id: str
    status: str
    results: List[Dict[str, Any]]
    created_at: datetime
    processed_at: Optional[datetime] = None

def create_data_sync_router(data_sync_url: str = "http://bizosaas-data-sync:8025") -> APIRouter:
    """Create Data Synchronization proxy router for Brain API"""
    router = APIRouter(prefix="/api/brain/data-sync", tags=["Data Synchronization"])
    
    @router.post("/events", response_model=Dict[str, str])
    async def create_sync_event(event: SyncEventRequest, request: Request):
        """Create a new cross-platform sync event"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{data_sync_url}/sync/events",
                    json=event.dict(),
                    headers=dict(request.headers),
                    timeout=30.0
                )
                
                if response.status_code in [200, 201]:
                    return response.json()
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Data sync service error: {response.text}"
                    )
                    
        except httpx.RequestError as e:
            logger.error(f"Data sync service request error: {e}")
            raise HTTPException(status_code=503, detail="Data sync service unavailable")
        except Exception as e:
            logger.error(f"Data sync proxy error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/events/{event_id}")
    async def get_sync_event_status(event_id: str, request: Request):
        """Get sync event status and results"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{data_sync_url}/sync/events/{event_id}",
                    headers=dict(request.headers),
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    raise HTTPException(status_code=404, detail="Sync event not found")
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Data sync service error: {response.text}"
                    )
                    
        except httpx.RequestError as e:
            logger.error(f"Data sync service request error: {e}")
            raise HTTPException(status_code=503, detail="Data sync service unavailable")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Data sync proxy error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/events")
    async def list_sync_events(
        request: Request,
        limit: int = 50,
        offset: int = 0,
        status: Optional[str] = None,
        tenant_id: Optional[str] = None
    ):
        """List sync events with filtering"""
        try:
            params = {"limit": limit, "offset": offset}
            if status:
                params["status"] = status
            if tenant_id:
                params["tenant_id"] = tenant_id
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{data_sync_url}/sync/events",
                    params=params,
                    headers=dict(request.headers),
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Data sync service error: {response.text}"
                    )
                    
        except httpx.RequestError as e:
            logger.error(f"Data sync service request error: {e}")
            raise HTTPException(status_code=503, detail="Data sync service unavailable")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Data sync proxy error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/events/{event_id}/retry")
    async def retry_sync_event(event_id: str, request: Request):
        """Retry a failed sync event"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{data_sync_url}/sync/events/{event_id}/retry",
                    headers=dict(request.headers),
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 400:
                    raise HTTPException(status_code=400, detail="Event cannot be retried")
                elif response.status_code == 404:
                    raise HTTPException(status_code=404, detail="Sync event not found")
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Data sync service error: {response.text}"
                    )
                    
        except httpx.RequestError as e:
            logger.error(f"Data sync service request error: {e}")
            raise HTTPException(status_code=503, detail="Data sync service unavailable")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Data sync proxy error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/metrics")
    async def get_sync_metrics(
        request: Request,
        tenant_id: Optional[str] = None,
        hours: int = 24
    ):
        """Get synchronization metrics"""
        try:
            params = {"hours": hours}
            if tenant_id:
                params["tenant_id"] = tenant_id
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{data_sync_url}/sync/metrics",
                    params=params,
                    headers=dict(request.headers),
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Data sync service error: {response.text}"
                    )
                    
        except httpx.RequestError as e:
            logger.error(f"Data sync service request error: {e}")
            raise HTTPException(status_code=503, detail="Data sync service unavailable")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Data sync proxy error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/status")
    async def get_sync_status(request: Request):
        """Get overall synchronization status"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{data_sync_url}/sync/status",
                    headers=dict(request.headers),
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Data sync service error: {response.text}"
                    )
                    
        except httpx.RequestError as e:
            logger.error(f"Data sync service request error: {e}")
            raise HTTPException(status_code=503, detail="Data sync service unavailable")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Data sync proxy error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/users")
    async def sync_cross_platform_user(user_data: Dict[str, Any], request: Request):
        """Create or update cross-platform user"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{data_sync_url}/sync/users",
                    json=user_data,
                    headers=dict(request.headers),
                    timeout=30.0
                )
                
                if response.status_code in [200, 201]:
                    return response.json()
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Data sync service error: {response.text}"
                    )
                    
        except httpx.RequestError as e:
            logger.error(f"Data sync service request error: {e}")
            raise HTTPException(status_code=503, detail="Data sync service unavailable")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Data sync proxy error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/users/{user_id}")
    async def get_cross_platform_user(user_id: str, tenant_id: str, request: Request):
        """Get cross-platform user data"""
        try:
            params = {"tenant_id": tenant_id}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{data_sync_url}/sync/users/{user_id}",
                    params=params,
                    headers=dict(request.headers),
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    raise HTTPException(status_code=404, detail="User not found")
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Data sync service error: {response.text}"
                    )
                    
        except httpx.RequestError as e:
            logger.error(f"Data sync service request error: {e}")
            raise HTTPException(status_code=503, detail="Data sync service unavailable")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Data sync proxy error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/health")
    async def get_data_sync_health(request: Request):
        """Get data sync service health status"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{data_sync_url}/health",
                    headers=dict(request.headers),
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Data sync service unhealthy: {response.text}"
                    )
                    
        except httpx.RequestError as e:
            logger.error(f"Data sync service request error: {e}")
            raise HTTPException(status_code=503, detail="Data sync service unavailable")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Data sync proxy error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    return router

# Helper functions for platform-specific integrations
def create_user_sync_event(user_data: Dict[str, Any], source_platform: str, tenant_id: str) -> SyncEventRequest:
    """Create a user synchronization event"""
    return SyncEventRequest(
        event_type="user_created" if not user_data.get("id") else "user_updated",
        source_platform=source_platform,
        target_platforms=["bizoholic", "coreldove", "bizosaas"],
        data=user_data,
        tenant_id=tenant_id,
        user_id=user_data.get("id"),
        priority=3  # High priority for user events
    )

def create_lead_sync_event(lead_data: Dict[str, Any], source_platform: str, tenant_id: str) -> SyncEventRequest:
    """Create a lead synchronization event"""
    return SyncEventRequest(
        event_type="lead_created" if not lead_data.get("id") else "lead_updated",
        source_platform=source_platform,
        target_platforms=["bizoholic", "bizosaas"],  # Leads typically sync to marketing platforms
        data=lead_data,
        tenant_id=tenant_id,
        user_id=lead_data.get("user_id"),
        priority=4  # Normal priority for leads
    )

def create_order_sync_event(order_data: Dict[str, Any], source_platform: str, tenant_id: str) -> SyncEventRequest:
    """Create an order synchronization event"""
    return SyncEventRequest(
        event_type="order_created" if not order_data.get("id") else "order_updated",
        source_platform=source_platform,
        target_platforms=["coreldove", "bizosaas"],  # Orders typically from e-commerce
        data=order_data,
        tenant_id=tenant_id,
        user_id=order_data.get("customer_id"),
        priority=2  # High priority for orders
    )

def create_campaign_sync_event(campaign_data: Dict[str, Any], source_platform: str, tenant_id: str) -> SyncEventRequest:
    """Create a campaign synchronization event"""
    return SyncEventRequest(
        event_type="campaign_created" if not campaign_data.get("id") else "campaign_updated",
        source_platform=source_platform,
        target_platforms=["bizoholic", "bizosaas"],  # Campaigns from marketing platforms
        data=campaign_data,
        tenant_id=tenant_id,
        priority=5  # Normal priority for campaigns
    )

def create_product_sync_event(product_data: Dict[str, Any], source_platform: str, tenant_id: str) -> SyncEventRequest:
    """Create a product synchronization event"""
    return SyncEventRequest(
        event_type="product_created" if not product_data.get("id") else "product_updated",
        source_platform=source_platform,
        target_platforms=["coreldove", "bizoholic", "bizosaas"],  # Products sync everywhere
        data=product_data,
        tenant_id=tenant_id,
        priority=4  # Normal priority for products
    )

def create_analytics_sync_event(analytics_data: Dict[str, Any], source_platform: str, tenant_id: str) -> SyncEventRequest:
    """Create an analytics synchronization event"""
    return SyncEventRequest(
        event_type="analytics_updated",
        source_platform=source_platform,
        target_platforms=["bizosaas"],  # Analytics typically go to central platform
        data=analytics_data,
        tenant_id=tenant_id,
        priority=6  # Lower priority for analytics
    )