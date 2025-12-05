"""
Campaign Management Service - BizoholicSaaS
Handles campaign lifecycle, AI agent integration, and optimization
Port: 8002
"""

from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime, timedelta
import logging
from enum import Enum

# Shared imports
import sys
import os
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas')

from shared.database.connection import get_postgres_session, get_redis_client, init_database
from shared.database.models import Campaign, CampaignExecution, AIAgentTask, SalesFunnel, FunnelStageExecution
from shared.events.event_bus import EventBus, EventFactory, EventType, event_handler
from shared.auth.jwt_auth import get_current_user, UserContext, require_permission, Permission

# Import funnel builder
from .funnel_builder import AdvancedFunnelBuilder, FunnelTemplate, FunnelStageType, TriggerType, ActionType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Campaign Management Service",
    description="Campaign lifecycle management and AI agent orchestration for BizoholicSaaS",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
event_bus: EventBus = None
redis_client = None

# Enums
class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

class CampaignType(str, Enum):
    GOOGLE_ADS = "google_ads"
    FACEBOOK_ADS = "facebook_ads"
    LINKEDIN_ADS = "linkedin_ads"
    EMAIL_MARKETING = "email_marketing"
    CONTENT_MARKETING = "content_marketing"
    SEO_CAMPAIGN = "seo_campaign"

class ExecutionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"

# Pydantic models
class CampaignCreate(BaseModel):
    name: str
    description: Optional[str] = None
    campaign_type: CampaignType
    budget: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    target_audience: Dict[str, Any] = {}
    creative_assets: List[Dict[str, Any]] = []
    ai_optimization_config: Dict[str, Any] = {}

class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[CampaignStatus] = None
    budget: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    target_audience: Optional[Dict[str, Any]] = None
    creative_assets: Optional[List[Dict[str, Any]]] = None
    ai_optimization_config: Optional[Dict[str, Any]] = None

class CampaignResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    status: CampaignStatus
    campaign_type: CampaignType
    budget: Optional[float]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    target_audience: Dict[str, Any]
    creative_assets: List[Dict[str, Any]]
    performance_metrics: Dict[str, Any]
    ai_optimization_config: Dict[str, Any]
    tenant_id: str
    created_by: str
    created_at: datetime
    updated_at: datetime

class CampaignExecutionCreate(BaseModel):
    campaign_id: str
    platform: str
    execution_data: Dict[str, Any] = {}

class CampaignExecutionResponse(BaseModel):
    id: str
    campaign_id: str
    platform: str
    execution_status: ExecutionStatus
    execution_data: Dict[str, Any]
    platform_campaign_id: Optional[str]
    metrics_snapshot: Dict[str, Any]
    error_logs: List[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

class AIAgentTaskCreate(BaseModel):
    campaign_id: Optional[str] = None
    task_type: str  # optimization, analysis, content_generation
    agent_name: str
    task_config: Dict[str, Any] = {}

class AIAgentTaskResponse(BaseModel):
    id: str
    campaign_id: Optional[str]
    task_type: str
    agent_name: str
    task_config: Dict[str, Any]
    execution_status: ExecutionStatus
    result_data: Dict[str, Any]
    execution_time_seconds: Optional[float]
    cost: Optional[float]
    tenant_id: str
    created_at: datetime
    updated_at: datetime

class SalesFunnelCreate(BaseModel):
    name: str
    description: Optional[str] = None
    funnel_type: str = "lead_nurturing"
    stages: List[Dict[str, Any]]
    automation_rules: Dict[str, Any] = {}
    conversion_goals: Dict[str, Any] = {}

class SalesFunnelResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    funnel_type: str
    stages: List[Dict[str, Any]]
    automation_rules: Dict[str, Any]
    mautic_campaign_id: Optional[str]
    conversion_goals: Dict[str, Any]
    is_active: bool
    tenant_id: str
    created_by: str
    created_at: datetime
    updated_at: datetime

class FunnelTemplateRequest(BaseModel):
    template: FunnelTemplate
    customizations: Dict[str, Any] = {}

class CustomFunnelRequest(BaseModel):
    funnel_config: Dict[str, Any]

class FunnelMauticSyncRequest(BaseModel):
    funnel_id: str
    mautic_integration_id: str

class FunnelOptimizationRequest(BaseModel):
    funnel_id: str
    performance_data: Dict[str, Any]

class FunnelAnalyticsRequest(BaseModel):
    funnel_id: str
    date_range: Dict[str, str] = {}
    include_predictions: bool = False

class CampaignOptimizationRequest(BaseModel):
    campaign_id: str
    optimization_type: str = "performance"  # performance, budget, targeting
    ai_config: Dict[str, Any] = {}

class CampaignAnalysisRequest(BaseModel):
    campaign_ids: List[str]
    analysis_type: str = "comprehensive"  # quick, comprehensive, competitive
    date_range: Dict[str, str] = {}

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database and event bus connections"""
    global event_bus, redis_client
    
    try:
        await init_database()
        logger.info("Database connections initialized")
        
        redis_client = await get_redis_client()
        
        event_bus = EventBus(redis_client, "campaign-management")
        await event_bus.initialize()
        await event_bus.start()
        logger.info("Event bus initialized")
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Clean shutdown of connections"""
    global event_bus
    
    if event_bus:
        await event_bus.stop()
    logger.info("Campaign Management Service shutdown complete")

# Health check endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "campaign-management",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    try:
        async with get_postgres_session("campaign_management") as session:
            await session.execute("SELECT 1")
        
        await redis_client.ping()
        
        return {
            "status": "ready",
            "service": "campaign-management",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service not ready: {str(e)}"
        )

# Campaign CRUD endpoints
@app.post("/campaigns", response_model=CampaignResponse)
async def create_campaign(
    campaign_data: CampaignCreate,
    current_user: UserContext = Depends(require_permission(Permission.CAMPAIGN_CREATE))
):
    """Create a new campaign"""
    
    try:
        async with get_postgres_session("campaign_management") as session:
            new_campaign = Campaign(
                id=uuid.uuid4(),
                name=campaign_data.name,
                description=campaign_data.description,
                status=CampaignStatus.DRAFT.value,
                campaign_type=campaign_data.campaign_type.value,
                budget=campaign_data.budget,
                start_date=campaign_data.start_date,
                end_date=campaign_data.end_date,
                target_audience=campaign_data.target_audience,
                creative_assets=campaign_data.creative_assets,
                ai_optimization_config=campaign_data.ai_optimization_config,
                tenant_id=uuid.UUID(current_user.tenant_id),
                created_by=uuid.UUID(current_user.user_id)
            )
            
            session.add(new_campaign)
            await session.commit()
            await session.refresh(new_campaign)
            
            # Publish campaign created event
            event = EventFactory.campaign_created(
                tenant_id=current_user.tenant_id,
                user_id=current_user.user_id,
                campaign_id=str(new_campaign.id),
                campaign_data={
                    "name": new_campaign.name,
                    "type": new_campaign.campaign_type,
                    "budget": new_campaign.budget,
                    "created_by": current_user.user_id
                }
            )
            await event_bus.publish(event)
            
            return CampaignResponse(
                id=str(new_campaign.id),
                name=new_campaign.name,
                description=new_campaign.description,
                status=CampaignStatus(new_campaign.status),
                campaign_type=CampaignType(new_campaign.campaign_type),
                budget=new_campaign.budget,
                start_date=new_campaign.start_date,
                end_date=new_campaign.end_date,
                target_audience=new_campaign.target_audience,
                creative_assets=new_campaign.creative_assets,
                performance_metrics=new_campaign.performance_metrics,
                ai_optimization_config=new_campaign.ai_optimization_config,
                tenant_id=str(new_campaign.tenant_id),
                created_by=str(new_campaign.created_by),
                created_at=new_campaign.created_at,
                updated_at=new_campaign.updated_at
            )
            
    except Exception as e:
        logger.error(f"Create campaign error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create campaign"
        )

@app.get("/campaigns", response_model=List[CampaignResponse])
async def list_campaigns(
    current_user: UserContext = Depends(require_permission(Permission.CAMPAIGN_READ)),
    status_filter: Optional[CampaignStatus] = None,
    campaign_type: Optional[CampaignType] = None,
    skip: int = 0,
    limit: int = 100
):
    """List campaigns for current tenant"""
    
    try:
        async with get_postgres_session("campaign_management") as session:
            from sqlalchemy import select
            
            stmt = select(Campaign).where(
                Campaign.tenant_id == uuid.UUID(current_user.tenant_id),
                Campaign.is_active == True
            )
            
            if status_filter:
                stmt = stmt.where(Campaign.status == status_filter.value)
            
            if campaign_type:
                stmt = stmt.where(Campaign.campaign_type == campaign_type.value)
            
            stmt = stmt.offset(skip).limit(limit).order_by(Campaign.created_at.desc())
            
            result = await session.execute(stmt)
            campaigns = result.scalars().all()
            
            return [
                CampaignResponse(
                    id=str(campaign.id),
                    name=campaign.name,
                    description=campaign.description,
                    status=CampaignStatus(campaign.status),
                    campaign_type=CampaignType(campaign.campaign_type),
                    budget=campaign.budget,
                    start_date=campaign.start_date,
                    end_date=campaign.end_date,
                    target_audience=campaign.target_audience,
                    creative_assets=campaign.creative_assets,
                    performance_metrics=campaign.performance_metrics,
                    ai_optimization_config=campaign.ai_optimization_config,
                    tenant_id=str(campaign.tenant_id),
                    created_by=str(campaign.created_by),
                    created_at=campaign.created_at,
                    updated_at=campaign.updated_at
                ) for campaign in campaigns
            ]
            
    except Exception as e:
        logger.error(f"List campaigns error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list campaigns"
        )

@app.get("/campaigns/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: str,
    current_user: UserContext = Depends(require_permission(Permission.CAMPAIGN_READ))
):
    """Get campaign by ID"""
    
    try:
        async with get_postgres_session("campaign_management") as session:
            from sqlalchemy import select
            stmt = select(Campaign).where(
                Campaign.id == uuid.UUID(campaign_id),
                Campaign.tenant_id == uuid.UUID(current_user.tenant_id),
                Campaign.is_active == True
            )
            result = await session.execute(stmt)
            campaign = result.scalar_one_or_none()
            
            if not campaign:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Campaign not found"
                )
            
            return CampaignResponse(
                id=str(campaign.id),
                name=campaign.name,
                description=campaign.description,
                status=CampaignStatus(campaign.status),
                campaign_type=CampaignType(campaign.campaign_type),
                budget=campaign.budget,
                start_date=campaign.start_date,
                end_date=campaign.end_date,
                target_audience=campaign.target_audience,
                creative_assets=campaign.creative_assets,
                performance_metrics=campaign.performance_metrics,
                ai_optimization_config=campaign.ai_optimization_config,
                tenant_id=str(campaign.tenant_id),
                created_by=str(campaign.created_by),
                created_at=campaign.created_at,
                updated_at=campaign.updated_at
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get campaign error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get campaign"
        )

@app.put("/campaigns/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: str,
    campaign_data: CampaignUpdate,
    current_user: UserContext = Depends(require_permission(Permission.CAMPAIGN_UPDATE))
):
    """Update campaign"""
    
    try:
        async with get_postgres_session("campaign_management") as session:
            from sqlalchemy import select
            stmt = select(Campaign).where(
                Campaign.id == uuid.UUID(campaign_id),
                Campaign.tenant_id == uuid.UUID(current_user.tenant_id),
                Campaign.is_active == True
            )
            result = await session.execute(stmt)
            campaign = result.scalar_one_or_none()
            
            if not campaign:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Campaign not found"
                )
            
            # Update fields
            update_data = campaign_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(campaign, field) and value is not None:
                    if field == 'status' and isinstance(value, CampaignStatus):
                        setattr(campaign, field, value.value)
                    else:
                        setattr(campaign, field, value)
            
            campaign.updated_at = datetime.utcnow()
            await session.commit()
            await session.refresh(campaign)
            
            # Publish campaign updated event
            event = EventFactory.campaign_updated(
                tenant_id=current_user.tenant_id,
                user_id=current_user.user_id,
                campaign_id=str(campaign.id),
                campaign_data={
                    "name": campaign.name,
                    "status": campaign.status,
                    "updated_by": current_user.user_id,
                    "updated_fields": list(update_data.keys())
                }
            )
            await event_bus.publish(event)
            
            return CampaignResponse(
                id=str(campaign.id),
                name=campaign.name,
                description=campaign.description,
                status=CampaignStatus(campaign.status),
                campaign_type=CampaignType(campaign.campaign_type),
                budget=campaign.budget,
                start_date=campaign.start_date,
                end_date=campaign.end_date,
                target_audience=campaign.target_audience,
                creative_assets=campaign.creative_assets,
                performance_metrics=campaign.performance_metrics,
                ai_optimization_config=campaign.ai_optimization_config,
                tenant_id=str(campaign.tenant_id),
                created_by=str(campaign.created_by),
                created_at=campaign.created_at,
                updated_at=campaign.updated_at
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update campaign error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update campaign"
        )

# Campaign execution endpoints
@app.post("/campaigns/{campaign_id}/start")
async def start_campaign(
    campaign_id: str,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.CAMPAIGN_EXECUTE))
):
    """Start campaign execution"""
    
    try:
        async with get_postgres_session("campaign_management") as session:
            from sqlalchemy import select
            stmt = select(Campaign).where(
                Campaign.id == uuid.UUID(campaign_id),
                Campaign.tenant_id == uuid.UUID(current_user.tenant_id),
                Campaign.is_active == True
            )
            result = await session.execute(stmt)
            campaign = result.scalar_one_or_none()
            
            if not campaign:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Campaign not found"
                )
            
            if campaign.status != CampaignStatus.DRAFT.value:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Campaign can only be started from draft status"
                )
            
            # Update campaign status
            campaign.status = CampaignStatus.ACTIVE.value
            campaign.start_date = datetime.utcnow()
            campaign.updated_at = datetime.utcnow()
            
            await session.commit()
            
            # Create campaign execution record
            execution = CampaignExecution(
                id=uuid.uuid4(),
                campaign_id=campaign.id,
                tenant_id=campaign.tenant_id,
                platform=campaign.campaign_type,
                execution_status=ExecutionStatus.PENDING.value,
                execution_data={"started_by": current_user.user_id, "start_time": datetime.utcnow().isoformat()}
            )
            
            session.add(execution)
            await session.commit()
            
            # Publish campaign started event
            event = EventFactory.campaign_started(
                tenant_id=current_user.tenant_id,
                user_id=current_user.user_id,
                campaign_id=str(campaign.id),
                campaign_data={
                    "name": campaign.name,
                    "type": campaign.campaign_type,
                    "budget": campaign.budget,
                    "execution_id": str(execution.id)
                }
            )
            await event_bus.publish(event)
            
            # Schedule background execution
            background_tasks.add_task(execute_campaign, campaign_id, str(execution.id))
            
            return {
                "message": "Campaign started successfully",
                "campaign_id": str(campaign.id),
                "execution_id": str(execution.id),
                "status": campaign.status
            }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Start campaign error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start campaign"
        )

async def execute_campaign(campaign_id: str, execution_id: str):
    """Background task to execute campaign on target platform"""
    
    try:
        async with get_postgres_session("campaign_management") as session:
            from sqlalchemy import select
            
            # Get campaign and execution
            campaign_stmt = select(Campaign).where(Campaign.id == uuid.UUID(campaign_id))
            campaign_result = await session.execute(campaign_stmt)
            campaign = campaign_result.scalar_one_or_none()
            
            execution_stmt = select(CampaignExecution).where(CampaignExecution.id == uuid.UUID(execution_id))
            execution_result = await session.execute(execution_stmt)
            execution = execution_result.scalar_one_or_none()
            
            if not campaign or not execution:
                logger.error(f"Campaign or execution not found: {campaign_id}, {execution_id}")
                return
            
            # Update execution status
            execution.execution_status = ExecutionStatus.RUNNING.value
            await session.commit()
            
            # Simulate platform-specific execution
            # In real implementation, this would call platform APIs
            await simulate_platform_execution(campaign, execution)
            
            # Update execution status to success
            execution.execution_status = ExecutionStatus.SUCCESS.value
            execution.platform_campaign_id = f"platform_{uuid.uuid4().hex[:8]}"
            execution.metrics_snapshot = {
                "impressions": 0,
                "clicks": 0,
                "conversions": 0,
                "cost": 0.0,
                "created_at": datetime.utcnow().isoformat()
            }
            
            await session.commit()
            
            # Publish execution completed event
            event = EventFactory.campaign_execution_completed(
                tenant_id=str(campaign.tenant_id),
                campaign_id=str(campaign.id),
                execution_data={
                    "execution_id": execution_id,
                    "platform": campaign.campaign_type,
                    "platform_campaign_id": execution.platform_campaign_id,
                    "status": ExecutionStatus.SUCCESS.value
                }
            )
            await event_bus.publish(event)
            
    except Exception as e:
        logger.error(f"Campaign execution error: {e}")
        
        # Update execution status to failed
        try:
            async with get_postgres_session("campaign_management") as session:
                from sqlalchemy import select
                stmt = select(CampaignExecution).where(CampaignExecution.id == uuid.UUID(execution_id))
                result = await session.execute(stmt)
                execution = result.scalar_one_or_none()
                
                if execution:
                    execution.execution_status = ExecutionStatus.FAILED.value
                    execution.error_logs = [{"error": str(e), "timestamp": datetime.utcnow().isoformat()}]
                    await session.commit()
        except Exception as commit_error:
            logger.error(f"Failed to update execution status: {commit_error}")

async def simulate_platform_execution(campaign: Campaign, execution: CampaignExecution):
    """Simulate platform-specific campaign execution"""
    
    import asyncio
    
    # Simulate API call delay
    await asyncio.sleep(2)
    
    logger.info(f"Executing {campaign.campaign_type} campaign: {campaign.name}")
    
    # Platform-specific logic would go here
    if campaign.campaign_type == CampaignType.GOOGLE_ADS.value:
        # Google Ads API calls
        pass
    elif campaign.campaign_type == CampaignType.FACEBOOK_ADS.value:
        # Facebook Marketing API calls
        pass
    elif campaign.campaign_type == CampaignType.LINKEDIN_ADS.value:
        # LinkedIn Marketing API calls
        pass
    
    logger.info(f"Campaign execution completed: {campaign.name}")

# AI Agent task endpoints
@app.post("/ai-tasks", response_model=AIAgentTaskResponse)
async def create_ai_task(
    task_data: AIAgentTaskCreate,
    current_user: UserContext = Depends(require_permission(Permission.AGENT_EXECUTE))
):
    """Create and execute AI agent task"""
    
    try:
        async with get_postgres_session("campaign_management") as session:
            new_task = AIAgentTask(
                id=uuid.uuid4(),
                campaign_id=uuid.UUID(task_data.campaign_id) if task_data.campaign_id else None,
                task_type=task_data.task_type,
                agent_name=task_data.agent_name,
                task_config=task_data.task_config,
                execution_status=ExecutionStatus.PENDING.value,
                tenant_id=uuid.UUID(current_user.tenant_id)
            )
            
            session.add(new_task)
            await session.commit()
            await session.refresh(new_task)
            
            # Publish agent task started event
            event = EventFactory.agent_task_started(
                tenant_id=current_user.tenant_id,
                task_id=str(new_task.id),
                agent_name=task_data.agent_name,
                task_data={
                    "task_type": task_data.task_type,
                    "campaign_id": task_data.campaign_id,
                    "config": task_data.task_config
                }
            )
            await event_bus.publish(event)
            
            return AIAgentTaskResponse(
                id=str(new_task.id),
                campaign_id=str(new_task.campaign_id) if new_task.campaign_id else None,
                task_type=new_task.task_type,
                agent_name=new_task.agent_name,
                task_config=new_task.task_config,
                execution_status=ExecutionStatus(new_task.execution_status),
                result_data=new_task.result_data,
                execution_time_seconds=new_task.execution_time_seconds,
                cost=new_task.cost,
                tenant_id=str(new_task.tenant_id),
                created_at=new_task.created_at,
                updated_at=new_task.updated_at
            )
            
    except Exception as e:
        logger.error(f"Create AI task error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create AI task"
        )

@app.post("/campaigns/{campaign_id}/optimize")
async def optimize_campaign(
    campaign_id: str,
    optimization_request: CampaignOptimizationRequest,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.AGENT_EXECUTE))
):
    """Trigger AI-powered campaign optimization"""
    
    try:
        # Create AI task for optimization
        task_data = AIAgentTaskCreate(
            campaign_id=campaign_id,
            task_type="optimization",
            agent_name="campaign_optimizer",
            task_config={
                "optimization_type": optimization_request.optimization_type,
                "ai_config": optimization_request.ai_config,
                "user_id": current_user.user_id
            }
        )
        
        ai_task = await create_ai_task(task_data, current_user)
        
        # Schedule background optimization
        background_tasks.add_task(execute_campaign_optimization, campaign_id, ai_task.id)
        
        return {
            "message": "Campaign optimization started",
            "campaign_id": campaign_id,
            "task_id": ai_task.id,
            "optimization_type": optimization_request.optimization_type
        }
        
    except Exception as e:
        logger.error(f"Campaign optimization error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start campaign optimization"
        )

async def execute_campaign_optimization(campaign_id: str, task_id: str):
    """Background task to execute campaign optimization using AI agents"""
    
    try:
        # Simulate AI-powered optimization
        import asyncio
        await asyncio.sleep(5)  # Simulate processing time
        
        # In real implementation, this would:
        # 1. Call CrewAI agents service
        # 2. Analyze campaign performance
        # 3. Generate optimization recommendations
        # 4. Apply approved optimizations
        
        optimization_results = {
            "recommendations": [
                {
                    "type": "budget_adjustment",
                    "current_value": 1000.0,
                    "recommended_value": 1200.0,
                    "expected_improvement": "15% increase in conversions"
                },
                {
                    "type": "targeting_optimization",
                    "current_audience": "broad",
                    "recommended_audience": "lookalike_optimized",
                    "expected_improvement": "20% better CTR"
                }
            ],
            "performance_prediction": {
                "estimated_roi_improvement": 25.5,
                "confidence_score": 0.87
            }
        }
        
        # Update task with results
        async with get_postgres_session("campaign_management") as session:
            from sqlalchemy import select
            stmt = select(AIAgentTask).where(AIAgentTask.id == uuid.UUID(task_id))
            result = await session.execute(stmt)
            task = result.scalar_one_or_none()
            
            if task:
                task.execution_status = ExecutionStatus.SUCCESS.value
                task.result_data = optimization_results
                task.execution_time_seconds = 5.0
                task.cost = 0.25  # Estimated AI API cost
                
                await session.commit()
                
                # Publish optimization completed event
                event = EventFactory.agent_task_completed(
                    tenant_id=str(task.tenant_id),
                    task_id=task_id,
                    agent_name=task.agent_name,
                    result_data=optimization_results
                )
                await event_bus.publish(event)
        
    except Exception as e:
        logger.error(f"Campaign optimization execution error: {e}")

# Advanced Sales Funnel Builder endpoints
@app.get("/funnel-templates")
async def get_funnel_templates(
    current_user: UserContext = Depends(require_permission(Permission.CAMPAIGN_READ))
):
    """Get available funnel templates"""
    
    try:
        builder = AdvancedFunnelBuilder(current_user.tenant_id, current_user.user_id)
        templates = builder.get_funnel_templates()
        
        return {
            "templates": templates,
            "total_templates": len(templates),
            "categories": ["SaaS", "Lead Generation", "E-commerce", "Webinar", "Consultation"]
        }
        
    except Exception as e:
        logger.error(f"Get funnel templates error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get funnel templates"
        )

@app.post("/funnels/from-template", response_model=SalesFunnelResponse)
async def create_funnel_from_template(
    template_request: FunnelTemplateRequest,
    current_user: UserContext = Depends(require_permission(Permission.CAMPAIGN_CREATE))
):
    """Create a funnel from a pre-built template"""
    
    try:
        builder = AdvancedFunnelBuilder(current_user.tenant_id, current_user.user_id)
        
        # Create funnel from template
        funnel_config = builder.create_funnel_from_template(
            template_request.template, 
            template_request.customizations
        )
        
        # Validate configuration
        validation_result = builder.validate_funnel_config(funnel_config)
        if not validation_result["is_valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid funnel configuration: {validation_result['errors']}"
            )
        
        # Save to database
        async with get_postgres_session("campaign_management") as session:
            new_funnel = SalesFunnel(
                id=uuid.UUID(funnel_config["id"]),
                name=funnel_config["name"],
                description=funnel_config.get("description"),
                funnel_type=funnel_config["funnel_type"],
                stages=funnel_config["stages"],
                automation_rules=funnel_config["automation_rules"],
                conversion_goals=funnel_config["conversion_goals"],
                tenant_id=uuid.UUID(current_user.tenant_id),
                created_by=uuid.UUID(current_user.user_id),
                is_active=True
            )
            
            session.add(new_funnel)
            await session.commit()
            await session.refresh(new_funnel)
            
            # Publish funnel created event
            event = EventFactory.funnel_created(
                tenant_id=current_user.tenant_id,
                funnel_id=str(new_funnel.id),
                funnel_data={
                    "name": new_funnel.name,
                    "template": template_request.template,
                    "stages_count": len(new_funnel.stages)
                }
            )
            await event_bus.publish(event)
            
            return SalesFunnelResponse(
                id=str(new_funnel.id),
                name=new_funnel.name,
                description=new_funnel.description,
                funnel_type=new_funnel.funnel_type,
                stages=new_funnel.stages,
                automation_rules=new_funnel.automation_rules,
                mautic_campaign_id=new_funnel.mautic_campaign_id,
                conversion_goals=new_funnel.conversion_goals,
                is_active=new_funnel.is_active,
                tenant_id=str(new_funnel.tenant_id),
                created_by=str(new_funnel.created_by),
                created_at=new_funnel.created_at,
                updated_at=new_funnel.updated_at
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create funnel from template error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create funnel from template"
        )

@app.post("/funnels/custom", response_model=SalesFunnelResponse)
async def create_custom_funnel(
    custom_request: CustomFunnelRequest,
    current_user: UserContext = Depends(require_permission(Permission.CAMPAIGN_CREATE))
):
    """Create a custom funnel from scratch"""
    
    try:
        builder = AdvancedFunnelBuilder(current_user.tenant_id, current_user.user_id)
        
        # Build custom funnel
        funnel_config = builder.build_custom_funnel(custom_request.funnel_config)
        
        # Validate configuration
        validation_result = builder.validate_funnel_config(funnel_config)
        if not validation_result["is_valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid funnel configuration: {validation_result['errors']}"
            )
        
        # Save to database
        async with get_postgres_session("campaign_management") as session:
            new_funnel = SalesFunnel(
                id=uuid.UUID(funnel_config["id"]),
                name=funnel_config["name"],
                description=funnel_config.get("description"),
                funnel_type=funnel_config["funnel_type"],
                stages=funnel_config["stages"],
                automation_rules=funnel_config["automation_rules"],
                conversion_goals=funnel_config["conversion_goals"],
                tenant_id=uuid.UUID(current_user.tenant_id),
                created_by=uuid.UUID(current_user.user_id),
                is_active=True
            )
            
            session.add(new_funnel)
            await session.commit()
            await session.refresh(new_funnel)
            
            return SalesFunnelResponse(
                id=str(new_funnel.id),
                name=new_funnel.name,
                description=new_funnel.description,
                funnel_type=new_funnel.funnel_type,
                stages=new_funnel.stages,
                automation_rules=new_funnel.automation_rules,
                mautic_campaign_id=new_funnel.mautic_campaign_id,
                conversion_goals=new_funnel.conversion_goals,
                is_active=new_funnel.is_active,
                tenant_id=str(new_funnel.tenant_id),
                created_by=str(new_funnel.created_by),
                created_at=new_funnel.created_at,
                updated_at=new_funnel.updated_at
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create custom funnel error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create custom funnel"
        )

@app.post("/funnels/{funnel_id}/sync-mautic")
async def sync_funnel_to_mautic(
    funnel_id: str,
    sync_request: FunnelMauticSyncRequest,
    current_user: UserContext = Depends(require_permission(Permission.INTEGRATION_READ))
):
    """Sync funnel to Mautic for email automation"""
    
    try:
        # Get funnel
        async with get_postgres_session("campaign_management") as session:
            from sqlalchemy import select
            stmt = select(SalesFunnel).where(
                SalesFunnel.id == uuid.UUID(funnel_id),
                SalesFunnel.tenant_id == uuid.UUID(current_user.tenant_id)
            )
            result = await session.execute(stmt)
            funnel = result.scalar_one_or_none()
            
            if not funnel:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Funnel not found"
                )
        
        # Get Mautic integration credentials from Integration Service
        # This would typically be an API call to the Integration Service
        mautic_integration_config = {
            "api_url": "http://mautic-service:8090",
            "client_id": "bizoholic_client",
            "client_secret": "bizoholic_secret_change_me",
            "username": "admin",
            "password": "MauticAdmin2024!"
        }
        
        # Sync to Mautic
        builder = AdvancedFunnelBuilder(current_user.tenant_id, current_user.user_id)
        
        funnel_config = {
            "id": str(funnel.id),
            "name": funnel.name,
            "description": funnel.description,
            "stages": funnel.stages
        }
        
        sync_result = await builder.sync_funnel_to_mautic(funnel_config, mautic_integration_config)
        
        if sync_result["success"]:
            # Update funnel with Mautic campaign ID
            async with get_postgres_session("campaign_management") as session:
                from sqlalchemy import select
                stmt = select(SalesFunnel).where(SalesFunnel.id == uuid.UUID(funnel_id))
                result = await session.execute(stmt)
                funnel = result.scalar_one_or_none()
                
                if funnel:
                    funnel.mautic_campaign_id = str(sync_result["mautic_campaign_id"])
                    funnel.updated_at = datetime.utcnow()
                    await session.commit()
            
            return {
                "success": True,
                "mautic_campaign_id": sync_result["mautic_campaign_id"],
                "email_mappings": sync_result["email_mappings"],
                "sync_timestamp": sync_result["sync_timestamp"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Mautic sync failed: {sync_result['error']}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Sync funnel to Mautic error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to sync funnel to Mautic"
        )

@app.get("/funnels/{funnel_id}/analytics")
async def get_funnel_analytics(
    funnel_id: str,
    analytics_request: FunnelAnalyticsRequest,
    current_user: UserContext = Depends(require_permission(Permission.CAMPAIGN_READ))
):
    """Get funnel performance analytics"""
    
    try:
        # Get funnel
        async with get_postgres_session("campaign_management") as session:
            from sqlalchemy import select
            stmt = select(SalesFunnel).where(
                SalesFunnel.id == uuid.UUID(funnel_id),
                SalesFunnel.tenant_id == uuid.UUID(current_user.tenant_id)
            )
            result = await session.execute(stmt)
            funnel = result.scalar_one_or_none()
            
            if not funnel:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Funnel not found"
                )
        
        # In real implementation, this would fetch actual performance data from Mautic/Analytics Service
        # For now, we'll simulate performance data
        performance_data = {
            "total_entries": 1250,
            "total_completions": 156,
            "revenue_generated": 15600.0,
            "total_cost": 2400.0,
            "average_completion_time": 8.5,
            "stage_data": [
                {"stage_id": "stage_1", "entries": 1250, "completions": 1000},
                {"stage_id": "stage_2", "entries": 1000, "completions": 750},
                {"stage_id": "stage_3", "entries": 750, "completions": 400},
                {"stage_id": "stage_4", "entries": 400, "completions": 156}
            ]
        }
        
        # Generate analytics
        builder = AdvancedFunnelBuilder(current_user.tenant_id, current_user.user_id)
        analytics = builder.generate_funnel_analytics(funnel_id, performance_data)
        
        return {
            "funnel_id": funnel_id,
            "analytics": analytics.dict(),
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get funnel analytics error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get funnel analytics"
        )

@app.post("/funnels/{funnel_id}/optimize")
async def optimize_funnel(
    funnel_id: str,
    optimization_request: FunnelOptimizationRequest,
    current_user: UserContext = Depends(require_permission(Permission.CAMPAIGN_UPDATE))
):
    """Generate funnel optimization recommendations"""
    
    try:
        # Get funnel
        async with get_postgres_session("campaign_management") as session:
            from sqlalchemy import select
            stmt = select(SalesFunnel).where(
                SalesFunnel.id == uuid.UUID(funnel_id),
                SalesFunnel.tenant_id == uuid.UUID(current_user.tenant_id)
            )
            result = await session.execute(stmt)
            funnel = result.scalar_one_or_none()
            
            if not funnel:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Funnel not found"
                )
        
        # Generate analytics from performance data
        builder = AdvancedFunnelBuilder(current_user.tenant_id, current_user.user_id)
        analytics = builder.generate_funnel_analytics(funnel_id, optimization_request.performance_data)
        
        # Generate optimization recommendations
        funnel_config = {
            "id": str(funnel.id),
            "name": funnel.name,
            "stages": funnel.stages
        }
        
        optimization_result = builder.optimize_funnel_performance(analytics, funnel_config)
        
        return {
            "funnel_id": funnel_id,
            "current_performance": analytics.dict(),
            "optimization": optimization_result,
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Optimize funnel error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to optimize funnel"
        )

@app.post("/funnels/{funnel_id}/validate")
async def validate_funnel(
    funnel_id: str,
    current_user: UserContext = Depends(require_permission(Permission.CAMPAIGN_READ))
):
    """Validate funnel configuration"""
    
    try:
        # Get funnel
        async with get_postgres_session("campaign_management") as session:
            from sqlalchemy import select
            stmt = select(SalesFunnel).where(
                SalesFunnel.id == uuid.UUID(funnel_id),
                SalesFunnel.tenant_id == uuid.UUID(current_user.tenant_id)
            )
            result = await session.execute(stmt)
            funnel = result.scalar_one_or_none()
            
            if not funnel:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Funnel not found"
                )
        
        # Validate funnel configuration
        builder = AdvancedFunnelBuilder(current_user.tenant_id, current_user.user_id)
        
        funnel_config = {
            "name": funnel.name,
            "stages": funnel.stages,
            "automation_rules": funnel.automation_rules
        }
        
        validation_result = builder.validate_funnel_config(funnel_config)
        
        return {
            "funnel_id": funnel_id,
            "validation": validation_result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Validate funnel error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to validate funnel"
        )

# Legacy funnel endpoint (for backward compatibility)
@app.post("/funnels", response_model=SalesFunnelResponse)
async def create_sales_funnel(
    funnel_data: SalesFunnelCreate,
    current_user: UserContext = Depends(require_permission(Permission.CAMPAIGN_CREATE))
):
    """Create a new sales funnel (legacy endpoint)"""
    
    try:
        async with get_postgres_session("campaign_management") as session:
            new_funnel = SalesFunnel(
                id=uuid.uuid4(),
                name=funnel_data.name,
                description=funnel_data.description,
                funnel_type=funnel_data.funnel_type,
                stages=funnel_data.stages,
                automation_rules=funnel_data.automation_rules,
                conversion_goals=funnel_data.conversion_goals,
                tenant_id=uuid.UUID(current_user.tenant_id),
                created_by=uuid.UUID(current_user.user_id),
                is_active=True
            )
            
            session.add(new_funnel)
            await session.commit()
            await session.refresh(new_funnel)
            
            return SalesFunnelResponse(
                id=str(new_funnel.id),
                name=new_funnel.name,
                description=new_funnel.description,
                funnel_type=new_funnel.funnel_type,
                stages=new_funnel.stages,
                automation_rules=new_funnel.automation_rules,
                mautic_campaign_id=new_funnel.mautic_campaign_id,
                conversion_goals=new_funnel.conversion_goals,
                is_active=new_funnel.is_active,
                tenant_id=str(new_funnel.tenant_id),
                created_by=str(new_funnel.created_by),
                created_at=new_funnel.created_at,
                updated_at=new_funnel.updated_at
            )
            
    except Exception as e:
        logger.error(f"Create sales funnel error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create sales funnel"
        )

# Event handlers
@event_handler(EventType.USER_CREATED)
async def handle_user_created(event):
    """Handle new user created - could trigger welcome campaign"""
    logger.info(f"New user created in tenant {event.tenant_id}: {event.data}")

@event_handler(EventType.INTEGRATION_SYNC_COMPLETED)
async def handle_integration_sync_completed(event):
    """Handle integration sync completion - update campaign metrics"""
    logger.info(f"Integration sync completed for tenant {event.tenant_id}: {event.data}")

# Metrics endpoint
@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return {
        "service": "campaign-management",
        "metrics": {
            "active_campaigns": 0,
            "total_campaigns": 0,
            "campaign_executions": 0,
            "ai_tasks_completed": 0,
            "optimization_requests": 0
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)