"""
Tenant-related Pydantic models
"""
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
from pydantic import Field, HttpUrl
from .base import BaseModel, TimestampedModel


class TenantStatus(str, Enum):
    """Tenant status"""
    ACTIVE = "active"
    TRIAL = "trial"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"


class SubscriptionPlan(str, Enum):
    """Subscription plans"""
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional" 
    ENTERPRISE = "enterprise"


class TenantBase(BaseModel):
    """Base tenant model"""
    name: str = Field(..., min_length=1, max_length=200)
    domain: str = Field(..., min_length=1, max_length=100)
    website: Optional[HttpUrl] = None
    industry: Optional[str] = Field(None, max_length=100)
    company_size: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=500)
    logo_url: Optional[str] = None


class TenantCreate(TenantBase):
    """Tenant creation model"""
    admin_email: str = Field(..., description="Admin user email")
    admin_first_name: str = Field(..., min_length=1, max_length=100)
    admin_last_name: str = Field(..., min_length=1, max_length=100)
    admin_password: str = Field(..., min_length=8, max_length=128)


class TenantUpdate(BaseModel):
    """Tenant update model"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    website: Optional[HttpUrl] = None
    industry: Optional[str] = Field(None, max_length=100)
    company_size: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=500)
    logo_url: Optional[str] = None


class Tenant(TenantBase, TimestampedModel):
    """Tenant model for API responses"""
    id: int
    status: TenantStatus = TenantStatus.TRIAL
    subscription_plan: SubscriptionPlan = SubscriptionPlan.FREE
    trial_ends_at: Optional[datetime] = None
    subscription_ends_at: Optional[datetime] = None
    settings: Dict[str, Any] = Field(default_factory=dict)
    usage_limits: Dict[str, int] = Field(default_factory=dict)
    current_usage: Dict[str, int] = Field(default_factory=dict)


class TenantSettings(BaseModel):
    """Tenant settings model"""
    branding: Dict[str, Any] = Field(default_factory=dict)
    notifications: Dict[str, bool] = Field(default_factory=dict)
    integrations: Dict[str, Any] = Field(default_factory=dict)
    security: Dict[str, Any] = Field(default_factory=dict)


class TenantUsage(BaseModel):
    """Tenant usage statistics"""
    tenant_id: int
    period: str  # month, week, day
    campaigns_created: int = 0
    leads_processed: int = 0
    ai_requests: int = 0
    storage_used_mb: int = 0
    api_calls: int = 0
    reports_generated: int = 0


class TenantInvite(BaseModel):
    """Tenant invitation model"""
    email: str
    role: str = "user"
    message: Optional[str] = None


class TenantInviteResponse(BaseModel):
    """Tenant invitation response"""
    invite_id: str
    email: str
    tenant_name: str
    invited_by: str
    expires_at: datetime