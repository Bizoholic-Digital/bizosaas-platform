from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from app.models.base import Base

class TrackedBacklink(Base):
    """
    Model for tracking proprietary backlink data over time.
    """
    __tablename__ = "tracked_backlinks"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, index=True)
    source_url = Column(String, index=True)
    target_url = Column(String, index=True)
    anchor_text = Column(String)
    is_dofollow = Column(Boolean, default=True)
    domain_rank = Column(Integer, default=0)
    is_broken = Column(Boolean, default=False)
    is_lost = Column(Boolean, default=False)
    lost_reason = Column(String, nullable=True)
    first_seen_at = Column(DateTime(timezone=True), server_default=func.now())
    last_seen_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    metadata_json = Column(JSON, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "source_url": self.source_url,
            "target_url": self.target_url,
            "anchor_text": self.anchor_text,
            "is_dofollow": self.is_dofollow,
            "domain_rank": self.domain_rank,
            "is_broken": self.is_broken,
            "is_lost": self.is_lost,
            "lost_reason": self.lost_reason,
            "first_seen_at": self.first_seen_at.isoformat() if self.first_seen_at else None,
            "last_seen_at": self.last_seen_at.isoformat() if self.last_seen_at else None,
            "metadata": self.metadata_json
        }
