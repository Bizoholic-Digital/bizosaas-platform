from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models.workflow import Workflow
from domain.ports.identity_port import AuthenticatedUser
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/workflows", tags=["workflows"])

class WorkflowConfigUpdate(BaseModel):
    retries: Optional[int] = None
    timeout: Optional[int] = None
    notifyOnError: Optional[bool] = None
    priority: Optional[str] = None

@router.get("/")
async def list_workflows(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """List all workflows for the tenant"""
    tenant_id = user.tenant_id or "default_tenant"
    workflows = db.query(Workflow).filter(Workflow.tenant_id == tenant_id).all()
    
    if not workflows:
        # Seed some default workflows if none exist
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
        db.add_all(default_wfs)
        db.commit()
        workflows = default_wfs
        
    return [wf.to_dict() for wf in workflows]

@router.post("/{workflow_id}/config")
async def update_workflow_config(
    workflow_id: str,
    config: WorkflowConfigUpdate,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Update workflow execution configuration"""
    tenant_id = user.tenant_id or "default_tenant"
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id, Workflow.tenant_id == tenant_id).first()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Update nested config
    if not workflow.config:
        workflow.config = {}
    
    current_config = dict(workflow.config)
    if config.retries is not None: current_config["retries"] = config.retries
    if config.timeout is not None: current_config["timeout"] = config.timeout
    if config.notifyOnError is not None: current_config["notifyOnError"] = config.notifyOnError
    if config.priority is not None: current_config["priority"] = config.priority
    
    workflow.config = current_config
    db.commit()
    
    return {"status": "success", "message": "Configuration updated"}

@router.post("/{workflow_id}/toggle")
async def toggle_workflow_status(
    workflow_id: str,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Toggle workflow running/paused status"""
    tenant_id = user.tenant_id or "default_tenant"
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id, Workflow.tenant_id == tenant_id).first()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow.status = "paused" if workflow.status == "running" else "running"
    db.commit()
    
    return {"status": "success", "new_status": workflow.status}
