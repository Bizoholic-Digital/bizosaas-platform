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

@router.post("/{workflow_id}/toggle")
async def toggle_workflow_status(
    workflow_id: str,
    service: WorkflowService = Depends(get_workflow_service),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Toggle workflow running/paused status"""
    tenant_id = user.tenant_id or "default_tenant"
    new_status = await service.toggle_status(tenant_id, workflow_id)
    
    if not new_status:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return {"status": "success", "new_status": new_status}

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
