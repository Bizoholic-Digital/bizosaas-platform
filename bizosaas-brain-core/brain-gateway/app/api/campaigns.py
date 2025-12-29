from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from app.middleware.auth import get_current_user
from domain.ports.identity_port import AuthenticatedUser
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.services.campaign_service import CampaignService
from app.models.campaign import CampaignStatus

router = APIRouter()

class ChannelCreateRequest(BaseModel):
    channel_type: str # email, social
    connector_id: str # mailchimp
    config: Dict[str, Any]

class CampaignCreateRequest(BaseModel):
    name: str
    goal: Optional[str] = None
    channels: List[ChannelCreateRequest] = []

class CampaignResponse(BaseModel):
    id: UUID
    name: str
    status: str
    goal: Optional[str]
    created_at: datetime
    channels: List[Dict[str, Any]] = []

    class Config:
        orm_mode = True

@router.post("/", response_model=CampaignResponse)
async def create_campaign(
    request: CampaignCreateRequest,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = CampaignService(db)
    tenant_id = UUID(user.tenant_id) if user.tenant_id != "default_tenant" else UUID("00000000-0000-0000-0000-000000000000") # Mock UUID for default
    
    # Create Campaign
    campaign = service.create_campaign(
        tenant_id=tenant_id,
        name=request.name,
        goal=request.goal,
        user_id=None # parsing user.id to UUID might fail if it's "system-user" string
    )
    
    # Add Channels
    for channel in request.channels:
        service.add_channel(
            campaign_id=campaign.id,
            channel_type=channel.channel_type,
            connector_id=channel.connector_id,
            config=channel.config
        )
        
    return campaign

@router.get("/", response_model=List[CampaignResponse])
def list_campaigns(
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = CampaignService(db)
    tenant_id = UUID(user.tenant_id) if user.tenant_id != "default_tenant" else UUID("00000000-0000-0000-0000-000000000000")
    return service.list_campaigns(tenant_id)

@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(
    campaign_id: UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = CampaignService(db)
    tenant_id = UUID(user.tenant_id) if user.tenant_id != "default_tenant" else UUID("00000000-0000-0000-0000-000000000000")
    
    campaign = service.get_campaign(campaign_id, tenant_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.post("/{campaign_id}/publish")
async def publish_campaign(
    campaign_id: UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = CampaignService(db)
    tenant_id = UUID(user.tenant_id) if user.tenant_id != "default_tenant" else UUID("00000000-0000-0000-0000-000000000000")
    
    try:
        results = await service.publish_campaign(campaign_id, tenant_id)
        return {"status": "published", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
