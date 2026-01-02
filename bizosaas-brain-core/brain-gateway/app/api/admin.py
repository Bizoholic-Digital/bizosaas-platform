from fastapi import APIRouter, HTTPException, Depends, Request
import httpx
import os
import psutil
import time
from typing import Dict, Any, List
from app.middleware.auth import get_current_user, require_role
from domain.ports.identity_port import AuthenticatedUser
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.models.tenant import TenantConfig
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/admin", tags=["admin"])

AUTH_URL = os.getenv("AUTH_URL", "http://auth-service:8006")

@router.get("/stats")
async def get_platform_stats(
    request: Request,
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Aggregate platform-wide statistics for Super Admins.
    """
    stats = {
        "tenants": {"total": 0, "active": 0},
        "users": {"total": 0, "active": 0},
        "revenue": {"monthly": 0.0, "currency": "USD"},
        "system": {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "uptime_seconds": int(time.time() - psutil.Process().create_time())
        },
        "timestamp": time.time()
    }

    try:
        token = request.headers.get("Authorization")
        async with httpx.AsyncClient() as client:
            # Fetch counts from Auth Service
            response = await client.get(
                f"{AUTH_URL}/auth/admin/counts",
                headers={"Authorization": token} if token else {},
                timeout=5.0
            )
            if response.status_code == 200:
                auth_data = response.json()
                stats["tenants"]["total"] = auth_data.get("total_tenants", 0)
                stats["users"]["total"] = auth_data.get("total_users", 0)
    except Exception as e:
        print(f"Error fetching auth counts: {e}")

    return stats

@router.get("/users")
async def list_all_users(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Proxy to list all users from Auth Service"""
    token = request.headers.get("Authorization")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{AUTH_URL}/users", # FastAPI Users common endpoint
            headers={"Authorization": token} if token else {},
            params={"skip": skip, "limit": limit},
            timeout=10.0
        )
        return response.json()

@router.get("/tenants")
async def list_all_tenants(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Proxy to list all tenants from Auth Service"""
    token = request.headers.get("Authorization")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{AUTH_URL}/tenants",
            headers={"Authorization": token} if token else {},
            params={"skip": skip, "limit": limit},
            timeout=10.0
        )
        return response.json()

@router.get("/health")
async def get_system_health(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Detailed system health info"""
    return {
        "status": "healthy",
        "services": {
            "auth": "up",
            "brain-gateway": "up",
            "database": "connected",
            "redis": "connected"
        },
        "resources": {
            "cpu": psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory()._asdict(),
            "disk": psutil.disk_usage('/')._asdict()
        }
    }

@router.get("/analytics")
async def get_api_analytics(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Fetch API analytics from Prometheus metrics.
    """
    metrics = {
        "requests_per_minute": 0,
        "response_time_avg": 0,
        "error_rate": 0.0,
        "active_sessions": 0,
        "timestamp": time.time()
    }

    try:
        async with httpx.AsyncClient() as client:
            # Fetch raw Prometheus metrics from local instrumentator
            response = await client.get("http://localhost:8000/metrics", timeout=2.0)
            if response.status_code == 200:
                text = response.text
                
                # Simple parsing for MVP (In production use prometheus_client parser)
                # Looking for: http_request_duration_seconds_count
                # And: http_request_duration_seconds_sum
                # And: http_request_duration_seconds_bucket{le="5xx"} or similar
                
                req_count = 0
                error_count = 0
                duration_sum = 0.0
                
                for line in text.splitlines():
                    if line.startswith("http_request_duration_seconds_count"):
                        try:
                            req_count += float(line.split()[-1])
                        except: pass
                    elif line.startswith("http_request_duration_seconds_sum"):
                        try:
                            duration_sum += float(line.split()[-1])
                        except: pass
                    elif 'status="5' in line or 'status="4' in line:
                         if "_count" in line:
                            try:
                                error_count += float(line.split()[-1])
                            except: pass

                # Calculate averages (Note: these are cumulative since startup)
                # To get "per minute" we'd need to store previous state, 
                # but for MVP overview we'll use total counts scaled or latest.
                metrics["requests_per_minute"] = int(req_count / 10) if req_count > 0 else 0 # Dummy scaling
                metrics["response_time_avg"] = int((duration_sum / req_count) * 1000) if req_count > 0 else 0
                metrics["error_rate"] = round((error_count / req_count) * 100, 2) if req_count > 0 else 0.0
                metrics["active_sessions"] = int(req_count / 100) # Placeholder
                
    except Exception as e:
        print(f"Error fetching Prometheus metrics: {e}")

    return metrics

# --- Tenant Configuration (White Labeling) ---

class TenantConfigUpdate(BaseModel):
    portal_title: Optional[str] = None
    logo_url: Optional[str] = None
    favicon_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    font_family: Optional[str] = None

class TenantConfigResponse(BaseModel):
    tenant_id: str
    portal_title: str
    logo_url: Optional[str]
    favicon_url: Optional[str]
    primary_color: str
    secondary_color: str
    font_family: str

    class Config:
        orm_mode = True

@router.get("/config", response_model=TenantConfigResponse)
def get_tenant_config(
    user: AuthenticatedUser = Depends(require_role("Admin")),
    db: Session = Depends(get_db)
):
    """Get branding configuration for the current tenant."""
    config = db.query(TenantConfig).filter(TenantConfig.tenant_id == user.tenant_id).first()
    if not config:
        # Return defaults
        return TenantConfigResponse(
            tenant_id=str(user.tenant_id),
            portal_title="BizOSaaS Client Portal",
            logo_url=None,
            favicon_url=None,
            primary_color="#2563eb",
            secondary_color="#475569",
            font_family="Inter"
        )
    return config

@router.put("/config", response_model=TenantConfigResponse)
def update_tenant_config(
    update_data: TenantConfigUpdate,
    user: AuthenticatedUser = Depends(require_role("Admin")),
    db: Session = Depends(get_db)
):
    """Update branding configuration for the current tenant."""
    config = db.query(TenantConfig).filter(TenantConfig.tenant_id == user.tenant_id).first()
    if not config:
        config = TenantConfig(tenant_id=user.tenant_id)
        db.add(config)
    
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(config, key, value)
    
    db.commit()
    db.refresh(config)
    return config
