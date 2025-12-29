from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum

from .user import Base

class CampaignStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    name = Column(String(255), nullable=False)
    status = Column(String(50), default=CampaignStatus.DRAFT, nullable=False)
    goal = Column(String(255), nullable=True) # e.g. "Increase Sales", "Brand Awareness"
    
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    channels = relationship("CampaignChannel", back_populates="campaign", cascade="all, delete-orphan")

class CampaignChannel(Base):
    __tablename__ = "campaign_channels"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    
    channel_type = Column(String(50), nullable=False) # email, social, sms
    connector_id = Column(String(100), nullable=True) # e.g. "mailchimp"
    remote_id = Column(String(255), nullable=True) # ID in external system
    
    status = Column(String(50), default="pending", nullable=False)
    config = Column(JSON, default={}, nullable=False) # specific config like subject, template_id
    stats = Column(JSON, default={}, nullable=False) # local copy of stats
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    campaign = relationship("Campaign", back_populates="channels")
