from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.tenant import TenantConfig
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/public", tags=["public"])

class PublicTenantConfigResponse(BaseModel):
    portal_title: str
    logo_url: Optional[str]
    favicon_url: Optional[str]
    primary_color: str
    secondary_color: str
    font_family: str

    class Config:
        orm_mode = True

@router.get("/config", response_model=PublicTenantConfigResponse)
def get_public_config(
    tenant_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get public branding configuration.
    If tenant_id is provided, fetch specific config.
    Otherwise, fetch the first available (default).
    """
    query = db.query(TenantConfig)
    
    if tenant_id:
        query = query.filter(TenantConfig.tenant_id == tenant_id)
    
    config = query.first()
    
    if not config:
         # Fallback default
        return PublicTenantConfigResponse(
            portal_title="BizOSaaS Client Portal",
            logo_url=None,
            favicon_url=None,
            primary_color="#2563eb",
            secondary_color="#475569",
            font_family="Inter"
        )
        
    return config
