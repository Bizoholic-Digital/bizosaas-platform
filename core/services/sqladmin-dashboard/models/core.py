"""
Core Data Models for SQLAdmin Dashboard
Handles basic platform entities: tenants, users, organizations, sessions
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, JSON, ForeignKey, UUID, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class TenantStatus(enum.Enum):
    TRIAL = "trial"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

class UserRole(enum.Enum):
    SUPER_ADMIN = "super_admin"
    TENANT_ADMIN = "tenant_admin"
    MANAGER = "manager"
    USER = "user"
    VIEWER = "viewer"
    CLIENT = "client"

class SubscriptionPlan(enum.Enum):
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"

# Core tenant model
class TenantAdmin(Base):
    __tablename__ = "tenants"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(Enum(TenantStatus), default=TenantStatus.TRIAL)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Subscription details
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.FREE)
    subscription_status = Column(String(20), default="trial")
    trial_ends_at = Column(DateTime(timezone=True))
    subscription_ends_at = Column(DateTime(timezone=True))
    
    # Platform access
    allowed_platforms = Column(JSON, default=['bizoholic'])
    settings = Column(JSON, default={})
    
    # Business details
    company_name = Column(String(200))
    industry = Column(String(100))
    website = Column(String(255))
    phone = Column(String(20))
    address = Column(Text)
    billing_email = Column(String(255))
    
    # Limits and quotas
    user_limit = Column(Integer, default=5)
    storage_limit_gb = Column(Float, default=1.0)
    api_call_limit = Column(Integer, default=1000)
    
    # Relationships
    users = relationship("UserAdmin", back_populates="tenant", cascade="all, delete-orphan")
    organizations = relationship("OrganizationAdmin", back_populates="tenant", cascade="all, delete-orphan")

# Enhanced user model
class UserAdmin(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    # Personal details
    first_name = Column(String(50))
    last_name = Column(String(50))
    full_name = Column(String(100))  # Computed field
    phone = Column(String(20))
    avatar_url = Column(String(500))
    
    # Account details
    role = Column(Enum(UserRole), default=UserRole.USER)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    
    # Status and permissions
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime(timezone=True))
    
    # Security
    two_factor_enabled = Column(Boolean, default=False)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime(timezone=True))
    password_reset_token = Column(String(255))
    password_reset_expires = Column(DateTime(timezone=True))
    
    # Activity tracking
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime(timezone=True))
    login_count = Column(Integer, default=0)
    last_activity_at = Column(DateTime(timezone=True))
    
    # Preferences and permissions
    preferences = Column(JSON, default={})
    allowed_services = Column(JSON, default=[])
    permissions = Column(JSON, default=[])
    timezone = Column(String(50), default="UTC")
    language = Column(String(10), default="en")
    
    # Relationships
    tenant = relationship("TenantAdmin", back_populates="users")
    organization = relationship("OrganizationAdmin", back_populates="users")
    sessions = relationship("UserSessionAdmin", back_populates="user", cascade="all, delete-orphan")

# User sessions for authentication tracking
class UserSessionAdmin(Base):
    __tablename__ = "user_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Session details
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    refresh_token = Column(String(255), unique=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    last_accessed_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Session context
    ip_address = Column(String(45))
    user_agent = Column(Text)
    platform = Column(String(50), default="bizosaas")
    device_type = Column(String(50))  # mobile, desktop, tablet
    browser = Column(String(100))
    location = Column(String(200))
    
    # Status
    is_active = Column(Boolean, default=True)
    terminated_at = Column(DateTime(timezone=True))
    termination_reason = Column(String(100))  # logout, expired, revoked, etc.
    
    # Relationships
    user = relationship("UserAdmin", back_populates="sessions")

# Organizations for enterprise customers
class OrganizationAdmin(Base):
    __tablename__ = "organizations"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Organization details
    name = Column(String(200), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    
    # Business details
    industry = Column(String(100))
    company_size = Column(String(50))  # 1-10, 11-50, 51-200, etc.
    website = Column(String(255))
    email = Column(String(255))
    phone = Column(String(20))
    
    # Address
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100))
    
    # Settings and configuration
    logo_url = Column(String(500))
    settings = Column(JSON, default={})
    metadata = Column(JSON, default={})
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("TenantAdmin", back_populates="organizations")
    users = relationship("UserAdmin", back_populates="organization")

# API Keys for external access
class APIKeyAdmin(Base):
    __tablename__ = "api_keys"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Key details
    name = Column(String(100), nullable=False)
    key_hash = Column(String(255), nullable=False, unique=True)
    key_prefix = Column(String(20))  # First few chars for identification
    
    # Permissions and scope
    scopes = Column(JSON, default=[])  # List of allowed API scopes
    allowed_ips = Column(JSON, default=[])  # IP whitelist
    rate_limit = Column(Integer, default=1000)  # Requests per hour
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    last_used_at = Column(DateTime(timezone=True))
    last_used_ip = Column(String(45))
    
    # Status
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Metadata
    description = Column(Text)
    metadata = Column(JSON, default={})

# System configuration settings
class SystemConfigAdmin(Base):
    __tablename__ = "system_config"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    
    # Configuration details
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(JSON)
    data_type = Column(String(20), default="string")  # string, integer, boolean, json
    category = Column(String(50), default="general")
    
    # Metadata
    description = Column(Text)
    is_public = Column(Boolean, default=False)  # Can be accessed by non-admin users
    is_encrypted = Column(Boolean, default=False)  # Sensitive data
    
    # Management
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Validation
    validation_rules = Column(JSON, default={})  # JSON schema for validation
    default_value = Column(JSON)