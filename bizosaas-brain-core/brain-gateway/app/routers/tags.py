from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
import uuid

from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User
from app.models.tag_config import TagConfig
from app.models.user import Tenant

router = APIRouter(prefix="/tags", tags=["tags"])

# Pydantic models
class TagConfigBase(BaseModel):
    container_id: str
    label: Optional[str] = None
    environment: str = "production"
    is_active: bool = True
    config: Optional[Dict[str, Any]] = None

class TagConfigCreate(TagConfigBase):
    pass

class TagConfigUpdate(BaseModel):
    container_id: Optional[str] = None
    label: Optional[str] = None
    environment: Optional[str] = None
    is_active: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None

class TagConfigResponse(TagConfigBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# --- Tenant Endpoints ---

@router.get("/gtm", response_model=List[TagConfigResponse])
def get_tenant_tags(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    environment: Optional[str] = None
):
    """List GTM configs for the current user's tenant"""
    query = db.query(TagConfig).filter(TagConfig.tenant_id == current_user.tenant_id)
    
    if environment:
        query = query.filter(TagConfig.environment == environment)
        
    return query.all()

@router.post("/gtm", response_model=TagConfigResponse)
def create_tag_config(
    tag_config: TagConfigCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new GTM config"""
    # Validate container ID format loosely
    if not tag_config.container_id.startswith("GTM-"):
        raise HTTPException(status_code=400, detail="Invalid GTM Container ID. Must start with 'GTM-'")
        
    db_tag = TagConfig(
        **tag_config.dict(),
        tenant_id=current_user.tenant_id
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@router.put("/gtm/{tag_id}", response_model=TagConfigResponse)
def update_tag_config(
    tag_id: str,
    tag_update: TagConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update GTM config"""
    db_tag = db.query(TagConfig).filter(
        TagConfig.id == tag_id,
        TagConfig.tenant_id == current_user.tenant_id
    ).first()
    
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag config not found")
        
    update_data = tag_update.dict(exclude_unset=True)
    
    if "container_id" in update_data and not update_data["container_id"].startswith("GTM-"):
         raise HTTPException(status_code=400, detail="Invalid GTM Container ID. Must start with 'GTM-'")

    for key, value in update_data.items():
        setattr(db_tag, key, value)
        
    db.commit()
    db.refresh(db_tag)
    return db_tag

@router.delete("/gtm/{tag_id}")
def delete_tag_config(
    tag_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete GTM config"""
    db_tag = db.query(TagConfig).filter(
        TagConfig.id == tag_id,
        TagConfig.tenant_id == current_user.tenant_id
    ).first()
    
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag config not found")
        
    db.delete(db_tag)
    db.commit()
    return {"status": "success"}

# --- Public Endpoint for Frontend Injection ---

@router.get("/gtm/snippet/{tenant_slug}")
def get_gtm_snippet(
    tenant_slug: str,
    environment: str = "production",
    db: Session = Depends(get_db)
):
    """
    Public endpoint to get GTM snippet details for a tenant.
    Used by frontend apps to inject the correct container.
    """
    # Find tenant by slug
    tenant = db.query(Tenant).filter(Tenant.slug == tenant_slug).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
        
    # Get active config for environment
    config = db.query(TagConfig).filter(
        TagConfig.tenant_id == tenant.id,
        TagConfig.environment == environment,
        TagConfig.is_active == True
    ).first()
    
    if not config:
        return {"container_id": None, "active": False}
        
    return {
        "container_id": config.container_id,
        "active": True,
        "environment": config.environment,
        "config": config.config
    }

# --- Admin Endpoint ---

@router.get("/gtm/admin/all", response_model=List[TagConfigResponse])
def get_all_tags(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Super Admin", "Admin"])),
    skip: int = 0,
    limit: int = 100
):
    """Admin: List all GTM configs"""
    return db.query(TagConfig).offset(skip).limit(limit).all()
