"""
Multi-Tenant Client Sites API
FastAPI service that integrates with the existing client-sites-service.py
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import asyncio
import json
from datetime import datetime
import os

# Import the existing client sites service
from client_sites_service import (
    MultiTenantClientSitesService,
    ClientSiteConfig,
    SiteDeployment
)

app = FastAPI(
    title="BizOSaaS Multi-Tenant Client Sites API",
    description="API for creating and managing client websites with domain routing and white-label capabilities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the client sites service
client_sites_service = MultiTenantClientSitesService()

# Pydantic models for API
class ClientSiteConfigRequest(BaseModel):
    client_id: str = Field(..., description="Unique client identifier")
    domain: Optional[str] = Field(None, description="Custom domain (e.g., marketing.acmecorp.com)")
    subdomain: Optional[str] = Field(None, description="Subdomain (e.g., acmecorp for acmecorp.bizoholic.app)")
    site_template: str = Field("startup_focus", description="Site template: bizoholic_pro, agency_essentials, startup_focus, enterprise_suite")
    
    branding: Dict[str, Any] = Field(default_factory=dict, description="Branding configuration")
    features_enabled: List[str] = Field(default_factory=list, description="List of enabled features")
    ai_agents_config: Dict[str, Any] = Field(default_factory=dict, description="AI agents configuration")
    custom_settings: Dict[str, Any] = Field(default_factory=dict, description="Custom site settings")

class ClientSiteResponse(BaseModel):
    success: bool
    client_site: Optional[Dict[str, Any]] = None
    deployment_details: Optional[Dict[str, Any]] = None
    next_steps: Optional[List[str]] = None
    error: Optional[str] = None

class ClientSiteStatusResponse(BaseModel):
    client_id: str
    site_status: str
    last_deployment: str
    uptime: str
    performance_metrics: Dict[str, Any]
    ai_agents_status: Dict[str, Any]
    traffic_metrics: Dict[str, Any]

class TemplateInfo(BaseModel):
    name: str
    description: str
    features: List[str]
    pages: List[str]
    ai_agents_displayed: int
    customization_level: str

# API Endpoints

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "BizOSaaS Multi-Tenant Client Sites API",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/templates", response_model=Dict[str, TemplateInfo])
async def get_available_templates():
    """Get all available site templates"""
    templates = client_sites_service.base_templates
    return {
        template_id: TemplateInfo(
            name=template["name"],
            description=template["description"],
            features=template["features"],
            pages=template["pages"],
            ai_agents_displayed=template["ai_agents_displayed"],
            customization_level=template["customization_level"]
        )
        for template_id, template in templates.items()
    }

@app.get("/features")
async def get_available_features():
    """Get all available feature modules"""
    return client_sites_service.feature_modules

@app.get("/domain-routing")
async def get_domain_routing_info():
    """Get domain routing configuration options"""
    return client_sites_service.domain_routing

@app.post("/sites", response_model=ClientSiteResponse)
async def create_client_site(
    site_config: ClientSiteConfigRequest,
    background_tasks: BackgroundTasks
):
    """Create a new client site"""
    
    # Convert request to service config
    config = ClientSiteConfig(
        client_id=site_config.client_id,
        domain=site_config.domain,
        subdomain=site_config.subdomain,
        site_template=site_config.site_template,
        branding=site_config.branding or _get_default_branding(site_config.client_id),
        features_enabled=site_config.features_enabled or _get_default_features(site_config.site_template),
        ai_agents_config=site_config.ai_agents_config or _get_default_ai_agents_config(site_config.site_template),
        custom_settings=site_config.custom_settings or {}
    )
    
    try:
        # Create the client site
        result = await client_sites_service.create_client_site(config)
        
        if result["success"]:
            # Schedule background tasks for post-deployment
            background_tasks.add_task(
                _post_deployment_tasks,
                site_config.client_id,
                result["client_site"]["site_url"]
            )
        
        return ClientSiteResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sites/{client_id}/status", response_model=ClientSiteStatusResponse)
async def get_client_site_status(client_id: str):
    """Get status and metrics for a client site"""
    
    try:
        status = await client_sites_service.get_client_site_status(client_id)
        return ClientSiteStatusResponse(**status)
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Client site not found: {str(e)}")

@app.put("/sites/{client_id}")
async def update_client_site(
    client_id: str,
    updates: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """Update an existing client site configuration"""
    
    try:
        result = await client_sites_service.update_client_site(client_id, updates)
        
        if result["success"]:
            # Schedule background redeployment if needed
            background_tasks.add_task(_handle_site_update, client_id, updates)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/sites/{client_id}")
async def delete_client_site(client_id: str):
    """Delete a client site (placeholder - implement based on requirements)"""
    # This would implement site deletion logic
    return {
        "success": True,
        "message": f"Client site {client_id} deletion initiated",
        "client_id": client_id
    }

@app.get("/sites/{client_id}/deployments")
async def get_site_deployments(client_id: str):
    """Get deployment history for a client site"""
    # This would return deployment history from storage
    return {
        "client_id": client_id,
        "deployments": [
            {
                "deployment_id": f"deploy_{client_id}_20250908_153000",
                "timestamp": "2025-09-08T15:30:00Z",
                "status": "successful",
                "version": "1.0.0",
                "changes": ["Updated AI agents configuration", "Applied new branding"]
            }
        ]
    }

@app.post("/sites/{client_id}/deploy")
async def trigger_site_deployment(
    client_id: str,
    background_tasks: BackgroundTasks
):
    """Trigger a new deployment for a client site"""
    
    background_tasks.add_task(_redeploy_site, client_id)
    
    return {
        "success": True,
        "message": f"Deployment triggered for client {client_id}",
        "client_id": client_id,
        "estimated_completion": "5 minutes"
    }

# Helper functions

def _get_default_branding(client_id: str) -> Dict[str, Any]:
    """Get default branding configuration based on client ID"""
    
    client_branding = {
        "bizoholic": {
            "company_name": "Bizoholic Digital",
            "primary_color": "#0ea5e9",
            "logo_url": "/logos/bizoholic-logo.png",
            "theme_mode": "light"
        },
        "coreldove": {
            "company_name": "CoreLDove Commerce",
            "primary_color": "#10b981",
            "logo_url": "/logos/coreldove-logo.png",
            "theme_mode": "light"
        },
        "thrillring": {
            "company_name": "Thrillring Events",
            "primary_color": "#f59e0b",
            "logo_url": "/logos/thrillring-logo.png",
            "theme_mode": "light"
        }
    }
    
    return client_branding.get(client_id, {
        "company_name": f"{client_id.title()} Portal",
        "primary_color": "#3b82f6",
        "logo_url": "/logos/default-logo.png",
        "theme_mode": "light"
    })

def _get_default_features(template: str) -> List[str]:
    """Get default features for a template"""
    
    template_features = {
        "bizoholic_pro": [
            "ai_agents_dashboard", "performance_analytics", "campaign_management",
            "client_reporting", "business_directory", "white_label_branding"
        ],
        "agency_essentials": [
            "core_ai_agents", "basic_analytics", "lead_capture",
            "client_portal", "e_commerce_tools"
        ],
        "startup_focus": [
            "lead_generation", "growth_analytics", "automation_showcase", "social_proof"
        ],
        "enterprise_suite": [
            "full_ai_ecosystem", "advanced_analytics", "multi_brand_management",
            "enterprise_integrations", "custom_workflows", "dedicated_support"
        ]
    }
    
    return template_features.get(template, ["ai_agents_dashboard"])

def _get_default_ai_agents_config(template: str) -> Dict[str, Any]:
    """Get default AI agents configuration for a template"""
    
    return {
        "agents_selection": "auto",
        "real_time_status": True,
        "agent_interaction": "read_only",
        "performance_metrics": True,
        "featured_agents": [
            "MarketingStrategistAgent", "ContentCreatorAgent", "SEOSpecialistAgent",
            "PerformanceAnalyticsAgent", "LeadScoringAgent", "ContactIntelligenceAgent"
        ]
    }

async def _post_deployment_tasks(client_id: str, site_url: str):
    """Background tasks to run after site deployment"""
    
    # Simulate post-deployment tasks
    await asyncio.sleep(5)  # Wait for deployment to stabilize
    
    # Tasks could include:
    # - Site health check
    # - SSL certificate setup
    # - DNS verification
    # - Analytics setup
    # - Performance baseline
    
    print(f"Post-deployment tasks completed for {client_id} at {site_url}")

async def _handle_site_update(client_id: str, updates: Dict[str, Any]):
    """Handle background tasks for site updates"""
    
    # Simulate update processing
    await asyncio.sleep(3)
    
    print(f"Site update processing completed for {client_id}")

async def _redeploy_site(client_id: str):
    """Handle site redeployment"""
    
    # Simulate redeployment process
    await asyncio.sleep(30)  # Simulate build and deploy time
    
    print(f"Site redeployment completed for {client_id}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)