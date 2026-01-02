from sqlalchemy import Column, String, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .user import Base

class TenantConfig(Base):
    __tablename__ = "tenant_configs"

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), primary_key=True)
    
    portal_title = Column(String, default="BizOSaaS Client Portal")
    logo_url = Column(String, nullable=True)
    favicon_url = Column(String, nullable=True)
    
    # Theme Colors
    primary_color = Column(String, default="#2563eb") # blue-600
    secondary_color = Column(String, default="#475569") # slate-600
    
    # Typography
    font_family = Column(String, default="Inter")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to Tenant
    tenant = relationship("Tenant", backref="config")
