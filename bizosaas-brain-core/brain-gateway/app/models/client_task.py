from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime
from app.database import Base

class ClientTask(Base):
    __tablename__ = "client_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Task Details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="todo", nullable=False)  # todo, in_progress, review, done
    priority = Column(String(20), default="medium", nullable=False) # low, medium, high
    
    # AI & Agents
    created_by_agent_id = Column(String(100), nullable=True) # e.g., 'marketing-agent'
    assigned_agent_id = Column(String(100), nullable=True)   # If AI is working on it
    
    # Dates
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Metadata for Agents (e.g. "Draft Content", "Campaign ID")
    metadata_json = Column(JSON, nullable=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "tenant_id": str(self.tenant_id),
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "created_by_agent_id": self.created_by_agent_id,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata_json
        }
