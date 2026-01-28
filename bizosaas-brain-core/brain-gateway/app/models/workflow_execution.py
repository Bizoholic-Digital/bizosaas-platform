"""
Workflow Execution Model
Stores execution history and metrics for workflow runs.
"""

from sqlalchemy import Column, String, DateTime, Integer, Float, Text
from sqlalchemy.sql import func
from app.models.base import Base


class WorkflowExecution(Base):
    """
    Tracks individual workflow executions for monitoring and analytics.
    """
    __tablename__ = "workflow_executions"

    id = Column(String, primary_key=True)  # Temporal workflow execution ID
    workflow_id = Column(String, nullable=False, index=True)
    workflow_name = Column(String, nullable=False)
    tenant_id = Column(String, index=True)
    
    # Execution status
    status = Column(String, nullable=False, index=True)  # running, completed, failed, timeout, cancelled
    
    # Timing
    started_at = Column(DateTime(timezone=True), nullable=False, index=True)
    completed_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Float)
    
    # Step tracking
    steps_total = Column(Integer, default=0)
    steps_completed = Column(Integer, default=0)
    steps_failed = Column(Integer, default=0)
    failed_step = Column(Integer)
    
    # Error tracking
    error_message = Column(Text)
    error_stack_trace = Column(Text)
    
    # Cost tracking
    cost_estimate = Column(Float, default=0.0)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "workflow_id": self.workflow_id,
            "workflow_name": self.workflow_name,
            "tenant_id": self.tenant_id,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": self.duration_seconds,
            "steps_total": self.steps_total,
            "steps_completed": self.steps_completed,
            "steps_failed": self.steps_failed,
            "error_message": self.error_message,
            "cost_estimate": self.cost_estimate
        }
