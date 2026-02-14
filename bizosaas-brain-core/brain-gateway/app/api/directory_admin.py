"""
Directory Administration API
Exposes fine-tuning and task management capabilities for the Business Directory.
"""

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from uuid import UUID

from app.dependencies import get_db, require_role
from app.services.directory_admin_service import DirectoryTaskService, DirectoryFineTuner
from app.domain.ports.identity_port import AuthenticatedUser

router = APIRouter(prefix="/api/admin/directory", tags=["directory-admin"])


@router.get("/stats")
async def get_directory_admin_stats(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Get high-level statistics for directory management."""
    task_service = DirectoryTaskService(db)
    return await task_service.get_crawling_stats()


@router.post("/tasks/seo-audit")
async def trigger_seo_audit(
    listing_ids: Optional[List[UUID]] = None,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Trigger an SEO audit for listings."""
    task_service = DirectoryTaskService(db)
    return await task_service.run_seo_audit(listing_ids)


@router.get("/claims")
@router.get("/claims/audit")
async def audit_claims(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Audit pending claim requests."""
    task_service = DirectoryTaskService(db)
    return await task_service.audit_pending_claims()


@router.get("/config")
async def get_fine_tuning_config(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Get the current fine-tuning configuration for directory agents."""
    return DirectoryFineTuner.get_config()


@router.patch("/config")
async def update_fine_tuning_config(
    new_config: Dict[str, Any],
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Update the fine-tuning configuration for directory agents."""
    return DirectoryFineTuner.update_config(new_config)


@router.post("/claims/{claim_id}/approve")
async def approve_claim(
    claim_id: UUID,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Approve a business claim request."""
    task_service = DirectoryTaskService(db)
    try:
        return await task_service.approve_claim(claim_id, user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/claims/{claim_id}/reject")
async def reject_claim(
    claim_id: UUID,
    reason: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Reject a business claim request."""
    task_service = DirectoryTaskService(db)
    try:
        return await task_service.reject_claim(claim_id, user.id, reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
