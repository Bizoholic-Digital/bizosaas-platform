from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer, JSON, Text
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .user import Base
from .utils import GUID

class McpCategory(Base):
    __tablename__ = "mcp_categories"
    
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)  # Lucide icon name
    sort_order = Column(Integer, default=0)
    
    # Relationships
    mcps = relationship("McpRegistry", back_populates="category")

class McpRegistry(Base):
    __tablename__ = "mcp_registry"
    
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    author = Column(String(100), nullable=True)
    homepage_url = Column(String(255), nullable=True)
    source_url = Column(String(255), nullable=True)
    
    # Configuration
    category_id = Column(GUID, ForeignKey("mcp_categories.id"), nullable=False)
    capabilities = Column(JSON, default=list)  # ["products", "orders", "analytics"]
    mcp_config = Column(JSON, nullable=False)  # { "type": "docker", "image": "...", "env": [...] }
    is_official = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    rating = Column(Integer, default=0)
    install_count = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    category = relationship("McpCategory", back_populates="mcps")
    installations = relationship("UserMcpInstallation", back_populates="mcp")

class UserMcpInstallation(Base):
    __tablename__ = "user_mcp_installations"
    
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    mcp_id = Column(GUID, ForeignKey("mcp_registry.id", ondelete="CASCADE"), nullable=False)
    
    status = Column(String(20), default="pending", nullable=False)  # pending, installed, configured, error, stopped
    config = Column(JSON, nullable=True)  # User-specific config overrides
    credentials_path = Column(String(255), nullable=True)  # Vault path
    error_message = Column(Text, nullable=True)
    
    last_health_check = Column(DateTime(timezone=True), nullable=True)
    is_healthy = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="mcp_installations")
    mcp = relationship("McpRegistry", back_populates="installations")
