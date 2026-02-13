from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user, get_workflow_port
from domain.ports.identity_port import AuthenticatedUser
from datetime import datetime

router = APIRouter(prefix="/api/content", tags=["content"])

class ContentCreateRequest(BaseModel):
    topic: str
    persona_id: Optional[str] = None
    target_cms: Optional[str] = "wagtail"
    require_approval: bool = True

class ApprovalRequest(BaseModel):
    workflow_id: str
    phase: str
    notes: Optional[str] = ""

@router.post("/create")
async def create_content(
    request: ContentCreateRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
    workflow_port = Depends(get_workflow_port)
):
    tenant_id = str(current_user.tenant_id or current_user.id)
    workflow_id = f"content-{tenant_id}-{datetime.now().strftime('%Y%m%d%H%M')}"
    
    try:
        await workflow_port.start_workflow(
            workflow_name="ContentCreationWorkflow",
            workflow_id=workflow_id,
            task_queue="brain-tasks",
            args=[{
                "tenant_id": tenant_id,
                "topic": request.topic,
                "persona_id": request.persona_id,
                "target_cms": request.target_cms,
                "require_approval": request.require_approval
            }]
        )
        return {"status": "success", "workflow_id": workflow_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/approve")
async def approve_content(
    request: ApprovalRequest,
    workflow_port = Depends(get_workflow_port)
):
    try:
        await workflow_port.signal_workflow(
            workflow_id=request.workflow_id,
            signal_name="approve_phase",
            args=[request.phase, request.notes]
        )
        return {"status": "success", "message": f"Phase {request.phase} approved."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reject")
async def reject_content(
    request: ApprovalRequest,
    workflow_port = Depends(get_workflow_port)
):
    try:
        await workflow_port.signal_workflow(
            workflow_id=request.workflow_id,
            signal_name="request_revision",
            args=[request.phase, request.notes]
        )
        return {"status": "success", "message": f"Revision requested for {request.phase}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{workflow_id}")
async def get_content_status(
    workflow_id: str,
    workflow_port = Depends(get_workflow_port)
):
    try:
        phase = await workflow_port.query_workflow(
            workflow_id=workflow_id,
            query_type="get_current_phase"
        )
        status = await workflow_port.get_workflow_status(workflow_id)
        return {"workflow_id": workflow_id, "phase": phase, "status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
