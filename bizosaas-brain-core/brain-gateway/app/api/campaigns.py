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
    tenant_id = UUID(user.tenant_id) if user.tenant_id != "default" else UUID("00000000-0000-0000-0000-000000000000") # Mock UUID for default
    
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
    tenant_id = UUID(user.tenant_id) if user.tenant_id != "default" else UUID("00000000-0000-0000-0000-000000000000")
    return service.list_campaigns(tenant_id)

@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(
    campaign_id: UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = CampaignService(db)
    tenant_id = UUID(user.tenant_id) if user.tenant_id != "default" else UUID("00000000-0000-0000-0000-000000000000")
    
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
    tenant_id = UUID(user.tenant_id) if user.tenant_id != "default" else UUID("00000000-0000-0000-0000-000000000000")
    
    try:
        results = await service.publish_campaign(campaign_id, tenant_id)
        return {"status": "published", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Strategy Validation (PRD Step 11: Feasibility Engine) ---

class StrategyValidationRequest(BaseModel):
    goal: str  # lead_gen, ecommerce_sales, brand_awareness, app_installs
    budget: float
    currency: str = "USD"
    platforms: List[str] = []  # google-ads, facebook-ads, etc.
    target_audience: Dict[str, Any] = {}
    timeline_months: float = 3.0
    industry: str = "general"


class StrategyValidationResponse(BaseModel):
    validation_id: str
    is_feasible: bool
    feasibility_score: Optional[float]
    analysis: Optional[str]
    recommendations: List[Dict[str, Any]] = []
    suggested_adjustments: Dict[str, Any] = {}


@router.post("/validate-strategy", response_model=StrategyValidationResponse)
async def validate_strategy(
    request: StrategyValidationRequest,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Validate a campaign strategy using the AI Feasibility Engine.
    
    This implements PRD Step 11: A loop where AI analyzes the proposed strategy
    against historical data and industry benchmarks, providing recommendations
    for refinement until the client is satisfied.
    """
    import os
    from temporalio.client import Client
    
    tenant_id = user.tenant_id or "default"
    
    strategy = {
        "goal": request.goal,
        "budget": request.budget,
        "currency": request.currency,
        "platforms": request.platforms,
        "target_audience": request.target_audience,
        "timeline_months": request.timeline_months,
        "industry": request.industry,
    }
    
    try:
        # Connect to Temporal
        temporal_host = os.environ.get("TEMPORAL_HOST", "localhost:7233")
        client = await Client.connect(temporal_host)
        
        # Execute the workflow
        from app.workflows.strategy_validation import StrategyValidationWorkflow
        
        result = await client.execute_workflow(
            StrategyValidationWorkflow.run,
            args=[tenant_id, user.id, strategy],
            id=f"strategy-validation-{tenant_id}-{user.id}-{int(datetime.now().timestamp())}",
            task_queue="bizosaas-workflows"
        )
        
        return StrategyValidationResponse(
            validation_id=result.get("validation_id", ""),
            is_feasible=result.get("is_feasible", False),
            feasibility_score=result.get("feasibility_score"),
            analysis=result.get("analysis"),
            recommendations=result.get("recommendations", []),
            suggested_adjustments=result.get("suggested_adjustments", {})
        )
        
    except Exception as e:
        # Fallback: Run synchronously without Temporal
        from app.workflows.strategy_validation import (
            fetch_connector_insights,
            get_industry_benchmarks,
            analyze_strategy_with_ai,
            save_validation_result
        )
        
        try:
            # Run activities directly
            insights = await fetch_connector_insights(tenant_id, request.platforms)
            benchmarks = await get_industry_benchmarks(request.industry, request.goal)
            analysis = await analyze_strategy_with_ai(strategy, insights, benchmarks)
            validation_id = await save_validation_result(
                tenant_id, user.id, strategy, analysis
            )
            
            return StrategyValidationResponse(
                validation_id=validation_id,
                is_feasible=analysis.get("feasibility_score", 0) >= 60,
                feasibility_score=analysis.get("feasibility_score"),
                analysis=analysis.get("analysis"),
                recommendations=analysis.get("recommendations", []),
                suggested_adjustments=analysis.get("suggested_adjustments", {})
            )
        except Exception as inner_e:
            raise HTTPException(
                status_code=500, 
                detail=f"Strategy validation failed: {str(inner_e)}"
            )


@router.get("/validations/{validation_id}")
async def get_validation_result(
    validation_id: UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific strategy validation result."""
    from app.models.strategy_validation import StrategyValidation
    
    validation = db.query(StrategyValidation).filter(
        StrategyValidation.id == validation_id,
        StrategyValidation.tenant_id == (user.tenant_id or "default")
    ).first()
    
    if not validation:
        raise HTTPException(status_code=404, detail="Validation not found")
    
    return validation.to_dict()


@router.get("/validations")
async def list_validations(
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """List recent strategy validations for the current tenant."""
    from app.models.strategy_validation import StrategyValidation
    
    validations = db.query(StrategyValidation).filter(
        StrategyValidation.tenant_id == (user.tenant_id or "default")
    ).order_by(StrategyValidation.created_at.desc()).limit(limit).all()
    
    return [v.to_dict() for v in validations]

