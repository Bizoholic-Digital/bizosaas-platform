from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .user import Base

class AuditLog(Base):
    """
    Centralized audit log for security and compliance (GDPR, SOC2).
    Tracks every significant action within the platform.
    """
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(50), index=True, nullable=False)
    user_id = Column(String(50), index=True, nullable=True)
    
    action = Column(String(100), nullable=False)  # e.g., "mcp_install", "data_export", "user_login"
    resource_type = Column(String(50), nullable=True)  # e.g., "mcp", "campaign", "user"
    resource_id = Column(String(100), nullable=True)
    
    status = Column(String(20))  # success, failure
    details = Column(JSON, nullable=True)  # Contextual data
    
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

class ConsentRecord(Base):
    """
    Documented user consent for privacy and integration permissions.
    Critical for GDPR compliance.
    """
    __tablename__ = "consent_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(50), index=True, nullable=False)
    tenant_id = Column(String(50), index=True, nullable=False)
    
    consent_type = Column(String(50), nullable=False)  # e.g., "marketing", "wp_plugin_discovery", "third_party_sync"
    granted = Column(Boolean, default=False, nullable=False)
    version = Column(String(20), default="1.0")
    
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Stores the exact text presented to the user at the time of consent
    presented_text = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
