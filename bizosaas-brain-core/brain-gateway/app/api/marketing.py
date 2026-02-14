from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from app.middleware.auth import get_current_user
from app.domain.ports.identity_port import AuthenticatedUser
from app.store import active_connectors
from app.connectors.registry import ConnectorRegistry
from app.connectors.base import ConnectorType, ConnectorStatus
from app.ports.marketing_port import MarketingPort
from app.dependencies import get_secret_service
from app.domain.services.secret_service import SecretService
from temporalio.client import Client
import os

router = APIRouter()

class EmailListMessage(BaseModel):
    id: str
    name: str
    subscriber_count: int

class CampaignMessage(BaseModel):
    id: str
    name: str
    status: str
    subject: Optional[str] = ""
    emails_sent: Optional[int] = 0

async def get_active_marketing_connector(tenant_id: str, secret_service: SecretService) -> MarketingPort:
    # 1. Get all Marketing connector types
    configs = [c for c in ConnectorRegistry.get_all_configs() if c.type == ConnectorType.MARKETING]
    
    # 2. Check in-memory store first
    for config in configs:
        key = f"{tenant_id}:{config.id}"
        if key in active_connectors:
            data = active_connectors[key]
            connector = ConnectorRegistry.create_connector(config.id, tenant_id, data["credentials"])
            return connector
            
    # 3. Check secret service (persistent)
    for config in configs:
        credentials = await secret_service.get_connector_credentials(tenant_id, config.id)
        if credentials:
            connector = ConnectorRegistry.create_connector(config.id, tenant_id, credentials)
            active_connectors[f"{tenant_id}:{config.id}"] = {"credentials": credentials}
            return connector
            
    raise HTTPException(status_code=404, detail="No Marketing connector configured.")

@router.get("/status")
async def get_marketing_status(
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    """Check connectivity to the active marketing platform"""
    tenant_id = user.tenant_id or "default_tenant"
    try:
        connector = await get_active_marketing_connector(tenant_id, secret_service)
        is_valid = await connector.validate_credentials()
        
        return {
            "connected": is_valid,
            "platform": connector.config.name if hasattr(connector, 'config') else "Mailchimp",
            "version": "Unknown" 
        }
    except HTTPException:
        return {"connected": False}
    except Exception as e:
        return {"connected": False, "error": str(e)}

@router.get("/stats")
async def get_marketing_stats(
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    """Get Marketing statistics"""
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_marketing_connector(tenant_id, secret_service)
    
    try:
        return await connector.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats Error: {str(e)}")

@router.get("/lists", response_model=List[EmailListMessage])
async def list_email_lists(
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_marketing_connector(tenant_id, secret_service)
    
    try:
        lists = await connector.get_lists()
        return [
            EmailListMessage(
                id=l.id,
                name=l.name,
                subscriber_count=l.member_count
            ) for l in lists
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Marketing Error: {str(e)}")

@router.get("/campaigns", response_model=List[CampaignMessage])
async def list_campaigns(
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_marketing_connector(tenant_id, secret_service)
    
    try:
        campaigns = await connector.get_campaigns()
        return [
            CampaignMessage(
                id=c.id,
                name=c.name,
                status=c.status,
                subject=c.subject,
                emails_sent=c.emails_sent
            ) for c in campaigns
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Marketing Error: {str(e)}")

@router.post("/lists", response_model=EmailListMessage)
async def create_list(
    name: str = Body(..., embed=True),
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_marketing_connector(tenant_id, secret_service)
    try:
        result = await connector.create_list({"name": name})
        return EmailListMessage(id=result.id, name=result.name, subscriber_count=result.member_count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/lists/{list_id}")
async def delete_list(
    list_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_marketing_connector(tenant_id, secret_service)
    try:
        await connector.delete_list(list_id)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/campaigns", response_model=CampaignMessage)
async def create_campaign(
    campaign: Dict[str, Any] = Body(...),
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_marketing_connector(tenant_id, secret_service)
    try:
        result = await connector.create_campaign(campaign)
        return CampaignMessage(
            id=result.id,
            name=result.name,
            status=result.status,
            subject=result.subject,
            emails_sent=result.emails_sent
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/campaigns/{campaign_id}")
async def delete_campaign(
    campaign_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_marketing_connector(tenant_id, secret_service)
    try:
        await connector.delete_campaign(campaign_id)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/orchestrate-social")
async def orchestrate_social_campaign(
    topic: str = Body(..., embed=True),
    platforms: List[str] = Body(["instagram", "linkedin"], embed=True),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Trigger an AI-orchestrated multi-channel social campaign via Temporal."""
    tenant_id = user.tenant_id or "default_tenant"
    temporal_url = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
    
    try:
        client = await Client.connect(temporal_url)
        
        workflow_id = f"social-campaign-{tenant_id}-{int(datetime.now().timestamp())}"
        
        await client.start_workflow(
            "MarketingCampaignWorkflow",
            {"topic": topic, "platforms": platforms, "tenant_id": tenant_id},
            id=workflow_id,
            task_queue="marketing-tasks"
        )
        
        return {
            "status": "triggered",
            "workflow_id": workflow_id,
            "topic": topic,
            "message": f"Social orchestration started for {topic}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start orchestration: {str(e)}")

@router.post("/orchestrate-ads")
async def orchestrate_ad_campaign(
    current_budgets: Dict[str, float] = Body(..., embed=True),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Trigger an AI-orchestrated ad budget optimization via Temporal."""
    tenant_id = user.tenant_id or "default_tenant"
    temporal_url = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
    
    try:
        client = await Client.connect(temporal_url)
        
        workflow_id = f"ad-orchestration-{tenant_id}-{int(datetime.now().timestamp())}"
        
        await client.start_workflow(
            "AdOrchestrationWorkflow",
            {"current_budgets": current_budgets, "tenant_id": tenant_id},
            id=workflow_id,
            task_queue="marketing-tasks"
        )
        
        return {
            "status": "triggered",
            "workflow_id": workflow_id,
            "message": "Ad budget orchestration started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start orchestration: {str(e)}")
