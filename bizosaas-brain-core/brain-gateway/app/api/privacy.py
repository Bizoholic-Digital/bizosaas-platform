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

router = APIRouter(prefix="/api/privacy", tags=["privacy", "gdpr"])


# --- Models ---

class ConsentType:
    MARKETING = "marketing"
    ANALYTICS = "analytics"
    PERSONALIZATION = "personalization"
    THIRD_PARTY = "third_party"
    ESSENTIAL = "essential"  # Always required, cannot be declined


class ConsentRecord(BaseModel):
    consent_type: str
    granted: bool
    timestamp: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class ConsentUpdateRequest(BaseModel):
    marketing: bool = False
    analytics: bool = False
    personalization: bool = False
    third_party: bool = False


class DataExportRequest(BaseModel):
    format: str = "json"  # json or csv
    include_connectors: bool = True
    include_campaigns: bool = True
    include_conversations: bool = True


class DataDeletionRequest(BaseModel):
    confirm_email: EmailStr
    reason: Optional[str] = None
    retain_billing_records: bool = True  # Required for legal compliance


# --- In-memory storage (replace with DB in production) ---
CONSENT_STORE: Dict[str, Dict[str, ConsentRecord]] = {}
DELETION_REQUESTS: Dict[str, Dict[str, Any]] = {}


# --- Endpoints ---

@router.get("/consent")
async def get_consent_preferences(
    user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Get current consent preferences for the user.
    GDPR Article 7: Conditions for consent
    """
    user_id = user.id
    
    consents = CONSENT_STORE.get(user_id, {})
    
    return {
        "user_id": user_id,
        "consents": {
            "marketing": consents.get("marketing", {}).get("granted", False) if consents.get("marketing") else False,
            "analytics": consents.get("analytics", {}).get("granted", False) if consents.get("analytics") else False,
            "personalization": consents.get("personalization", {}).get("granted", False) if consents.get("personalization") else False,
            "third_party": consents.get("third_party", {}).get("granted", False) if consents.get("third_party") else False,
            "essential": True,  # Always true
        },
        "last_updated": max(
            [c.get("timestamp") for c in consents.values() if c.get("timestamp")],
            default=None
        )
    }


@router.post("/consent")
async def update_consent_preferences(
    request: ConsentUpdateRequest,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Update consent preferences.
    GDPR Article 7: Withdrawal of consent must be as easy as giving it.
    """
    user_id = user.id
    now = datetime.utcnow()
    
    if user_id not in CONSENT_STORE:
        CONSENT_STORE[user_id] = {}
    
    for consent_type, granted in [
        ("marketing", request.marketing),
        ("analytics", request.analytics),
        ("personalization", request.personalization),
        ("third_party", request.third_party),
    ]:
        CONSENT_STORE[user_id][consent_type] = {
            "granted": granted,
            "timestamp": now.isoformat(),
        }
    
    return {
        "status": "success",
        "message": "Consent preferences updated",
        "updated_at": now.isoformat()
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
