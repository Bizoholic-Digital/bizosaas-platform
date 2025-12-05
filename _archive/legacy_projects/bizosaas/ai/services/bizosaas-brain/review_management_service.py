"""
Review Management & Response Automation Service for BizOSaaS Brain API

FastAPI service that integrates Temporal workflows with CrewAI agents for 
comprehensive review management and automated response generation.
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import structlog

# Temporal client imports
from temporalio.client import Client as TemporalClient
from temporalio.common import RetryPolicy

# Import workflow and agent modules
from review_management_workflows import (
    ReviewCollectionWorkflow, ReviewResponseWorkflow, 
    ReputationMonitoringWorkflow, ReviewSyncWorkflow,
    ReviewData, ReviewResponse, ReviewCollectionConfig,
    ReviewPlatform, ReviewSentiment, ResponseStatus,
    RepuationAlert
)
from review_management_agents import get_review_workflow_crew

# Import event bus integration
from event_bus_integration import (
    publish_brain_event,
    publish_ai_agent_result,
    BrainEventTypes
)

# Import unified tenant system
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
from unified_tenant_middleware import UnifiedTenant, get_current_tenant

logger = structlog.get_logger(__name__)


# Request/Response Models

class ReviewCollectionRequest(BaseModel):
    """Request model for review collection"""
    platforms: List[ReviewPlatform] = Field(..., description="Platforms to collect from")
    business_ids: List[str] = Field(..., description="Business IDs to collect for")
    collection_frequency: int = Field(default=3600, description="Collection frequency in seconds")
    force_collection: bool = Field(default=False, description="Force immediate collection")


class ReviewAnalysisRequest(BaseModel):
    """Request model for review analysis"""
    review_ids: Optional[List[str]] = None
    platforms: Optional[List[ReviewPlatform]] = None
    date_range: Optional[Dict[str, str]] = None
    sentiment_filter: Optional[ReviewSentiment] = None
    include_analysis: bool = True


class ResponseGenerationRequest(BaseModel):
    """Request model for response generation"""
    review_id: str = Field(..., description="Review ID to respond to")
    custom_instructions: Optional[str] = None
    tone: str = Field(default="professional", description="Response tone")
    language: str = Field(default="en", description="Response language")
    require_approval: Optional[bool] = None


class ResponseApprovalRequest(BaseModel):
    """Request model for response approval"""
    response_id: str = Field(..., description="Response ID to approve/reject")
    approved: bool = Field(..., description="Approval decision")
    approver: str = Field(..., description="Approver identifier")
    notes: Optional[str] = None


class ReputationMonitoringConfig(BaseModel):
    """Configuration for reputation monitoring"""
    monitoring_enabled: bool = True
    alert_thresholds: Dict[str, float] = Field(default_factory=dict)
    notification_channels: List[str] = Field(default_factory=list)
    monitoring_frequency: int = 3600


class CompetitorAnalysisRequest(BaseModel):
    """Request model for competitor analysis"""
    competitors: List[str] = Field(..., description="Competitor business names or IDs")
    analysis_type: str = Field(default="comprehensive", description="Type of analysis")
    include_benchmarking: bool = True


# Response Models

class WorkflowStatusResponse(BaseModel):
    """Workflow execution status response"""
    workflow_id: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    progress: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class ReviewSummaryResponse(BaseModel):
    """Review summary response"""
    total_reviews: int
    platform_breakdown: Dict[str, int]
    sentiment_distribution: Dict[str, int]
    average_rating: float
    response_rate: float
    recent_activity: List[Dict[str, Any]]


class ReputationScoreResponse(BaseModel):
    """Reputation score response"""
    overall_score: float
    platform_scores: Dict[str, float]
    sentiment_trend: List[Dict[str, Any]]
    key_metrics: Dict[str, float]
    recommendations: List[str]


# Service Class

class ReviewManagementService:
    """Comprehensive review management service"""
    
    def __init__(self):
        self.temporal_client: Optional[TemporalClient] = None
        self.crew = get_review_workflow_crew()
        self.logger = logger.bind(component="review_management_service")
        
        # Initialize Temporal client
        asyncio.create_task(self._initialize_temporal_client())
    
    async def _initialize_temporal_client(self):
        """Initialize Temporal client connection"""
        try:
            self.temporal_client = await TemporalClient.connect("localhost:7233")
            self.logger.info("Temporal client connected successfully")
        except Exception as e:
            self.logger.error(f"Failed to connect to Temporal: {e}")
            self.temporal_client = None
    
    async def start_review_collection(
        self,
        tenant: UnifiedTenant,
        request: ReviewCollectionRequest
    ) -> WorkflowStatusResponse:
        """Start review collection workflow"""
        try:
            if not self.temporal_client:
                raise HTTPException(status_code=503, detail="Temporal service unavailable")
            
            # Create collection configuration
            config = ReviewCollectionConfig(
                tenant_id=tenant.tenant_id,
                platforms=request.platforms,
                business_ids=request.business_ids,
                collection_frequency=request.collection_frequency,
                platform_credentials=await self._get_platform_credentials(tenant)
            )
            
            # Start Temporal workflow
            workflow_id = f"review-collection-{tenant.tenant_id}-{uuid4()}"
            
            handle = await self.temporal_client.start_workflow(
                ReviewCollectionWorkflow.run,
                config,
                id=workflow_id,
                task_queue="review-management",
                execution_timeout=timedelta(hours=2)
            )
            
            self.logger.info(f"Started review collection workflow: {workflow_id}")
            
            # Publish event
            await publish_brain_event(
                tenant=tenant,
                event_type=BrainEventTypes.AI_WORKFLOW_STARTED,
                data={
                    "workflow_type": "review_collection",
                    "workflow_id": workflow_id,
                    "platforms": [p.value for p in request.platforms],
                    "business_ids": request.business_ids
                }
            )
            
            return WorkflowStatusResponse(
                workflow_id=workflow_id,
                status="running",
                started_at=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Failed to start review collection: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def generate_review_response(
        self,
        tenant: UnifiedTenant,
        request: ResponseGenerationRequest
    ) -> WorkflowStatusResponse:
        """Generate AI response for a review"""
        try:
            if not self.temporal_client:
                raise HTTPException(status_code=503, detail="Temporal service unavailable")
            
            # Get review data
            review = await self._get_review_data(request.review_id, tenant)
            if not review:
                raise HTTPException(status_code=404, detail="Review not found")
            
            # Get business context
            business_context = await self._get_business_context(tenant)
            
            # Add custom instructions if provided
            if request.custom_instructions:
                business_context["custom_instructions"] = request.custom_instructions
                business_context["preferred_tone"] = request.tone
                business_context["response_language"] = request.language
            
            # Start response generation workflow
            workflow_id = f"review-response-{request.review_id}-{uuid4()}"
            
            handle = await self.temporal_client.start_workflow(
                ReviewResponseWorkflow.run,
                review,
                business_context,
                id=workflow_id,
                task_queue="review-management",
                execution_timeout=timedelta(hours=24)  # Allow time for approval
            )
            
            self.logger.info(f"Started response generation workflow: {workflow_id}")
            
            # Publish event
            await publish_brain_event(
                tenant=tenant,
                event_type=BrainEventTypes.AI_WORKFLOW_STARTED,
                data={
                    "workflow_type": "review_response",
                    "workflow_id": workflow_id,
                    "review_id": request.review_id,
                    "platform": review.platform.value
                }
            )
            
            return WorkflowStatusResponse(
                workflow_id=workflow_id,
                status="running",
                started_at=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate review response: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def approve_response(
        self,
        tenant: UnifiedTenant,
        request: ResponseApprovalRequest
    ) -> Dict[str, Any]:
        """Approve or reject a generated response"""
        try:
            if not self.temporal_client:
                raise HTTPException(status_code=503, detail="Temporal service unavailable")
            
            # Find the workflow handling this response
            workflow_id = await self._get_workflow_for_response(request.response_id, tenant)
            if not workflow_id:
                raise HTTPException(status_code=404, detail="Response workflow not found")
            
            # Get workflow handle
            handle = self.temporal_client.get_workflow_handle(workflow_id)
            
            # Send approval signal
            await handle.signal(
                ReviewResponseWorkflow.approve_response,
                request.approved,
                request.approver,
                request.notes or ""
            )
            
            self.logger.info(f"Sent approval signal for response {request.response_id}")
            
            # Publish event
            await publish_brain_event(
                tenant=tenant,
                event_type="brain.review.response_approval",
                data={
                    "response_id": request.response_id,
                    "approved": request.approved,
                    "approver": request.approver,
                    "workflow_id": workflow_id
                }
            )
            
            return {
                "status": "success",
                "response_id": request.response_id,
                "approved": request.approved,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to approve response: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def start_reputation_monitoring(
        self,
        tenant: UnifiedTenant,
        config: ReputationMonitoringConfig
    ) -> WorkflowStatusResponse:
        """Start continuous reputation monitoring"""
        try:
            if not self.temporal_client:
                raise HTTPException(status_code=503, detail="Temporal service unavailable")
            
            # Start monitoring workflow
            workflow_id = f"reputation-monitoring-{tenant.tenant_id}"
            
            handle = await self.temporal_client.start_workflow(
                ReputationMonitoringWorkflow.run,
                tenant.tenant_id,
                config.model_dump(),
                id=workflow_id,
                task_queue="review-management",
                # This is a long-running workflow
                execution_timeout=timedelta(days=365)
            )
            
            self.logger.info(f"Started reputation monitoring workflow: {workflow_id}")
            
            return WorkflowStatusResponse(
                workflow_id=workflow_id,
                status="running",
                started_at=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Failed to start reputation monitoring: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def analyze_reviews(
        self,
        tenant: UnifiedTenant,
        request: ReviewAnalysisRequest
    ) -> Dict[str, Any]:
        """Analyze reviews using CrewAI agents"""
        try:
            # Get reviews based on request criteria
            reviews = await self._get_reviews_for_analysis(tenant, request)
            
            if not reviews:
                return {
                    "status": "no_reviews",
                    "message": "No reviews found matching criteria",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Execute analysis using CrewAI
            tenant_context = await self._get_tenant_context(tenant)
            
            analysis_result = await self.crew.execute_review_analysis_workflow(
                reviews, tenant_context
            )
            
            # Publish analysis result
            await publish_ai_agent_result(
                tenant=tenant,
                agent_name="Review Analysis Crew",
                result=analysis_result,
                execution_time_ms=0,  # Would track actual time
                success=analysis_result.get("status") == "completed"
            )
            
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"Review analysis failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def analyze_competitors(
        self,
        tenant: UnifiedTenant,
        request: CompetitorAnalysisRequest
    ) -> Dict[str, Any]:
        """Analyze competitor reviews and strategies"""
        try:
            # Get tenant and reputation context
            tenant_context = await self._get_tenant_context(tenant)
            reputation_data = await self._get_reputation_data(tenant)
            
            # Execute competitor analysis using CrewAI
            analysis_result = await self.crew.execute_reputation_strategy_workflow(
                tenant_context, reputation_data, request.competitors
            )
            
            # Publish analysis result
            await publish_ai_agent_result(
                tenant=tenant,
                agent_name="Competitor Analysis Crew",
                result=analysis_result,
                execution_time_ms=0,
                success=analysis_result.get("status") == "completed"
            )
            
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"Competitor analysis failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_workflow_status(
        self,
        tenant: UnifiedTenant,
        workflow_id: str
    ) -> WorkflowStatusResponse:
        """Get status of a running workflow"""
        try:
            if not self.temporal_client:
                raise HTTPException(status_code=503, detail="Temporal service unavailable")
            
            handle = self.temporal_client.get_workflow_handle(workflow_id)
            
            # Get workflow description
            describe_result = await handle.describe()
            
            status = "running"
            result = None
            error = None
            
            if describe_result.status.name == "COMPLETED":
                status = "completed"
                try:
                    result = await handle.result()
                except Exception as e:
                    error = str(e)
                    status = "failed"
            elif describe_result.status.name == "FAILED":
                status = "failed"
                # Get failure details if available
            elif describe_result.status.name == "CANCELLED":
                status = "cancelled"
            
            return WorkflowStatusResponse(
                workflow_id=workflow_id,
                status=status,
                started_at=describe_result.start_time,
                completed_at=describe_result.close_time if describe_result.close_time else None,
                result=result,
                error=error
            )
            
        except Exception as e:
            self.logger.error(f"Failed to get workflow status: {e}")
            raise HTTPException(status_code=404, detail="Workflow not found")
    
    async def get_review_summary(
        self,
        tenant: UnifiedTenant,
        days: int = 30
    ) -> ReviewSummaryResponse:
        """Get review summary and metrics"""
        try:
            # Get review data for the specified period
            summary_data = await self._get_review_summary_data(tenant, days)
            
            return ReviewSummaryResponse(**summary_data)
            
        except Exception as e:
            self.logger.error(f"Failed to get review summary: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_reputation_score(
        self,
        tenant: UnifiedTenant
    ) -> ReputationScoreResponse:
        """Get overall reputation score and metrics"""
        try:
            # Calculate reputation metrics
            reputation_data = await self._calculate_reputation_score(tenant)
            
            return ReputationScoreResponse(**reputation_data)
            
        except Exception as e:
            self.logger.error(f"Failed to get reputation score: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    # Helper methods
    
    async def _get_platform_credentials(self, tenant: UnifiedTenant) -> Dict[str, str]:
        """Get encrypted platform credentials from Vault"""
        # This would integrate with HashiCorp Vault to get encrypted credentials
        return {
            "google_business": "encrypted_google_credentials",
            "yelp": "encrypted_yelp_credentials",
            "facebook": "encrypted_facebook_credentials"
        }
    
    async def _get_review_data(self, review_id: str, tenant: UnifiedTenant) -> Optional[ReviewData]:
        """Get review data from database"""
        # This would query the review database
        # For now, return mock data
        return None
    
    async def _get_business_context(self, tenant: UnifiedTenant) -> Dict[str, Any]:
        """Get business context for response generation"""
        return {
            "business_name": tenant.business_name,
            "industry": getattr(tenant, 'industry', 'general'),
            "brand_voice": "professional_friendly",
            "response_guidelines": [
                "Always thank customers for feedback",
                "Address specific concerns mentioned",
                "Offer concrete solutions when possible",
                "Maintain professional and empathetic tone"
            ]
        }
    
    async def _get_workflow_for_response(self, response_id: str, tenant: UnifiedTenant) -> Optional[str]:
        """Get workflow ID handling a specific response"""
        # This would query workflow tracking database
        return None
    
    async def _get_reviews_for_analysis(
        self, 
        tenant: UnifiedTenant, 
        request: ReviewAnalysisRequest
    ) -> List[ReviewData]:
        """Get reviews matching analysis criteria"""
        # This would query the review database with filters
        return []
    
    async def _get_tenant_context(self, tenant: UnifiedTenant) -> Dict[str, Any]:
        """Get comprehensive tenant context"""
        return {
            "tenant_id": tenant.tenant_id,
            "business_name": tenant.business_name,
            "industry": getattr(tenant, 'industry', 'general'),
            "locations": getattr(tenant, 'locations', []),
            "brand_guidelines": {}
        }
    
    async def _get_reputation_data(self, tenant: UnifiedTenant) -> Dict[str, Any]:
        """Get current reputation data"""
        return {
            "current_score": 4.2,
            "total_reviews": 150,
            "platform_distribution": {"google": 80, "yelp": 45, "facebook": 25},
            "sentiment_breakdown": {"positive": 0.7, "neutral": 0.2, "negative": 0.1}
        }
    
    async def _get_review_summary_data(self, tenant: UnifiedTenant, days: int) -> Dict[str, Any]:
        """Get review summary data"""
        return {
            "total_reviews": 45,
            "platform_breakdown": {"google_business": 25, "yelp": 15, "facebook": 5},
            "sentiment_distribution": {"positive": 30, "neutral": 10, "negative": 5},
            "average_rating": 4.2,
            "response_rate": 0.89,
            "recent_activity": []
        }
    
    async def _calculate_reputation_score(self, tenant: UnifiedTenant) -> Dict[str, Any]:
        """Calculate comprehensive reputation score"""
        return {
            "overall_score": 4.2,
            "platform_scores": {
                "google_business": 4.3,
                "yelp": 4.1,
                "facebook": 4.0
            },
            "sentiment_trend": [
                {"date": "2023-12-01", "score": 4.1},
                {"date": "2023-12-02", "score": 4.2}
            ],
            "key_metrics": {
                "response_rate": 0.89,
                "response_time_hours": 2.5,
                "resolution_rate": 0.95
            },
            "recommendations": [
                "Improve response time to negative reviews",
                "Increase response rate on Yelp platform",
                "Implement proactive review collection"
            ]
        }


# Global service instance
_review_service: Optional[ReviewManagementService] = None


def get_review_service() -> ReviewManagementService:
    """Get or create the global review management service"""
    global _review_service
    
    if _review_service is None:
        _review_service = ReviewManagementService()
    
    return _review_service


# FastAPI Routes

def create_review_routes(app: FastAPI):
    """Create review management routes"""
    
    service = get_review_service()
    
    @app.post("/review-management/collect")
    async def start_review_collection(
        request: ReviewCollectionRequest,
        tenant: UnifiedTenant = Depends(get_current_tenant)
    ) -> WorkflowStatusResponse:
        """Start review collection workflow"""
        return await service.start_review_collection(tenant, request)
    
    @app.post("/review-management/respond")
    async def generate_review_response(
        request: ResponseGenerationRequest,
        tenant: UnifiedTenant = Depends(get_current_tenant)
    ) -> WorkflowStatusResponse:
        """Generate AI response for a review"""
        return await service.generate_review_response(tenant, request)
    
    @app.post("/review-management/approve")
    async def approve_response(
        request: ResponseApprovalRequest,
        tenant: UnifiedTenant = Depends(get_current_tenant)
    ) -> Dict[str, Any]:
        """Approve or reject a generated response"""
        return await service.approve_response(tenant, request)
    
    @app.post("/review-management/monitor")
    async def start_reputation_monitoring(
        config: ReputationMonitoringConfig,
        tenant: UnifiedTenant = Depends(get_current_tenant)
    ) -> WorkflowStatusResponse:
        """Start reputation monitoring"""
        return await service.start_reputation_monitoring(tenant, config)
    
    @app.post("/review-management/analyze")
    async def analyze_reviews(
        request: ReviewAnalysisRequest,
        tenant: UnifiedTenant = Depends(get_current_tenant)
    ) -> Dict[str, Any]:
        """Analyze reviews using AI"""
        return await service.analyze_reviews(tenant, request)
    
    @app.post("/review-management/competitors")
    async def analyze_competitors(
        request: CompetitorAnalysisRequest,
        tenant: UnifiedTenant = Depends(get_current_tenant)
    ) -> Dict[str, Any]:
        """Analyze competitor reviews"""
        return await service.analyze_competitors(tenant, request)
    
    @app.get("/review-management/workflow/{workflow_id}")
    async def get_workflow_status(
        workflow_id: str,
        tenant: UnifiedTenant = Depends(get_current_tenant)
    ) -> WorkflowStatusResponse:
        """Get workflow execution status"""
        return await service.get_workflow_status(tenant, workflow_id)
    
    @app.get("/review-management/summary")
    async def get_review_summary(
        days: int = Query(30, description="Number of days to include"),
        tenant: UnifiedTenant = Depends(get_current_tenant)
    ) -> ReviewSummaryResponse:
        """Get review summary and metrics"""
        return await service.get_review_summary(tenant, days)
    
    @app.get("/review-management/reputation")
    async def get_reputation_score(
        tenant: UnifiedTenant = Depends(get_current_tenant)
    ) -> ReputationScoreResponse:
        """Get reputation score and metrics"""
        return await service.get_reputation_score(tenant)