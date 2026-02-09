"""
Predictive Analytics Service
Provides predictive insights for tenant churn, workflow reliability, and system performance.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import math
from sqlalchemy.orm import Session
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Prediction:
    """A predictive insight"""
    target_id: str
    target_type: str  # 'tenant', 'workflow', 'system'
    prediction_type: str  # 'churn_risk', 'failure_probability', 'growth'
    score: float  # 0.0 to 1.0 (probability)
    confidence: float  # 0.0 to 1.0
    factors: List[str]
    forecast_date: datetime


class PredictiveAnalyticsEngine:
    """
    Engine for generating predictive insights using statistical models.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def predict_churn_risk(self, tenant_id: str) -> Prediction:
        """
        Predict churn risk for a specific tenant based on activity patterns.
        """
        from app.models.user import User
        # Placeholder for activity log model
        # from app.models.activity import ActivityLog
        
        user = self.db.query(User).filter(User.id == tenant_id).first()
        if not user:
            raise ValueError(f"Tenant not found: {tenant_id}")
        
        # Factor 1: Login recency (High impact)
        days_since_login = (datetime.utcnow() - user.last_login).days if user.last_login else 30
        recency_score = min(days_since_login / 30, 1.0)
        
        # Factor 2: Workflow usage (Medium impact)
        # Using a placeholder value since we need to aggregate workflow executions by tenant
        # In production, this would query the workflow_executions table
        workflow_usage_score = 0.5  # Neutral default
        
        # Calculate probablity
        probability = (recency_score * 0.7) + ((1 - workflow_usage_score) * 0.3)
        
        factors = []
        if days_since_login > 14:
            factors.append(f" inactivity ({days_since_login} days)")
        
        return Prediction(
            target_id=tenant_id,
            target_type="tenant",
            prediction_type="churn_risk",
            score=probability,
            confidence=0.8,  # Heuristic model has moderate confidence
            factors=factors,
            forecast_date=datetime.utcnow() + timedelta(days=30)
        )
    
    async def predict_workflow_failure(self, workflow_id: str) -> Prediction:
        """
        Predict failure probability for a workflow based on recent history.
        """
        from app.services.workflow_monitor import WorkflowMonitor
        
        monitor = WorkflowMonitor(self.db)
        metrics = await monitor.get_workflow_metrics(workflow_id, time_range_hours=72)
        
        # Simple trend analysis: Is failure rate increasing?
        failure_rate = 1.0 - (metrics["success_rate"] / 100.0)
        
        factors = []
        if failure_rate > 0.1:
            factors.append("high_recent_failure_rate")
        
        return Prediction(
            target_id=workflow_id,
            target_type="workflow",
            prediction_type="failure_probability",
            score=failure_rate,
            confidence=0.9 if metrics["total_executions"] > 10 else 0.5,
            factors=factors,
            forecast_date=datetime.utcnow() + timedelta(hours=24)
        )
    
    async def forecast_platform_growth(self) -> Dict[str, Any]:
        """
        Forecast platform growth (tenants, workflows) for the next 30 days.
        """
        from app.models.user import User
        from app.models.workflow import Workflow
        
        # Simple linear regression (placeholder implementation)
        current_tenants = self.db.query(User).filter(User.role == "tenant").count()
        current_workflows = self.db.query(Workflow).count()
        
        # Assume 5% MoM growth for now
        projected_tenants = math.ceil(current_tenants * 1.05)
        projected_workflows = math.ceil(current_workflows * 1.05)
        
        return {
            "forecast_period": "30_days",
            "current_tenants": current_tenants,
            "projected_tenants": projected_tenants,
            "growth_rate": "5.0%",
            "current_workflows": current_workflows,
            "projected_workflows": projected_workflows,
            "confidence": "low_heuristic"
        }


async def get_predictive_engine(db: Session) -> PredictiveAnalyticsEngine:
    """Helper to get prediction engine instance."""
    return PredictiveAnalyticsEngine(db)
