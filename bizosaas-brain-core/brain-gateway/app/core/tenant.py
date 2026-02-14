from fastapi import Header, HTTPException
from typing import Optional
import os

def get_tenant_id(x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID")) -> str:
    """
    Dependency to extract Tenant ID from headers.
    In a real scenario, this might also validate against the database or auth token.
    For now, we default to 'default_tenant' to prevent crashes if the header is missing,
    but in production, this should likely be strict.
    """
    if x_tenant_id:
        return x_tenant_id
    
    # Fallback to env var or default
    default = os.getenv("DEFAULT_TENANT_ID", "default_tenant")
    return default
