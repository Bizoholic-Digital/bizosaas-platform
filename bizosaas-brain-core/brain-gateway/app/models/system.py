from sqlalchemy import Column, String, JSON, DateTime, Boolean
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from .base import Base

class SystemSetting(Base):
    __tablename__ = "system_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String(100), unique=True, nullable=False, index=True) # e.g. "registrar:namecheap:config"
    value = Column(JSON, nullable=False)
    description = Column(String(255), nullable=True)
    is_secret = Column(Boolean, default=False) # If true, only store in Vault, this is just a reminder
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
