from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Dict, Any, Optional
from pydantic import BaseModel
from app.dependencies import get_current_user
from app.domain.ports.identity_port import AuthenticatedUser
from app.services.agent_orchestrator import agent_orchestrator

router = APIRouter(prefix="/api/collaboration", tags=["collaboration"])

class CollaborationRequest(BaseModel):
    task: str
    context: Optional[Dict[str, Any]] = None

@router.post("/orchestrate")
async def orchestrate_task(
    request: CollaborationRequest,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Submit a complex task to the Master Orchestrator, which will 
    delegate sub-tasks to specialized agents.
    """
    result = await agent_orchestrator.process_request(
        user_request=request.task,
        user=user,
        context=request.context
    )
    return result
