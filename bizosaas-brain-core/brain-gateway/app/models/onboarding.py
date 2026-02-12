from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship
from .utils import GUID
from .base import Base
import uuid
from datetime import datetime

class OnboardingSession(Base):
    """
    Tracks the onboarding progress for a tenant.
    Used by AdminPrime for briefings and WorkflowDiscovery for identifying gaps.
    """
    __tablename__ = "onboarding_sessions"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(GUID, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    current_step = Column(String(50), default="welcome")
    
    # Stores selected MCPs, business profile info, etc.
    # Structure: {"selectedMcps": ["gtm", "woocommerce", ...], "business_profile": {...}}
    tools = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    tenant = relationship("Tenant")
