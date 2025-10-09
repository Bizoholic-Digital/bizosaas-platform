"""
FastAPI Endpoints for Tenant-Aware AI Coordinator
Provides unified API access to 93+ AI agents with intelligent tenant routing
"""

import asyncio
from typing import Dict, Any, List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Request, HTTPException, status, Depends, BackgroundTasks
from pydantic import BaseModel, Field

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from shared.enhanced_tenant_context import (
    EnhancedTenantContext,
    PlatformType,
    TenantTier
)
from shared.rls_middleware import (
    RLSRequestHelper,
    get_tenant_context,
    get_rls_context
)
from .tenant_aware_ai_coordinator import (
    TenantAwareAICoordinator,
    AgentSpecialization,
    AgentCapability
)

import structlog

logger = structlog.get_logger(__name__)

# Initialize router
router = APIRouter(prefix="/api/brain/ai-coordinator", tags=["AI Coordinator"])


# Request/Response Models
class AgentTaskRequest(BaseModel):
    """Request model for agent task execution"""
    task_description: str = Field(..., description="Description of the task to execute")
    platform: PlatformType = Field(..., description="Target platform")
    task_data: Dict[str, Any] = Field(default_factory=dict, description="Task-specific data")
    agent_preference: Optional[str] = Field(None, description="Preferred agent ID")
    specialization_preference: Optional[AgentSpecialization] = Field(None, description="Preferred agent specialization")
    priority: str = Field("normal", description="Task priority: low, normal, high, urgent")
    timeout_seconds: int = Field(300, description="Task timeout in seconds")


class AgentTaskResponse(BaseModel):
    """Response model for agent task execution"""
    success: bool
    task_id: str
    agent_id: str
    agent_name: str
    execution_time: float
    result: Dict[str, Any]
    tenant_id: str
    platform: str
    timestamp: str
    error: Optional[str] = None


class AgentRecommendationRequest(BaseModel):
    """Request model for agent recommendations"""
    platform: PlatformType = Field(..., description="Target platform")
    task_type: str = Field(..., description="Type of task")
    max_recommendations: int = Field(5, description="Maximum number of recommendations")


class ChatRequest(BaseModel):
    """Request model for conversational AI chat"""
    message: str = Field(..., description="User message")
    platform: PlatformType = Field(..., description="Platform context")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    agent_preference: Optional[str] = Field(None, description="Preferred agent ID")
    context_data: Dict[str, Any] = Field(default_factory=dict, description="Additional context data")


class ChatResponse(BaseModel):
    """Response model for conversational AI chat"""
    success: bool
    message: str
    agent_id: str
    agent_name: str
    conversation_id: str
    platform: str
    suggestions: List[str] = Field(default_factory=list)
    actions: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None


class DashboardResponse(BaseModel):
    """Response model for tenant performance dashboard"""
    tenant_id: str
    subscription_tier: str
    platform_access: Dict[str, bool]
    overall_stats: Dict[str, Any]
    agent_usage: Dict[str, Any]
    platform_performance: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    generated_at: str


# Global coordinator instance (initialized in main app)
ai_coordinator: Optional[TenantAwareAICoordinator] = None


def get_ai_coordinator() -> TenantAwareAICoordinator:
    """Get the global AI coordinator instance"""
    if ai_coordinator is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI Coordinator not initialized"
        )
    return ai_coordinator


@router.post("/execute-task", response_model=AgentTaskResponse)
async def execute_agent_task(
    request: AgentTaskRequest,
    http_request: Request,
    background_tasks: BackgroundTasks,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    coordinator: TenantAwareAICoordinator = Depends(get_ai_coordinator)
):
    """
    Execute a task using the optimal AI agent for the tenant and platform

    This endpoint:
    1. Validates tenant access to the target platform
    2. Finds the optimal agent based on task requirements and performance
    3. Executes the task with tenant-specific context
    4. Returns comprehensive results and performance metrics
    """
    try:
        # Validate platform access
        await RLSRequestHelper.require_platform_access(
            http_request, request.platform, "read"
        )

        # Determine the agent to use
        if request.agent_preference:
            # Use specific agent if requested
            agent = coordinator.agents.get(request.agent_preference)
            if not agent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Agent {request.agent_preference} not found"
                )
            if not agent.can_serve_tenant(tenant_context):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Agent {request.agent_preference} cannot serve this tenant"
                )
            selected_agent_id = request.agent_preference
        else:
            # Find optimal agent
            optimal_agent = await coordinator.find_optimal_agent(
                tenant_context,
                request.task_description,
                request.platform,
                request.specialization_preference
            )
            if not optimal_agent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No suitable agent found for this task"
                )
            selected_agent_id = optimal_agent.agent_id

        # Execute the task
        task_result = await coordinator.execute_agent_task(
            tenant_context,
            selected_agent_id,
            request.task_description,
            request.task_data,
            request.platform
        )

        # Log usage for analytics (background task)
        background_tasks.add_task(
            _log_agent_usage,
            tenant_context.tenant_id,
            selected_agent_id,
            request.platform.value,
            task_result.get("success", False)
        )

        return AgentTaskResponse(
            success=task_result["success"],
            task_id=str(UUID(int=hash(f"{tenant_context.tenant_id}_{selected_agent_id}_{datetime.utcnow().timestamp()}"))),
            agent_id=task_result["agent_id"],
            agent_name=task_result["agent_name"],
            execution_time=task_result["execution_time"],
            result=task_result["result"],
            tenant_id=task_result["tenant_id"],
            platform=task_result["platform"],
            timestamp=task_result["timestamp"],
            error=task_result.get("error")
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Task execution failed",
            tenant_id=tenant_context.tenant_id,
            platform=request.platform.value,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Task execution failed: {str(e)}"
        )


@router.post("/chat", response_model=ChatResponse)
async def conversational_ai_chat(
    request: ChatRequest,
    http_request: Request,
    background_tasks: BackgroundTasks,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    coordinator: TenantAwareAICoordinator = Depends(get_ai_coordinator)
):
    """
    Engage in conversational AI chat powered by specialized agents

    This endpoint:
    1. Analyzes the user message to determine the best agent specialization
    2. Maintains conversation context and history
    3. Provides intelligent responses with actionable suggestions
    4. Routes to platform-specific agents for specialized assistance
    """
    try:
        # Validate platform access
        await RLSRequestHelper.require_platform_access(
            http_request, request.platform, "read"
        )

        # Analyze message to determine optimal agent specialization
        suggested_specialization = await _analyze_message_for_specialization(
            request.message, request.platform
        )

        # Find optimal agent for conversation
        if request.agent_preference:
            agent = coordinator.agents.get(request.agent_preference)
            if not agent or not agent.can_serve_tenant(tenant_context):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Requested agent not available"
                )
            selected_agent = agent
        else:
            selected_agent = await coordinator.find_optimal_agent(
                tenant_context,
                request.message,
                request.platform,
                suggested_specialization
            )

        if not selected_agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No suitable agent available for conversation"
            )

        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid4())

        # Prepare conversational task data
        task_data = {
            "message": request.message,
            "conversation_id": conversation_id,
            "context_data": request.context_data,
            "conversation_history": await _get_conversation_history(
                tenant_context.tenant_id, conversation_id
            )
        }

        # Execute conversational task
        chat_result = await coordinator.execute_agent_task(
            tenant_context,
            selected_agent.agent_id,
            f"Conversational assistance: {request.message}",
            task_data,
            request.platform
        )

        if not chat_result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=chat_result.get("error", "Chat processing failed")
            )

        # Extract response components
        result_data = chat_result["result"]
        response_message = result_data.get("output", "I'm here to help!")
        suggestions = result_data.get("recommendations", [])

        # Generate contextual actions based on platform and conversation
        actions = await _generate_contextual_actions(
            request.platform, request.message, selected_agent.specialization
        )

        # Store conversation in background
        background_tasks.add_task(
            _store_conversation,
            tenant_context.tenant_id,
            conversation_id,
            request.platform.value,
            request.message,
            response_message,
            selected_agent.agent_id
        )

        return ChatResponse(
            success=True,
            message=response_message,
            agent_id=selected_agent.agent_id,
            agent_name=selected_agent.name,
            conversation_id=conversation_id,
            platform=request.platform.value,
            suggestions=suggestions,
            actions=actions,
            metadata={
                "agent_specialization": selected_agent.specialization.value,
                "execution_time": chat_result["execution_time"],
                "quality_score": result_data.get("quality_score", 0.8)
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Chat processing failed",
            tenant_id=tenant_context.tenant_id,
            platform=request.platform.value,
            message=request.message[:100],
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {str(e)}"
        )


@router.post("/recommendations", response_model=List[Dict[str, Any]])
async def get_agent_recommendations(
    request: AgentRecommendationRequest,
    http_request: Request,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    coordinator: TenantAwareAICoordinator = Depends(get_ai_coordinator)
):
    """
    Get AI agent recommendations for specific tasks and platforms

    Returns a ranked list of agents best suited for the task, including:
    - Agent capabilities and specializations
    - Tenant-specific performance metrics
    - Suitability scores for the requested task type
    """
    try:
        # Validate platform access
        await RLSRequestHelper.require_platform_access(
            http_request, request.platform, "read"
        )

        # Get recommendations
        recommendations = await coordinator.get_agent_recommendations(
            tenant_context,
            request.platform,
            request.task_type
        )

        # Limit results
        limited_recommendations = recommendations[:request.max_recommendations]

        logger.info(
            "Agent recommendations generated",
            tenant_id=tenant_context.tenant_id,
            platform=request.platform.value,
            task_type=request.task_type,
            recommendation_count=len(limited_recommendations)
        )

        return limited_recommendations

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to generate recommendations",
            tenant_id=tenant_context.tenant_id,
            platform=request.platform.value,
            task_type=request.task_type,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@router.get("/dashboard", response_model=DashboardResponse)
async def get_tenant_dashboard(
    http_request: Request,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    coordinator: TenantAwareAICoordinator = Depends(get_ai_coordinator)
):
    """
    Get comprehensive tenant performance dashboard

    Provides detailed analytics including:
    - Overall AI agent usage statistics
    - Platform-specific performance metrics
    - Individual agent performance data
    - Actionable recommendations for optimization
    """
    try:
        # Generate dashboard data
        dashboard_data = await coordinator.get_tenant_performance_dashboard(
            tenant_context
        )

        return DashboardResponse(
            tenant_id=dashboard_data["tenant_id"],
            subscription_tier=dashboard_data["subscription_tier"],
            platform_access=dashboard_data["platform_access"],
            overall_stats=dashboard_data.get("overall_stats", {}),
            agent_usage=dashboard_data.get("agent_usage", {}),
            platform_performance=dashboard_data.get("platform_performance", {}),
            recommendations=dashboard_data.get("recommendations", []),
            generated_at=dashboard_data["generated_at"]
        )

    except Exception as e:
        logger.error(
            "Failed to generate dashboard",
            tenant_id=tenant_context.tenant_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate dashboard: {str(e)}"
        )


@router.get("/agents", response_model=List[Dict[str, Any]])
async def list_available_agents(
    http_request: Request,
    platform: Optional[PlatformType] = None,
    specialization: Optional[AgentSpecialization] = None,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    coordinator: TenantAwareAICoordinator = Depends(get_ai_coordinator)
):
    """
    List all available AI agents for the tenant

    Optionally filter by platform and specialization.
    Returns agent details, capabilities, and tenant-specific performance.
    """
    try:
        available_agents = []

        for agent_id, agent in coordinator.agents.items():
            # Check if agent can serve the tenant
            if not agent.can_serve_tenant(tenant_context):
                continue

            # Apply platform filter
            if platform and platform not in agent.supported_platforms:
                continue

            # Apply specialization filter
            if specialization and agent.specialization != specialization:
                continue

            # Get tenant-specific performance
            tenant_memory = agent.get_tenant_memory(tenant_context.tenant_id)

            agent_info = {
                "agent_id": agent_id,
                "name": agent.name,
                "specialization": agent.specialization.value,
                "capabilities": [cap.value for cap in agent.capabilities],
                "supported_platforms": [p.value for p in agent.supported_platforms],
                "tier_restrictions": [t.value for t in agent.tier_restrictions],
                "tenant_performance": {
                    "interaction_count": tenant_memory.interaction_count,
                    "success_rate": tenant_memory.success_rate,
                    "last_interaction": (
                        tenant_memory.last_interaction.isoformat()
                        if tenant_memory.last_interaction else None
                    )
                },
                "created_at": agent.created_at.isoformat(),
                "last_updated": agent.last_updated.isoformat()
            }

            available_agents.append(agent_info)

        logger.info(
            "Listed available agents",
            tenant_id=tenant_context.tenant_id,
            total_agents=len(available_agents),
            platform_filter=platform.value if platform else None,
            specialization_filter=specialization.value if specialization else None
        )

        return available_agents

    except Exception as e:
        logger.error(
            "Failed to list agents",
            tenant_id=tenant_context.tenant_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list agents: {str(e)}"
        )


@router.get("/agent/{agent_id}", response_model=Dict[str, Any])
async def get_agent_details(
    agent_id: str,
    http_request: Request,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    coordinator: TenantAwareAICoordinator = Depends(get_ai_coordinator)
):
    """
    Get detailed information about a specific AI agent

    Includes agent capabilities, tenant-specific performance,
    and interaction history summary.
    """
    try:
        agent = coordinator.agents.get(agent_id)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent {agent_id} not found"
            )

        if not agent.can_serve_tenant(tenant_context):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Agent not available for this tenant"
            )

        # Get comprehensive agent details
        tenant_memory = agent.get_tenant_memory(tenant_context.tenant_id)
        global_stats = coordinator.global_performance_stats.get(agent_id, {})

        agent_details = {
            "agent_id": agent_id,
            "name": agent.name,
            "specialization": agent.specialization.value,
            "capabilities": [cap.value for cap in agent.capabilities],
            "supported_platforms": [p.value for p in agent.supported_platforms],
            "tier_restrictions": [t.value for t in agent.tier_restrictions],
            "tenant_specific": {
                "interaction_count": tenant_memory.interaction_count,
                "success_rate": tenant_memory.success_rate,
                "performance_metrics": tenant_memory.performance_metrics,
                "learned_preferences": tenant_memory.learned_preferences,
                "last_interaction": (
                    tenant_memory.last_interaction.isoformat()
                    if tenant_memory.last_interaction else None
                )
            },
            "global_performance": {
                "total_executions": global_stats.get("total_executions", 0),
                "successful_executions": global_stats.get("successful_executions", 0),
                "average_execution_time": global_stats.get("average_execution_time", 0.0),
                "average_quality_score": global_stats.get("average_quality_score", 0.0)
            },
            "created_at": agent.created_at.isoformat(),
            "last_updated": agent.last_updated.isoformat()
        }

        return agent_details

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to get agent details",
            agent_id=agent_id,
            tenant_id=tenant_context.tenant_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get agent details: {str(e)}"
        )


# Utility functions
async def _analyze_message_for_specialization(
    message: str,
    platform: PlatformType
) -> Optional[AgentSpecialization]:
    """Analyze user message to suggest optimal agent specialization"""
    message_lower = message.lower()

    # Content creation keywords
    if any(keyword in message_lower for keyword in [
        "write", "create", "content", "blog", "article", "post", "copy"
    ]):
        return AgentSpecialization.CONTENT_CREATOR

    # SEO keywords
    if any(keyword in message_lower for keyword in [
        "seo", "optimize", "ranking", "keywords", "search"
    ]):
        return AgentSpecialization.SEO_OPTIMIZER

    # Social media keywords
    if any(keyword in message_lower for keyword in [
        "social", "instagram", "facebook", "twitter", "linkedin", "tiktok"
    ]):
        return AgentSpecialization.SOCIAL_MEDIA_MANAGER

    # Analytics keywords
    if any(keyword in message_lower for keyword in [
        "analyze", "data", "metrics", "report", "analytics", "performance"
    ]):
        return AgentSpecialization.DATA_ANALYST

    # E-commerce keywords (for CORELDOVE platform)
    if platform == PlatformType.CORELDOVE and any(keyword in message_lower for keyword in [
        "product", "price", "inventory", "order", "shop", "store"
    ]):
        return AgentSpecialization.PRODUCT_MANAGER

    # Trading keywords (for QUANTTRADE platform)
    if platform == PlatformType.QUANTTRADE and any(keyword in message_lower for keyword in [
        "trade", "portfolio", "stock", "market", "invest"
    ]):
        return AgentSpecialization.TRADING_ANALYST

    # Gaming keywords (for THRILLRING platform)
    if platform == PlatformType.THRILLRING and any(keyword in message_lower for keyword in [
        "game", "tournament", "player", "match", "competition"
    ]):
        return AgentSpecialization.GAME_CURATOR

    # Default to customer support for general queries
    return AgentSpecialization.CUSTOMER_SUPPORT


async def _generate_contextual_actions(
    platform: PlatformType,
    message: str,
    agent_specialization: AgentSpecialization
) -> List[Dict[str, Any]]:
    """Generate contextual actions based on platform and conversation"""
    actions = []

    # Platform-specific actions
    if platform == PlatformType.BIZOHOLIC:
        actions.extend([
            {
                "type": "create_campaign",
                "title": "Create New Campaign",
                "description": "Set up a new marketing campaign",
                "url": "/campaigns/create"
            },
            {
                "type": "analyze_leads",
                "title": "Analyze Leads",
                "description": "Review and score recent leads",
                "url": "/leads/analytics"
            }
        ])
    elif platform == PlatformType.CORELDOVE:
        actions.extend([
            {
                "type": "add_product",
                "title": "Add New Product",
                "description": "Add a product to your store",
                "url": "/products/add"
            },
            {
                "type": "view_orders",
                "title": "View Orders",
                "description": "Check recent orders and fulfillment",
                "url": "/orders"
            }
        ])
    elif platform == PlatformType.QUANTTRADE:
        actions.extend([
            {
                "type": "create_portfolio",
                "title": "Create Portfolio",
                "description": "Set up a new trading portfolio",
                "url": "/portfolios/create"
            },
            {
                "type": "view_trades",
                "title": "View Recent Trades",
                "description": "Review trading history and performance",
                "url": "/trades"
            }
        ])

    # Specialization-specific actions
    if agent_specialization == AgentSpecialization.CONTENT_CREATOR:
        actions.append({
            "type": "content_library",
            "title": "Browse Content Templates",
            "description": "Explore pre-built content templates",
            "url": "/content/templates"
        })
    elif agent_specialization == AgentSpecialization.DATA_ANALYST:
        actions.append({
            "type": "analytics_dashboard",
            "title": "View Analytics Dashboard",
            "description": "Access comprehensive analytics",
            "url": "/analytics"
        })

    return actions


async def _get_conversation_history(
    tenant_id: str,
    conversation_id: str,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """Get recent conversation history for context"""
    # Mock implementation - replace with actual database query
    return []


async def _store_conversation(
    tenant_id: str,
    conversation_id: str,
    platform: str,
    user_message: str,
    agent_response: str,
    agent_id: str
):
    """Store conversation in database (background task)"""
    try:
        # This would use the RLS manager to store conversation history
        # in the ai_conversation_history table
        pass
    except Exception as e:
        logger.error(
            "Failed to store conversation",
            tenant_id=tenant_id,
            conversation_id=conversation_id,
            error=str(e)
        )


async def _log_agent_usage(
    tenant_id: str,
    agent_id: str,
    platform: str,
    success: bool
):
    """Log agent usage for analytics (background task)"""
    try:
        # This would log usage statistics for billing and analytics
        pass
    except Exception as e:
        logger.error(
            "Failed to log agent usage",
            tenant_id=tenant_id,
            agent_id=agent_id,
            error=str(e)
        )


# Initialize coordinator (called from main app)
def initialize_ai_coordinator(rls_manager, vector_store=None):
    """Initialize the global AI coordinator instance"""
    global ai_coordinator
    ai_coordinator = TenantAwareAICoordinator(
        rls_manager=rls_manager,
        vector_store=vector_store,
        enable_cross_tenant_learning=True
    )
    logger.info("AI Coordinator initialized with 93+ agents")