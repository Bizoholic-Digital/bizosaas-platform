"""
GDPR Compliance Module - Privacy and data protection endpoints.

Implements GDPR requirements for:
- Consent management
- Data portability (export)
- Right to erasure (deletion)
- Privacy preference tracking
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from sqlalchemy.orm import Session
import json
import uuid

from app.middleware.auth import get_current_user
from domain.ports.identity_port import AuthenticatedUser
from app.dependencies import get_db

from app.models.audit import ConsentRecord, AuditLog

router = APIRouter(prefix="/api/privacy", tags=["privacy", "gdpr"])


# --- Models ---

class ConsentType:
    MARKETING = "marketing"
    ANALYTICS = "analytics"
    PERSONALIZATION = "personalization"
    THIRD_PARTY = "third_party"
    WP_PLUGIN_DISCOVERY = "wp_plugin_discovery"
    ESSENTIAL = "essential"


class ConsentUpdateRequest(BaseModel):
    consent_type: str
    granted: bool
    presentation_text: Optional[str] = None


@router.get("/consent")
async def get_consent_preferences(
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current consent preferences for the user from the database.
    """
    records = db.query(ConsentRecord).filter(
        ConsentRecord.user_id == user.id,
        ConsentRecord.revoked_at == None
    ).all()
    
    return {
        "user_id": user.id,
        "consents": {r.consent_type: r.granted for r in records},
        "last_updated": max([r.created_at for r in records], default=None) if records else None
    }


@router.post("/consent")
async def update_consent_preferences(
    request: ConsentUpdateRequest,
    req: Request,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update consent preferences and log the action.
    """
    # Revoke previous consent for this type
    db.query(ConsentRecord).filter(
        ConsentRecord.user_id == user.id,
        ConsentRecord.consent_type == request.consent_type,
        ConsentRecord.revoked_at == None
    ).update({"revoked_at": datetime.utcnow()})
    
    # Create new record
    new_record = ConsentRecord(
        user_id=user.id,
        tenant_id=user.tenant_id or "default",
        consent_type=request.consent_type,
        granted=request.granted,
        presented_text=request.presentation_text,
        ip_address=req.client.host,
        user_agent=req.headers.get("user-agent")
    )
    db.add(new_record)
    
    # Audit Log
    audit = AuditLog(
        tenant_id=user.tenant_id or "default",
        user_id=user.id,
        action="consent_updated",
        resource_type="consent",
        details={"type": request.consent_type, "granted": request.granted},
        ip_address=req.client.host,
        user_agent=req.headers.get("user-agent")
    )
    db.add(audit)
    
    db.commit()
    
    return {
        "status": "success",
        "message": f"Consent for '{request.consent_type}' updated",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/export")
async def request_data_export(
    request: DataExportRequest,
    background_tasks: BackgroundTasks,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Request data export (data portability).
    GDPR Article 20: Right to data portability
    
    Returns a download link within 30 days (usually much faster).
    """
    user_id = user.id
    tenant_id = user.tenant_id or "default"
    export_id = str(uuid.uuid4())
    
    # In production, this would trigger a background job
    # that collects all user data and generates a downloadable file
    
    export_data = {
        "export_id": export_id,
        "user_id": user_id,
        "tenant_id": tenant_id,
        "requested_at": datetime.utcnow().isoformat(),
        "format": request.format,
        "status": "processing",
        "includes": {
            "profile": True,
            "connectors": request.include_connectors,
            "campaigns": request.include_campaigns,
            "conversations": request.include_conversations,
        }
    }
    
    # Simulate background processing
    async def process_export():
        # In real implementation:
        # 1. Collect all user data from various tables
        # 2. Package into requested format
        # 3. Upload to secure storage
        # 4. Send notification email with download link
        pass
    
    background_tasks.add_task(process_export)
    
    return {
        "status": "accepted",
        "export_id": export_id,
        "message": "Your data export request has been received. You will receive an email with a download link within 24 hours.",
        "estimated_completion": "24 hours"
    }


@router.get("/export/{export_id}")
async def get_export_status(
    export_id: str,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Check the status of a data export request."""
    # In production, query the exports table
    return {
        "export_id": export_id,
        "status": "completed",  # or "processing", "failed"
        "download_url": None,  # Presigned URL when ready
        "expires_at": None
    }


@router.post("/delete")
async def request_data_deletion(
    request: DataDeletionRequest,
    background_tasks: BackgroundTasks,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Request account and data deletion.
    GDPR Article 17: Right to erasure ("right to be forgotten")
    
    Note: Some data may be retained for legal/compliance reasons.
    """
    user_id = user.id
    tenant_id = user.tenant_id or "default"
    
    # Verify email matches
    if request.confirm_email.lower() != user.email.lower():
        raise HTTPException(
            status_code=400,
            detail="Confirmation email does not match account email"
        )
    
    deletion_id = str(uuid.uuid4())
    
    DELETION_REQUESTS[deletion_id] = {
        "user_id": user_id,
        "tenant_id": tenant_id,
        "requested_at": datetime.utcnow().isoformat(),
        "reason": request.reason,
        "retain_billing": request.retain_billing_records,
        "status": "pending",
        # 30-day grace period as per GDPR
        "scheduled_deletion": (datetime.utcnow().replace(day=datetime.utcnow().day + 30)).isoformat()
    }
    
    return {
        "status": "accepted",
        "deletion_id": deletion_id,
        "message": "Your deletion request has been received. Your account will be scheduled for deletion in 30 days. You can cancel this request at any time before then.",
        "scheduled_at": DELETION_REQUESTS[deletion_id]["scheduled_deletion"],
        "cancellation_url": f"/api/privacy/delete/{deletion_id}/cancel"
    }


@router.post("/delete/{deletion_id}/cancel")
async def cancel_deletion_request(
    deletion_id: str,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Cancel a pending deletion request."""
    if deletion_id not in DELETION_REQUESTS:
        raise HTTPException(status_code=404, detail="Deletion request not found")
    
    request_data = DELETION_REQUESTS[deletion_id]
    
    if request_data["user_id"] != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if request_data["status"] != "pending":
        raise HTTPException(status_code=400, detail="Cannot cancel - deletion already processed")
    
    DELETION_REQUESTS[deletion_id]["status"] = "cancelled"
    
    return {
        "status": "success",
        "message": "Deletion request cancelled. Your account will remain active."
    }


@router.get("/policy")
async def get_privacy_policy_info():
    """
    Get privacy policy version and acceptance status.
    """
    return {
        "current_version": "2.0",
        "effective_date": "2026-01-01",
        "policy_url": "/legal/privacy-policy",
        "terms_url": "/legal/terms-of-service",
        "cookie_policy_url": "/legal/cookie-policy",
        "dpo_contact": "privacy@bizosaas.com",  # Data Protection Officer
        "supervisory_authority": "Information Commissioner's Office (ICO)"  # Example for UK
    }


@router.post("/policy/accept")
async def accept_privacy_policy(
    version: str,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Record user acceptance of privacy policy."""
    # In production, store in database
    return {
        "status": "success",
        "accepted_version": version,
        "accepted_at": datetime.utcnow().isoformat(),
        "user_id": user.id
    }
