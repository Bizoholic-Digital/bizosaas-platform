from sqlalchemy import Column, String, JSON, DateTime, ForeignKey, Boolean, Float, Integer, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .user import Base
from .utils import GUID

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    type = Column(String) # 'Marketing', 'E-commerce', 'Content', etc.
    status = Column(String, default="running") # 'running', 'paused', 'error', 'active'
    category = Column(String, default="all")  # 'infrastructure', 'hitl', 'all'
    config = Column(JSON, default={}) # retries, timeout, etc.
    workflow_blueprint = Column(JSON)  # Complete workflow definition from agent proposal
    last_run = Column(DateTime, nullable=True)
    success_rate = Column(Float, default=100.0)
    runs_today = Column(Integer, default=0)
    
    # Approval tracking
    approved_by = Column(String)
    approved_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "status": self.status,
            "category": self.category,
            "config": self.config,
            "workflow_blueprint": self.workflow_blueprint,
            "lastRun": self.last_run.isoformat() if self.last_run else None,
            "successRate": self.success_rate,
            "runsToday": self.runs_today,
            "approvedBy": self.approved_by,
            "approvedAt": self.approved_at.isoformat() if self.approved_at else None,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None
        }
