from sqlalchemy import Column, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .user import Base  # Assuming user.py has the Base class

class Agent(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    role = Column(String)
    category = Column(String, default="general")
    status = Column(String, default="active")
    capabilities = Column(JSON, default=[])
    tools = Column(JSON, default=[])
    icon = Column(String, default="🤖")
    color = Column(String, default="#4f46e5")
    cost_tier = Column(String, default="standard")
    instructions = Column(String)  # System prompt
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String)  # User email/ID

    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "description": self.description,
            "role": self.role,
            "category": self.category,
            "status": self.status,
            "capabilities": self.capabilities,
            "tools": self.tools,
            "icon": self.icon,
            "color": self.color,
            "cost_tier": self.cost_tier,
            "instructions": self.instructions,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
            "createdBy": self.created_by
        }
