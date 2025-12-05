"""
FastAPI Endpoints for Platform-Specific AI Marketing
Provides specialized AI marketing automation for each platform's unique business model
"""

from typing import Dict, Any, List, Optional
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
    require_bizoholic_access,
    require_coreldove_access,
    require_directory_access,
    require_thrillring_access,
    require_quanttrade_access
)
from .platform_specific_ai_marketing import (
    PlatformSpecificAIMarketing,
    MarketingCampaignType,
    PlatformMarketingStrategy
)

import structlog

logger = structlog.get_logger(__name__)

# Initialize router
router = APIRouter(prefix="/api/brain/platform-marketing", tags=["Platform Marketing"])


# Request/Response Models
class CreateStrategyRequest(BaseModel):
    """Request model for creating platform marketing strategy"""
    campaign_type: MarketingCampaignType = Field(..., description="Type of marketing campaign")
    strategy_config: Dict[str, Any] = Field(default_factory=dict, description="Strategy configuration")
    target_metrics: Optional[Dict[str, float]] = Field(None, description="Custom target metrics")
    automation_frequency: str = Field("daily", description="Automation frequency: hourly, daily, weekly")


class CreateStrategyResponse(BaseModel):
    """Response model for strategy creation"""
    success: bool
    strategy_id: str
    platform: str
    campaign_type: str
    target_metrics: Dict[str, float]
    ai_agents_assigned: List[str]
    created_at: str
    message: str


class ExecuteAutomationRequest(BaseModel):
    """Request model for executing marketing automation"""
    strategy_id: str = Field(..., description="Strategy ID to execute")
    force_execution: bool = Field(False, description="Force execution even if not scheduled")


class ExecuteAutomationResponse(BaseModel):
    """Response model for automation execution"""
    success: bool
    strategy_id: str
    platform: str
    actions_executed: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    execution_time: str
    message: str
    error: Optional[str] = None


class OptimizationResponse(BaseModel):
    """Response model for platform optimization"""
    success: bool
    platform: str
    total_strategies: int
    successful_optimizations: int
    optimizations: List[Dict[str, Any]]
    generated_at: str


class InsightsResponse(BaseModel):
    """Response model for platform insights"""
    platform: str
    time_range_days: int
    insights: List[str]
    metrics_data: Dict[str, Any]
    generated_at: str


# Global marketing engine instance
platform_marketing: Optional[PlatformSpecificAIMarketing] = None


def get_platform_marketing() -> PlatformSpecificAIMarketing:
    """Get the global platform marketing instance"""
    if platform_marketing is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Platform marketing engine not initialized"
        )
    return platform_marketing


# ========================================================================================
# BIZOHOLIC MARKETING ENDPOINTS
# ========================================================================================

@router.post("/bizoholic/strategy", response_model=CreateStrategyResponse)
async def create_bizoholic_strategy(
    request: CreateStrategyRequest,
    http_request: Request,
    background_tasks: BackgroundTasks,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    _: None = Depends(require_bizoholic_access),
    marketing_engine: PlatformSpecificAIMarketing = Depends(get_platform_marketing)
):
    """
    Create AI marketing strategy for Bizoholic marketing agency platform

    Specializes in:
    - Lead generation and scoring optimization
    - Content marketing automation
    - SEO and PPC campaign management
    - Client onboarding workflows
    """
    try:
        strategy = await marketing_engine.create_platform_strategy(
            tenant_context,
            PlatformType.BIZOHOLIC,
            request.campaign_type,
            request.strategy_config
        )

        background_tasks.add_task(
            _log_strategy_creation,
            tenant_context.tenant_id,
            strategy.strategy_id,
            "bizoholic",
            request.campaign_type.value
        )

        return CreateStrategyResponse(
            success=True,
            strategy_id=strategy.strategy_id,
            platform=strategy.platform.value,
            campaign_type=strategy.campaign_type.value,
            target_metrics=strategy.target_metrics,
            ai_agents_assigned=strategy.ai_agents_assigned,
            created_at=strategy.created_at.isoformat(),
            message=f"Bizoholic {request.campaign_type.value} strategy created successfully"
        )

    except Exception as e:
        logger.error(
            "Failed to create Bizoholic strategy",
            tenant_id=tenant_context.tenant_id,
            campaign_type=request.campaign_type.value,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create strategy: {str(e)}"
        )


@router.post("/bizoholic/execute/{strategy_id}", response_model=ExecuteAutomationResponse)
async def execute_bizoholic_automation(
    strategy_id: str,
    request: ExecuteAutomationRequest,
    http_request: Request,
    background_tasks: BackgroundTasks,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    _: None = Depends(require_bizoholic_access),
    marketing_engine: PlatformSpecificAIMarketing = Depends(get_platform_marketing)
):
    """
    Execute automated marketing actions for Bizoholic strategy

    Actions include:
    - Lead scoring optimization using AI
    - Content generation for campaigns
    - SEO optimization recommendations
    - Campaign performance optimization
    """
    try:
        result = await marketing_engine.execute_automated_marketing(
            tenant_context,
            strategy_id
        )

        background_tasks.add_task(
            _log_automation_execution,
            tenant_context.tenant_id,
            strategy_id,
            "bizoholic",
            result.get("success", False)
        )

        return ExecuteAutomationResponse(
            success=result["success"],
            strategy_id=strategy_id,
            platform="bizoholic",
            actions_executed=result.get("actions", []),
            metrics=result.get("metrics", {}),
            execution_time=result.get("execution_time", datetime.utcnow().isoformat()),
            message="Bizoholic marketing automation executed successfully" if result["success"] else "Automation execution failed",
            error=result.get("error")
        )

    except Exception as e:
        logger.error(
            "Failed to execute Bizoholic automation",
            tenant_id=tenant_context.tenant_id,
            strategy_id=strategy_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute automation: {str(e)}"
        )


@router.post("/bizoholic/optimize", response_model=OptimizationResponse)
async def optimize_bizoholic_performance(
    http_request: Request,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    _: None = Depends(require_bizoholic_access),
    marketing_engine: PlatformSpecificAIMarketing = Depends(get_platform_marketing)
):
    """
    Optimize all Bizoholic marketing strategies for maximum performance

    Optimization includes:
    - Lead conversion rate improvements
    - Campaign ROI optimization
    - Content performance enhancement
    - SEO ranking improvements
    """
    try:
        result = await marketing_engine.optimize_platform_performance(
            tenant_context,
            PlatformType.BIZOHOLIC
        )

        return OptimizationResponse(
            success=result["success"],
            platform=result["platform"],
            total_strategies=result["total_strategies"],
            successful_optimizations=result["successful_optimizations"],
            optimizations=result["optimizations"],
            generated_at=datetime.utcnow().isoformat()
        )

    except Exception as e:
        logger.error(
            "Failed to optimize Bizoholic performance",
            tenant_id=tenant_context.tenant_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to optimize performance: {str(e)}"
        )


@router.get("/bizoholic/insights", response_model=InsightsResponse)
async def get_bizoholic_insights(
    http_request: Request,
    time_range_days: int = 30,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    _: None = Depends(require_bizoholic_access),
    marketing_engine: PlatformSpecificAIMarketing = Depends(get_platform_marketing)
):
    """
    Get AI-powered insights for Bizoholic marketing performance

    Insights include:
    - Lead generation trends and patterns
    - Campaign performance analytics
    - Content effectiveness metrics
    - SEO performance tracking
    """
    try:
        insights = await marketing_engine.get_platform_insights(
            tenant_context,
            PlatformType.BIZOHOLIC,
            time_range_days
        )

        return InsightsResponse(
            platform=insights["platform"],
            time_range_days=insights["time_range_days"],
            insights=insights["insights"],
            metrics_data={
                "leads_trend": insights.get("leads_trend", []),
                "campaign_breakdown": insights.get("campaign_breakdown", [])
            },
            generated_at=insights["generated_at"]
        )

    except Exception as e:
        logger.error(
            "Failed to get Bizoholic insights",
            tenant_id=tenant_context.tenant_id,
            time_range_days=time_range_days,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get insights: {str(e)}"
        )


# ========================================================================================
# CORELDOVE E-COMMERCE ENDPOINTS
# ========================================================================================

@router.post("/coreldove/strategy", response_model=CreateStrategyResponse)
async def create_coreldove_strategy(
    request: CreateStrategyRequest,
    http_request: Request,
    background_tasks: BackgroundTasks,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    _: None = Depends(require_coreldove_access),
    marketing_engine: PlatformSpecificAIMarketing = Depends(get_platform_marketing)
):
    """
    Create AI marketing strategy for CoreLDove e-commerce platform

    Specializes in:
    - Product launch campaigns
    - Dynamic pricing optimization
    - Inventory management automation
    - Abandoned cart recovery
    """
    try:
        strategy = await marketing_engine.create_platform_strategy(
            tenant_context,
            PlatformType.CORELDOVE,
            request.campaign_type,
            request.strategy_config
        )

        background_tasks.add_task(
            _log_strategy_creation,
            tenant_context.tenant_id,
            strategy.strategy_id,
            "coreldove",
            request.campaign_type.value
        )

        return CreateStrategyResponse(
            success=True,
            strategy_id=strategy.strategy_id,
            platform=strategy.platform.value,
            campaign_type=strategy.campaign_type.value,
            target_metrics=strategy.target_metrics,
            ai_agents_assigned=strategy.ai_agents_assigned,
            created_at=strategy.created_at.isoformat(),
            message=f"CoreLDove {request.campaign_type.value} strategy created successfully"
        )

    except Exception as e:
        logger.error(
            "Failed to create CoreLDove strategy",
            tenant_id=tenant_context.tenant_id,
            campaign_type=request.campaign_type.value,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create strategy: {str(e)}"
        )


@router.post("/coreldove/execute/{strategy_id}", response_model=ExecuteAutomationResponse)
async def execute_coreldove_automation(
    strategy_id: str,
    request: ExecuteAutomationRequest,
    http_request: Request,
    background_tasks: BackgroundTasks,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    _: None = Depends(require_coreldove_access),
    marketing_engine: PlatformSpecificAIMarketing = Depends(get_platform_marketing)
):
    """
    Execute automated e-commerce marketing for CoreLDove

    Actions include:
    - Product description optimization
    - Dynamic pricing adjustments
    - Inventory level optimization
    - Cross-sell and upsell campaigns
    """
    try:
        result = await marketing_engine.execute_automated_marketing(
            tenant_context,
            strategy_id
        )

        background_tasks.add_task(
            _log_automation_execution,
            tenant_context.tenant_id,
            strategy_id,
            "coreldove",
            result.get("success", False)
        )

        return ExecuteAutomationResponse(
            success=result["success"],
            strategy_id=strategy_id,
            platform="coreldove",
            actions_executed=result.get("actions", []),
            metrics=result.get("metrics", {}),
            execution_time=result.get("execution_time", datetime.utcnow().isoformat()),
            message="CoreLDove e-commerce automation executed successfully" if result["success"] else "Automation execution failed",
            error=result.get("error")
        )

    except Exception as e:
        logger.error(
            "Failed to execute CoreLDove automation",
            tenant_id=tenant_context.tenant_id,
            strategy_id=strategy_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute automation: {str(e)}"
        )


@router.get("/coreldove/insights", response_model=InsightsResponse)
async def get_coreldove_insights(
    http_request: Request,
    time_range_days: int = 30,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    _: None = Depends(require_coreldove_access),
    marketing_engine: PlatformSpecificAIMarketing = Depends(get_platform_marketing)
):
    """
    Get AI-powered e-commerce insights for CoreLDove

    Insights include:
    - Product performance analytics
    - Revenue trends and forecasting
    - Customer behavior patterns
    - Inventory optimization recommendations
    """
    try:
        insights = await marketing_engine.get_platform_insights(
            tenant_context,
            PlatformType.CORELDOVE,
            time_range_days
        )

        return InsightsResponse(
            platform=insights["platform"],
            time_range_days=insights["time_range_days"],
            insights=insights["insights"],
            metrics_data={
                "product_breakdown": insights.get("product_breakdown", []),
                "revenue_trend": insights.get("revenue_trend", []),
                "total_revenue": insights.get("total_revenue", 0)
            },
            generated_at=insights["generated_at"]
        )

    except Exception as e:
        logger.error(
            "Failed to get CoreLDove insights",
            tenant_id=tenant_context.tenant_id,
            time_range_days=time_range_days,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get insights: {str(e)}"
        )


# ========================================================================================
# BUSINESS DIRECTORY ENDPOINTS
# ========================================================================================

@router.post("/business-directory/strategy", response_model=CreateStrategyResponse)
async def create_directory_strategy(
    request: CreateStrategyRequest,
    http_request: Request,
    background_tasks: BackgroundTasks,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    _: None = Depends(require_directory_access),
    marketing_engine: PlatformSpecificAIMarketing = Depends(get_platform_marketing)
):
    """
    Create AI marketing strategy for Business Directory platform

    Specializes in:
    - Local SEO optimization
    - Business listing enhancement
    - Review generation campaigns
    - Directory curation automation
    """
    try:
        strategy = await marketing_engine.create_platform_strategy(
            tenant_context,
            PlatformType.BUSINESS_DIRECTORY,
            request.campaign_type,
            request.strategy_config
        )

        return CreateStrategyResponse(
            success=True,
            strategy_id=strategy.strategy_id,
            platform=strategy.platform.value,
            campaign_type=strategy.campaign_type.value,
            target_metrics=strategy.target_metrics,
            ai_agents_assigned=strategy.ai_agents_assigned,
            created_at=strategy.created_at.isoformat(),
            message=f"Business Directory {request.campaign_type.value} strategy created successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create strategy: {str(e)}"
        )


# ========================================================================================
# THRILLRING GAMING ENDPOINTS
# ========================================================================================

@router.post("/thrillring/strategy", response_model=CreateStrategyResponse)
async def create_thrillring_strategy(
    request: CreateStrategyRequest,
    http_request: Request,
    background_tasks: BackgroundTasks,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    _: None = Depends(require_thrillring_access),
    marketing_engine: PlatformSpecificAIMarketing = Depends(get_platform_marketing)
):
    """
    Create AI marketing strategy for ThrillRing gaming platform

    Specializes in:
    - Tournament promotion campaigns
    - Game discovery optimization
    - Community engagement automation
    - Player retention strategies
    """
    try:
        strategy = await marketing_engine.create_platform_strategy(
            tenant_context,
            PlatformType.THRILLRING,
            request.campaign_type,
            request.strategy_config
        )

        return CreateStrategyResponse(
            success=True,
            strategy_id=strategy.strategy_id,
            platform=strategy.platform.value,
            campaign_type=strategy.campaign_type.value,
            target_metrics=strategy.target_metrics,
            ai_agents_assigned=strategy.ai_agents_assigned,
            created_at=strategy.created_at.isoformat(),
            message=f"ThrillRing {request.campaign_type.value} strategy created successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create strategy: {str(e)}"
        )


# ========================================================================================
# QUANTTRADE FINANCIAL ENDPOINTS
# ========================================================================================

@router.post("/quanttrade/strategy", response_model=CreateStrategyResponse)
async def create_quanttrade_strategy(
    request: CreateStrategyRequest,
    http_request: Request,
    background_tasks: BackgroundTasks,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    _: None = Depends(require_quanttrade_access),
    marketing_engine: PlatformSpecificAIMarketing = Depends(get_platform_marketing)
):
    """
    Create AI marketing strategy for QuantTrade financial platform

    Specializes in:
    - Trading education campaigns
    - Risk awareness automation
    - Portfolio optimization strategies
    - Client onboarding workflows
    """
    try:
        strategy = await marketing_engine.create_platform_strategy(
            tenant_context,
            PlatformType.QUANTTRADE,
            request.campaign_type,
            request.strategy_config
        )

        return CreateStrategyResponse(
            success=True,
            strategy_id=strategy.strategy_id,
            platform=strategy.platform.value,
            campaign_type=strategy.campaign_type.value,
            target_metrics=strategy.target_metrics,
            ai_agents_assigned=strategy.ai_agents_assigned,
            created_at=strategy.created_at.isoformat(),
            message=f"QuantTrade {request.campaign_type.value} strategy created successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create strategy: {str(e)}"
        )


# ========================================================================================
# CROSS-PLATFORM ENDPOINTS
# ========================================================================================

@router.get("/strategies/list", response_model=List[Dict[str, Any]])
async def list_tenant_strategies(
    http_request: Request,
    platform: Optional[PlatformType] = None,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    marketing_engine: PlatformSpecificAIMarketing = Depends(get_platform_marketing)
):
    """
    List all marketing strategies for the tenant across platforms

    Optionally filter by specific platform
    """
    try:
        tenant_strategies = marketing_engine.active_strategies.get(tenant_context.tenant_id, {})

        strategies_list = []
        for strategy_id, strategy in tenant_strategies.items():
            if platform and strategy.platform != platform:
                continue

            strategies_list.append({
                "strategy_id": strategy.strategy_id,
                "platform": strategy.platform.value,
                "campaign_type": strategy.campaign_type.value,
                "created_at": strategy.created_at.isoformat(),
                "last_optimized": strategy.last_optimized.isoformat() if strategy.last_optimized else None,
                "ai_agents_assigned": len(strategy.ai_agents_assigned),
                "performance_history_count": len(strategy.performance_history),
                "target_metrics": strategy.target_metrics
            })

        return strategies_list

    except Exception as e:
        logger.error(
            "Failed to list tenant strategies",
            tenant_id=tenant_context.tenant_id,
            platform=platform.value if platform else None,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list strategies: {str(e)}"
        )


@router.get("/performance/dashboard", response_model=Dict[str, Any])
async def get_marketing_dashboard(
    http_request: Request,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    marketing_engine: PlatformSpecificAIMarketing = Depends(get_platform_marketing)
):
    """
    Get comprehensive marketing performance dashboard across all platforms

    Provides unified view of:
    - Cross-platform marketing performance
    - AI agent utilization
    - Strategy effectiveness
    - ROI and conversion metrics
    """
    try:
        dashboard_data = {
            "tenant_id": tenant_context.tenant_id,
            "platforms": {},
            "overall_stats": {
                "total_strategies": 0,
                "active_automations": 0,
                "successful_executions": 0,
                "total_ai_agents": 0
            },
            "recent_activity": [],
            "top_performing_strategies": [],
            "generated_at": datetime.utcnow().isoformat()
        }

        tenant_strategies = marketing_engine.active_strategies.get(tenant_context.tenant_id, {})

        # Calculate overall statistics
        for strategy in tenant_strategies.values():
            dashboard_data["overall_stats"]["total_strategies"] += 1
            dashboard_data["overall_stats"]["total_ai_agents"] += len(strategy.ai_agents_assigned)

            # Platform-specific stats
            platform_key = strategy.platform.value
            if platform_key not in dashboard_data["platforms"]:
                dashboard_data["platforms"][platform_key] = {
                    "strategies": 0,
                    "automations": 0,
                    "performance": []
                }

            dashboard_data["platforms"][platform_key]["strategies"] += 1
            dashboard_data["platforms"][platform_key]["performance"].extend(
                strategy.performance_history[-5:]  # Last 5 executions
            )

        return dashboard_data

    except Exception as e:
        logger.error(
            "Failed to generate marketing dashboard",
            tenant_id=tenant_context.tenant_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate dashboard: {str(e)}"
        )


# ========================================================================================
# UTILITY FUNCTIONS
# ========================================================================================

async def _log_strategy_creation(
    tenant_id: str,
    strategy_id: str,
    platform: str,
    campaign_type: str
):
    """Log strategy creation for analytics"""
    try:
        # This would log to analytics database
        logger.info(
            "Marketing strategy created",
            tenant_id=tenant_id,
            strategy_id=strategy_id,
            platform=platform,
            campaign_type=campaign_type
        )
    except Exception as e:
        logger.error("Failed to log strategy creation", error=str(e))


async def _log_automation_execution(
    tenant_id: str,
    strategy_id: str,
    platform: str,
    success: bool
):
    """Log automation execution for analytics"""
    try:
        # This would log to analytics database
        logger.info(
            "Marketing automation executed",
            tenant_id=tenant_id,
            strategy_id=strategy_id,
            platform=platform,
            success=success
        )
    except Exception as e:
        logger.error("Failed to log automation execution", error=str(e))


# Initialize platform marketing (called from main app)
def initialize_platform_marketing(ai_coordinator, rls_manager):
    """Initialize the global platform marketing instance"""
    global platform_marketing
    platform_marketing = PlatformSpecificAIMarketing(
        ai_coordinator=ai_coordinator,
        rls_manager=rls_manager
    )
    logger.info("Platform-specific AI marketing initialized for all 5 platforms")