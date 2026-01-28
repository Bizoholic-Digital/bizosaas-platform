"""
Workflow Monitoring Service
Tracks execution metrics, detects failures, and provides observability for agentic workflows.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from enum import Enum

logger = logging.getLogger(__name__)


class WorkflowExecutionStatus(str, Enum):
    """Workflow execution status"""
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


@dataclass
class WorkflowMetrics:
    """Metrics for a single workflow execution"""
    workflow_id: str
    workflow_name: str
    execution_id: str
    status: WorkflowExecutionStatus
    started_at: datetime
    completed_at: Optional[datetime]
    duration_seconds: Optional[float]
    steps_total: int
    steps_completed: int
    steps_failed: int
    error_message: Optional[str]
    cost_estimate: float
    tenant_id: Optional[str]


@dataclass
class AggregatedMetrics:
    """Aggregated metrics across all workflows"""
    total_executions: int
    successful_executions: int
    failed_executions: int
    success_rate: float
    average_duration_seconds: float
    total_cost: float
    executions_by_type: Dict[str, int]
    executions_by_status: Dict[str, int]
    top_failing_workflows: List[Dict[str, Any]]


class WorkflowMonitor:
    """
    Monitors workflow execution and provides observability.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def record_execution_start(
        self,
        workflow_id: str,
        workflow_name: str,
        execution_id: str,
        tenant_id: Optional[str] = None
    ) -> str:
        """
        Record the start of a workflow execution.
        """
        from app.models.workflow_execution import WorkflowExecution
        
        execution = WorkflowExecution(
            id=execution_id,
            workflow_id=workflow_id,
            workflow_name=workflow_name,
            tenant_id=tenant_id,
            status=WorkflowExecutionStatus.RUNNING.value,
            started_at=datetime.utcnow(),
            steps_total=0,
            steps_completed=0,
            steps_failed=0,
            cost_estimate=0.0
        )
        
        self.db.add(execution)
        self.db.commit()
        
        logger.info(f"Started tracking execution: {execution_id} for workflow: {workflow_name}")
        return execution_id
    
    async def record_execution_complete(
        self,
        execution_id: str,
        steps_completed: int,
        cost_estimate: float
    ):
        """
        Record successful completion of a workflow execution.
        """
        from app.models.workflow_execution import WorkflowExecution
        
        execution = self.db.query(WorkflowExecution).filter(
            WorkflowExecution.id == execution_id
        ).first()
        
        if not execution:
            logger.error(f"Execution not found: {execution_id}")
            return
        
        execution.status = WorkflowExecutionStatus.COMPLETED.value
        execution.completed_at = datetime.utcnow()
        execution.steps_completed = steps_completed
        execution.cost_estimate = cost_estimate
        execution.duration_seconds = (execution.completed_at - execution.started_at).total_seconds()
        
        self.db.commit()
        
        logger.info(f"Execution completed: {execution_id} in {execution.duration_seconds}s")
    
    async def record_execution_failure(
        self,
        execution_id: str,
        error_message: str,
        failed_step: Optional[int] = None
    ):
        """
        Record failure of a workflow execution.
        """
        from app.models.workflow_execution import WorkflowExecution
        
        execution = self.db.query(WorkflowExecution).filter(
            WorkflowExecution.id == execution_id
        ).first()
        
        if not execution:
            logger.error(f"Execution not found: {execution_id}")
            return
        
        execution.status = WorkflowExecutionStatus.FAILED.value
        execution.completed_at = datetime.utcnow()
        execution.error_message = error_message
        execution.failed_step = failed_step
        execution.duration_seconds = (execution.completed_at - execution.started_at).total_seconds()
        
        self.db.commit()
        
        logger.error(f"Execution failed: {execution_id} - {error_message}")
        
        # Trigger alert if failure rate is high
        await self._check_failure_threshold(execution.workflow_id)
    
    async def get_workflow_metrics(
        self,
        workflow_id: str,
        time_range_hours: int = 24
    ) -> Dict[str, Any]:
        """
        Get metrics for a specific workflow.
        """
        from app.models.workflow_execution import WorkflowExecution
        
        since = datetime.utcnow() - timedelta(hours=time_range_hours)
        
        executions = self.db.query(WorkflowExecution).filter(
            and_(
                WorkflowExecution.workflow_id == workflow_id,
                WorkflowExecution.started_at >= since
            )
        ).all()
        
        if not executions:
            return {
                "workflow_id": workflow_id,
                "total_executions": 0,
                "success_rate": 0.0,
                "average_duration": 0.0
            }
        
        total = len(executions)
        successful = sum(1 for e in executions if e.status == WorkflowExecutionStatus.COMPLETED.value)
        failed = sum(1 for e in executions if e.status == WorkflowExecutionStatus.FAILED.value)
        
        completed_executions = [e for e in executions if e.duration_seconds is not None]
        avg_duration = sum(e.duration_seconds for e in completed_executions) / len(completed_executions) if completed_executions else 0
        
        total_cost = sum(e.cost_estimate or 0 for e in executions)
        
        return {
            "workflow_id": workflow_id,
            "workflow_name": executions[0].workflow_name if executions else "Unknown",
            "time_range_hours": time_range_hours,
            "total_executions": total,
            "successful_executions": successful,
            "failed_executions": failed,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "average_duration_seconds": avg_duration,
            "total_cost": total_cost,
            "recent_failures": [
                {
                    "execution_id": e.id,
                    "error": e.error_message,
                    "timestamp": e.completed_at.isoformat() if e.completed_at else None
                }
                for e in executions if e.status == WorkflowExecutionStatus.FAILED.value
            ][-5:]  # Last 5 failures
        }
    
    async def get_aggregated_metrics(
        self,
        time_range_hours: int = 24
    ) -> AggregatedMetrics:
        """
        Get aggregated metrics across all workflows.
        """
        from app.models.workflow_execution import WorkflowExecution
        from app.models.workflow import Workflow
        
        since = datetime.utcnow() - timedelta(hours=time_range_hours)
        
        executions = self.db.query(WorkflowExecution).filter(
            WorkflowExecution.started_at >= since
        ).all()
        
        total = len(executions)
        successful = sum(1 for e in executions if e.status == WorkflowExecutionStatus.COMPLETED.value)
        failed = sum(1 for e in executions if e.status == WorkflowExecutionStatus.FAILED.value)
        
        completed_executions = [e for e in executions if e.duration_seconds is not None]
        avg_duration = sum(e.duration_seconds for e in completed_executions) / len(completed_executions) if completed_executions else 0
        
        total_cost = sum(e.cost_estimate or 0 for e in executions)
        
        # Group by workflow type
        workflows = self.db.query(Workflow).all()
        workflow_types = {w.id: w.type for w in workflows}
        
        executions_by_type = {}
        for execution in executions:
            wf_type = workflow_types.get(execution.workflow_id, "Unknown")
            executions_by_type[wf_type] = executions_by_type.get(wf_type, 0) + 1
        
        # Group by status
        executions_by_status = {}
        for execution in executions:
            status = execution.status
            executions_by_status[status] = executions_by_status.get(status, 0) + 1
        
        # Find top failing workflows
        failure_counts = {}
        for execution in executions:
            if execution.status == WorkflowExecutionStatus.FAILED.value:
                failure_counts[execution.workflow_id] = failure_counts.get(execution.workflow_id, 0) + 1
        
        top_failing = sorted(
            [{"workflow_id": wf_id, "workflow_name": workflows[0].name if workflows else "Unknown", "failure_count": count}
             for wf_id, count in failure_counts.items()],
            key=lambda x: x["failure_count"],
            reverse=True
        )[:5]
        
        return AggregatedMetrics(
            total_executions=total,
            successful_executions=successful,
            failed_executions=failed,
            success_rate=(successful / total * 100) if total > 0 else 0,
            average_duration_seconds=avg_duration,
            total_cost=total_cost,
            executions_by_type=executions_by_type,
            executions_by_status=executions_by_status,
            top_failing_workflows=top_failing
        )
    
    async def _check_failure_threshold(self, workflow_id: str):
        """
        Check if workflow failure rate exceeds threshold and trigger alert.
        """
        metrics = await self.get_workflow_metrics(workflow_id, time_range_hours=1)
        
        if metrics["total_executions"] >= 5 and metrics["success_rate"] < 50:
            # High failure rate detected
            await self._send_alert(
                workflow_id=workflow_id,
                alert_type="high_failure_rate",
                message=f"Workflow {metrics['workflow_name']} has {metrics['success_rate']:.1f}% success rate in the last hour",
                severity="critical"
            )
    
    async def _send_alert(
        self,
        workflow_id: str,
        alert_type: str,
        message: str,
        severity: str = "warning"
    ):
        """
        Send alert to admin notification system.
        """
        logger.warning(f"ALERT [{severity.upper()}]: {alert_type} - {message}")
        
        # TODO: Integrate with admin notification service
        # await notification_service.send_alert({
        #     "workflow_id": workflow_id,
        #     "type": alert_type,
        #     "message": message,
        #     "severity": severity,
        #     "timestamp": datetime.utcnow().isoformat()
        # })


async def get_workflow_monitor(db: Session) -> WorkflowMonitor:
    """Helper to get workflow monitor instance."""
    return WorkflowMonitor(db)
