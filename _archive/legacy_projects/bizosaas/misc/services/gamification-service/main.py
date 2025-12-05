"""
BizOSaaS Gamification Service
FastAPI service implementing ThrillRing-inspired gamification features
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import uuid

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
import structlog

# Import gamification agents
import sys
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas')

from services.ai_agents.agents.gamification_agents import (
    GamificationOrchestrationAgent,
    ReferralSystemAgent
)
from services.ai_agents.agents.base_agent import AgentTaskRequest, TaskStatus, TaskPriority

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

# FastAPI app configuration
app = FastAPI(
    title="BizOSaaS Gamification Service",
    description="Gamification features for client engagement and retention across Bizoholic, CoreLDove, and BizOSaaS platforms",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# =============================================
# PYDANTIC MODELS
# =============================================

class ReferralCodeRequest(BaseModel):
    tenant_id: str
    program_type: str = "standard"
    custom_rewards: Optional[Dict[str, Any]] = None
    expiry_days: Optional[int] = 365
    base_url: Optional[str] = "https://bizosaas.com"
    
    @validator('program_type')
    def validate_program_type(cls, v):
        allowed = ['standard', 'premium', 'enterprise', 'custom']
        if v not in allowed:
            raise ValueError(f'program_type must be one of: {allowed}')
        return v

class ReferralCodeResponse(BaseModel):
    referral_code: str
    tracking_url: str
    share_templates: Dict[str, str]
    reward_structure: Dict[str, Any]
    analytics_dashboard_url: str
    expires_at: str

class ReferralConversionRequest(BaseModel):
    referral_code: str
    conversion_type: str = "signup"
    conversion_value: float = 0.0
    referee_email: Optional[str] = None
    referee_metadata: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    device_fingerprint: Optional[str] = None
    
    @validator('conversion_type')
    def validate_conversion_type(cls, v):
        allowed = ['signup', 'subscription', 'purchase', 'trial_start', 'upgrade']
        if v not in allowed:
            raise ValueError(f'conversion_type must be one of: {allowed}')
        return v

class AchievementProgressRequest(BaseModel):
    tenant_id: str
    platform: str = "bizoholic"
    force_refresh: bool = False
    
    @validator('platform')
    def validate_platform(cls, v):
        allowed = ['bizoholic', 'coreldove', 'bizosaas']
        if v not in allowed:
            raise ValueError(f'platform must be one of: {allowed}')
        return v

class AchievementProgressResponse(BaseModel):
    unlocked_achievements: List[Dict[str, Any]]
    updated_progress: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    engagement_score: float
    cross_client_insights_count: int

class CustomAchievementRequest(BaseModel):
    tenant_id: str
    achievement_name: str
    description: str
    platform: str = "bizoholic"
    achievement_type: str = "custom"
    trigger_conditions: Dict[str, Any]
    reward_config: Dict[str, Any]
    difficulty_level: int = Field(default=1, ge=1, le=5)
    is_repeatable: bool = False
    
    @validator('achievement_type')
    def validate_achievement_type(cls, v):
        allowed = ['milestone', 'performance', 'social', 'custom', 'streak']
        if v not in allowed:
            raise ValueError(f'achievement_type must be one of: {allowed}')
        return v

class LeaderboardRequest(BaseModel):
    platform: str = "bizoholic"
    leaderboard_type: str = "performance"
    time_period: str = "monthly"
    limit: int = Field(default=50, ge=1, le=100)
    include_user_position: bool = True
    
    @validator('leaderboard_type')
    def validate_leaderboard_type(cls, v):
        allowed = ['performance', 'growth', 'engagement', 'innovation', 'global']
        if v not in allowed:
            raise ValueError(f'leaderboard_type must be one of: {allowed}')
        return v
    
    @validator('time_period')
    def validate_time_period(cls, v):
        allowed = ['daily', 'weekly', 'monthly', 'quarterly', 'all_time']
        if v not in allowed:
            raise ValueError(f'time_period must be one of: {allowed}')
        return v

class LeaderboardResponse(BaseModel):
    leaderboard_data: List[Dict[str, Any]]
    user_position: Optional[Dict[str, Any]]
    leaderboard_metadata: Dict[str, Any]
    competitive_insights: List[Dict[str, Any]]
    next_update: str

class PortfolioShowcaseRequest(BaseModel):
    tenant_id: str
    platform: str = "bizoholic"
    showcase_type: str = "comprehensive"
    include_testimonials: bool = True
    seo_optimize: bool = True
    custom_branding: Optional[Dict[str, Any]] = None
    
    @validator('showcase_type')
    def validate_showcase_type(cls, v):
        allowed = ['basic', 'comprehensive', 'premium', 'custom']
        if v not in allowed:
            raise ValueError(f'showcase_type must be one of: {allowed}')
        return v

class PortfolioShowcaseResponse(BaseModel):
    portfolio_id: str
    portfolio_url: str
    featured_metrics: List[Dict[str, Any]]
    case_studies: List[Dict[str, Any]]
    social_templates: List[Dict[str, Any]]
    estimated_impact: Dict[str, Any]
    optimization_suggestions: List[Dict[str, Any]]

class GamificationAnalyticsRequest(BaseModel):
    tenant_id: str
    time_period: str = "30d"
    metrics: str = "all"
    include_predictions: bool = True
    
    @validator('time_period')
    def validate_time_period(cls, v):
        allowed = ['7d', '30d', '90d', '1y', 'all_time']
        if v not in allowed:
            raise ValueError(f'time_period must be one of: {allowed}')
        return v

# =============================================
# AUTHENTICATION AND AUTHORIZATION
# =============================================

def extract_user_id_from_token(token: str) -> str:
    """Extract user ID from JWT token"""
    # This would implement actual JWT token parsing
    # For now, return a placeholder
    return "user_" + str(uuid.uuid4())[:8]

def extract_tenant_id_from_token(token: str) -> str:
    """Extract tenant ID from JWT token"""
    # This would implement actual JWT token parsing
    # For now, return a placeholder
    return "tenant_" + str(uuid.uuid4())[:8]

async def verify_tenant_access(tenant_id: str, token: str) -> bool:
    """Verify that the user has access to the specified tenant"""
    # This would implement actual tenant access verification
    # For now, return True for development
    return True

# =============================================
# REFERRAL SYSTEM ENDPOINTS
# =============================================

@app.post("/api/v1/referrals/generate-code", response_model=ReferralCodeResponse)
async def generate_referral_code(
    request: ReferralCodeRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Generate a new referral code with custom rewards configuration"""
    
    try:
        # Verify tenant access
        if not await verify_tenant_access(request.tenant_id, credentials.credentials):
            raise HTTPException(status_code=403, detail="Access denied to tenant")
        
        # Create agent task request
        task_request = AgentTaskRequest(
            tenant_id=request.tenant_id,
            user_id=extract_user_id_from_token(credentials.credentials),
            task_type="generate_referral_code",
            input_data=request.dict(),
            priority=TaskPriority.NORMAL
        )
        
        # Execute through ReferralSystemAgent
        agent = ReferralSystemAgent()
        await agent.initialize()
        result = await agent.execute_task(task_request)
        
        if result.status == TaskStatus.FAILED:
            logger.error("Referral code generation failed", error=result.error_message)
            raise HTTPException(status_code=500, detail=result.error_message)
        
        logger.info("Referral code generated successfully", 
                   tenant_id=request.tenant_id, 
                   code=result.result.get("referral_code"))
        
        return ReferralCodeResponse(**result.result)
    
    except Exception as e:
        logger.error("Unexpected error in referral code generation", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/v1/referrals/track-conversion")
async def track_referral_conversion(
    request: ReferralConversionRequest,
    background_tasks: BackgroundTasks,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Track a referral conversion with AI fraud detection"""
    
    try:
        # Add conversion processing to background tasks for immediate response
        background_tasks.add_task(
            process_referral_conversion_async,
            request.dict(),
            credentials.credentials
        )
        
        logger.info("Referral conversion tracking initiated", 
                   referral_code=request.referral_code, 
                   conversion_type=request.conversion_type)
        
        return {
            "status": "processing",
            "message": "Referral conversion is being processed",
            "tracking_id": str(uuid.uuid4()),
            "estimated_processing_time": "2-5 minutes"
        }
    
    except Exception as e:
        logger.error("Error initiating referral conversion tracking", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to initiate conversion tracking")

@app.get("/api/v1/referrals/{referral_code}/analytics")
async def get_referral_analytics(
    referral_code: str,
    time_period: str = Query("30d", regex="^(7d|30d|90d|1y|all_time)$"),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get analytics for a specific referral code"""
    
    try:
        # Mock analytics data (would be fetched from database)
        analytics_data = {
            "referral_code": referral_code,
            "total_clicks": 156,
            "total_conversions": 23,
            "conversion_rate": 14.7,
            "total_revenue_generated": 2340.50,
            "total_rewards_paid": 234.05,
            "roi": 900.2,
            "top_conversion_sources": [
                {"source": "twitter", "conversions": 8},
                {"source": "email", "conversions": 6},
                {"source": "direct", "conversions": 9}
            ],
            "conversion_timeline": [],  # Would contain daily/weekly data
            "geographic_distribution": {},
            "device_breakdown": {},
            "fraud_prevention_stats": {
                "total_attempts": 45,
                "blocked_attempts": 3,
                "false_positive_rate": 0.02
            }
        }
        
        return analytics_data
    
    except Exception as e:
        logger.error("Error fetching referral analytics", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch analytics")

# =============================================
# ACHIEVEMENT SYSTEM ENDPOINTS
# =============================================

@app.get("/api/v1/achievements/progress/{tenant_id}", response_model=AchievementProgressResponse)
async def get_achievement_progress(
    tenant_id: str,
    platform: str = Query("bizoholic", regex="^(bizoholic|coreldove|bizosaas)$"),
    force_refresh: bool = Query(False),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get current achievement progress for a tenant"""
    
    try:
        # Verify tenant access
        if not await verify_tenant_access(tenant_id, credentials.credentials):
            raise HTTPException(status_code=403, detail="Access denied to tenant")
        
        task_request = AgentTaskRequest(
            tenant_id=tenant_id,
            user_id=extract_user_id_from_token(credentials.credentials),
            task_type="check_achievements",
            input_data={
                "tenant_id": tenant_id,
                "platform": platform,
                "force_refresh": force_refresh
            }
        )
        
        agent = GamificationOrchestrationAgent()
        await agent.initialize()
        result = await agent.execute_task(task_request)
        
        if result.status == TaskStatus.FAILED:
            logger.error("Achievement progress check failed", error=result.error_message)
            raise HTTPException(status_code=500, detail=result.error_message)
        
        logger.info("Achievement progress retrieved successfully", 
                   tenant_id=tenant_id, 
                   unlocked_count=len(result.result.get("unlocked_achievements", [])))
        
        return AchievementProgressResponse(
            unlocked_achievements=result.result.get("unlocked_achievements", []),
            updated_progress=result.result.get("updated_progress", []),
            recommendations=result.result.get("recommendations", []),
            engagement_score=result.result.get("engagement_score", 0.0),
            cross_client_insights_count=result.result.get("cross_client_insights", 0)
        )
    
    except Exception as e:
        logger.error("Error fetching achievement progress", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch achievement progress")

@app.post("/api/v1/achievements/custom")
async def create_custom_achievement(
    request: CustomAchievementRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a custom achievement for a tenant"""
    
    try:
        # Verify tenant access
        if not await verify_tenant_access(request.tenant_id, credentials.credentials):
            raise HTTPException(status_code=403, detail="Access denied to tenant")
        
        task_request = AgentTaskRequest(
            tenant_id=request.tenant_id,
            user_id=extract_user_id_from_token(credentials.credentials),
            task_type="create_custom_achievement",
            input_data=request.dict()
        )
        
        agent = GamificationOrchestrationAgent()
        await agent.initialize()
        result = await agent.execute_task(task_request)
        
        if result.status == TaskStatus.FAILED:
            logger.error("Custom achievement creation failed", error=result.error_message)
            raise HTTPException(status_code=500, detail=result.error_message)
        
        logger.info("Custom achievement created successfully", 
                   tenant_id=request.tenant_id, 
                   achievement_name=request.achievement_name)
        
        return result.result
    
    except Exception as e:
        logger.error("Error creating custom achievement", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to create custom achievement")

# =============================================
# LEADERBOARD SYSTEM ENDPOINTS
# =============================================

@app.get("/api/v1/leaderboards", response_model=LeaderboardResponse)
async def get_leaderboards(
    platform: str = Query("bizoholic", regex="^(bizoholic|coreldove|bizosaas)$"),
    leaderboard_type: str = Query("performance", regex="^(performance|growth|engagement|innovation|global)$"),
    time_period: str = Query("monthly", regex="^(daily|weekly|monthly|quarterly|all_time)$"),
    limit: int = Query(50, ge=1, le=100),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get leaderboard rankings with user position"""
    
    try:
        user_id = extract_user_id_from_token(credentials.credentials)
        
        task_request = AgentTaskRequest(
            tenant_id="system",  # System-level task
            user_id=user_id,
            task_type="get_leaderboard_rankings",
            input_data={
                "platform": platform,
                "leaderboard_type": leaderboard_type,
                "time_period": time_period,
                "limit": limit,
                "user_id": user_id
            }
        )
        
        agent = GamificationOrchestrationAgent()
        await agent.initialize()
        result = await agent.execute_task(task_request)
        
        if result.status == TaskStatus.FAILED:
            logger.error("Leaderboard retrieval failed", error=result.error_message)
            raise HTTPException(status_code=500, detail=result.error_message)
        
        logger.info("Leaderboard data retrieved successfully", 
                   platform=platform, 
                   leaderboard_type=leaderboard_type)
        
        return LeaderboardResponse(
            leaderboard_data=result.result.get("leaderboard_data", []),
            user_position=result.result.get("user_position"),
            leaderboard_metadata=result.result.get("metadata", {}),
            competitive_insights=result.result.get("competitive_insights", []),
            next_update=(datetime.now() + timedelta(hours=24)).isoformat()
        )
    
    except Exception as e:
        logger.error("Error fetching leaderboard data", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch leaderboard data")

# =============================================
# PORTFOLIO SHOWCASE ENDPOINTS
# =============================================

@app.post("/api/v1/portfolio/generate", response_model=PortfolioShowcaseResponse)
async def generate_portfolio_showcase(
    request: PortfolioShowcaseRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Generate AI-powered portfolio showcase"""
    
    try:
        # Verify tenant access
        if not await verify_tenant_access(request.tenant_id, credentials.credentials):
            raise HTTPException(status_code=403, detail="Access denied to tenant")
        
        task_request = AgentTaskRequest(
            tenant_id=request.tenant_id,
            user_id=extract_user_id_from_token(credentials.credentials),
            task_type="generate_showcase",
            input_data=request.dict(),
            priority=TaskPriority.HIGH  # Portfolio generation is high priority
        )
        
        agent = GamificationOrchestrationAgent()
        await agent.initialize()
        result = await agent.execute_task(task_request)
        
        if result.status == TaskStatus.FAILED:
            logger.error("Portfolio showcase generation failed", error=result.error_message)
            raise HTTPException(status_code=500, detail=result.error_message)
        
        logger.info("Portfolio showcase generated successfully", 
                   tenant_id=request.tenant_id, 
                   portfolio_id=result.result.get("portfolio_data", {}).get("portfolio_id"))
        
        portfolio_data = result.result.get("portfolio_data", {})
        
        return PortfolioShowcaseResponse(
            portfolio_id=portfolio_data.get("portfolio_id"),
            portfolio_url=portfolio_data.get("portfolio_url"),
            featured_metrics=portfolio_data.get("featured_metrics", []),
            case_studies=portfolio_data.get("case_studies", []),
            social_templates=portfolio_data.get("social_templates", []),
            estimated_impact=result.result.get("estimated_impact", {}),
            optimization_suggestions=result.result.get("optimization_suggestions", [])
        )
    
    except Exception as e:
        logger.error("Error generating portfolio showcase", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate portfolio showcase")

# =============================================
# ANALYTICS AND REPORTING ENDPOINTS
# =============================================

@app.get("/api/v1/analytics/gamification/{tenant_id}")
async def get_gamification_analytics(
    tenant_id: str,
    time_period: str = Query("30d", regex="^(7d|30d|90d|1y|all_time)$"),
    metrics: str = Query("all"),
    include_predictions: bool = Query(True),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get comprehensive gamification analytics"""
    
    try:
        # Verify tenant access
        if not await verify_tenant_access(tenant_id, credentials.credentials):
            raise HTTPException(status_code=403, detail="Access denied to tenant")
        
        task_request = AgentTaskRequest(
            tenant_id=tenant_id,
            user_id=extract_user_id_from_token(credentials.credentials),
            task_type="gamification_analytics",
            input_data={
                "tenant_id": tenant_id,
                "time_period": time_period,
                "metrics": metrics,
                "include_predictions": include_predictions
            }
        )
        
        agent = GamificationOrchestrationAgent()
        await agent.initialize()
        result = await agent.execute_task(task_request)
        
        if result.status == TaskStatus.FAILED:
            logger.error("Gamification analytics generation failed", error=result.error_message)
            raise HTTPException(status_code=500, detail=result.error_message)
        
        logger.info("Gamification analytics generated successfully", tenant_id=tenant_id)
        
        return result.result.get("analytics_data", {})
    
    except Exception as e:
        logger.error("Error generating gamification analytics", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate analytics")

# =============================================
# HEALTH AND STATUS ENDPOINTS
# =============================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    
    try:
        # Check agent health
        agent = GamificationOrchestrationAgent()
        await agent.initialize()
        health_result = await agent.health_check()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "agent_health": health_result,
            "features": {
                "referral_system": True,
                "achievement_system": True,
                "leaderboard_system": True,
                "portfolio_showcase": True,
                "fraud_detection": True,
                "cross_client_learning": True
            }
        }
    
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/status")
async def get_service_status():
    """Get detailed service status"""
    
    return {
        "service": "BizOSaaS Gamification Service",
        "version": "1.0.0",
        "status": "operational",
        "uptime": "99.9%",
        "active_features": [
            "referral_tracking",
            "achievement_system", 
            "leaderboards",
            "portfolio_generation",
            "fraud_detection",
            "analytics"
        ],
        "performance_metrics": {
            "avg_response_time_ms": 85,
            "requests_per_minute": 150,
            "error_rate": 0.01
        },
        "last_updated": datetime.now().isoformat()
    }

# =============================================
# BACKGROUND TASKS
# =============================================

async def process_referral_conversion_async(conversion_data: Dict[str, Any], token: str):
    """Background task for processing referral conversions"""
    
    try:
        agent = GamificationOrchestrationAgent()
        await agent.initialize()
        
        task_request = AgentTaskRequest(
            tenant_id=conversion_data.get("tenant_id", "unknown"),
            user_id=extract_user_id_from_token(token),
            task_type="process_referral",
            input_data=conversion_data
        )
        
        result = await agent.execute_task(task_request)
        
        # Handle result - send notifications, update records, etc.
        if result.status == TaskStatus.COMPLETED:
            logger.info("Referral conversion processed successfully", 
                       referral_code=conversion_data.get("referral_code"))
            # Additional post-processing logic here
        else:
            logger.error("Referral conversion processing failed", 
                        error=result.error_message)
    
    except Exception as e:
        logger.error("Background referral processing failed", error=str(e))

# =============================================
# STARTUP AND SHUTDOWN EVENTS
# =============================================

@app.on_event("startup")
async def startup_event():
    """Initialize service on startup"""
    logger.info("BizOSaaS Gamification Service starting up")
    
    # Initialize agents
    try:
        orchestrator = GamificationOrchestrationAgent()
        await orchestrator.initialize()
        
        referral_agent = ReferralSystemAgent()
        await referral_agent.initialize()
        
        logger.info("All gamification agents initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize agents", error=str(e))
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("BizOSaaS Gamification Service shutting down")
    # Cleanup tasks here

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006, log_level="info")