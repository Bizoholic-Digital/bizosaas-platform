"""
Alerts Administration API.

Endpoints for managing alert rules and viewing alert history.
"""

from typing import List, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.dependencies import get_db, require_role
from app.domain.ports.identity_port import AuthenticatedUser
from app.config.alert_rules import alert_config, get_default_alert_rules
from app.models.alert_history import AlertHistory

router = APIRouter(prefix="/api/admin/alerts", tags=["alerts-admin"])


@router.get("/rules")
async def get_alert_rules(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get all configured alert rules.
    """
    rules = get_default_alert_rules()
    return {
        "enabled": alert_config.alerts_enabled,
        "rules": rules
    }

@router.put("/config")
async def update_alert_config(
    enabled: Optional[bool] = None,
    webhook_url: Optional[str] = None,
    email_enabled: Optional[bool] = None,
    email_to: Optional[str] = None,
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Update global alert configuration.
    Note: In a real app, this would update dynamic settings or .env file.
    For this MVP, we'll just return the values as if updated, or update runtime config if possible.
    """
    # This is a bit hacky for pydantic settings, but sufficient for MVP API contract
    if enabled is not None:
        alert_config.alerts_enabled = enabled
    if webhook_url is not None:
        alert_config.alert_webhook_url = webhook_url
    if email_enabled is not None:
        alert_config.alert_email_enabled = email_enabled
    if email_to is not None:
        alert_config.alert_email_to = email_to
        
    return {
        "status": "updated",
        "config": {
            "enabled": alert_config.alerts_enabled,
            "webhook_url": alert_config.alert_webhook_url,
            "email_enabled": alert_config.alert_email_enabled,
            "email_to": alert_config.alert_email_to
        }
    }

@router.get("/history")
async def get_alert_history(
    limit: int = 50,
    status: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get alert history log.
    """
    query = db.query(AlertHistory)
    
    if status:
        query = query.filter(AlertHistory.status == status)
    
    if category:
        query = query.filter(AlertHistory.category == category)
        
    alerts = query.order_by(desc(AlertHistory.created_at)).limit(limit).all()
    
    return [a.to_dict() for a in alerts]

@router.post("/history/{alert_id}/resolve")
async def resolve_alert(
    alert_id: str,
    note: Optional[str] = None,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Mark an alert as resolved.
    """
    alert = db.query(AlertHistory).filter(AlertHistory.id == alert_id).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
        
    alert.status = "resolved"
    alert.resolved_at = datetime.utcnow()
    alert.resolved_by = user.email
    alert.resolution_note = note
    
    db.commit()
    
    return alert.to_dict()
