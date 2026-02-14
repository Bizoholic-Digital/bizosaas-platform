from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.domain.services.workflow_service import workflow_service
from app.core.tenant import get_tenant_id
import logging

router = APIRouter(prefix="/social", tags=["Social Content"])
logger = logging.getLogger(__name__)

class SocialPostRequest(BaseModel):
    platform: str
    topic: str
    persona_id: Optional[str] = None
    scheduled_at: Optional[str] = None
    require_approval: bool = True
    as_thread: bool = False
    context: Optional[str] = None

@router.post("/generate")
async def generate_social_content(
    request: SocialPostRequest,
    tenant_id: str = Depends(get_tenant_id)
):
    """Trigger a social media content generation workflow."""
    try:
        workflow_id = f"social-{request.platform}-{tenant_id}-{int(logging.root.process)}" # Simplified ID
        params = request.dict()
        params["tenant_id"] = tenant_id
        
        await workflow_service.start_workflow(
            "SocialContentWorkflow",
            params,
            workflow_id=workflow_id,
            task_queue="brain-tasks"
        )
        return {"workflow_id": workflow_id, "status": "started"}
    except Exception as e:
        logger.error(f"Failed to start social workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{workflow_id}")
async def get_social_workflow_status(workflow_id: str):
    """Query the status of a social content workflow."""
    try:
        status = await workflow_service.query_workflow(workflow_id, "get_status")
        draft = await workflow_service.query_workflow(workflow_id, "get_draft")
        return {"workflow_id": workflow_id, "status": status, "draft": draft}
    except Exception as e:
        logger.error(f"Failed to query social workflow: {e}")
        raise HTTPException(status_code=404, detail="Workflow not found or inaccessible")

@router.post("/approve/{workflow_id}")
async def approve_social_post(workflow_id: str, notes: Optional[str] = None):
    """Approve a social post for scheduling."""
    try:
        await workflow_service.signal_workflow(workflow_id, "approve_post", notes)
        return {"status": "approved"}
    except Exception as e:
        logger.error(f"Failed to signal approval: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reject/{workflow_id}")
async def reject_social_post(workflow_id: str, notes: str):
    """Reject a social post and request revision."""
    try:
        await workflow_service.signal_workflow(workflow_id, "request_revision", notes)
        return {"status": "revision_requested"}
    except Exception as e:
        logger.error(f"Failed to signal rejection: {e}")
        raise HTTPException(status_code=500, detail=str(e))
