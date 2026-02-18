from sqlalchemy import Column, String, JSON, DateTime, Boolean, Text
from datetime import datetime
import uuid
from .base import Base

class PromptTemplate(Base):
    """
    Model for storing versioned and categorized prompt templates.
    Supports system-wide defaults and tenant-specific overrides.
    """
    __tablename__ = "prompt_templates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, index=True)
    category = Column(String, default="instruction", index=True) # persona, instruction, formatting, rag_grounding
    template_text = Column(Text, nullable=False)
    variables = Column(JSON, default={}) # List of expected variables like ["tenant_name", "business_goal"]
    strategy = Column(String, default="basic") # basic, chain_of_thought, few_shot, self_refine
    is_default = Column(Boolean, default=False)
    tenant_id = Column(String, index=True, nullable=True) # Null means platform-wide default
    version = Column(String, default="1.0.0")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "templateText": self.template_text,
            "variables": self.variables,
            "strategy": self.strategy,
            "isDefault": self.is_default,
            "tenantId": self.tenant_id,
            "version": self.version,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None
        }
