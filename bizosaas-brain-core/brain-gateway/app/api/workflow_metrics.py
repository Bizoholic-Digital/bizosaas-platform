"""
Workflow Metrics API
Provides endpoints for workflow execution metrics and monitoring.
"""

from fastapi import APIRouter, Depends, Query
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.dependencies import get_db, require_role
from app.services.workflow_monitor import WorkflowMonitor
from domain.ports.identity_port import AuthenticatedUser

router = APIRouter(prefix="/api/admin/workflows/metrics", tags=["workflow-metrics"])


@router.get("/aggregated")
async def get_aggregated_metrics(
    time_range_hours: int = Query(24, ge=1, le=168),  # 1 hour to 7 days
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get aggregated metrics across all workflows.
    """
    monitor = WorkflowMonitor(db)
    metrics = await monitor.get_aggregated_metrics(time_range_hours)
    
    return {
        "time_range_hours": time_range_hours,
        "metrics": {
            "total_executions": metrics.total_executions,
            "successful_executions": metrics.successful_executions,
            "failed_executions": metrics.failed_executions,
            "success_rate": round(metrics.success_rate, 2),
            "average_duration_seconds": round(metrics.average_duration_seconds, 2),
            "total_cost": round(metrics.total_cost, 2),
            "executions_by_type": metrics.executions_by_type,
            "executions_by_status": metrics.executions_by_status,
            "top_failing_workflows": metrics.top_failing_workflows
        }
    }


@router.get("/{workflow_id}")
async def get_workflow_metrics(
    workflow_id: str,
    time_range_hours: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get metrics for a specific workflow.
    """
    monitor = WorkflowMonitor(db)
    metrics = await monitor.get_workflow_metrics(workflow_id, time_range_hours)
    
    return metrics


@router.get("/executions/recent")
async def get_recent_executions(
    limit: int = Query(50, ge=1, le=200),
    status: Optional[str] = None,
    workflow_id: Optional[str] = None,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get recent workflow executions with optional filtering.
    """
    from app.models.workflow_execution import WorkflowExecution
    
    query = db.query(WorkflowExecution)
    
    if status:
        query = query.filter(WorkflowExecution.status == status)
    if workflow_id:
        query = query.filter(WorkflowExecution.workflow_id == workflow_id)
    
    executions = query.order_by(
        WorkflowExecution.started_at.desc()
    ).limit(limit).all()
    
    return {
        "total": len(executions),
        "executions": [e.to_dict() for e in executions]
    }


@router.get("/executions/{execution_id}")
async def get_execution_details(
    execution_id: str,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get detailed information about a specific execution.
    """
    from app.models.workflow_execution import WorkflowExecution
    
    execution = db.query(WorkflowExecution).filter(
        WorkflowExecution.id == execution_id
    ).first()
    
    if not execution:
        return {"error": "Execution not found"}, 404
    
    return execution.to_dict()


@router.get("/health/overview")
async def get_health_overview(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get overall health status of the agentic workflow system.
    """
    monitor = WorkflowMonitor(db)
    
    # Get metrics for different time windows
    last_hour = await monitor.get_aggregated_metrics(time_range_hours=1)
    last_day = await monitor.get_aggregated_metrics(time_range_hours=24)
    last_week = await monitor.get_aggregated_metrics(time_range_hours=168)
    
    # Determine overall health status
    health_status = "healthy"
    if last_hour.success_rate < 80:
        health_status = "degraded"
    if last_hour.success_rate < 50:
        health_status = "critical"
    
    return {
        "status": health_status,
        "timestamp": datetime.utcnow().isoformat(),
        "metrics": {
            "last_hour": {
                "executions": last_hour.total_executions,
                "success_rate": round(last_hour.success_rate, 2),
                "failures": last_hour.failed_executions
            },
            "last_24_hours": {
                "executions": last_day.total_executions,
                "success_rate": round(last_day.success_rate, 2),
                "failures": last_day.failed_executions,
                "total_cost": round(last_day.total_cost, 2)
            },
            "last_7_days": {
                "executions": last_week.total_executions,
                "success_rate": round(last_week.success_rate, 2),
                "failures": last_week.failed_executions,
                "total_cost": round(last_week.total_cost, 2)
            }
        },
        "alerts": {
            "high_failure_rate": last_hour.success_rate < 80,
            "critical_failure_rate": last_hour.success_rate < 50,
            "top_failing_workflows": last_day.top_failing_workflows[:3]
        }
    }
