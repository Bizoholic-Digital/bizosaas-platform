import logging
from fastapi import APIRouter, Depends, HTTPException, Request, Header
from typing import Dict, Any, List, Optional
from app.dependencies import get_workflow_service
from app.domain.services.workflow_service import WorkflowService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/triggers", tags=["autonomous-triggers"])

@router.post("/webhook/{path:path}")
async def handle_external_webhook(
    path: str,
    request: Request,
    workflow_service: WorkflowService = Depends(get_workflow_service),
    x_bizos_key: Optional[str] = Header(None)
):
    """
    Universal webhook listener for autonomous workflow triggers.
    Inbound requests are matched against registered workflow triggers.
    """
    # Normalize path
    full_path = f"/{path.strip('/')}"
    logger.info(f"Received autonomous trigger request on path: {full_path}")
    
    # Get request body
    try:
        payload = await request.json()
    except:
        payload = {}
        
    # Find matching workflows
    matched_workflows = await workflow_service.find_workflows_by_trigger(
        trigger_type="webhook",
        match_key="path",
        match_value=full_path
    )
    
    if not matched_workflows:
        logger.warning(f"No active workflow found and running for webhook path: {full_path}")
        return {"status": "ignored", "reason": "no_matching_workflow"}
    
    triggered_runs = []
    for wf in matched_workflows:
        # Check security key if defined in trigger
        # (This is a simple implementation, usually would use more robust auth)
        trigger_config = next(t for t in wf.triggers if t.get("path") == full_path)
        secret_key = trigger_config.get("secret_key")
        
        if secret_key and x_bizos_key != secret_key:
            logger.warning(f"Unauthorized trigger attempt for workflow {wf.id}")
            continue
            
        logger.info(f"Triggering workflow {wf.name} (ID: {wf.id}) from autonomous webhook")
        result = await workflow_service.trigger_workflow(
            tenant_id=wf.tenant_id,
            workflow_id=str(wf.id),
            params={"source": "webhook", "path": full_path, "payload": payload}
        )
        triggered_runs.append({"workflow_id": str(wf.id), "result": result})
        
    return {
        "status": "processed",
        "matches": len(matched_workflows),
        "executions": triggered_runs
    }

@router.get("/config/{workflow_id}")
async def get_workflow_triggers(
    workflow_id: str,
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """Get configured triggers for a specific workflow"""
    # Note: In a real app, we'd check tenant_id too
    all_wfs = await workflow_service.list_workflows(tenant_id=None) # Need to fix list_workflows to support all or pass tenant
    # For now fetching specific workflow via DB
    from app.models.workflow import Workflow
    wf = workflow_service.db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {"workflow_id": workflow_id, "triggers": wf.triggers}

@router.post("/config/{workflow_id}")
async def configure_triggers(
    workflow_id: str,
    triggers: List[Dict[str, Any]],
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """Update autonomous triggers for a workflow"""
    # For now using ID to find tenant
    from app.models.workflow import Workflow
    wf = workflow_service.db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
        
    success = await workflow_service.set_triggers(wf.tenant_id, workflow_id, triggers)
    return {"status": "success", "updated": success}
