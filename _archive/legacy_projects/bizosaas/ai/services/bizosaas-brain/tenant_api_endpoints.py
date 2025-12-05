"""
Tenant Context API Endpoints
Provides tenant management and context switching for Client Portal
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/brain/tenant", tags=["Tenant Management"])


# Pydantic Models
class TenantInfo(BaseModel):
    id: str
    name: str
    slug: str
    domain: Optional[str] = None
    logo_url: Optional[str] = None
    status: str = "active"
    subscription_plan: str = "basic"
    created_at: datetime
    settings: Dict[str, Any] = {}


class TenantStats(BaseModel):
    total_users: int
    total_leads: int
    total_products: int
    total_orders: int
    total_revenue: float
    active_campaigns: int


class TenantSwitchRequest(BaseModel):
    tenant_id: str


# Mock tenant data (replace with database queries)
MOCK_TENANTS = {
    "coreldove": TenantInfo(
        id="coreldove",
        name="CorelDove",
        slug="coreldove",
        domain="coreldove.com",
        logo_url="/logos/coreldove.png",
        status="active",
        subscription_plan="enterprise",
        created_at=datetime(2024, 1, 15),
        settings={
            "theme": "ecommerce",
            "currency": "INR",
            "timezone": "Asia/Kolkata",
            "features": ["ecommerce", "ai_content", "amazon_integration"]
        }
    ),
    "bizoholic": TenantInfo(
        id="bizoholic",
        name="Bizoholic",
        slug="bizoholic",
        domain="bizoholic.com",
        logo_url="/logos/bizoholic.png",
        status="active",
        subscription_plan="professional",
        created_at=datetime(2024, 1, 10),
        settings={
            "theme": "marketing",
            "currency": "USD",
            "timezone": "America/New_York",
            "features": ["crm", "marketing_automation", "ai_agents"]
        }
    ),
    "thrillring": TenantInfo(
        id="thrillring",
        name="ThrillRing Gaming",
        slug="thrillring",
        domain="thrillring.com",
        logo_url="/logos/thrillring.png",
        status="active",
        subscription_plan="professional",
        created_at=datetime(2024, 2, 1),
        settings={
            "theme": "gaming",
            "currency": "USD",
            "timezone": "America/Los_Angeles",
            "features": ["gaming", "tournaments", "player_matching"]
        }
    )
}

MOCK_STATS = {
    "coreldove": TenantStats(
        total_users=150,
        total_leads=0,
        total_products=247,
        total_orders=1834,
        total_revenue=145820.50,
        active_campaigns=3
    ),
    "bizoholic": TenantStats(
        total_users=45,
        total_leads=328,
        total_products=0,
        total_orders=0,
        total_revenue=0.0,
        active_campaigns=12
    ),
    "thrillring": TenantStats(
        total_users=2341,
        total_leads=0,
        total_products=0,
        total_orders=0,
        total_revenue=0.0,
        active_campaigns=5
    )
}


def get_current_tenant_id(x_tenant: Optional[str] = Header(None)) -> str:
    """Extract tenant ID from header or return default"""
    if x_tenant:
        return x_tenant
    return "coreldove"  # Default tenant


@router.get("/current", response_model=TenantInfo)
async def get_current_tenant(tenant_id: str = Depends(get_current_tenant_id)):
    """
    Get current tenant information

    Returns tenant details based on X-Tenant header or default
    """
    try:
        if tenant_id in MOCK_TENANTS:
            return MOCK_TENANTS[tenant_id]

        # If tenant not found, return default
        logger.warning(f"Tenant {tenant_id} not found, using coreldove")
        return MOCK_TENANTS["coreldove"]

    except Exception as e:
        logger.error(f"Error getting current tenant: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving tenant information")


@router.get("/{tenant_id}", response_model=TenantInfo)
async def get_tenant(tenant_id: str):
    """Get specific tenant by ID"""
    try:
        if tenant_id not in MOCK_TENANTS:
            raise HTTPException(status_code=404, detail=f"Tenant {tenant_id} not found")

        return MOCK_TENANTS[tenant_id]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting tenant {tenant_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving tenant")


@router.get("/{tenant_id}/stats", response_model=TenantStats)
async def get_tenant_stats(tenant_id: str):
    """Get tenant statistics"""
    try:
        if tenant_id not in MOCK_STATS:
            raise HTTPException(status_code=404, detail=f"Stats for tenant {tenant_id} not found")

        return MOCK_STATS[tenant_id]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting stats for tenant {tenant_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving tenant stats")


@router.post("/switch")
async def switch_tenant(request: TenantSwitchRequest):
    """
    Switch tenant context

    Returns new tenant information and JWT token for context
    """
    try:
        tenant_id = request.tenant_id

        if tenant_id not in MOCK_TENANTS:
            raise HTTPException(status_code=404, detail=f"Tenant {tenant_id} not found")

        tenant = MOCK_TENANTS[tenant_id]

        # In production, generate new JWT token with tenant context
        # For now, return tenant info
        return {
            "success": True,
            "tenant": tenant,
            "message": f"Switched to tenant: {tenant.name}",
            "token": f"mock_jwt_token_for_{tenant_id}"  # Replace with real JWT
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error switching tenant: {e}")
        raise HTTPException(status_code=500, detail="Error switching tenant")


@router.get("/list/all")
async def list_all_tenants():
    """
    List all available tenants

    Used for tenant switcher dropdown
    """
    try:
        return {
            "success": True,
            "tenants": list(MOCK_TENANTS.values()),
            "total": len(MOCK_TENANTS)
        }
    except Exception as e:
        logger.error(f"Error listing tenants: {e}")
        raise HTTPException(status_code=500, detail="Error listing tenants")


@router.get("/health")
async def tenant_api_health():
    """Health check for tenant API"""
    return {
        "status": "healthy",
        "service": "tenant-api",
        "tenants_available": len(MOCK_TENANTS)
    }
