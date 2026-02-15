"""
Platform Metrics Model
Stores aggregated platform-wide analytics snapshots.
"""

from sqlalchemy import Column, String, DateTime, JSON, Float, Integer
from sqlalchemy.sql import func
from datetime import datetime
from .base import Base


class PlatformMetrics(Base):
    """
    Stores periodic snapshots of platform-wide metrics for historical tracking.
    """
    __tablename__ = "platform_metrics"

    id = Column(String, primary_key=True)
    
    # Snapshot metadata
    snapshot_type = Column(String, nullable=False, index=True)  # hourly, daily, weekly
    snapshot_time = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Workflow metrics
    total_workflow_executions = Column(Integer, default=0)
    workflow_success_rate = Column(Float, default=0.0)
    avg_workflow_duration = Column(Float, default=0.0)
    total_workflow_cost = Column(Float, default=0.0)
    
    # Tenant metrics
    total_tenants = Column(Integer, default=0)
    active_tenants = Column(Integer, default=0)
    
    # Campaign metrics
    total_campaigns = Column(Integer, default=0)
    active_campaigns = Column(Integer, default=0)
    platform_ctr = Column(Float, default=0.0)
    platform_conversion_rate = Column(Float, default=0.0)
    
    # Detailed breakdown (JSON)
    workflow_breakdown = Column(JSON, default={})
    tenant_breakdown = Column(JSON, default=[])
    insights = Column(JSON, default=[])
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "snapshot_type": self.snapshot_type,
            "snapshot_time": self.snapshot_time.isoformat() if self.snapshot_time else None,
            "workflow_metrics": {
                "total_executions": self.total_workflow_executions,
                "success_rate": self.workflow_success_rate,
                "avg_duration": self.avg_workflow_duration,
                "total_cost": self.total_workflow_cost,
                "breakdown": self.workflow_breakdown
            },
            "tenant_metrics": {
                "total_tenants": self.total_tenants,
                "active_tenants": self.active_tenants,
                "breakdown": self.tenant_breakdown
            },
            "campaign_metrics": {
                "total_campaigns": self.total_campaigns,
                "active_campaigns": self.active_campaigns,
                "platform_ctr": self.platform_ctr,
                "platform_conversion_rate": self.platform_conversion_rate
            },
            "insights": self.insights,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
