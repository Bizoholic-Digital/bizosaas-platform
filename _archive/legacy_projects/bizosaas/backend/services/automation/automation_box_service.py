# =============================================================================
# AUTOMATION-IN-A-BOX SERVICE
# =============================================================================
# FastAPI service for SMB automation solutions with measurable ROI
# Week 2 Day 1 Afternoon Task - CoreLDove Vertical Intelligence Platform
# Integrates with AutomationBoxEngine for practical, embedded AI solutions
# =============================================================================

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any, Union
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import json
import os
import logging
from contextlib import asynccontextmanager

# Import automation engine
import sys
sys.path.append('/home/alagiri/projects/bizoholic/n8n/crewai/automation_box')
from automation_engine import (
    AutomationBoxEngine, 
    AutomationCategory, 
    AutomationSolution,
    EmbeddedAIService
)

# Import existing CrewAI integration
sys.path.append('/home/alagiri/projects/bizoholic/n8n/crewai')
try:
    from auth import current_active_user, get_user_context
    from models.auth_models import User
    AUTH_ENABLED = True
except ImportError:
    AUTH_ENABLED = False
    logging.warning("Authentication not available, running in development mode")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# PYDANTIC MODELS
# =============================================================================

class DeploymentStatus(str, Enum):
    PENDING = "pending"
    CONFIGURING = "configuring"
    DEPLOYING = "deploying"
    TESTING = "testing"
    DEPLOYED = "deployed"
    FAILED = "failed"
    ROLLBACK = "rollback"

class BusinessProfile(BaseModel):
    """Business profile for solution recommendations"""
    industry: str = Field(..., description="Business industry")
    employee_count: int = Field(..., ge=1, description="Number of employees")
    annual_revenue: Optional[int] = Field(None, ge=0, description="Annual revenue in USD")
    pain_points: List[str] = Field(default_factory=list, description="Business pain points")
    current_tools: List[str] = Field(default_factory=list, description="Current software tools")
    integration_requirements: List[str] = Field(default_factory=list, description="Required integrations")
    budget_range: Optional[str] = Field(None, description="Budget range (starter/professional/enterprise)")
    
class CustomizationOptions(BaseModel):
    """Customization options for automation solutions"""
    priority_components: Optional[List[str]] = Field(None, description="Priority components to deploy first")
    excluded_components: Optional[List[str]] = Field(None, description="Components to exclude")
    integration_preferences: Optional[Dict[str, str]] = Field(None, description="Integration preferences")
    automation_level: Optional[float] = Field(0.8, ge=0.0, le=1.0, description="Desired automation level")
    custom_workflows: Optional[List[Dict]] = Field(None, description="Custom workflow definitions")

class DeploymentRequest(BaseModel):
    """Request model for automation solution deployment"""
    category: AutomationCategory = Field(..., description="Automation solution category")
    tenant_id: Optional[UUID] = Field(None, description="Tenant ID (auto-assigned if not provided)")
    customization: Optional[CustomizationOptions] = Field(None, description="Customization options")
    business_context: Optional[Dict[str, Any]] = Field(None, description="Business context information")
    deployment_schedule: Optional[datetime] = Field(None, description="Scheduled deployment time")

class DeploymentResponse(BaseModel):
    """Response model for deployment requests"""
    success: bool = Field(..., description="Deployment success status")
    deployment_id: str = Field(..., description="Unique deployment identifier")
    solution_name: str = Field(..., description="Name of deployed solution")
    status: DeploymentStatus = Field(..., description="Current deployment status")
    components_deployed: int = Field(..., description="Number of components deployed")
    setup_timeline: str = Field(..., description="Expected setup timeline")
    expected_roi: Dict[str, str] = Field(..., description="Expected ROI metrics")
    success_metrics: Dict[str, str] = Field(..., description="Success metrics to track")
    go_live_checklist: List[str] = Field(..., description="Go-live checklist items")
    estimated_completion: Optional[datetime] = Field(None, description="Estimated completion time")

class SolutionCatalogItem(BaseModel):
    """Catalog item for available solutions"""
    category: AutomationCategory
    display_name: str
    description: str
    target_problem: str
    business_value: str
    components_count: int
    setup_timeline: str
    pricing_tier: str
    key_roi_points: List[str]
    integration_requirements: List[str]

class DeploymentProgress(BaseModel):
    """Deployment progress tracking"""
    deployment_id: str
    status: DeploymentStatus
    progress_percentage: float = Field(ge=0.0, le=100.0)
    current_phase: str
    completed_components: List[str]
    remaining_components: List[str]
    estimated_completion: Optional[datetime]
    success_metrics: Dict[str, Any]
    issues: List[str] = Field(default_factory=list)

class ROIMetrics(BaseModel):
    """ROI and success metrics tracking"""
    deployment_id: str
    time_since_deployment: timedelta
    baseline_metrics: Dict[str, float]
    current_metrics: Dict[str, float]
    improvement_percentage: Dict[str, float]
    roi_calculation: Dict[str, Union[float, str]]
    success_rate: float = Field(ge=0.0, le=100.0)
    recommendations: List[str]

# =============================================================================
# AUTOMATION BOX SERVICE
# =============================================================================

class AutomationBoxService:
    """
    Core service managing automation-in-a-box solutions
    Provides REST API interface for the AutomationBoxEngine
    """
    
    def __init__(self):
        self.engine = AutomationBoxEngine()
        self.embedded_ai = EmbeddedAIService(self.engine)
        self.active_deployments: Dict[str, Dict] = {}
        self.deployment_metrics: Dict[str, Dict] = {}
        
    async def deploy_solution(
        self, 
        request: DeploymentRequest, 
        background_tasks: BackgroundTasks,
        user_id: Optional[str] = None
    ) -> DeploymentResponse:
        """Deploy automation solution with background monitoring"""
        
        try:
            # Generate tenant ID if not provided
            tenant_id = request.tenant_id or uuid4()
            
            # Convert customization options
            customization_dict = None
            if request.customization:
                customization_dict = request.customization.dict(exclude_none=True)
            
            # Deploy solution using engine
            deployment_result = await self.engine.deploy_automation_solution(
                tenant_id=tenant_id,
                category=request.category,
                customization_options=customization_dict
            )
            
            # Create deployment tracking entry
            deployment_id = deployment_result["deployment_id"]
            self.active_deployments[deployment_id] = {
                "tenant_id": str(tenant_id),
                "user_id": user_id,
                "category": request.category,
                "start_time": datetime.utcnow(),
                "status": DeploymentStatus.DEPLOYING,
                "progress": 25.0,
                "current_phase": "Component Configuration",
                "business_context": request.business_context or {}
            }
            
            # Start background monitoring
            background_tasks.add_task(
                self._monitor_deployment_progress, 
                deployment_id, 
                deployment_result
            )
            
            # Calculate estimated completion
            estimated_completion = datetime.utcnow() + timedelta(days=14)  # Default timeline
            
            return DeploymentResponse(
                success=deployment_result["success"],
                deployment_id=deployment_id,
                solution_name=deployment_result["solution_name"],
                status=DeploymentStatus.DEPLOYING,
                components_deployed=deployment_result["components_deployed"],
                setup_timeline=deployment_result["setup_timeline"],
                expected_roi=deployment_result["expected_roi"],
                success_metrics=deployment_result["success_metrics"],
                go_live_checklist=deployment_result["go_live_checklist"],
                estimated_completion=estimated_completion
            )
            
        except Exception as e:
            logger.error(f"Deployment failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Deployment failed: {str(e)}"
            )
    
    async def get_solution_catalog(self) -> List[SolutionCatalogItem]:
        """Get catalog of available automation solutions"""
        
        try:
            solutions = self.engine.get_available_solutions()
            
            catalog_items = []
            for solution in solutions:
                catalog_item = SolutionCatalogItem(
                    category=solution["category"],
                    display_name=solution["display_name"],
                    description=solution["description"],
                    target_problem=solution["target_problem"],
                    business_value=solution["business_value"],
                    components_count=solution["components_count"],
                    setup_timeline=solution["setup_timeline"],
                    pricing_tier=solution["pricing_tier"],
                    key_roi_points=solution["key_roi"],
                    integration_requirements=[]  # Would be populated from solution details
                )
                catalog_items.append(catalog_item)
            
            return catalog_items
            
        except Exception as e:
            logger.error(f"Failed to get solution catalog: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve solution catalog: {str(e)}"
            )
    
    async def get_recommendations(
        self, 
        business_profile: BusinessProfile
    ) -> Dict[str, Any]:
        """Get solution recommendations based on business profile"""
        
        try:
            # Convert business profile to engine format
            profile_dict = {
                "industry": business_profile.industry,
                "employee_count": business_profile.employee_count,
                "annual_revenue": business_profile.annual_revenue,
                "pain_points": business_profile.pain_points
            }
            
            # Generate tenant ID for recommendation
            temp_tenant_id = uuid4()
            
            recommendations = await self.engine.get_solution_recommendation(
                tenant_id=temp_tenant_id,
                business_profile=profile_dict
            )
            
            # Enhance recommendations with additional context
            enhanced_recommendations = {
                **recommendations,
                "business_profile_analysis": {
                    "industry_focus": business_profile.industry,
                    "scale_assessment": self._assess_business_scale(business_profile),
                    "priority_areas": self._identify_priority_areas(business_profile),
                    "integration_complexity": self._assess_integration_complexity(business_profile)
                },
                "implementation_roadmap": self._generate_implementation_roadmap(
                    recommendations.get("recommendations", [])
                )
            }
            
            return enhanced_recommendations
            
        except Exception as e:
            logger.error(f"Failed to generate recommendations: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate recommendations: {str(e)}"
            )
    
    async def get_deployment_progress(self, deployment_id: str) -> DeploymentProgress:
        """Get current deployment progress and status"""
        
        if deployment_id not in self.active_deployments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Deployment {deployment_id} not found"
            )
        
        deployment = self.active_deployments[deployment_id]
        
        # Simulate progress calculation (in production, this would be real metrics)
        progress_info = self._calculate_deployment_progress(deployment)
        
        return DeploymentProgress(
            deployment_id=deployment_id,
            status=deployment["status"],
            progress_percentage=deployment["progress"],
            current_phase=deployment["current_phase"],
            completed_components=progress_info["completed"],
            remaining_components=progress_info["remaining"],
            estimated_completion=deployment.get("estimated_completion"),
            success_metrics=deployment.get("metrics", {}),
            issues=deployment.get("issues", [])
        )
    
    async def get_roi_metrics(self, deployment_id: str) -> ROIMetrics:
        """Get ROI and performance metrics for deployed solution"""
        
        if deployment_id not in self.deployment_metrics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Metrics for deployment {deployment_id} not found"
            )
        
        metrics_data = self.deployment_metrics[deployment_id]
        
        # Calculate ROI metrics (in production, this would query real data)
        roi_metrics = self._calculate_roi_metrics(deployment_id, metrics_data)
        
        return ROIMetrics(
            deployment_id=deployment_id,
            time_since_deployment=roi_metrics["time_since_deployment"],
            baseline_metrics=roi_metrics["baseline"],
            current_metrics=roi_metrics["current"],
            improvement_percentage=roi_metrics["improvements"],
            roi_calculation=roi_metrics["roi"],
            success_rate=roi_metrics["success_rate"],
            recommendations=roi_metrics["recommendations"]
        )
    
    async def _monitor_deployment_progress(
        self, 
        deployment_id: str, 
        deployment_result: Dict
    ):
        """Background task to monitor deployment progress"""
        
        try:
            deployment = self.active_deployments[deployment_id]
            
            # Simulate deployment phases
            phases = [
                ("Component Configuration", 25.0, 2),
                ("Integration Setup", 50.0, 3), 
                ("AI Agent Training", 75.0, 2),
                ("Testing & Validation", 90.0, 1),
                ("Go-Live Preparation", 100.0, 1)
            ]
            
            for phase_name, progress, duration_hours in phases:
                if deployment["status"] == DeploymentStatus.FAILED:
                    break
                    
                # Update phase
                deployment["current_phase"] = phase_name
                deployment["progress"] = progress
                
                # Simulate phase duration
                await asyncio.sleep(duration_hours * 3600)  # Convert to seconds
                
                logger.info(f"Deployment {deployment_id} completed phase: {phase_name}")
            
            # Mark as deployed
            if deployment["status"] != DeploymentStatus.FAILED:
                deployment["status"] = DeploymentStatus.DEPLOYED
                deployment["completion_time"] = datetime.utcnow()
                
                # Initialize metrics tracking
                self._initialize_metrics_tracking(deployment_id, deployment_result)
                
                logger.info(f"Deployment {deployment_id} completed successfully")
            
        except Exception as e:
            logger.error(f"Deployment monitoring failed for {deployment_id}: {str(e)}")
            if deployment_id in self.active_deployments:
                self.active_deployments[deployment_id]["status"] = DeploymentStatus.FAILED
                self.active_deployments[deployment_id]["issues"] = [str(e)]
    
    def _assess_business_scale(self, profile: BusinessProfile) -> str:
        """Assess business scale category"""
        if profile.employee_count <= 10:
            return "micro_business"
        elif profile.employee_count <= 50:
            return "small_business"
        elif profile.employee_count <= 250:
            return "medium_business"
        else:
            return "large_business"
    
    def _identify_priority_areas(self, profile: BusinessProfile) -> List[str]:
        """Identify priority automation areas based on profile"""
        priorities = []
        
        # Industry-based priorities
        if profile.industry in ["ecommerce", "retail"]:
            priorities.extend(["inventory_management", "customer_engagement"])
        elif profile.industry in ["services", "consulting"]:
            priorities.extend(["client_management", "project_automation"])
        elif profile.industry == "healthcare":
            priorities.extend(["patient_management", "compliance_automation"])
        
        # Scale-based priorities
        if profile.employee_count > 20:
            priorities.append("hr_automation")
        
        # Pain point-based priorities
        if "customer_support" in profile.pain_points:
            priorities.append("customer_engagement")
        if "inventory_tracking" in profile.pain_points:
            priorities.append("inventory_management")
        
        return list(set(priorities))  # Remove duplicates
    
    def _assess_integration_complexity(self, profile: BusinessProfile) -> str:
        """Assess integration complexity level"""
        tool_count = len(profile.current_tools)
        integration_count = len(profile.integration_requirements)
        
        complexity_score = tool_count + (integration_count * 2)
        
        if complexity_score <= 3:
            return "simple"
        elif complexity_score <= 8:
            return "moderate"
        else:
            return "complex"
    
    def _generate_implementation_roadmap(self, recommendations: List[Dict]) -> Dict[str, Any]:
        """Generate implementation roadmap based on recommendations"""
        
        if not recommendations:
            return {"phases": [], "total_timeline": "0 weeks"}
        
        # Sort recommendations by priority
        high_priority = [r for r in recommendations if r["priority"] == "HIGH"]
        medium_priority = [r for r in recommendations if r["priority"] == "MEDIUM"]
        
        phases = []
        current_week = 0
        
        # Phase 1: High priority solutions
        if high_priority:
            phases.append({
                "phase": 1,
                "name": "Core Automation Deployment",
                "solutions": [r["solution"].value for r in high_priority],
                "timeline": "Weeks 1-2",
                "focus": "Address critical pain points with immediate ROI"
            })
            current_week = 2
        
        # Phase 2: Medium priority solutions
        if medium_priority:
            phases.append({
                "phase": 2,
                "name": "Extended Automation Suite",
                "solutions": [r["solution"].value for r in medium_priority],
                "timeline": f"Weeks {current_week + 1}-{current_week + 3}",
                "focus": "Scale automation capabilities"
            })
            current_week += 3
        
        return {
            "phases": phases,
            "total_timeline": f"{current_week} weeks",
            "parallel_deployments": len(high_priority) > 1,
            "success_criteria": [
                "All solutions deployed successfully",
                "Integration tests passed",
                "User training completed",
                "Success metrics baseline established"
            ]
        }
    
    def _calculate_deployment_progress(self, deployment: Dict) -> Dict[str, List[str]]:
        """Calculate deployment progress details"""
        
        # Mock component progress (in production, this would be real data)
        all_components = [
            "ai_agent_configuration",
            "integration_setup",
            "workflow_automation",
            "monitoring_setup",
            "user_training"
        ]
        
        progress = deployment["progress"]
        completed_count = int((progress / 100) * len(all_components))
        
        return {
            "completed": all_components[:completed_count],
            "remaining": all_components[completed_count:]
        }
    
    def _initialize_metrics_tracking(self, deployment_id: str, deployment_result: Dict):
        """Initialize metrics tracking for deployed solution"""
        
        self.deployment_metrics[deployment_id] = {
            "deployment_time": datetime.utcnow(),
            "baseline_metrics": {
                "efficiency_score": 100.0,
                "cost_per_task": 10.0,
                "completion_time_hours": 8.0,
                "error_rate_percent": 5.0
            },
            "success_metrics": deployment_result.get("success_metrics", {}),
            "expected_roi": deployment_result.get("expected_roi", {})
        }
    
    def _calculate_roi_metrics(self, deployment_id: str, metrics_data: Dict) -> Dict[str, Any]:
        """Calculate ROI metrics for deployment"""
        
        time_since = datetime.utcnow() - metrics_data["deployment_time"]
        
        # Mock current metrics (in production, this would be real performance data)
        baseline = metrics_data["baseline_metrics"]
        current = {
            "efficiency_score": baseline["efficiency_score"] * 1.4,  # 40% improvement
            "cost_per_task": baseline["cost_per_task"] * 0.6,      # 40% cost reduction
            "completion_time_hours": baseline["completion_time_hours"] * 0.7,  # 30% faster
            "error_rate_percent": baseline["error_rate_percent"] * 0.2  # 80% error reduction
        }
        
        # Calculate improvements
        improvements = {
            metric: ((current[metric] - baseline[metric]) / baseline[metric]) * 100
            for metric in baseline.keys()
        }
        
        # Calculate overall ROI
        cost_savings = (baseline["cost_per_task"] - current["cost_per_task"]) * 1000  # Per 1000 tasks
        time_savings_value = (baseline["completion_time_hours"] - current["completion_time_hours"]) * 50  # $50/hour
        total_roi = cost_savings + time_savings_value
        
        return {
            "time_since_deployment": time_since,
            "baseline": baseline,
            "current": current,
            "improvements": improvements,
            "roi": {
                "cost_savings_usd": cost_savings,
                "time_savings_value_usd": time_savings_value,
                "total_roi_usd": total_roi,
                "roi_percentage": (total_roi / 10000) * 100  # Assuming $10k investment
            },
            "success_rate": min(85.0 + (time_since.days * 2), 95.0),  # Improve over time
            "recommendations": [
                "Continue monitoring key performance indicators",
                "Consider expanding automation to related processes",
                "Schedule quarterly optimization reviews"
            ]
        }

# =============================================================================
# FASTAPI APPLICATION
# =============================================================================

# Global service instance
automation_service = AutomationBoxService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting AutomationBox Service...")
    yield
    logger.info("Shutting down AutomationBox Service...")

app = FastAPI(
    title="CoreLDove AutomationBox Service",
    description="Automation-in-a-Box solutions for SMBs with measurable ROI",
    version="2.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5678",
        "http://localhost:8080",
        "https://bizoholic.com",
        "https://app.bizoholic.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/", response_model=Dict[str, Any])
async def root():
    """Service information and health check"""
    return {
        "service": "AutomationBox Service",
        "version": "2.0.0",
        "status": "operational",
        "available_solutions": len(automation_service.engine.solutions),
        "active_deployments": len(automation_service.active_deployments),
        "features": [
            "Solution Catalog",
            "Smart Recommendations", 
            "Automated Deployment",
            "Progress Monitoring",
            "ROI Tracking"
        ]
    }

@app.get("/health", response_model=Dict[str, str])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "automation_box_service"
    }

@app.get("/solutions/catalog", response_model=List[SolutionCatalogItem])
async def get_solution_catalog():
    """Get catalog of available automation solutions"""
    return await automation_service.get_solution_catalog()

@app.post("/solutions/recommend", response_model=Dict[str, Any])
async def get_solution_recommendations(business_profile: BusinessProfile):
    """Get personalized solution recommendations"""
    return await automation_service.get_recommendations(business_profile)

@app.post("/deployments/deploy", response_model=DeploymentResponse)
async def deploy_automation_solution(
    request: DeploymentRequest,
    background_tasks: BackgroundTasks,
    current_user: Optional[User] = Depends(current_active_user) if AUTH_ENABLED else None
):
    """Deploy automation solution"""
    user_id = str(current_user.id) if current_user else None
    return await automation_service.deploy_solution(request, background_tasks, user_id)

@app.get("/deployments/{deployment_id}/progress", response_model=DeploymentProgress)
async def get_deployment_progress(deployment_id: str):
    """Get deployment progress and status"""
    return await automation_service.get_deployment_progress(deployment_id)

@app.get("/deployments/{deployment_id}/metrics", response_model=ROIMetrics)
async def get_deployment_metrics(deployment_id: str):
    """Get ROI and performance metrics for deployment"""
    return await automation_service.get_roi_metrics(deployment_id)

@app.get("/deployments", response_model=List[Dict[str, Any]])
async def list_active_deployments(
    current_user: Optional[User] = Depends(current_active_user) if AUTH_ENABLED else None
):
    """List all active deployments"""
    deployments = []
    for deployment_id, deployment in automation_service.active_deployments.items():
        deployments.append({
            "deployment_id": deployment_id,
            "tenant_id": deployment["tenant_id"],
            "category": deployment["category"],
            "status": deployment["status"],
            "progress": deployment["progress"],
            "start_time": deployment["start_time"].isoformat(),
            "current_phase": deployment["current_phase"]
        })
    return deployments

@app.post("/ai/embed", response_model=Dict[str, Any])
async def embed_ai_capabilities(
    request: Dict[str, Any],
    current_user: Optional[User] = Depends(current_active_user) if AUTH_ENABLED else None
):
    """Embed AI capabilities in existing business processes"""
    tenant_id = UUID(request.get("tenant_id", str(uuid4())))
    business_processes = request.get("business_processes", [])
    
    return await automation_service.embedded_ai.embed_ai_capabilities(
        tenant_id=tenant_id,
        business_processes=business_processes
    )

@app.get("/categories", response_model=List[Dict[str, str]])
async def get_automation_categories():
    """Get list of available automation categories"""
    return [
        {"id": category.value, "name": category.value.replace("_", " ").title()}
        for category in AutomationCategory
    ]

@app.post("/solutions/{category}/preview", response_model=Dict[str, Any])
async def preview_solution(
    category: AutomationCategory,
    customization: Optional[CustomizationOptions] = None
):
    """Preview solution details with customization options"""
    
    solution = automation_service.engine.solutions.get(category)
    if not solution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Solution not found: {category}"
        )
    
    # Apply customization preview
    preview_data = {
        "solution_id": solution.solution_id,
        "display_name": solution.display_name,
        "description": solution.description,
        "category": solution.category,
        "components": [
            {
                "id": comp.component_id,
                "name": comp.name,
                "description": comp.description,
                "automation_level": comp.automation_level,
                "roi_impact": comp.roi_impact,
                "setup_time": comp.setup_time
            }
            for comp in solution.components
        ],
        "integration_requirements": solution.integration_requirements,
        "expected_roi": solution.expected_roi,
        "success_metrics": solution.success_metrics,
        "pricing_tier": solution.pricing_tier
    }
    
    if customization:
        # Apply customization preview
        if customization.excluded_components:
            preview_data["components"] = [
                comp for comp in preview_data["components"] 
                if comp["id"] not in customization.excluded_components
            ]
        
        if customization.automation_level:
            for comp in preview_data["components"]:
                comp["automation_level"] = min(comp["automation_level"], customization.automation_level)
    
    return preview_data

# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url)
        }
    )

# =============================================================================
# STANDALONE APPLICATION ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "automation_box_service:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )