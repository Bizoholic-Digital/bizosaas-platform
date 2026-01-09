from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer, JSON, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .utils import GUID
import uuid
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    # Association table for Partners managing Tenants
    partner_managed_tenants = Table(
        'partner_managed_tenants',
        Base.metadata,
        Column('user_id', GUID, ForeignKey('users.id'), primary_key=True),
        Column('tenant_id', GUID, ForeignKey('tenants.id'), primary_key=True)
    )
    
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    email = Column(String(320), unique=True, nullable=False, index=True)
    hashed_password = Column(String(1024), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    role = Column(String(20), default="user", nullable=False)
    login_count = Column(Integer, default=0, nullable=False)
    two_factor_enabled = Column(Boolean, default=False, nullable=False)
    marketing_consent = Column(Boolean, default=False, nullable=False)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    
    # Optional fields from existing schema
    phone = Column(String(20), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    permissions = Column(JSON, nullable=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    last_activity_at = Column(DateTime(timezone=True), nullable=True)
    allowed_platforms = Column(JSON, nullable=True)
    platform_preferences = Column(JSON, nullable=True)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    password_changed_at = Column(DateTime(timezone=True), nullable=True)
    two_factor_secret = Column(String(32), nullable=True)
    terms_accepted_at = Column(DateTime(timezone=True), nullable=True)
    privacy_accepted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    tenant_id = Column(GUID, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    tenant = relationship("Tenant", back_populates="users")
    mcp_installations = relationship("UserMcpInstallation", back_populates="user", cascade="all, delete-orphan")
    managed_tenants = relationship(
        "Tenant",
        secondary="partner_managed_tenants",
        back_populates="managers",
        lazy="selectin"
    )
    audit_logs = relationship("AuditLog", back_populates="user")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(100), nullable=False) # e.g. "PROMOTE_TO_PARTNER"
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    ip_address = Column(String(45), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")

class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    domain = Column(String(100), unique=True, nullable=True)
    status = Column(String(20), default="active", nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    max_users = Column(Integer, default=10, nullable=False)
    api_rate_limit = Column(Integer, default=1000, nullable=False)
    
    # Optional fields from existing schema
    subscription_plan = Column(String(50), nullable=True)
    subscription_status = Column(String(20), nullable=True)
    trial_ends_at = Column(DateTime(timezone=True), nullable=True)
    allowed_platforms = Column(JSON, nullable=True)
    settings = Column(JSON, nullable=True)
    features = Column(JSON, nullable=True)
    
    # Relationships
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    managers = relationship(
        "User",
        secondary="partner_managed_tenants",
        back_populates="managed_tenants",
        lazy="selectin"
    )
