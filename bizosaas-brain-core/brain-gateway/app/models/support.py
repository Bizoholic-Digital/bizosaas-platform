from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .base import Base
from .utils import GUID

class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(GUID, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    creator_id = Column(GUID, ForeignKey("users.id"), nullable=False)
    assigned_partner_id = Column(GUID, ForeignKey("users.id"), nullable=True)
    
    subject = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(20), default="open", nullable=False) # open, in_progress, resolved, closed
    priority = Column(String(20), default="medium", nullable=False) # low, medium, high, urgent
    category = Column(String(50), nullable=True) # billing, technical, platform, account
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    metadata_json = Column(JSON, nullable=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "tenant_id": str(self.tenant_id),
            "creator_id": str(self.creator_id),
            "assigned_partner_id": str(self.assigned_partner_id) if self.assigned_partner_id else None,
            "subject": self.subject,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "category": self.category,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "metadata": self.metadata_json
        }
