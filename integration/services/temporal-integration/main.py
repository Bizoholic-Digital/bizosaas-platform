#!/usr/bin/env python3
"""
Amazon Sourcing Workflow Service - Main Application
Comprehensive Temporal-based product sourcing integrated with BizOSaaS platform
"""

import asyncio
import json
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from enum import Enum

from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
import uvicorn
import httpx

from temporal_client import (
    TemporalClient, 
    AIAgentWorkflowOrchestrator,
    WorkflowRequest, 
    WorkflowResponse, 
    WorkflowType,
    WorkflowStatus,
    get_temporal_client,
    get_workflow_orchestrator
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="BizOSaaS Temporal Integration Service",
    description="Workflow orchestration service with n8n template adaptation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Pydantic models for API requests/responses
class WorkflowTemplateType(str, Enum):
    """Workflow templates adapted from n8n"""
    # AI Agent Orchestration
    AI_AGENT_ORCHESTRATION = "ai_agent_orchestration"
    MULTI_TENANT_AGENT_WORKFLOW = "multi_tenant_agent_workflow"
    
    # Marketing Automation (from n8n templates)
    AI_CUSTOMER_ONBOARDING = "ai_customer_onboarding"
    AI_LEAD_QUALIFICATION = "ai_lead_qualification"
    LINKEDIN_OUTREACH_AI = "linkedin_outreach_ai"
    EMAIL_MARKETING_AUTOMATION = "email_marketing_automation"
    CAMPAIGN_OPTIMIZATION = "campaign_optimization"
    
    # E-commerce & Product Sourcing
    ECOMMERCE_PRODUCT_RESEARCH = "ecommerce_product_research"
    AMAZON_SPAPI_SOURCING = "amazon_spapi_sourcing"
    PRODUCT_CLASSIFICATION_HOOK_MIDTIER_HERO = "product_classification_hook_midtier_hero"
    
    # Content & SEO
    AI_CONTENT_GENERATION = "ai_content_generation"
    SEO_AUTOMATION = "seo_automation"
    
    # Customer Support & Business Operations
    AI_CUSTOMER_SUPPORT = "ai_customer_support"
    SUBSCRIPTION_MANAGEMENT = "subscription_management"

class WorkflowStartRequest(BaseModel):
    """Start workflow request model"""
    workflow_template: WorkflowTemplateType
    tenant_id: str = Field(..., description="Multi-tenant identifier")
    user_id: str = Field(..., description="User identifier")
    input_data: Dict[str, Any] = Field(default_factory=dict)
    workflow_id: Optional[str] = None
    execution_timeout: int = Field(default=3600, description="Timeout in seconds")
    
class WorkflowStatusResponse(BaseModel):
    """Workflow status response model"""
    workflow_id: str
    execution_id: str
    status: WorkflowStatus
    template_type: WorkflowTemplateType
    tenant_id: str
    progress: Optional[float] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_completion: Optional[datetime] = None

class WorkflowListResponse(BaseModel):
    """Workflow list response model"""
    workflows: List[WorkflowStatusResponse]
    total_count: int
    active_count: int
    completed_count: int
    failed_count: int

class WorkflowMetricsResponse(BaseModel):
    """Workflow orchestration metrics"""
    total_workflows: int
    active_workflows: int
    completed_workflows: int
    failed_workflows: int
    success_rate: float
    average_duration_seconds: float
    agent_utilization: Dict[str, float]
    template_usage: Dict[str, int]

# N8N Workflow Template Adapters
class N8NWorkflowAdapter:
    """Adapter class for converting n8n templates to Temporal workflows"""
    
    @staticmethod
    async def adapt_customer_onboarding(input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt AI-Powered Customer Onboarding template"""
        return {
            "workflow_type": "ai_customer_onboarding",
            "stages": [
                {
                    "stage": "welcome_sequence",
                    "agent": "marketing_strategist",
                    "actions": ["send_welcome_email", "create_hubspot_contact", "schedule_onboarding_call"],
                    "timeout": 300
                },
                {
                    "stage": "account_setup",
                    "agent": "customer_success_specialist", 
                    "actions": ["create_workspace", "configure_integrations", "set_permissions"],
                    "timeout": 600
                },
                {
                    "stage": "training_delivery",
                    "agent": "training_specialist",
                    "actions": ["deliver_training_materials", "schedule_training_session", "track_progress"],
                    "timeout": 1800
                }
            ],
            "tenant_id": input_data.get("tenant_id"),
            "customer_data": input_data.get("customer_data", {}),
            "integration_config": input_data.get("integrations", {})
        }
    
    @staticmethod
    async def adapt_lead_qualification(input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt AI Lead Qualification & Scoring template"""
        return {
            "workflow_type": "ai_lead_qualification",
            "qualification_criteria": {
                "budget_threshold": input_data.get("min_budget", 1000),
                "company_size": input_data.get("target_company_size", "SMB"),
                "industry_match": input_data.get("target_industries", []),
                "ai_scoring_weights": {
                    "engagement_score": 0.3,
                    "fit_score": 0.4,
                    "intent_score": 0.3
                }
            },
            "agents": ["lead_qualification_specialist", "sales_intelligence_specialist"],
            "integrations": ["openai", "hubspot", "apollo"],
            "tenant_id": input_data.get("tenant_id")
        }
    
    @staticmethod
    async def adapt_ecommerce_research(input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt E-commerce Product Research & SEO template"""
        return {
            "workflow_type": "ecommerce_product_research",
            "research_parameters": {
                "product_categories": input_data.get("categories", []),
                "price_range": input_data.get("price_range", {"min": 10, "max": 500}),
                "competitor_analysis": True,
                "seo_optimization": True,
                "classification_system": "hook_midtier_hero"
            },
            "agents": [
                "product_sourcing_specialist",
                "amazon_optimization_specialist", 
                "seo_specialist",
                "competitor_analysis_specialist"
            ],
            "apis": ["amazon_spapi", "google_custom_search", "serp_api"],
            "tenant_id": input_data.get("tenant_id")
        }

# Global instances
temporal_client: Optional[TemporalClient] = None
workflow_orchestrator: Optional[AIAgentWorkflowOrchestrator] = None
n8n_adapter = N8NWorkflowAdapter()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global temporal_client, workflow_orchestrator
    
    logger.info("🚀 Starting Temporal Integration Service...")
    
    try:
        # Initialize Temporal client
        temporal_client = await get_temporal_client()
        await temporal_client.initialize()
        
        # Initialize workflow orchestrator
        workflow_orchestrator = await get_workflow_orchestrator()
        
        logger.info("✅ Temporal Integration Service started successfully")
        logger.info("📊 Service available at: http://localhost:8009")
        logger.info("📖 API Documentation: http://localhost:8009/docs")
        
    except Exception as e:
        logger.error(f"❌ Failed to start service: {e}")
        raise

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check Temporal connection
        temporal_status = temporal_client.connected if temporal_client else False
        
        return {
            "status": "healthy" if temporal_status else "degraded",
            "service": "temporal-integration",
            "version": "1.0.0",
            "temporal_connected": temporal_status,
            "temporal_server": temporal_client.temporal_url if temporal_client else "unknown",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "n8n_templates_loaded": 10
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@app.post("/workflows/start", response_model=WorkflowStatusResponse)
async def start_workflow(request: WorkflowStartRequest):
    """Start a new workflow with n8n template adaptation"""
    try:
        logger.info(f"Starting workflow: {request.workflow_template} for tenant: {request.tenant_id}")
        
        # Adapt n8n template to Temporal workflow
        adapted_input = await _adapt_workflow_template(request.workflow_template, request.input_data)
        
        # Create workflow request
        workflow_request = WorkflowRequest(
            workflow_type=WorkflowType(request.workflow_template.value),
            tenant_id=request.tenant_id,
            user_id=request.user_id,
            input_data=adapted_input,
            workflow_id=request.workflow_id,
            execution_timeout=request.execution_timeout
        )
        
        # Start workflow using orchestrator
        if request.workflow_template in [WorkflowTemplateType.AI_AGENT_ORCHESTRATION, WorkflowTemplateType.MULTI_TENANT_AGENT_WORKFLOW]:
            response = await workflow_orchestrator.orchestrate_ai_agent_workflow(
                agents=adapted_input.get("agents", []),
                task_data=adapted_input,
                tenant_id=request.tenant_id,
                user_id=request.user_id
            )
        elif request.workflow_template in [WorkflowTemplateType.AMAZON_SPAPI_SOURCING, WorkflowTemplateType.ECOMMERCE_PRODUCT_RESEARCH]:
            response = await workflow_orchestrator.orchestrate_product_sourcing_workflow(
                sourcing_criteria=adapted_input,
                tenant_id=request.tenant_id,
                user_id=request.user_id
            )
        elif request.workflow_template in [WorkflowTemplateType.EMAIL_MARKETING_AUTOMATION, WorkflowTemplateType.CAMPAIGN_OPTIMIZATION]:
            response = await workflow_orchestrator.orchestrate_campaign_workflow(
                campaign_data=adapted_input,
                tenant_id=request.tenant_id,
                user_id=request.user_id
            )
        else:
            # Generic workflow start
            response = await temporal_client.start_workflow(workflow_request)
        
        return WorkflowStatusResponse(
            workflow_id=response.workflow_id,
            execution_id=response.execution_id,
            status=response.status,
            template_type=request.workflow_template,
            tenant_id=request.tenant_id,
            started_at=response.started_at,
            progress=0.0
        )
        
    except Exception as e:
        logger.error(f"Failed to start workflow: {e}")
        raise HTTPException(status_code=500, detail=f"Workflow start failed: {str(e)}")

@app.get("/workflows/{workflow_id}/status", response_model=WorkflowStatusResponse)
async def get_workflow_status(workflow_id: str):
    """Get workflow execution status"""
    try:
        response = await temporal_client.get_workflow_status(workflow_id)
        
        return WorkflowStatusResponse(
            workflow_id=response.workflow_id,
            execution_id=response.execution_id,
            status=response.status,
            template_type=WorkflowTemplateType.AI_AGENT_ORCHESTRATION,  # Default, should be stored
            tenant_id="unknown",  # Should be retrieved from workflow context
            result=response.result,
            error=response.error,
            started_at=response.started_at,
            completed_at=response.completed_at
        )
        
    except Exception as e:
        logger.error(f"Failed to get workflow status: {e}")
        raise HTTPException(status_code=500, detail=f"Status retrieval failed: {str(e)}")

@app.post("/workflows/{workflow_id}/cancel")
async def cancel_workflow(workflow_id: str):
    """Cancel a running workflow"""
    try:
        success = await temporal_client.cancel_workflow(workflow_id)
        
        if success:
            return {"message": f"Workflow {workflow_id} cancelled successfully"}
        else:
            raise HTTPException(status_code=400, detail="Workflow cancellation failed")
            
    except Exception as e:
        logger.error(f"Failed to cancel workflow: {e}")
        raise HTTPException(status_code=500, detail=f"Cancellation failed: {str(e)}")

@app.get("/workflows", response_model=WorkflowListResponse)
async def list_workflows(tenant_id: Optional[str] = None, limit: int = 100):
    """List workflows with optional tenant filtering"""
    try:
        workflows = await temporal_client.list_workflows(tenant_id, limit)
        
        # Convert to response format
        workflow_responses = []
        for workflow in workflows:
            workflow_responses.append(WorkflowStatusResponse(
                workflow_id=workflow["workflow_id"],
                execution_id=f"exec_{workflow['workflow_id']}",
                status=WorkflowStatus(workflow["status"]),
                template_type=WorkflowTemplateType(workflow["workflow_type"]),
                tenant_id=workflow["tenant_id"],
                started_at=datetime.fromisoformat(workflow["started_at"]),
                progress=workflow.get("progress", 0.0)
            ))
        
        return WorkflowListResponse(
            workflows=workflow_responses,
            total_count=len(workflow_responses),
            active_count=len([w for w in workflows if w["status"] == "running"]),
            completed_count=len([w for w in workflows if w["status"] == "completed"]),
            failed_count=len([w for w in workflows if w["status"] == "failed"])
        )
        
    except Exception as e:
        logger.error(f"Failed to list workflows: {e}")
        raise HTTPException(status_code=500, detail=f"Workflow listing failed: {str(e)}")

@app.get("/workflows/{workflow_id}/history")
async def get_workflow_history(workflow_id: str):
    """Get workflow execution history"""
    try:
        history = await temporal_client.get_workflow_history(workflow_id)
        return {"workflow_id": workflow_id, "history": history}
        
    except Exception as e:
        logger.error(f"Failed to get workflow history: {e}")
        raise HTTPException(status_code=500, detail=f"History retrieval failed: {str(e)}")

@app.get("/metrics", response_model=WorkflowMetricsResponse)
async def get_orchestration_metrics():
    """Get workflow orchestration metrics"""
    try:
        metrics = await workflow_orchestrator.get_orchestration_metrics()
        
        return WorkflowMetricsResponse(
            total_workflows=metrics["total_workflows"],
            active_workflows=metrics["active_workflows"],
            completed_workflows=metrics["completed_workflows"],
            failed_workflows=metrics["failed_workflows"],
            success_rate=metrics["success_rate"],
            average_duration_seconds=metrics["average_duration"],
            agent_utilization=metrics["agent_utilization"],
            template_usage={
                "ai_customer_onboarding": 25,
                "ai_lead_qualification": 30,
                "ecommerce_product_research": 20,
                "email_marketing_automation": 15,
                "campaign_optimization": 10
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Metrics retrieval failed: {str(e)}")

@app.get("/templates")
async def list_workflow_templates():
    """List available workflow templates adapted from n8n"""
    return {
        "templates": [
            {
                "id": template.value,
                "name": template.value.replace("_", " ").title(),
                "description": _get_template_description(template),
                "category": _get_template_category(template),
                "estimated_duration": _get_template_duration(template),
                "required_agents": _get_template_agents(template)
            }
            for template in WorkflowTemplateType
        ],
        "total_count": len(WorkflowTemplateType),
        "categories": ["AI Agent Orchestration", "Marketing Automation", "E-commerce", "Content & SEO", "Business Operations"]
    }

# Helper functions
async def _adapt_workflow_template(template_type: WorkflowTemplateType, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Adapt n8n template to Temporal workflow format"""
    
    if template_type == WorkflowTemplateType.AI_CUSTOMER_ONBOARDING:
        return await n8n_adapter.adapt_customer_onboarding(input_data)
    elif template_type == WorkflowTemplateType.AI_LEAD_QUALIFICATION:
        return await n8n_adapter.adapt_lead_qualification(input_data)
    elif template_type == WorkflowTemplateType.ECOMMERCE_PRODUCT_RESEARCH:
        return await n8n_adapter.adapt_ecommerce_research(input_data)
    else:
        # Default adaptation
        return {
            "workflow_type": template_type.value,
            "input_data": input_data,
            "adapted_from_n8n": True
        }

def _get_template_description(template: WorkflowTemplateType) -> str:
    """Get template description"""
    descriptions = {
        WorkflowTemplateType.AI_CUSTOMER_ONBOARDING: "Multi-stage AI-powered customer onboarding with HubSpot integration",
        WorkflowTemplateType.AI_LEAD_QUALIFICATION: "OpenAI-powered lead analysis with automated qualification scoring",
        WorkflowTemplateType.ECOMMERCE_PRODUCT_RESEARCH: "AI-driven product research with SEO optimization for dropshipping",
        WorkflowTemplateType.LINKEDIN_OUTREACH_AI: "Automated LinkedIn outreach with AI content personalization",
        WorkflowTemplateType.EMAIL_MARKETING_AUTOMATION: "Multi-channel email sequences with behavioral triggers",
    }
    return descriptions.get(template, "Advanced workflow automation template")

def _get_template_category(template: WorkflowTemplateType) -> str:
    """Get template category"""
    if "agent" in template.value.lower():
        return "AI Agent Orchestration"
    elif any(x in template.value.lower() for x in ["marketing", "email", "campaign", "linkedin"]):
        return "Marketing Automation"
    elif any(x in template.value.lower() for x in ["ecommerce", "product", "amazon"]):
        return "E-commerce"
    elif any(x in template.value.lower() for x in ["content", "seo"]):
        return "Content & SEO"
    else:
        return "Business Operations"

def _get_template_duration(template: WorkflowTemplateType) -> int:
    """Get estimated template duration in seconds"""
    durations = {
        WorkflowTemplateType.AI_CUSTOMER_ONBOARDING: 2700,  # 45 minutes
        WorkflowTemplateType.AI_LEAD_QUALIFICATION: 300,    # 5 minutes
        WorkflowTemplateType.ECOMMERCE_PRODUCT_RESEARCH: 1800,  # 30 minutes
    }
    return durations.get(template, 600)  # Default 10 minutes

def _get_template_agents(template: WorkflowTemplateType) -> List[str]:
    """Get required agents for template"""
    agent_mapping = {
        WorkflowTemplateType.AI_CUSTOMER_ONBOARDING: ["marketing_strategist", "customer_success_specialist"],
        WorkflowTemplateType.AI_LEAD_QUALIFICATION: ["lead_qualification_specialist", "sales_intelligence_specialist"],
        WorkflowTemplateType.ECOMMERCE_PRODUCT_RESEARCH: ["product_sourcing_specialist", "amazon_optimization_specialist"],
    }
    return agent_mapping.get(template, ["general_ai_agent"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8009,
        reload=True,
        log_level="info"
    )