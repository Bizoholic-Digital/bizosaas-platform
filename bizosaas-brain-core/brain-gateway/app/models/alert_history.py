"""
Alert history model.

Tracks occurrences of alerts, their resolution status, and associated metadata.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class AlertHistory(Base):
    """Model for tracking alert history."""
    __tablename__ = "alert_history"

    id = Column(String, primary_key=True)  # UUID
    
    # Alert details
    rule_id = Column(String, nullable=False, index=True)
    rule_name = Column(String, nullable=False)
    severity = Column(String, nullable=False)  # low, medium, high, critical
    category = Column(String, nullable=False)  # performance, cost, security, marketing
    
    # Trigger details
    metric_name = Column(String, nullable=False)
    metric_value = Column(Float, nullable=False)
    threshold_value = Column(Float, nullable=False)
    message = Column(Text, nullable=False)
    details = Column(JSON, default={})  # Additional context
    
    # Status
    status = Column(String, default="active")  # active, resolved, acknowledged
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolved_by = Column(String, nullable=True)
    resolution_note = Column(Text, nullable=True)
    
    # Notifications
    notification_sent = Column(Boolean, default=False)
    notification_channels = Column(JSON, default=[])  # List of channels sent to
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        """Convert object to dictionary."""
        return {
            "id": self.id,
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "severity": self.severity,
            "category": self.category,
            "metric_name": self.metric_name,
            "metric_value": self.metric_value,
            "threshold_value": self.threshold_value,
            "message": self.message,
            "details": self.details,
            "status": self.status,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "resolved_by": self.resolved_by,
            "notification_sent": self.notification_sent,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
