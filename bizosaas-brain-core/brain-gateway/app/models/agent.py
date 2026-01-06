from sqlalchemy import Column, String, JSON, DateTime, ForeignKey, Boolean
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

    # Relationship to optimizations
    optimizations = relationship("AgentOptimization", back_populates="agent", cascade="all, delete-orphan")

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

class AgentOptimization(Base):
    __tablename__ = "agent_optimizations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String, ForeignKey("agents.id"))
    type = Column(String)  # 'prompt', 'performance', 'cost', 'latency'
    description = Column(String)
    improvement = Column(String)
    impact = Column(String)  # 'High', 'Medium', 'Low'
    status = Column(String, default="pending")  # 'pending', 'approved', 'rejected', 'executed'
    auto_execute = Column(Boolean, default=False)
    suggested_at = Column(DateTime, default=datetime.utcnow)
    executed_at = Column(DateTime, nullable=True)

    agent = relationship("Agent", back_populates="optimizations")

    def to_dict(self):
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "type": self.type,
            "description": self.description,
            "improvement": self.improvement,
            "impact": self.impact,
            "status": self.status,
            "auto_execute": self.auto_execute,
            "suggestedAt": self.suggested_at.isoformat() if self.suggested_at else None,
            "executedAt": self.executed_at.isoformat() if self.executed_at else None
        }
