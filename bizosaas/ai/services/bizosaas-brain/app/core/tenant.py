"""
Tenant context management for multi-tenant analytics
"""

from typing import Optional
from fastapi import Header, HTTPException
from pydantic import BaseModel

class TenantContext(BaseModel):
    """Tenant context information"""
    tenant_id: str
    tenant_name: Optional[str] = None
    subscription_tier: str = "basic"

async def get_tenant_context(
    x_tenant_id: Optional[str] = Header(None),
    tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID")
) -> TenantContext:
    """
    Extract tenant context from request headers
    Supports both 'x-tenant-id' and 'X-Tenant-ID' headers
    """
    
    # Try different header formats
    tenant_id_value = x_tenant_id or tenant_id
    
    if not tenant_id_value:
        # For development, use default tenant
        tenant_id_value = "demo"
    
    return TenantContext(
        tenant_id=tenant_id_value,
        tenant_name=f"Tenant {tenant_id_value}",
        subscription_tier="premium"  # Default for analytics access
    )