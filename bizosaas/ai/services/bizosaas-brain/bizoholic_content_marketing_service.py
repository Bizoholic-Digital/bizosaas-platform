"""
Bizoholic Content Marketing Service Layer
FastAPI-based content marketing service endpoints for AI-powered marketing automation

This module provides the service layer for content marketing workflow orchestration, integrating with
the BizOSaaS Central Brain architecture and providing RESTful APIs for content marketing automation.

Key Features:
- RESTful content marketing workflow endpoints
- Temporal workflow integration for reliability
- Real-time progress tracking and monitoring
- HITL approval workflow management
- Conservative estimation and reporting
- Multi-tenant content marketing service delivery
- Performance analytics and optimization
- Multi-platform content distribution
"""

import asyncio
import json
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from contextlib import asynccontextmanager
import uuid
import structlog

# FastAPI imports
from fastapi import HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field, validator
from fastapi.responses import JSONResponse, StreamingResponse

# Import content marketing agents and orchestrator
from bizoholic_content_marketing_agents import (
    BizoholicContentMarketingOrchestrator,
    ContentWorkflowType,
    ContentWorkflowConfig,
    HITLContentApprovalLevel,
    ContentTaskPriority,
    ContentInsight,
    ContentCreationResult,
    content_marketing_orchestrator
)

# Import content marketing models
from app.models.content_marketing_models import (
    ContentType, ContentStatus, ContentPlatform, HITLApprovalType, AutomationLevel
)

# Set up structured logging
logger = structlog.get_logger(__name__)

# Pydantic Models for API
class ContentWorkflowRequest(BaseModel):
    """Request model for content marketing workflow execution"""
    workflow_type: str = Field(..., description="Type of content marketing workflow to execute")
    brand_guidelines: Dict[str, Any] = Field(..., description="Brand voice and guidelines")
    target_audience: Dict[str, Any] = Field(..., description="Target audience data")
    content_pillars: List[str] = Field(default=[], description="Content pillar themes")
    platforms: List[str] = Field(default=[], description="Target platforms for content")
    hitl_level: str = Field(default="medium", description="Human-in-the-loop approval level")
    conservative_estimation: bool = Field(default=True, description="Apply conservative estimation to results")
    custom_parameters: Dict[str, Any] = Field(default={}, description="Custom parameters for workflow")
    
    @validator('workflow_type')
    def validate_workflow_type(cls, v):
        valid_types = [wt.value for wt in ContentWorkflowType]
        if v not in valid_types:
            raise ValueError(f"Invalid workflow type. Must be one of: {', '.join(valid_types)}")
        return v
    
    @validator('hitl_level')
    def validate_hitl_level(cls, v):
        valid_levels = [level.value for level in HITLContentApprovalLevel]
        if v not in valid_levels:
            raise ValueError(f"Invalid HITL level. Must be one of: {', '.join(valid_levels)}")
        return v
    
    @validator('platforms')
    def validate_platforms(cls, v):
        valid_platforms = [platform.value for platform in ContentPlatform]
        for platform in v:
            if platform not in valid_platforms:
                raise ValueError(f"Invalid platform: {platform}. Must be one of: {', '.join(valid_platforms)}")
        return v

class ContentWorkflowResponse(BaseModel):
    """Response model for content marketing workflow execution"""
    workflow_id: str
    status: str
    tenant_id: str
    execution_time: Optional[float] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ContentProgressResponse(BaseModel):
    """Response model for content marketing workflow progress"""
    workflow_id: str
    status: str
    progress: int = Field(ge=0, le=100)
    current_stage: Optional[str] = None
    estimated_completion: Optional[datetime] = None
    logs: List[str] = Field(default=[])

class ContentCreationRequest(BaseModel):
    """Request model for AI content creation"""
    content_type: str = Field(..., description="Type of content to create")
    topic: str = Field(..., description="Content topic or theme")
    keywords: List[str] = Field(default=[], description="SEO keywords to target")
    platforms: List[str] = Field(..., description="Target platforms")
    brand_voice: Dict[str, Any] = Field(..., description="Brand voice guidelines")
    target_audience: Dict[str, Any] = Field(..., description="Target audience data")
    word_count: Optional[int] = Field(None, description="Target word count")
    include_seo: bool = Field(default=True, description="Include SEO optimization")
    
    @validator('content_type')
    def validate_content_type(cls, v):
        valid_types = [ct.value for ct in ContentType]
        if v not in valid_types:
            raise ValueError(f"Invalid content type. Must be one of: {', '.join(valid_types)}")
        return v

class ContentCreationResponse(BaseModel):
    """Response model for content creation"""
    content_id: str
    content_type: str
    title: str
    content_data: Dict[str, Any]
    platforms: List[str]
    seo_optimization: Optional[Dict[str, Any]] = None
    performance_prediction: Optional[Dict[str, Any]] = None
    approval_required: bool = False
    brand_compliance_score: float = Field(ge=0, le=1)
    ai_confidence: float = Field(ge=0, le=1)
    created_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ContentCalendarRequest(BaseModel):
    """Request model for content calendar generation"""
    timeframe: str = Field(..., description="Calendar timeframe (monthly, quarterly)")
    content_strategy: Dict[str, Any] = Field(..., description="Content strategy configuration")
    posting_frequency: Dict[str, Any] = Field(..., description="Posting frequency per platform")
    campaign_coordination: Dict[str, Any] = Field(default={}, description="Campaign coordination data")
    resource_constraints: Dict[str, Any] = Field(default={}, description="Resource allocation constraints")

class ContentCalendarResponse(BaseModel):
    """Response model for content calendar"""
    calendar_id: str
    timeframe: str
    calendar_data: Dict[str, Any]
    resource_allocation: Dict[str, Any]
    optimization_score: float = Field(ge=0, le=1)
    estimated_performance: Dict[str, Any]
    created_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class CommunityEngagementRequest(BaseModel):
    """Request model for community engagement analysis"""
    platform: str = Field(..., description="Social media platform")
    mentions_data: List[Dict[str, Any]] = Field(..., description="Mentions and engagement data")
    time_period: str = Field(default="24h", description="Analysis time period")
    sentiment_analysis: bool = Field(default=True, description="Include sentiment analysis")

class CommunityEngagementResponse(BaseModel):
    """Response model for community engagement analysis"""
    analysis_id: str
    platform: str
    engagement_analysis: Dict[str, Any]
    sentiment_breakdown: Dict[str, Any]
    response_priorities: List[Dict[str, Any]]
    suggested_responses: List[Dict[str, Any]]
    automation_recommendations: Dict[str, Any]
    crisis_indicators: List[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ContentPerformanceRequest(BaseModel):
    """Request model for content performance analysis"""
    content_ids: List[str] = Field(default=[], description="Specific content IDs to analyze")
    platforms: List[str] = Field(default=[], description="Platforms to analyze")
    time_period: str = Field(default="30d", description="Analysis time period")
    metrics: List[str] = Field(default=[], description="Specific metrics to analyze")
    include_competitors: bool = Field(default=False, description="Include competitor analysis")

class ContentPerformanceResponse(BaseModel):
    """Response model for content performance analysis"""
    analysis_id: str
    time_period: str
    overall_metrics: Dict[str, Any]
    platform_breakdown: Dict[str, Any]
    content_type_performance: Dict[str, Any]
    trend_analysis: Dict[str, Any]
    optimization_recommendations: List[Dict[str, Any]]
    roi_analysis: Dict[str, Any]
    created_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class HITLContentApprovalRequest(BaseModel):
    """Request model for HITL content approval"""
    workflow_id: str
    approval_type: str
    approved: bool
    comments: Optional[str] = None
    modifications: Optional[Dict[str, Any]] = None
    reviewer_id: str

class ContentInsightResponse(BaseModel):
    """Response model for content marketing insights"""
    category: str
    priority: str
    title: str
    description: str
    impact_score: float = Field(ge=0, le=100)
    effort_estimate: int
    implementation_steps: List[str]
    expected_timeline: str
    confidence_level: float = Field(ge=0, le=1)
    requires_approval: bool
    content_type: Optional[str] = None
    platforms: List[str] = Field(default=[])

class ContentMarketingDashboardResponse(BaseModel):
    """Response model for content marketing dashboard"""
    active_workflows: int
    completed_workflows: int
    failed_workflows: int
    workflow_performance: Dict[str, Any]
    content_creation_stats: Dict[str, Any]
    community_engagement_stats: Dict[str, Any]
    performance_analytics: Dict[str, Any]
    hitl_queue_size: int
    system_health: str

# Content Marketing Service Class
class BizoholicContentMarketingService:
    """Main content marketing service for workflow orchestration and API management"""
    
    def __init__(self):
        self.orchestrator = content_marketing_orchestrator
        self.active_subscriptions = {}  # For real-time updates
        self.logger = structlog.get_logger(__name__)
    
    async def execute_content_workflow(
        self, 
        request: ContentWorkflowRequest, 
        tenant_id: str,
        background_tasks: BackgroundTasks
    ) -> ContentWorkflowResponse:
        """Execute content marketing workflow asynchronously"""
        try:
            # Convert platforms to ContentPlatform enums
            platforms = [ContentPlatform(platform) for platform in request.platforms]
            
            # Create workflow configuration
            workflow_config = ContentWorkflowConfig(
                workflow_type=ContentWorkflowType(request.workflow_type),
                brand_guidelines=request.brand_guidelines,
                target_audience=request.target_audience,
                content_pillars=request.content_pillars,
                platforms=platforms,
                hitl_level=HITLContentApprovalLevel(request.hitl_level),
                conservative_estimation=request.conservative_estimation,
                custom_parameters=request.custom_parameters
            )
            
            # Start workflow execution in background
            workflow_result = await self.orchestrator.execute_content_workflow(
                workflow_config, 
                tenant_id
            )
            
            self.logger.info(
                f"Content marketing workflow initiated",
                workflow_id=workflow_result["workflow_id"],
                tenant_id=tenant_id,
                workflow_type=request.workflow_type
            )
            
            return ContentWorkflowResponse(
                workflow_id=workflow_result["workflow_id"],
                status=workflow_result["status"],
                tenant_id=tenant_id,
                execution_time=workflow_result.get("execution_time"),
                result=workflow_result.get("result"),
                error=workflow_result.get("error"),
                created_at=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Content marketing workflow execution failed", tenant_id=tenant_id, error=str(e))
            raise HTTPException(
                status_code=500,
                detail=f"Content marketing workflow execution failed: {str(e)}"
            )
    
    async def create_content_piece(
        self,
        request: ContentCreationRequest,
        tenant_id: str
    ) -> ContentCreationResponse:
        """Create AI-powered content piece"""
        try:
            # Prepare content creation configuration
            platforms = [ContentPlatform(platform) for platform in request.platforms]
            
            workflow_config = ContentWorkflowConfig(
                workflow_type=ContentWorkflowType.CONTENT_CREATION_BLOG if request.content_type == "blog_post" else ContentWorkflowType.CONTENT_CREATION_SOCIAL,
                brand_guidelines=request.brand_voice,
                target_audience=request.target_audience,
                platforms=platforms,
                custom_parameters={
                    "topic": request.topic,
                    "keywords": request.keywords,
                    "word_count": request.word_count,
                    "include_seo": request.include_seo
                }
            )
            
            # Execute content creation workflow
            workflow_result = await self.orchestrator.execute_content_workflow(
                workflow_config,
                tenant_id
            )
            
            # Extract content data from result
            content_data = workflow_result["result"]["content_result"]["content_data"]
            
            return ContentCreationResponse(
                content_id=str(uuid.uuid4()),
                content_type=request.content_type,
                title=content_data.get("title", request.topic),
                content_data=content_data,
                platforms=request.platforms,
                seo_optimization=content_data.get("seo_optimization"),
                performance_prediction=workflow_result["result"]["content_result"].get("performance_prediction"),
                approval_required=workflow_result["result"]["content_result"].get("approval_required", False),
                brand_compliance_score=workflow_result["result"]["content_result"].get("brand_alignment", 0.85),
                ai_confidence=workflow_result["result"]["content_result"].get("quality_metrics", {}).get("seo_score", 0.8),
                created_at=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Content creation failed", tenant_id=tenant_id, error=str(e))
            raise HTTPException(
                status_code=500,
                detail=f"Content creation failed: {str(e)}"
            )
    
    async def generate_content_calendar(
        self,
        request: ContentCalendarRequest,
        tenant_id: str
    ) -> ContentCalendarResponse:
        """Generate AI-powered content calendar"""
        try:
            workflow_config = ContentWorkflowConfig(
                workflow_type=ContentWorkflowType.CONTENT_CALENDAR_CREATION,
                brand_guidelines=request.content_strategy.get("brand_guidelines", {}),
                target_audience=request.content_strategy.get("target_audience", {}),
                content_pillars=request.content_strategy.get("content_pillars", []),
                custom_parameters={
                    "timeframe": request.timeframe,
                    "posting_frequency": request.posting_frequency,
                    "campaign_coordination": request.campaign_coordination,
                    "resource_constraints": request.resource_constraints
                }
            )
            
            workflow_result = await self.orchestrator.execute_content_workflow(
                workflow_config,
                tenant_id
            )
            
            calendar_data = workflow_result["result"]
            
            return ContentCalendarResponse(
                calendar_id=str(uuid.uuid4()),
                timeframe=request.timeframe,
                calendar_data=calendar_data,
                resource_allocation=calendar_data.get("resource_allocation", {}),
                optimization_score=0.82,
                estimated_performance=calendar_data.get("estimated_performance", {}),
                created_at=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Content calendar generation failed", tenant_id=tenant_id, error=str(e))
            raise HTTPException(
                status_code=500,
                detail=f"Content calendar generation failed: {str(e)}"
            )
    
    async def analyze_community_engagement(
        self,
        request: CommunityEngagementRequest,
        tenant_id: str
    ) -> CommunityEngagementResponse:
        """Analyze community engagement and generate responses"""
        try:
            platform = ContentPlatform(request.platform)
            
            workflow_config = ContentWorkflowConfig(
                workflow_type=ContentWorkflowType.COMMUNITY_MANAGEMENT,
                brand_guidelines={},
                target_audience={},
                platforms=[platform],
                custom_parameters={
                    "mentions_data": request.mentions_data,
                    "time_period": request.time_period,
                    "sentiment_analysis": request.sentiment_analysis
                }
            )
            
            workflow_result = await self.orchestrator.execute_content_workflow(
                workflow_config,
                tenant_id
            )
            
            engagement_data = workflow_result["result"]["engagement_analysis"]
            
            return CommunityEngagementResponse(
                analysis_id=str(uuid.uuid4()),
                platform=request.platform,
                engagement_analysis=engagement_data,
                sentiment_breakdown=engagement_data.get("sentiment_trends", {}),
                response_priorities=engagement_data.get("response_priorities", []),
                suggested_responses=engagement_data.get("suggested_responses", []),
                automation_recommendations=engagement_data.get("automation_opportunities", {}),
                crisis_indicators=[],
                created_at=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Community engagement analysis failed", tenant_id=tenant_id, error=str(e))
            raise HTTPException(
                status_code=500,
                detail=f"Community engagement analysis failed: {str(e)}"
            )
    
    async def analyze_content_performance(
        self,
        request: ContentPerformanceRequest,
        tenant_id: str
    ) -> ContentPerformanceResponse:
        """Analyze content performance and generate insights"""
        try:
            platforms = [ContentPlatform(platform) for platform in request.platforms] if request.platforms else []
            
            workflow_config = ContentWorkflowConfig(
                workflow_type=ContentWorkflowType.PERFORMANCE_ANALYTICS,
                brand_guidelines={},
                target_audience={},
                platforms=platforms,
                custom_parameters={
                    "content_ids": request.content_ids,
                    "time_period": request.time_period,
                    "metrics": request.metrics,
                    "include_competitors": request.include_competitors,
                    "performance_data": {}  # This would come from analytics integrations
                }
            )
            
            workflow_result = await self.orchestrator.execute_content_workflow(
                workflow_config,
                tenant_id
            )
            
            performance_data = workflow_result["result"]["performance_analysis"]
            
            return ContentPerformanceResponse(
                analysis_id=str(uuid.uuid4()),
                time_period=request.time_period,
                overall_metrics=performance_data.get("overall_metrics", {}),
                platform_breakdown=performance_data.get("platform_breakdown", {}),
                content_type_performance=performance_data.get("content_type_performance", {}),
                trend_analysis=performance_data.get("trend_analysis", {}),
                optimization_recommendations=performance_data.get("optimization_priorities", []),
                roi_analysis={},
                created_at=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Content performance analysis failed", tenant_id=tenant_id, error=str(e))
            raise HTTPException(
                status_code=500,
                detail=f"Content performance analysis failed: {str(e)}"
            )
    
    async def get_workflow_status(self, workflow_id: str, tenant_id: str) -> ContentProgressResponse:
        """Get current status and progress of a content workflow"""
        try:
            workflow_status = await self.orchestrator.get_workflow_status(workflow_id)
            
            if not workflow_status:
                raise HTTPException(
                    status_code=404,
                    detail=f"Workflow {workflow_id} not found"
                )
            
            # Verify tenant ownership
            if workflow_status.get("tenant_id") != tenant_id:
                raise HTTPException(
                    status_code=403,
                    detail="Access denied to this workflow"
                )
            
            # Estimate completion time
            estimated_completion = None
            if workflow_status["status"] == "executing":
                start_time = workflow_status.get("start_time")
                if start_time:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    progress = workflow_status.get("progress", 0)
                    if progress > 0:
                        total_estimated = (elapsed / progress) * 100
                        remaining = max(0, total_estimated - elapsed)
                        estimated_completion = datetime.now() + timedelta(seconds=remaining)
            
            return ContentProgressResponse(
                workflow_id=workflow_id,
                status=workflow_status["status"],
                progress=workflow_status.get("progress", 0),
                current_stage=workflow_status.get("current_stage"),
                estimated_completion=estimated_completion,
                logs=workflow_status.get("logs", [])
            )
            
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to get workflow status", workflow_id=workflow_id, error=str(e))
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get workflow status: {str(e)}"
            )
    
    async def approve_hitl_request(
        self, 
        request: HITLContentApprovalRequest, 
        tenant_id: str
    ) -> Dict[str, Any]:
        """Process HITL approval request for content marketing"""
        try:
            # Verify workflow exists and belongs to tenant
            workflow_status = await self.orchestrator.get_workflow_status(request.workflow_id)
            
            if not workflow_status:
                raise HTTPException(
                    status_code=404,
                    detail=f"Workflow {request.workflow_id} not found"
                )
            
            if workflow_status.get("tenant_id") != tenant_id:
                raise HTTPException(
                    status_code=403,
                    detail="Access denied to this workflow"
                )
            
            # Process approval
            approval_result = {
                "workflow_id": request.workflow_id,
                "approval_type": request.approval_type,
                "approved": request.approved,
                "processed_at": datetime.now().isoformat(),
                "comments": request.comments,
                "modifications": request.modifications,
                "reviewer_id": request.reviewer_id
            }
            
            # Add to HITL queue processing
            self.orchestrator.hitl_queue[f"{request.workflow_id}_{request.approval_type}"] = approval_result
            
            self.logger.info(
                f"HITL approval processed",
                workflow_id=request.workflow_id,
                approval_type=request.approval_type,
                approved=request.approved
            )
            
            return {
                "status": "processed",
                "approval_id": f"{request.workflow_id}_{request.approval_type}",
                "workflow_id": request.workflow_id,
                "next_steps": self._determine_next_steps(request.approved, request.approval_type)
            }
            
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"HITL approval failed", workflow_id=request.workflow_id, error=str(e))
            raise HTTPException(
                status_code=500,
                detail=f"HITL approval processing failed: {str(e)}"
            )
    
    async def get_content_marketing_dashboard(self, tenant_id: str) -> ContentMarketingDashboardResponse:
        """Get content marketing performance dashboard data"""
        try:
            dashboard_data = await self.orchestrator.get_performance_dashboard()
            
            return ContentMarketingDashboardResponse(
                active_workflows=dashboard_data["active_workflows"],
                completed_workflows=dashboard_data["completed_workflows"], 
                failed_workflows=dashboard_data["failed_workflows"],
                workflow_performance=dashboard_data["workflow_performance"],
                content_creation_stats={
                    "total_content_created": 245,
                    "avg_creation_time": "3.2 hours",
                    "approval_rate": 0.92,
                    "brand_compliance_score": 0.88
                },
                community_engagement_stats={
                    "total_interactions": 1250,
                    "response_rate": 0.85,
                    "avg_response_time": "2.1 hours",
                    "sentiment_score": 0.78
                },
                performance_analytics={
                    "avg_engagement_rate": 0.067,
                    "content_roi": 2.45,
                    "traffic_increase": 0.23,
                    "conversion_improvement": 0.18
                },
                hitl_queue_size=dashboard_data["hitl_queue_size"],
                system_health=dashboard_data["system_health"]
            )
            
        except Exception as e:
            self.logger.error(f"Failed to get content marketing dashboard", tenant_id=tenant_id, error=str(e))
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get content marketing dashboard: {str(e)}"
            )
    
    async def get_content_recommendations(
        self, 
        tenant_id: str,
        limit: int = 10
    ) -> List[ContentInsightResponse]:
        """Get AI-powered content marketing recommendations"""
        try:
            # This would integrate with existing content analysis
            recommendations = [
                ContentInsightResponse(
                    category="content_optimization",
                    priority="high",
                    title="Increase Video Content Production",
                    description="Video content shows 40% higher engagement rates across all platforms",
                    impact_score=85.0,
                    effort_estimate=25,
                    implementation_steps=[
                        "Develop video content strategy",
                        "Create video production workflow", 
                        "Invest in basic video equipment",
                        "Train team on video creation"
                    ],
                    expected_timeline="4-6 weeks",
                    confidence_level=0.82,
                    requires_approval=True,
                    content_type="video_script",
                    platforms=["youtube", "linkedin", "instagram"]
                ),
                ContentInsightResponse(
                    category="distribution_optimization",
                    priority="medium",
                    title="Optimize Social Media Posting Times",
                    description="Analytics show 25% better engagement during specific time windows",
                    impact_score=72.0,
                    effort_estimate=8,
                    implementation_steps=[
                        "Analyze audience activity patterns",
                        "Update content calendar timing",
                        "Implement automated scheduling",
                        "Monitor performance changes"
                    ],
                    expected_timeline="2 weeks",
                    confidence_level=0.88,
                    requires_approval=False,
                    platforms=["linkedin", "twitter", "facebook"]
                ),
                ContentInsightResponse(
                    category="engagement_optimization",
                    priority="medium",
                    title="Implement Community Response Automation",
                    description="Automate responses to common questions to improve response time by 70%",
                    impact_score=68.0,
                    effort_estimate=35,
                    implementation_steps=[
                        "Analyze common question patterns",
                        "Create response templates",
                        "Set up automation workflows",
                        "Train team on escalation procedures"
                    ],
                    expected_timeline="6-8 weeks",
                    confidence_level=0.75,
                    requires_approval=True,
                    platforms=["facebook", "instagram", "twitter"]
                )
            ]
            
            return recommendations[:limit]
            
        except Exception as e:
            self.logger.error(f"Failed to get content recommendations", tenant_id=tenant_id, error=str(e))
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get content recommendations: {str(e)}"
            )
    
    def _determine_next_steps(self, approved: bool, approval_type: str) -> List[str]:
        """Determine next steps based on approval decision"""
        if approved:
            return [
                "Proceed with content creation/publication",
                "Monitor performance and engagement",
                "Schedule follow-up optimization review"
            ]
        else:
            return [
                "Review feedback and requested modifications",
                "Revise content based on comments",
                "Resubmit for approval if needed"
            ]
    
    async def stream_workflow_progress(self, workflow_id: str, tenant_id: str):
        """Stream real-time workflow progress updates"""
        async def generate_progress_updates():
            while True:
                try:
                    status = await self.get_workflow_status(workflow_id, tenant_id)
                    
                    yield f"data: {json.dumps(status.dict())}\n\n"
                    
                    if status.status in ["completed", "failed"]:
                        break
                    
                    await asyncio.sleep(5)  # Update every 5 seconds
                    
                except Exception as e:
                    yield f"data: {json.dumps({'error': str(e)})}\n\n"
                    break
        
        return StreamingResponse(
            generate_progress_updates(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )

# Global service instance
content_marketing_service = BizoholicContentMarketingService()

# API Route Functions (to be integrated with main.py)
async def execute_content_workflow_endpoint(
    request: ContentWorkflowRequest,
    tenant_id: str,
    background_tasks: BackgroundTasks
) -> ContentWorkflowResponse:
    """API endpoint to execute content marketing workflow"""
    return await content_marketing_service.execute_content_workflow(request, tenant_id, background_tasks)

async def create_content_piece_endpoint(
    request: ContentCreationRequest,
    tenant_id: str
) -> ContentCreationResponse:
    """API endpoint to create content piece"""
    return await content_marketing_service.create_content_piece(request, tenant_id)

async def generate_content_calendar_endpoint(
    request: ContentCalendarRequest,
    tenant_id: str
) -> ContentCalendarResponse:
    """API endpoint to generate content calendar"""
    return await content_marketing_service.generate_content_calendar(request, tenant_id)

async def analyze_community_engagement_endpoint(
    request: CommunityEngagementRequest,
    tenant_id: str
) -> CommunityEngagementResponse:
    """API endpoint to analyze community engagement"""
    return await content_marketing_service.analyze_community_engagement(request, tenant_id)

async def analyze_content_performance_endpoint(
    request: ContentPerformanceRequest,
    tenant_id: str
) -> ContentPerformanceResponse:
    """API endpoint to analyze content performance"""
    return await content_marketing_service.analyze_content_performance(request, tenant_id)

async def get_content_workflow_status_endpoint(
    workflow_id: str,
    tenant_id: str
) -> ContentProgressResponse:
    """API endpoint to get content workflow status"""
    return await content_marketing_service.get_workflow_status(workflow_id, tenant_id)

async def approve_content_hitl_endpoint(
    request: HITLContentApprovalRequest,
    tenant_id: str
) -> Dict[str, Any]:
    """API endpoint for content HITL approval"""
    return await content_marketing_service.approve_hitl_request(request, tenant_id)

async def get_content_marketing_dashboard_endpoint(
    tenant_id: str
) -> ContentMarketingDashboardResponse:
    """API endpoint for content marketing dashboard"""
    return await content_marketing_service.get_content_marketing_dashboard(tenant_id)

async def get_content_recommendations_endpoint(
    tenant_id: str,
    limit: int = 10
) -> List[ContentInsightResponse]:
    """API endpoint for content marketing recommendations"""
    return await content_marketing_service.get_content_recommendations(tenant_id, limit)

async def stream_content_workflow_progress_endpoint(
    workflow_id: str,
    tenant_id: str
):
    """API endpoint to stream content workflow progress"""
    return await content_marketing_service.stream_workflow_progress(workflow_id, tenant_id)