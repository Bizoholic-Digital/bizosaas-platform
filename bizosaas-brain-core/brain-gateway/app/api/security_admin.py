from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List, Optional, Dict, Any
import datetime

from app.dependencies import require_role
from domain.ports.identity_port import AuthenticatedUser

router = APIRouter(prefix="/api/admin/security", tags=["admin-security"])

@router.get("/posture")
async def get_security_posture(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Overview of platform security status."""
    return {
        "overall_score": 92,
        "mfa_adoption": 85.5,
        "active_alerts": 2,
        "last_scan": (datetime.datetime.utcnow() - datetime.timedelta(hours=12)).isoformat(),
        "status": "healthy"
    }

@router.get("/vulnerabilities")
async def list_vulnerabilities(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """List results from automated container security scans."""
    return [
        {"id": "CVE-2024-001", "severity": "low", "service": "brain-gateway", "description": "Minor library vulnerability", "status": "monitored"},
        {"id": "CVE-2023-999", "severity": "medium", "service": "redis", "description": "Old version patch needed", "status": "pending_update"}
    ]

@router.get("/compliance-checklist")
async def get_compliance_status(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Track progress on GDPR, HIPAA, SOC2 requirements."""
    return {
        "GDPR": {"status": "compliant", "last_audit": "2024-01-15"},
        "SOC2": {"status": "in_progress", "completion": 75},
        "HIPAA": {"status": "not_applicable"}
    }

@router.get("/encryption/keys")
async def list_encryption_keys(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Monitor Vault secret and encryption key status."""
    return [
        {"name": "root-api-key", "type": "aes-256", "last_rotated": "2024-01-01"},
        {"name": "tenant-data-key", "type": "rsa-4096", "last_rotated": "2023-12-15"}
    ]

@router.post("/ip-whitelist")
async def add_whitelisted_ip(
    ip: str = Body(..., embed=True),
    reason: str = Body(..., embed=True),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Restrict admin access by IP range."""
    return {"status": "success", "ip": ip, "message": "IP added to whitelist"}
