"""
Tenant Management API
Handles administrative oversight of business tenants, including onboarding tracking,
configuration, and bulk operations.
"""

from fastapi import APIRouter, Depends, HTTPException, Body
import pydantic
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from app.dependencies import get_db, require_role
from app.models.user import Tenant, User
from domain.ports.identity_port import AuthenticatedUser

router = APIRouter(prefix="/api/admin/tenants", tags=["tenant-management"])

class BulkActionRequest(pydantic.BaseModel):
    tenant_ids: List[UUID]
    action: str # "suspend", "activate", "delete"
    reason: Optional[str] = None


@router.get("/")
async def list_tenants(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """List all tenants with key metrics."""
    query = db.query(Tenant)
    if status:
        query = query.filter(Tenant.status == status)
    
    total = query.count()
    tenants = query.offset(skip).limit(limit).all()
    
    results = []
    for t in tenants:
        user_count = db.query(User).filter(User.tenant_id == t.id).count()
        results.append({
            "id": str(t.id),
            "name": t.name,
            "slug": t.slug,
            "status": t.status,
            "user_count": user_count,
            "subscription": t.subscription_plan or "Free",
            "created_at": t.created_at,
            "onboarding_completed": t.settings.get("onboarding_done", False) if t.settings else False
        })
        
    return {"total": total, "tenants": results}


@router.get("/{tenant_id}")
async def get_tenant_details(
    tenant_id: UUID,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Get detailed information about a specific tenant."""
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
        
    return {
        "id": str(tenant.id),
        "name": tenant.name,
        "slug": tenant.slug,
        "domain": tenant.domain,
        "status": tenant.status,
        "settings": tenant.settings or {},
        "features": tenant.features or {},
        "limits": {
            "max_users": tenant.max_users,
            "api_rate_limit": tenant.api_rate_limit
        },
        "created_at": tenant.created_at,
        "updated_at": tenant.updated_at
    }


@router.patch("/{tenant_id}/config")
async def update_tenant_config(
    tenant_id: UUID,
    updates: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Update tenant-specific settings and features."""
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
        
    if "settings" in updates:
        tenant.settings = {**(tenant.settings or {}), **updates["settings"]}
    if "features" in updates:
        tenant.features = {**(tenant.features or {}), **updates["features"]}
    if "status" in updates:
        tenant.status = updates["status"]
    if "limits" in updates:
        limits = updates["limits"]
        if "max_users" in limits: tenant.max_users = limits["max_users"]
        if "api_rate_limit" in limits: tenant.api_rate_limit = limits["api_rate_limit"]
        
    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(tenant, "settings")
    flag_modified(tenant, "features")
    
    db.commit()
    db.refresh(tenant)
    return {"status": "success", "message": "Tenant configuration updated"}


@router.get("/stats/onboarding")
async def get_onboarding_stats(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Track completion of onboarding steps per tenant."""
    total = db.query(Tenant).count()
    # Assuming onboarding_done is a flag in settings
    completed = db.query(Tenant).filter(Tenant.settings.op('->>')('onboarding_done') == 'true').count()
    
    return {
        "total_tenants": total,
        "completed_onboarding": completed,
        "completion_rate": (completed / total * 100) if total > 0 else 0
    }


@router.get("/{tenant_id}/analytics")
async def get_tenant_analytics(
    tenant_id: UUID,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Get usage analytics for a specific tenant."""
    from datetime import timedelta
    
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
        
    # User stats
    users = db.query(User).filter(User.tenant_id == tenant_id).all()
    total_users = len(users)
    active_30d = 0
    total_logins = 0
    
    now = datetime.utcnow()
    thirty_days_ago = now - timedelta(days=30)
    
    for u in users:
        total_logins += u.login_count
        if u.last_login_at and u.last_login_at >= thirty_days_ago:
            active_30d += 1
            
    # Feature Usage (Simplified: count enabled features)
    features_enabled = 0
    if tenant.features:
        features_enabled = sum(1 for v in tenant.features.values() if v)
        
    return {
        "tenant_id": str(tenant.id),
        "user_engagement": {
            "total_users": total_users,
            "active_users_30d": active_30d,
            "total_logins": total_logins,
            "engagement_rate": (active_30d / total_users * 100) if total_users > 0 else 0
        },
        "feature_adoption": {
            "enabled_features": features_enabled,
            "total_available": len(tenant.features) if tenant.features else 0,
            "breakdown": tenant.features or {}
        }
    }


@router.post("/bulk")
async def bulk_tenant_operations(
    payload: BulkActionRequest,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Perform bulk actions on tenants."""
    query = db.query(Tenant).filter(Tenant.id.in_(payload.tenant_ids))
    tenants = query.all()
    
    if not tenants:
        return {"processed": 0, "message": "No tenants found"}
        
    count = 0
    for t in tenants:
        if payload.action == "suspend":
            t.status = "suspended"
            count += 1
        elif payload.action == "activate":
            t.status = "active"
            count += 1
        elif payload.action == "maintenance":
            t.status = "maintenance"
            count += 1
        # 'delete' would be more complex due to cascades, skipping for safety in this iteration unless strictly required
        
    db.commit()
    return {"status": "success", "processed": count, "action": payload.action}
