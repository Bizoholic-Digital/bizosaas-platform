"""
Admin Prime API
Exposes the Admin Prime Copilot capabilities to the Admin Portal.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.dependencies import get_db, require_role
from app.services.admin_prime import AdminPrimeCopilot
from app.domain.ports.identity_port import AuthenticatedUser

router = APIRouter(prefix="/api/admin/prime", tags=["admin-prime"])


@router.get("/daily-brief")
async def get_daily_brief(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get the daily briefing from Admin Prime Copilot.
    Provides a comprehensive overview of platform health, insights, and action items.
    """
    copilot = AdminPrimeCopilot(db)
    brief = await copilot.generate_daily_brief()
    
    return brief


@router.get("/insights")
async def get_insights(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get AI-generated insights about the platform.
    """
    copilot = AdminPrimeCopilot(db)
    brief = await copilot.generate_daily_brief()
    
    return {
        "insights": brief["insights"],
        "generated_at": brief["generated_at"]
    }


@router.get("/action-items")
async def get_action_items(
    priority: Optional[str] = None,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get prioritized action items.
    """
    copilot = AdminPrimeCopilot(db)
    brief = await copilot.generate_daily_brief()
    
    action_items = brief["action_items"]
    
    if priority:
        action_items = [item for item in action_items if item["priority"] == priority]
    
    return {
        "total": len(action_items),
        "action_items": action_items
    }


@router.get("/recommendations")
async def get_recommendations(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get strategic recommendations from Admin Prime.
    """
    copilot = AdminPrimeCopilot(db)
    brief = await copilot.generate_daily_brief()
    
    return {
        "recommendations": brief["recommendations"],
        "generated_at": brief["generated_at"]
    }


@router.get("/health-summary")
async def get_health_summary(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get a quick health summary of all platform subsystems.
    """
    copilot = AdminPrimeCopilot(db)
    brief = await copilot.generate_daily_brief()
    
    return {
        "summary": brief["summary"],
        "overall_health": brief["summary"]["system_health"]["status"],
        "critical_issues": [
            item for item in brief["action_items"] 
            if item["priority"] == "high"
        ]
    }
