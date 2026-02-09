"""
Multi-tenant Isolation Testing API
Exposes security testing capabilities to the Admin Portal.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.dependencies import get_db, require_role
from app.services.isolation_testing import MultiTenantIsolationTester
from domain.ports.identity_port import AuthenticatedUser

router = APIRouter(prefix="/api/admin/security/isolation", tags=["security-testing"])


@router.post("/run-suite")
async def run_isolation_tests(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Trigger a full isolation security test suite.
    """
    tester = MultiTenantIsolationTester(db)
    results = await tester.run_isolation_suite()
    
    return results


@router.get("/status")
async def get_isolation_status(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get the latest isolation status overview.
    """
    # In production, this might fetch the last run from a table 'security_audit_logs'
    tester = MultiTenantIsolationTester(db)
    results = await tester.run_isolation_suite() # For demo, we run it live
    
    return {
        "status": results["overall_status"],
        "last_checked": results["timestamp"],
        "failed_checks": results["failures"]
    }
