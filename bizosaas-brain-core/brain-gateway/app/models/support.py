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
    
    messages = relationship("TicketMessage", back_populates="ticket", cascade="all, delete-orphan")

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
            "metadata": self.metadata_json,
            "messages": [m.to_dict() for m in self.messages]
        }

class TicketMessage(Base):
    __tablename__ = "support_ticket_messages"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    ticket_id = Column(GUID, ForeignKey("support_tickets.id", ondelete="CASCADE"), nullable=False)
    sender_id = Column(GUID, ForeignKey("users.id"), nullable=True) # Null if system/AI
    sender_type = Column(String(20), default="user", nullable=False) # user, agent, ai, system
    
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    
    ticket = relationship("SupportTicket", back_populates="messages")

    def to_dict(self):
        return {
            "id": str(self.id),
            "ticket_id": str(self.ticket_id),
            "sender_id": str(self.sender_id) if self.sender_id else None,
            "sender_type": self.sender_type,
            "content": self.content,
            "created_at": self.created_at.isoformat()
        }
