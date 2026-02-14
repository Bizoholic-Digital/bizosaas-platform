from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Dict, Any, Optional
from app.dependencies import get_current_user, get_workflow_service
from app.domain.services.workflow_service import WorkflowService
from app.domain.ports.identity_port import AuthenticatedUser
from pydantic import BaseModel

router = APIRouter(prefix="/api/seo", tags=["seo"])

class SiteAuditRequest(BaseModel):
    url: str
    max_pages: int = 100

class KeywordResearchRequest(BaseModel):
    seed_keywords: List[str]
    country_code: str = "us"

class BacklinkRequest(BaseModel):
    domain: str

class RankTrackerScheduleRequest(BaseModel):
    domains: List[str]
    keywords: List[str]
    cron: str = "0 0 * * *" # Daily at midnight

@router.post("/audit")
async def trigger_site_audit(
    request: SiteAuditRequest,
    service: WorkflowService = Depends(get_workflow_service),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Trigger a comprehensive site audit workflow."""
    tenant_id = user.tenant_id or "default_tenant"
    
    # Trigger SiteAuditWorkflow
    params = {
        "tenant_id": tenant_id,
        "url": request.url,
        "max_pages": request.max_pages
    }
    
    # We use the generic trigger_workflow, assuming a Workflow record exists or we create one ad-hoc.
    # Ideally, we should look up the workflow ID for "Site Audit" for this tenant.
    # For now, we'll try to trigger by name/convention in a real app, 
    # but here we'll assume the frontend will pass the workflow ID or we look it up.
    
    # Find workflow definition for Site Audit
    wfs = await service.list_workflows(tenant_id)
    audit_wf = next((w for w in wfs if w.name == "SEO Site Audit"), None)
    
    if not audit_wf:
        # Auto-create if not exists (for ease of use)
        audit_wf = await service.create_workflow(tenant_id, {
            "name": "SEO Site Audit",
            "type": "SEO",
            "status": "active",
            "description": "Comprehensive site audit"
        })
        
    result = await service.trigger_workflow(tenant_id, audit_wf.id, params)
    return result

@router.post("/keywords/research")
async def trigger_keyword_research(
    request: KeywordResearchRequest,
    service: WorkflowService = Depends(get_workflow_service),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Trigger AI keyword research workflow."""
    tenant_id = user.tenant_id or "default_tenant"
    
    # Find workflow
    wfs = await service.list_workflows(tenant_id)
    kw_wf = next((w for w in wfs if w.name == "Keyword Research"), None)
    
    if not kw_wf:
        kw_wf = await service.create_workflow(tenant_id, {
            "name": "Keyword Research",
            "type": "SEO",
            "status": "active",
            "description": "AI-driven keyword research"
        })
            
    params = {
        "tenant_id": tenant_id,
        "seed_keywords": request.seed_keywords
    }
    
    result = await service.trigger_workflow(tenant_id, kw_wf.id, params)
    return result

@router.post("/backlinks/monitor")
async def trigger_backlink_monitor(
    request: BacklinkRequest,
    service: WorkflowService = Depends(get_workflow_service),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Trigger backlink monitoring workflow."""
    tenant_id = user.tenant_id or "default_tenant"
    
    wfs = await service.list_workflows(tenant_id)
    bl_wf = next((w for w in wfs if w.name == "Backlink Monitor"), None)
    
    if not bl_wf:
        bl_wf = await service.create_workflow(tenant_id, {
            "name": "Backlink Monitor",
            "type": "SEO",
            "status": "active",
            "description": "Backlink profile monitoring"
        })
        
    params = {
        "tenant_id": tenant_id,
        "domain": request.domain
    }
    
    result = await service.trigger_workflow(tenant_id, bl_wf.id, params)
    return result

@router.post("/rank-tracker/schedule")
async def schedule_rank_tracker(
    request: RankTrackerScheduleRequest,
    service: WorkflowService = Depends(get_workflow_service),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Schedule recurring rank tracking."""
    tenant_id = user.tenant_id or "default_tenant"
    
    # Check if workflow exists, else create
    wfs = await service.list_workflows(tenant_id)
    rt_wf = next((w for w in wfs if w.name == "Rank Tracker"), None)
    
    if not rt_wf:
        rt_wf = await service.create_workflow(tenant_id, {
            "name": "Rank Tracker",
            "type": "SEO",
            "status": "active",
            "description": "Daily Rank Tracking"
        })
        
    params = {
        "tenant_id": tenant_id,
        "domains": request.domains,
        "keywords": request.keywords
    }
    
    result = await service.schedule_workflow(tenant_id, rt_wf.id, request.cron, params)
    return result

@router.get("/reports/{report_id}")
async def get_seo_report(
    report_id: str,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Get a stored SEO report."""
    # In production, fetch from DB
    return {
        "report_id": report_id,
        "status": "ready",
        "summary": "Mock report summary"
    }
