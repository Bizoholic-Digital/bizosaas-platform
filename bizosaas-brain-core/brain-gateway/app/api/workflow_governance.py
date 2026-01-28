"""
Workflow Governance API
Handles admin approval, rejection, and refinement of agent-proposed workflows.
"""

from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
import logging

from app.dependencies import get_db, require_role
from app.models.workflow import Workflow, WorkflowProposal
from domain.ports.identity_port import AuthenticatedUser

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin/workflows", tags=["admin-workflows"])


class WorkflowApprovalRequest(BaseModel):
    """Request to approve a proposed workflow"""
    notes: Optional[str] = None
    config_overrides: Optional[Dict[str, Any]] = None


class WorkflowRejectionRequest(BaseModel):
    """Request to reject a proposed workflow"""
    reason: str
    archive: bool = True


class WorkflowRefinementRequest(BaseModel):
    """Request refinement of a proposed workflow"""
    feedback: str
    suggested_changes: Optional[Dict[str, Any]] = None


class WorkflowProposalCreate(BaseModel):
    """Agent-submitted workflow proposal"""
    name: str
    description: str
    type: str
    category: str
    workflow_definition: Dict[str, Any]  # JSON/YAML blueprint
    estimated_cost: Optional[float] = None
    impact_analysis: Optional[str] = None
    discovered_by: str = "autonomous_agent"


@router.post("/{workflow_id}/approve")
async def approve_workflow(
    workflow_id: str,
    request: WorkflowApprovalRequest,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Approve an agent-proposed workflow and transition it to Active status.
    This triggers deployment to Temporal for execution.
    """
    proposal = db.query(WorkflowProposal).filter(
        WorkflowProposal.id == workflow_id,
        WorkflowProposal.status == "proposed"
    ).first()
    
    if not proposal:
        raise HTTPException(status_code=404, detail="Workflow proposal not found or already processed")
    
    # Create active workflow from proposal
    workflow = Workflow(
        tenant_id="platform",  # Platform-level workflow
        name=proposal.name,
        type=proposal.type,
        status="active",
        description=proposal.description,
        config=request.config_overrides or proposal.workflow_definition.get("config", {}),
        workflow_blueprint=proposal.workflow_definition,
        approved_by=user.user_id,
        approved_at=datetime.utcnow()
    )
    
    # Update proposal status
    proposal.status = "approved"
    proposal.approved_by = user.user_id
    proposal.approved_at = datetime.utcnow()
    proposal.admin_notes = request.notes
    
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    
    # Deploy to Temporal
    deployment_status = "queued"
    temporal_workflow_id = None
    
    try:
        from app.services.temporal_executor import deploy_approved_workflow
        temporal_workflow_id = await deploy_approved_workflow(
            str(workflow.id),
            proposal.workflow_definition
        )
        deployment_status = "deployed"
        logger.info(f"Workflow {workflow.id} deployed to Temporal: {temporal_workflow_id}")
    except Exception as e:
        logger.error(f"Failed to deploy workflow to Temporal: {e}")
        deployment_status = "deployment_failed"
        # Don't fail the approval, just log the error
    
    return {
        "status": "success",
        "message": f"Workflow '{proposal.name}' approved and deployed",
        "workflow_id": workflow.id,
        "temporal_workflow_id": temporal_workflow_id,
        "deployment_status": deployment_status
    }


@router.post("/{workflow_id}/reject")
async def reject_workflow(
    workflow_id: str,
    request: WorkflowRejectionRequest,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Reject an agent-proposed workflow and optionally archive it.
    """
    proposal = db.query(WorkflowProposal).filter(
        WorkflowProposal.id == workflow_id,
        WorkflowProposal.status == "proposed"
    ).first()
    
    if not proposal:
        raise HTTPException(status_code=404, detail="Workflow proposal not found or already processed")
    
    proposal.status = "rejected" if request.archive else "archived"
    proposal.rejected_by = user.user_id
    proposal.rejected_at = datetime.utcnow()
    proposal.rejection_reason = request.reason
    
    db.commit()
    
    return {
        "status": "success",
        "message": f"Workflow '{proposal.name}' rejected",
        "archived": request.archive
    }


@router.post("/{workflow_id}/refine")
async def request_refinement(
    workflow_id: str,
    request: WorkflowRefinementRequest,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Request refinement of a proposed workflow.
    This sends feedback back to the proposing agent for redesign.
    """
    proposal = db.query(WorkflowProposal).filter(
        WorkflowProposal.id == workflow_id,
        WorkflowProposal.status == "proposed"
    ).first()
    
    if not proposal:
        raise HTTPException(status_code=404, detail="Workflow proposal not found or already processed")
    
    proposal.status = "refinement_requested"
    proposal.admin_feedback = request.feedback
    proposal.suggested_changes = request.suggested_changes
    proposal.refinement_requested_at = datetime.utcnow()
    
    db.commit()
    
    # TODO: Notify the proposing agent via message queue
    # await agent_notifier.send_refinement_request(proposal.discovered_by, proposal.id, request.feedback)
    
    return {
        "status": "success",
        "message": f"Refinement requested for workflow '{proposal.name}'",
        "feedback_sent_to": proposal.discovered_by
    }


@router.get("/registry")
async def get_workflow_registry(
    status: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Fetch the complete workflow inventory including active, proposed, and required workflows.
    """
    query = db.query(WorkflowProposal)
    
    if status:
        query = query.filter(WorkflowProposal.status == status)
    if category:
        query = query.filter(WorkflowProposal.category == category)
    
    proposals = query.order_by(WorkflowProposal.created_at.desc()).all()
    
    return {
        "total": len(proposals),
        "workflows": [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "type": p.type,
                "category": p.category,
                "status": p.status,
                "discovered_by": p.discovered_by,
                "created_at": p.created_at.isoformat(),
                "estimated_cost": p.estimated_cost,
                "impact_analysis": p.impact_analysis
            }
            for p in proposals
        ]
    }


@router.post("/registry")
async def propose_workflow(
    proposal: WorkflowProposalCreate,
    db: Session = Depends(get_db),
    # Note: This endpoint is called by AI agents, not admins
    # Authentication should verify agent identity
):
    """
    Agent endpoint to propose a new workflow.
    This is called by autonomous agents when they identify a new automation opportunity.
    """
    workflow_proposal = WorkflowProposal(
        name=proposal.name,
        description=proposal.description,
        type=proposal.type,
        category=proposal.category,
        status="proposed",
        workflow_definition=proposal.workflow_definition,
        estimated_cost=proposal.estimated_cost,
        impact_analysis=proposal.impact_analysis,
        discovered_by=proposal.discovered_by,
        created_at=datetime.utcnow()
    )
    
    db.add(workflow_proposal)
    db.commit()
    db.refresh(workflow_proposal)
    
    return {
        "status": "success",
        "message": f"Workflow proposal '{proposal.name}' submitted for admin review",
        "proposal_id": workflow_proposal.id,
        "review_url": f"/admin/dashboard/workflows?tab=hitl&id={workflow_proposal.id}"
    }


@router.patch("/{workflow_id}/config")
async def update_workflow_config(
    workflow_id: str,
    config: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Update configuration parameters for an active workflow.
    """
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.status == "active"
    ).first()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Active workflow not found")
    
    workflow.config = {**workflow.config, **config}
    workflow.updated_at = datetime.utcnow()
    
    db.commit()
    
    # TODO: Trigger Temporal workflow update
    # await temporal_client.update_workflow(workflow_id, config)
    
    return {
        "status": "success",
        "message": f"Configuration updated for workflow '{workflow.name}'",
        "updated_config": workflow.config
    }
