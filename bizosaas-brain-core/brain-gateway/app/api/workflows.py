from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user, get_workflow_service
from app.models.workflow import Workflow
from app.domain.services.workflow_service import WorkflowService
from domain.ports.identity_port import AuthenticatedUser
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/workflows", tags=["workflows"])

class WorkflowConfigUpdate(BaseModel):
    retries: Optional[int] = None
    timeout: Optional[int] = None
    notifyOnError: Optional[bool] = None
    priority: Optional[str] = None

class WorkflowCreate(BaseModel):
    name: str
    description: Optional[str] = None
    type: str = "Custom"
    status: str = "paused"
    template_id: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

@router.post("/")
async def create_workflow(
    workflow_data: WorkflowCreate,
    service: WorkflowService = Depends(get_workflow_service),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Create a new workflow"""
    tenant_id = user.tenant_id or "default_tenant"
    workflow = await service.create_workflow(tenant_id, workflow_data.model_dump())
    return workflow.to_dict()

@router.get("/")
async def list_workflows(
    service: WorkflowService = Depends(get_workflow_service),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """List all workflows for the tenant"""
    tenant_id = user.tenant_id or "default_tenant"
    workflows = await service.list_workflows(tenant_id)
    
    if not workflows:
        # We'll keep the seeding logic in the service or here for now
        # Actually, let's keep it here briefly if needed, but it should be in service
        from app.models.workflow import Workflow
        default_wfs = [
            Workflow(
                tenant_id=tenant_id,
                name="Marketing Email Sequence",
                type="Marketing",
                status="running",
                description="Automates welcome sequence and follow-ups for new leads.",
                success_rate=98.5,
                runs_today=12,
                last_run=datetime.utcnow(),
                config={"retries": 3, "timeout": 30, "notifyOnError": True, "priority": "medium"}
            ),
            Workflow(
                tenant_id=tenant_id,
                name="Shopify Inventory Sync",
                type="E-commerce",
                status="paused",
                description="Updates product levels between Shopify and local database every 15 minutes.",
                success_rate=100,
                runs_today=4,
                last_run=datetime.utcnow(),
                config={"retries": 5, "timeout": 60, "notifyOnError": True, "priority": "high"}
            )
        ]
        service.db.add_all(default_wfs)
        service.db.commit()
        workflows = default_wfs
        
    return [wf.to_dict() for wf in workflows]

@router.post("/{workflow_id}/config")
async def update_workflow_config(
    workflow_id: str,
    config: WorkflowConfigUpdate,
    service: WorkflowService = Depends(get_workflow_service),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Update workflow execution configuration"""
    tenant_id = user.tenant_id or "default_tenant"
    success = await service.update_config(tenant_id, workflow_id, config.model_dump(exclude_unset=True))
    
    if not success:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return {"status": "success", "message": "Configuration updated"}

    return {"status": "success", "new_status": new_status}

@router.post("/{workflow_id}/hitl")
async def update_hitl_settings(
    workflow_id: str,
    enabled: bool = Body(..., embed=True),
    service: WorkflowService = Depends(get_workflow_service),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Enable or disable HITL for a workflow"""
    tenant_id = user.tenant_id or "default_tenant"
    success = await service.update_hitl_settings(tenant_id, workflow_id, enabled)
    if not success:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {"status": "success", "hitl_enabled": enabled}

@router.get("/proposals")
async def list_proposals(
    status: Optional[str] = None,
    service: WorkflowService = Depends(get_workflow_service),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """List agent-proposed workflows for approval"""
    # Only admins can see platform-wide proposals
    if "admin" not in user.roles and "super_admin" not in user.roles:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    proposals = await service.list_proposals(status)
    return [p.to_dict() for p in proposals]

@router.post("/proposals/{proposal_id}/action")
async def handle_proposal_action(
    proposal_id: str,
    action: str = Body(..., embed=True), # 'approve' or 'reject'
    notes: Optional[str] = Body(None, embed=True),
    service: WorkflowService = Depends(get_workflow_service),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Approve or reject an agent-proposed workflow"""
    if "admin" not in user.roles and "super_admin" not in user.roles:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    success = await service.handle_proposal(proposal_id, action, user.user_id, notes)
    if not success:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    return {"status": "success", "action": action}

@router.get("/approvals")
async def list_approvals(
    status: Optional[str] = "pending",
    service: WorkflowService = Depends(get_workflow_service),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """List pending human-in-the-loop approvals"""
    tenant_id = user.tenant_id or "default_tenant"
    tasks = await service.list_approval_tasks(tenant_id, status)
    return [t.to_dict() for t in tasks]

@router.post("/approvals/{task_id}/action")
async def handle_approval_action(
    task_id: str,
    action: str = Body(..., embed=True), # 'approve' or 'reject'
    notes: Optional[str] = Body(None, embed=True),
    service: WorkflowService = Depends(get_workflow_service),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Approve or reject a human-in-the-loop task"""
    success = await service.handle_approval_task(task_id, action, user.user_id, notes)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "success", "action": action}

@router.get("/optimizations")
async def get_workflow_optimizations(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Get AI-powered optimization suggestions for workflows"""
    tenant_id = user.tenant_id or "default_tenant"
    workflows = db.query(Workflow).filter(Workflow.tenant_id == tenant_id).all()
    
    suggestions = []
    
    for wf in workflows:
        # Heuristic 1: Low success rate
        if wf.success_rate < 98.0:
            suggestions.append({
                "id": f"opt_success_{wf.id}",
                "workflow_id": wf.id,
                "workflow_name": wf.name,
                "type": "reliability",
                "severity": "high",
                "message": f"Success rate is {wf.success_rate}%. Consider increasing retry attempts or adding error handlers.",
                "action": "Configure Retries"
            })
            
        # Heuristic 2: High frequency (mock)
        if wf.runs_today > 10:
             suggestions.append({
                "id": f"opt_scale_{wf.id}",
                "workflow_id": wf.id,
                "workflow_name": wf.name,
                "type": "performance",
                "severity": "medium",
                "message": f"High usage detected ({wf.runs_today} runs). Consider enabling batch processing to reduce overhead.",
                "action": "Enable Batching"
            })
            
    # Default message if no specific insights
    if not suggestions:
        suggestions.append({
            "id": "opt_gen_1",
            "type": "general",
            "severity": "low",
            "message": "All workflows are running smoothly. No optimizations needed at this time.",
            "action": "View Analytics"
        })
        
    return suggestions
