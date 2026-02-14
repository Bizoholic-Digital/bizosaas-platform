"""
Predictive Analytics API
Exposes predictive insights to the Admin Portal.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.dependencies import get_db, require_role
from app.services.predictive_analytics import PredictiveAnalyticsEngine
from app.domain.ports.identity_port import AuthenticatedUser

router = APIRouter(prefix="/api/admin/predictions", tags=["predictive-analytics"])


@router.get("/tenant/{tenant_id}/churn-risk")
async def get_tenant_churn_risk(
    tenant_id: str,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get churn risk prediction for a specific tenant.
    """
    engine = PredictiveAnalyticsEngine(db)
    try:
        prediction = await engine.predict_churn_risk(tenant_id)
        return vars(prediction)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/workflow/{workflow_id}/failure-risk")
async def get_workflow_failure_risk(
    workflow_id: str,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get failure risk prediction for a specific workflow.
    """
    engine = PredictiveAnalyticsEngine(db)
    prediction = await engine.predict_workflow_failure(workflow_id)
    return vars(prediction)


@router.get("/platform/growth-forecast")
async def get_growth_forecast(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get 30-day platform growth forecast.
    """
    engine = PredictiveAnalyticsEngine(db)
    forecast = await engine.forecast_platform_growth()
    return forecast
