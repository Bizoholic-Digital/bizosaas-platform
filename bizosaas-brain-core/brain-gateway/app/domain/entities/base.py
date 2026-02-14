from datetime import datetime
from typing import Optional, TypeVar, Generic
from pydantic import BaseModel, Field
import uuid

T = TypeVar('T')

class BaseEntity(BaseModel):
    """
    Base generic entity for all domain objects.
    Enforces tenant isolation and audit fields.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = Field(..., description="Multi-tenancy isolation field")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = {
        "validate_assignment": True,
        "arbitrary_types_allowed": True
    }

    def update(self, data: dict):
        """Update entity fields with provided data"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
