from sqlalchemy import Column, String, Boolean, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .base import Base
from .utils import GUID

class TagConfig(Base):
    __tablename__ = "tag_configs"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(GUID, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    
    container_id = Column(String(50), nullable=False) # GTM-XXXXXXX
    label = Column(String(100), nullable=True) # e.g. "Main Website"
    environment = Column(String(20), default="production", nullable=False) # production, staging, development
    is_active = Column(Boolean, default=True, nullable=False)
    config = Column(JSON, nullable=True) # Custom data layer vars, consent settings
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    tenant = relationship("Tenant", backref="tag_configs")

    def to_dict(self):
        return {
            "id": str(self.id),
            "tenant_id": str(self.tenant_id),
            "container_id": self.container_id,
            "label": self.label,
            "environment": self.environment,
            "is_active": self.is_active,
            "config": self.config,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
