from sqlalchemy import Column, String, JSON, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .user import Base

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    type = Column(String) # 'Marketing', 'E-commerce', 'Content', etc.
    status = Column(String, default="running") # 'running', 'paused', 'error'
    config = Column(JSON, default={}) # retries, timeout, etc.
    last_run = Column(DateTime, nullable=True)
    success_rate = Column(JSON, default=100.0)
    runs_today = Column(JSON, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "status": self.status,
            "config": self.config,
            "lastRun": self.last_run.isoformat() if self.last_run else None,
            "successRate": self.success_rate,
            "runsToday": self.runs_today,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None
        }
