"""
Unified Authentication System for BizOSaas Platform
FastAPI-Users based SSO with JWT tokens, multi-tenant support, and role-based access
"""

import asyncio
import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any, Union
from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from fastapi import Depends, HTTPException
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
    CookieTransport
)
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, Text, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
import bcrypt
from jose import JWTError, jwt

# Import our vault client for secure configuration
from .vault_client import VaultClient
from .logging_system import get_logger, LogCategory, LogLevel

class Base(DeclarativeBase):
    pass

# User roles and permissions
class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    TENANT_ADMIN = "tenant_admin" 
    USER = "user"
    READONLY = "readonly"
    AGENT = "agent"  # For AI agents and service accounts

class TenantStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TRIAL = "trial"
    CANCELLED = "cancelled"

# Database Models
class Tenant(Base):
    __tablename__ = "tenants"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    status: Mapped[TenantStatus] = mapped_column(String(20), default=TenantStatus.TRIAL)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Subscription info
    subscription_plan: Mapped[Optional[str]] = mapped_column(String(50))
    subscription_status: Mapped[Optional[str]] = mapped_column(String(20))
    trial_ends_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Platform configuration
    allowed_platforms: Mapped[Optional[List[str]]] = mapped_column(JSON, default=["bizoholic"])
    settings: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, default={})
    
    # Relationships
    users: Mapped[List["User"]] = relationship("User", back_populates="tenant")

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    
    # Extended user fields
    first_name: Mapped[Optional[str]] = mapped_column(String(50))
    last_name: Mapped[Optional[str]] = mapped_column(String(50))
    role: Mapped[UserRole] = mapped_column(String(20), default=UserRole.USER)
    
    # Multi-tenant support
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    tenant: Mapped[Tenant] = relationship("Tenant", back_populates="users")
    
    # Additional metadata
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    login_count: Mapped[int] = mapped_column(Integer, default=0)
    preferences: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, default={})
    
    # Platform access permissions
    allowed_services: Mapped[Optional[List[str]]] = mapped_column(JSON, default=[])
    
    # Security fields
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0)
    locked_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    
    # Session metadata
    session_token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_accessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Security tracking
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(Text)
    platform: Mapped[Optional[str]] = mapped_column(String(50))  # Which BizOSaas platform
    
    # Session state
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    logout_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

# Pydantic schemas
class UserRead(BaseUser[uuid.UUID]):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole
    tenant_id: uuid.UUID
    last_login_at: Optional[datetime] = None
    login_count: int
    allowed_services: Optional[List[str]] = []
    
    # Computed fields
    full_name: Optional[str] = None
    is_locked: bool = False
    
    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

class UserCreate(BaseUserCreate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    tenant_id: uuid.UUID
    role: UserRole = UserRole.USER
    allowed_services: Optional[List[str]] = []

class UserUpdate(BaseUserUpdate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None
    allowed_services: Optional[List[str]] = None

class TenantCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    slug: str = Field(..., min_length=2, max_length=50, regex=r'^[a-z0-9-]+$')
    allowed_platforms: List[str] = ["bizoholic"]

class TenantRead(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    status: TenantStatus
    created_at: datetime
    subscription_plan: Optional[str] = None
    subscription_status: Optional[str] = None
    trial_ends_at: Optional[datetime] = None
    allowed_platforms: List[str]

# User Manager
class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = None
    verification_token_secret = None
    
    def __init__(self):
        self.vault_client = VaultClient()
        self.logger = get_logger()
        
        # Get secrets from Vault
        auth_secrets = self.vault_client.get_secret("auth/secrets") or {}
        self.reset_password_token_secret = auth_secrets.get("reset_password_secret", "change-me-reset")
        self.verification_token_secret = auth_secrets.get("verification_secret", "change-me-verify")
        self.jwt_secret = auth_secrets.get("jwt_secret", "change-me-jwt")

    async def on_after_register(self, user: User, request=None):
        """Actions after user registration"""
        await self.logger.log(
            LogLevel.INFO,
            LogCategory.AUTHENTICATION,
            "auth-service",
            f"User registered: {user.email}",
            details={"user_id": str(user.id), "tenant_id": str(user.tenant_id)},
            user_id=str(user.id),
            tenant_id=str(user.tenant_id)
        )

    async def on_after_login(
        self,
        user: User,
        request=None,
        response=None
    ):
        """Actions after successful login"""
        # Update login statistics
        user.last_login_at = datetime.now(timezone.utc)
        user.login_count += 1
        user.failed_login_attempts = 0
        
        await self.logger.log(
            LogLevel.INFO,
            LogCategory.AUTHENTICATION,
            "auth-service",
            f"User login successful: {user.email}",
            details={"login_count": user.login_count},
            user_id=str(user.id),
            tenant_id=str(user.tenant_id)
        )

    async def on_after_login_failed(
        self,
        user: Optional[User],
        request=None
    ):
        """Actions after failed login attempt"""
        if user:
            user.failed_login_attempts += 1
            
            # Lock account after 5 failed attempts
            if user.failed_login_attempts >= 5:
                user.locked_until = datetime.now(timezone.utc) + timedelta(hours=1)
                
                await self.logger.log(
                    LogLevel.WARNING,
                    LogCategory.SECURITY,
                    "auth-service",
                    f"Account locked due to failed login attempts: {user.email}",
                    details={"failed_attempts": user.failed_login_attempts},
                    user_id=str(user.id),
                    tenant_id=str(user.tenant_id)
                )
        
        await self.logger.log(
            LogLevel.WARNING,
            LogCategory.AUTHENTICATION,
            "auth-service",
            "Failed login attempt",
            details={"email": user.email if user else "unknown"}
        )

    async def authenticate(
        self,
        credentials,
        user_db: SQLAlchemyUserDatabase,
        **kwargs
    ) -> Optional[User]:
        """Enhanced authentication with security checks"""
        user = await super().authenticate(credentials, user_db, **kwargs)
        
        if user and user.locked_until and user.locked_until > datetime.now(timezone.utc):
            await self.logger.log(
                LogLevel.WARNING,
                LogCategory.SECURITY,
                "auth-service",
                f"Login attempt on locked account: {user.email}",
                user_id=str(user.id),
                tenant_id=str(user.tenant_id)
            )
            return None
            
        return user

# Authentication Configuration
class AuthConfig:
    def __init__(self):
        self.vault_client = VaultClient()
        auth_secrets = self.vault_client.get_secret("auth/secrets") or {}
        
        self.jwt_secret = auth_secrets.get("jwt_secret", "change-me-jwt-secret")
        self.jwt_lifetime_seconds = 3600  # 1 hour
        self.refresh_token_lifetime_seconds = 86400 * 7  # 7 days
        
        # Database configuration
        db_creds = self.vault_client.get_database_credentials("bizosaas")
        self.database_url = f"postgresql+asyncpg://{db_creds['username']}:{db_creds['password']}@{db_creds['host']}:{db_creds['port']}/{db_creds['database']}"

# Database setup
auth_config = AuthConfig()
engine = create_async_engine(auth_config.database_url, echo=False)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager()

# Authentication backends
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
cookie_transport = CookieTransport(cookie_name="bizosaas_auth", cookie_max_age=auth_config.jwt_lifetime_seconds)

jwt_strategy = JWTStrategy(
    secret=auth_config.jwt_secret,
    lifetime_seconds=auth_config.jwt_lifetime_seconds
)

# Create authentication backends
jwt_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=lambda: jwt_strategy,
)

cookie_backend = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=lambda: jwt_strategy,
)

# FastAPI Users instance
fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [jwt_backend, cookie_backend])

# Authentication utilities
current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

# Custom dependency for tenant-aware authentication
async def get_current_tenant_user(
    user: User = Depends(current_active_user),
    tenant_slug: Optional[str] = None
) -> User:
    """Get current user with tenant validation"""
    if tenant_slug:
        # Validate user belongs to the requested tenant
        if user.tenant.slug != tenant_slug:
            raise HTTPException(
                status_code=403,
                detail="Access denied: User does not belong to this tenant"
            )
    return user

# Role-based access control
def require_role(required_role: UserRole):
    """Dependency to require specific role"""
    async def check_role(user: User = Depends(current_active_user)):
        if user.role != required_role and user.role != UserRole.SUPER_ADMIN:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied: Requires {required_role} role"
            )
        return user
    return check_role

def require_service_access(service_name: str):
    """Dependency to check service access permissions"""
    async def check_service_access(user: User = Depends(current_active_user)):
        if service_name not in user.allowed_services and user.role != UserRole.SUPER_ADMIN:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied: No permission for {service_name} service"
            )
        return user
    return check_service_access

# Token utilities
class TokenService:
    def __init__(self):
        self.vault_client = VaultClient()
        auth_secrets = self.vault_client.get_secret("auth/secrets") or {}
        self.secret_key = auth_secrets.get("jwt_secret", "change-me-jwt-secret")
        self.algorithm = "HS256"
        
    def create_access_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=1)
            
        to_encode.update({"exp": expire, "type": "access"})
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=7)
            
        to_encode.update({"exp": expire, "type": "refresh"})
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None

# Session management
class SessionManager:
    def __init__(self):
        self.vault_client = VaultClient()
        self.logger = get_logger()
        
    async def create_session(
        self,
        user_id: uuid.UUID,
        tenant_id: uuid.UUID,
        ip_address: str,
        user_agent: str,
        platform: str = "bizosaas"
    ) -> UserSession:
        """Create new user session"""
        token_service = TokenService()
        
        session_token = token_service.create_access_token({
            "user_id": str(user_id),
            "tenant_id": str(tenant_id),
            "platform": platform
        })
        
        refresh_token = token_service.create_refresh_token({
            "user_id": str(user_id),
            "tenant_id": str(tenant_id),
            "platform": platform
        })
        
        session = UserSession(
            user_id=user_id,
            tenant_id=tenant_id,
            session_token=session_token,
            refresh_token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(hours=1),
            ip_address=ip_address,
            user_agent=user_agent,
            platform=platform
        )
        
        await self.logger.log(
            LogLevel.INFO,
            LogCategory.AUTHENTICATION,
            "session-manager",
            f"Session created for user {user_id}",
            details={"platform": platform, "ip_address": ip_address},
            user_id=str(user_id),
            tenant_id=str(tenant_id)
        )
        
        return session
    
    async def validate_session(self, session_token: str) -> Optional[UserSession]:
        """Validate session token"""
        token_service = TokenService()
        payload = token_service.verify_token(session_token)
        
        if not payload:
            return None
            
        # Additional session validation logic would go here
        return payload

# Global instances
token_service = TokenService()
session_manager = SessionManager()