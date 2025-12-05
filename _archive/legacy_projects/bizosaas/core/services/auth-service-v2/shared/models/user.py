"""
User-related Pydantic models
"""
from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import EmailStr, Field
from .base import BaseModel, TenantTimestampedModel


class UserRole(str, Enum):
    """User roles in the system"""
    SUPER_ADMIN = "super_admin"
    TENANT_ADMIN = "tenant_admin" 
    MANAGER = "manager"
    USER = "user"
    VIEWER = "viewer"


class UserStatus(str, Enum):
    """User account status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class UserBase(BaseModel):
    """Base user model with common fields"""
    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: UserRole = Field(default=UserRole.USER)
    is_active: bool = Field(default=True)
    phone: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    """User creation model"""
    password: str = Field(..., min_length=8, max_length=128)
    tenant_id: int = Field(..., description="Tenant ID for multi-tenancy")


class UserUpdate(BaseModel):
    """User update model"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    phone: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = None


class User(UserBase, TenantTimestampedModel):
    """User model for API responses"""
    id: int
    status: UserStatus = UserStatus.ACTIVE
    last_login: Optional[datetime] = None
    email_verified: bool = False
    two_factor_enabled: bool = False


class UserInDB(User):
    """User model with password hash (internal use)"""
    hashed_password: str
    email_verification_token: Optional[str] = None
    password_reset_token: Optional[str] = None
    two_factor_secret: Optional[str] = None


class UserLogin(BaseModel):
    """User login request"""
    email: EmailStr
    password: str
    remember_me: bool = False


class UserLoginResponse(BaseModel):
    """User login response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: User


class PasswordChange(BaseModel):
    """Password change request"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)


class PasswordReset(BaseModel):
    """Password reset request"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation"""
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)