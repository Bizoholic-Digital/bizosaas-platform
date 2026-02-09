from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, JSON, Text
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .base import Base
from .utils import GUID

class CampaignStatus:
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    DELETED = "deleted"

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(GUID, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    goal = Column(Text, nullable=True)
    status = Column(String(20), default=CampaignStatus.DRAFT, nullable=False)
    type = Column(String(50), nullable=True)
    
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    
    config = Column(JSON, nullable=True)
    results = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(GUID, ForeignKey("users.id"), nullable=True)

    # Relationships
    channels = relationship("CampaignChannel", back_populates="campaign", cascade="all, delete-orphan")
    analytics = relationship("CampaignAnalytics", back_populates="campaign", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": str(self.id),
            "tenant_id": str(self.tenant_id),
            "name": self.name,
            "goal": self.goal,
            "status": self.status,
            "type": self.type,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "config": self.config,
            "results": self.results,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": str(self.created_by) if self.created_by else None,
            "channels": [c.to_dict() for c in self.channels]
        }

class CampaignChannel(Base):
    __tablename__ = "campaign_channels"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    campaign_id = Column(GUID, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    channel_type = Column(String(50), nullable=False) # email, social, etc.
    connector_id = Column(String(100), nullable=False) # mailchimp, etc.
    status = Column(String(20), default="pending") # pending, synced, sent, error
    remote_id = Column(String(255), nullable=True) # external system id
    config = Column(JSON, nullable=True)
    stats = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    campaign = relationship("Campaign", back_populates="channels")

    def to_dict(self):
        return {
            "id": str(self.id),
            "campaign_id": str(self.campaign_id),
            "channel_type": self.channel_type,
            "connector_id": self.connector_id,
            "status": self.status,
            "remote_id": self.remote_id,
            "config": self.config,
            "stats": self.stats
        }

class CampaignAnalytics(Base):
    __tablename__ = "campaign_analytics"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    campaign_id = Column(GUID, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    metric_name = Column(String(50), nullable=False) # impressions, clicks, conversions
    metric_value = Column(Integer, default=0, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    
    # Relationships
    campaign = relationship("Campaign", back_populates="analytics")
