#!/usr/bin/env python3
"""
BizOSaaS Unified Authentication Service
Production-ready FastAPI-Users implementation with:
- Multi-tenant authentication
- JWT + Cookie authentication backends
- Redis session management
- Role-based access control
- Cross-platform SSO
- Rate limiting and security features
- Vault integration for secrets
"""


# CI/CD Trigger Test - 2025-12-20
import asyncio
import os
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any, Union, AsyncGenerator

from fastapi import (
    FastAPI, Depends, HTTPException, Request, Response, 
    status, BackgroundTasks, Security
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

# FastAPI Users imports
from fastapi_users import FastAPIUsers, BaseUserManager, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from fastapi_users.password import PasswordHelper

# Database imports
from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, Integer, 
    JSON, String, Text, select, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, selectinload

# Utility imports
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
import redis.asyncio as redis
import uvicorn
from enum import Enum
# bcrypt import removed - using FastAPI-Users password helper
from jose import JWTError, jwt
import structlog
from prometheus_client import Counter, Histogram, generate_latest
from contextlib import asynccontextmanager

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Metrics
auth_requests = Counter('auth_requests_total', 'Total authentication requests', ['method', 'status'])
auth_duration = Histogram('auth_request_duration_seconds', 'Authentication request duration')

# Configuration
class Settings:
    # Database
    display_url: str = os.getenv("DATABASE_URL_FIX")
    database_url: str = display_url if display_url else os.getenv(
        "DATABASE_URL", 
        "postgresql+asyncpg://postgres:Bizoholic2024Alagiri@bizosaas-postgres-unified:5432/bizosaas"
    )
    
    # Redis
    redis_url: str = os.getenv(
        "REDIS_URL", 
        "redis://bizosaas-redis-unified:6379/0"
    )
    
    # Security
    secret_key: str = os.getenv(
        "JWT_SECRET", 
        "your-super-secret-jwt-key-change-in-production"
    )
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))
    nextauth_secret: str = os.getenv("NEXTAUTH_SECRET", "your-super-secret-nextauth-key")
    
    # CORS
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:3004",
        "https://bizoholic.com",
        "https://coreldove.com",
        "https://app.bizosaas.com"
    ]
    
    # Service configuration
    service_name: str = "bizosaas-auth-unified"
    service_version: str = "2.0.0"
    environment: str = os.getenv("ENVIRONMENT", "development")
    port: int = int(os.getenv("PORT", "8007"))

settings = Settings()

# Database Models
class Base(DeclarativeBase):
    pass

class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    TENANT_ADMIN = "tenant_admin"
    USER = "user"
    READONLY = "readonly"
    AGENT = "agent"
    SERVICE_ACCOUNT = "service_account"

class TenantStatus(str, Enum):
    ACTIVE = "active"
    TRIAL = "trial"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"

class PlatformType(str, Enum):
    BIZOHOLIC = "bizoholic"
    CORELDOVE = "coreldove"
    BIZOSAAS_ADMIN = "bizosaas-admin"
    ANALYTICS = "analytics"
    BUSINESS_DIRECTORY = "business-directory"

class Tenant(Base):
    __tablename__ = "tenants"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    domain: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    status: Mapped[TenantStatus] = mapped_column(
        String(20), default=TenantStatus.ACTIVE
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    
    # Subscription
    subscription_plan: Mapped[Optional[str]] = mapped_column(String(50))
    subscription_status: Mapped[Optional[str]] = mapped_column(String(20))
    trial_ends_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Configuration
    allowed_platforms: Mapped[Optional[List[str]]] = mapped_column(
        JSON, default=lambda: ["bizoholic"]
    )
    settings: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, default=dict)
    features: Mapped[Optional[Dict[str, bool]]] = mapped_column(JSON, default=dict)
    
    # Limits
    max_users: Mapped[int] = mapped_column(Integer, default=10)
    api_rate_limit: Mapped[int] = mapped_column(Integer, default=1000)  # requests per hour
    
    # Relationships
    users: Mapped[List["User"]] = relationship("User", back_populates="tenant")
    sessions: Mapped[List["UserSession"]] = relationship("UserSession", back_populates="tenant")

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    
    # Profile information
    first_name: Mapped[Optional[str]] = mapped_column(String(50))
    last_name: Mapped[Optional[str]] = mapped_column(String(50))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Role and permissions
    role: Mapped[UserRole] = mapped_column(String(20), default=UserRole.USER)
    permissions: Mapped[Optional[List[str]]] = mapped_column(JSON, default=list)
    
    # Multi-tenant support
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    tenant: Mapped[Tenant] = relationship("Tenant", back_populates="users")
    
    # Activity tracking
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    login_count: Mapped[int] = mapped_column(Integer, default=0)
    last_activity_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Platform access
    allowed_platforms: Mapped[Optional[List[str]]] = mapped_column(JSON, default=list)
    platform_preferences: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, default=dict)
    
    # Security
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0)
    locked_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    password_changed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    two_factor_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    two_factor_secret: Mapped[Optional[str]] = mapped_column(String(32))
    
    # Compliance
    terms_accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    privacy_accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    marketing_consent: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationships
    sessions: Mapped[List["UserSession"]] = relationship("UserSession", back_populates="user")
    audit_logs: Mapped[List["AuditLog"]] = relationship("AuditLog", back_populates="user")

class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    
    # Session data
    session_token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    platform: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Metadata
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(Text)
    location: Mapped[Optional[str]] = mapped_column(String(100))
    device_fingerprint: Mapped[Optional[str]] = mapped_column(String(64))
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    last_accessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    revocation_reason: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Relationships
    user: Mapped[User] = relationship("User", back_populates="sessions")
    tenant: Mapped[Tenant] = relationship("Tenant", back_populates="sessions")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("tenants.id", ondelete="SET NULL")
    )
    
    # Event details
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    event_description: Mapped[str] = mapped_column(Text, nullable=False)
    resource_type: Mapped[Optional[str]] = mapped_column(String(50))
    resource_id: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Context
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(Text)
    platform: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Additional data
    audit_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, default=dict)
    
    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    
    # Relationships
    user: Mapped[Optional[User]] = relationship("User", back_populates="audit_logs")

# Pydantic schemas
class UserRead(BaseUser[uuid.UUID]):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    role: str
    tenant_id: uuid.UUID
    allowed_platforms: List[str] = []
    last_login_at: Optional[datetime] = None
    login_count: int = 0
    two_factor_enabled: bool = False
    

    
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseUserCreate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    tenant_id: Optional[uuid.UUID] = None
    role: UserRole = UserRole.USER
    allowed_platforms: List[str] = []
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if not v or '@' not in v:
            raise ValueError('Valid email required')
        return v.lower().strip()

class UserUpdate(BaseUserUpdate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    allowed_platforms: Optional[List[str]] = None
    platform_preferences: Optional[Dict[str, Any]] = None

class TenantCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    slug: str = Field(..., min_length=2, max_length=50, pattern=r'^[a-z0-9-]+$')
    domain: Optional[str] = Field(None, max_length=100)
    subscription_plan: Optional[str] = None
    allowed_platforms: List[str] = ["bizoholic"]
    max_users: int = 10

class TenantRead(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    domain: Optional[str] = None
    status: str
    subscription_plan: Optional[str] = None
    allowed_platforms: List[str]
    max_users: int
    created_at: datetime
    

    
    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    platform: str = "bizosaas"
    remember_me: bool = False
    device_fingerprint: Optional[str] = None

class SSOExchangeRequest(BaseModel):
    email: str
    provider: str
    secret: str
    platform: str = "bizoholic"
    name: Optional[str] = None
    avatar_url: Optional[str] = None

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserRead
    tenant: TenantRead
    permissions: List[str]

# Database setup
engine = create_async_engine(
    settings.database_url,
    echo=settings.environment == "development",
    pool_pre_ping=True,
    pool_recycle=300,
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

# Redis setup
redis_client = None

async def get_redis() -> redis.Redis:
    return redis_client

# Authentication setup
class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.secret_key
    verification_token_secret = settings.secret_key
    
    async def on_after_register(self, user: User, request: Optional[Request] = None):
        await logger.ainfo(
            "User registered",
            user_id=str(user.id),
            email=user.email,
            tenant_id=str(user.tenant_id)
        )
        auth_requests.labels(method="register", status="success").inc()
    
    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ):
        # Update login statistics
        user.last_login_at = datetime.now(timezone.utc)
        user.login_count += 1
        user.failed_login_attempts = 0
        
        await logger.ainfo(
            "User logged in",
            user_id=str(user.id),
            email=user.email,
            tenant_id=str(user.tenant_id),
            login_count=user.login_count
        )
        auth_requests.labels(method="login", status="success").inc()
    
    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        await logger.ainfo(
            "Verification requested",
            user_id=str(user.id),
            email=user.email
        )

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

# JWT Strategy
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.secret_key,
        lifetime_seconds=settings.access_token_expire_minutes * 60,
        algorithm="HS256"
    )

# Authentication backends
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
cookie_transport = CookieTransport(
    cookie_name="bizosaas_auth",
    cookie_max_age=settings.access_token_expire_minutes * 60,
    cookie_secure=settings.environment == "production",
    cookie_httponly=True,
    cookie_samesite="lax"
)

jwt_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

cookie_backend = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [jwt_backend, cookie_backend],
)

current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

# Custom dependencies
async def get_current_tenant_user(
    user: User = Depends(current_active_user)
) -> User:
    """Get current user with tenant information loaded"""
    return user

def require_role(required_roles: Union[UserRole, List[UserRole]]):
    """Dependency to require specific user roles"""
    if isinstance(required_roles, UserRole):
        required_roles = [required_roles]
    
    def role_checker(user: User = Depends(current_active_user)):
        if user.role not in required_roles and user.role != UserRole.SUPER_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required roles: {[r.value for r in required_roles]}"
            )
        return user
    
    return role_checker

def require_platform_access(platform: str):
    """Dependency to require access to specific platform"""
    def platform_checker(user: User = Depends(current_active_user)):
        if (
            user.role != UserRole.SUPER_ADMIN and
            platform not in user.allowed_platforms and
            platform not in user.tenant.allowed_platforms
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied to platform: {platform}"
            )
        return user
    
    return platform_checker

# Utility functions
async def create_audit_log(
    session: AsyncSession,
    user_id: Optional[uuid.UUID],
    tenant_id: Optional[uuid.UUID],
    event_type: str,
    event_description: str,
    request: Optional[Request] = None,
    audit_metadata: Optional[Dict[str, Any]] = None
):
    """Create audit log entry"""
    audit_log = AuditLog(
        user_id=user_id,
        tenant_id=tenant_id,
        event_type=event_type,
        event_description=event_description,
        ip_address=request.client.host if request else None,
        user_agent=request.headers.get("User-Agent") if request else None,
        audit_metadata=audit_metadata or {}
    )
    
    session.add(audit_log)
    await session.commit()
    return audit_log

# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    global redis_client
    
    # Startup
    try:
        # Initialize Redis
        redis_client = redis.from_url(settings.redis_url)
        await redis_client.ping()
        
        # Initialize rate limiter
        await FastAPILimiter.init(redis_client)
        
        # Create database tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        await logger.ainfo(
            "Auth service started",
            service=settings.service_name,
            version=settings.service_version,
            environment=settings.environment
        )
        
        yield
        
    except Exception as e:
        await logger.aerror("Failed to start auth service", error=str(e))
        raise
    finally:
        # Shutdown
        if redis_client:
            await redis_client.close()
        await engine.dispose()
        
        await logger.ainfo("Auth service stopped")

# Create FastAPI application
app = FastAPI(
    title="BizOSaaS Unified Authentication Service",
    description="Production-ready multi-tenant authentication with FastAPI-Users",
    version=settings.service_version,
    docs_url="/auth/docs",
    redoc_url="/auth/redoc",
    openapi_url="/auth/openapi.json",
    lifespan=lifespan
)

# Security middleware
if settings.environment == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "bizoholic.com",
            "*.bizoholic.com",
            "coreldove.com", 
            "*.coreldove.com",
            "bizosaas.com",
            "*.bizosaas.com"
        ]
    )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "X-Requested-With",
        "X-CSRF-Token",
        "X-Platform",
        "X-Tenant-ID"
    ],
)

# Include FastAPI Users routes
app.include_router(
    fastapi_users.get_auth_router(jwt_backend),
    prefix="/auth/jwt",
    tags=["auth:jwt"]
)

app.include_router(
    fastapi_users.get_auth_router(cookie_backend),
    prefix="/auth/cookie",
    tags=["auth:cookie"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth:register"]
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth:reset"]
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth:verify"]
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"]
)

# Health check endpoints
@app.get("/", tags=["health"])
@app.get("/health", tags=["health"])
async def health_check():
    """Service health check"""
    try:
        # Check database
        async with AsyncSessionLocal() as session:
            await session.execute(select(func.now()))
        
        # Check Redis
        await redis_client.ping()
        
        return {
            "service": settings.service_name,
            "version": settings.service_version,
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "database": "connected",
            "redis": "connected",
            "environment": settings.environment
        }
    except Exception as e:
        await logger.aerror("Health check failed", error=str(e))
        return JSONResponse(
            status_code=503,
            content={
                "service": settings.service_name,
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )

# Metrics endpoint
@app.get("/metrics", tags=["monitoring"])
async def metrics():
    """Prometheus metrics"""
    return Response(
        generate_latest(),
        media_type="text/plain"
    )

# Custom authentication endpoints
@app.post("/auth/sso/login", response_model=AuthResponse, tags=["auth:sso"])
async def sso_login(
    request: Request,
    login_data: LoginRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    # ratelimit: str = Depends(RateLimiter(times=5, seconds=60)) # Temporarily disabled
):
    """Single Sign-On login with enhanced features"""
    try:
        # Find user with tenant eagerly loaded
        result = await session.execute(
            select(User).options(selectinload(User.tenant)).where(User.email == login_data.email.lower())
        )
        user = result.scalar_one_or_none()
        
        if not user:
            auth_requests.labels(method="sso_login", status="user_not_found").inc()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Check if user is locked
        if user.locked_until and user.locked_until > datetime.now(timezone.utc):
            auth_requests.labels(method="sso_login", status="account_locked").inc()
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail=f"Account locked until {user.locked_until}"
            )
        
        # Verify password using FastAPI-Users proper method
        password_helper = PasswordHelper()
        verified, updated_hash = password_helper.verify_and_update(login_data.password, user.hashed_password)
        if not verified:
            user.failed_login_attempts += 1
            
            # Lock account after 5 failed attempts
            if user.failed_login_attempts >= 5:
                user.locked_until = datetime.now(timezone.utc) + timedelta(hours=1)
            
            await session.commit()
            auth_requests.labels(method="sso_login", status="invalid_password").inc()
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Update password hash if it was rehashed
        if updated_hash:
            user.hashed_password = updated_hash

        
        # Check platform access
        if (
            user.role != UserRole.SUPER_ADMIN and 
            login_data.platform not in user.allowed_platforms and
            login_data.platform not in user.tenant.allowed_platforms
        ):
            auth_requests.labels(method="sso_login", status="platform_denied").inc()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied to platform: {login_data.platform}"
            )
        
        # Update user login info
        user.last_login_at = datetime.now(timezone.utc)
        user.login_count += 1
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_activity_at = datetime.now(timezone.utc)
        
        # Create session
        session_expires = datetime.now(timezone.utc) + timedelta(
            days=settings.refresh_token_expire_days if login_data.remember_me 
            else 1
        )
        
        user_session = UserSession(
            user_id=user.id,
            tenant_id=user.tenant_id,
            session_token=str(uuid.uuid4()),
            refresh_token=str(uuid.uuid4()),
            platform=login_data.platform,
            ip_address=request.client.host,
            user_agent=request.headers.get("User-Agent"),
            device_fingerprint=login_data.device_fingerprint,
            expires_at=session_expires
        )
        
        session.add(user_session)
        await session.commit()
        
        # Generate JWT token
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role if isinstance(user.role, str) else user.role.value,
            "tenant_id": str(user.tenant_id),
            "platform": login_data.platform,
            "session_id": str(user_session.id),
            "exp": datetime.now(timezone.utc) + timedelta(
                minutes=settings.access_token_expire_minutes
            )
        }
        
        access_token = jwt.encode(
            token_data,
            settings.secret_key,
            algorithm="HS256"
        )
        
        # Helper for background task to manage session
        async def log_audit_event(uid, tid, platform, remember_me, ip, ua):
            async with AsyncSessionLocal() as audit_session:
                await create_audit_log(
                    audit_session,
                    uid,
                    tid,
                    "sso_login",
                    f"User logged in via SSO to {platform}",
                    None, # Request object not safe to pass to background
                    {"platform": platform, "remember_me": remember_me, "ip": ip, "ua": ua}
                )

        # Create audit log in background
        background_tasks.add_task(
            log_audit_event,
            user.id,
            user.tenant_id,
            login_data.platform,
            login_data.remember_me,
            request.client.host,
            request.headers.get("User-Agent")
        )
        
        auth_requests.labels(method="sso_login", status="success").inc()
        
        return AuthResponse(
            access_token=access_token,
            refresh_token=user_session.refresh_token,
            expires_in=settings.access_token_expire_minutes * 60,
            user=UserRead.model_validate(user),
            tenant=TenantRead.model_validate(user.tenant),
            permissions=user.permissions or []
        )
        

        
    except HTTPException:
        raise
    except Exception as e:
        auth_requests.labels(method="sso_login", status="error").inc()
        await logger.aerror(
            "SSO login failed",
            email=login_data.email,
            platform=login_data.platform,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed"
        )

@app.post("/auth/sso/exchange")
async def sso_exchange(request: Request):
    """
    Debug endpoint - No Pydantic
    """
    exchange_data = await request.json()
    return {"status": "ok", "email": exchange_data.get("email")}

@app.post("/auth/sso/logout", tags=["auth:sso"])
async def sso_logout(
    request: Request,
    background_tasks: BackgroundTasks,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Single Sign-On logout"""
    try:
        # Get session token from header
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            
            try:
                payload = jwt.decode(
                    token, 
                    settings.secret_key, 
                    algorithms=["HS256"]
                )
                session_id = payload.get("session_id")
                
                if session_id:
                    # Revoke session
                    result = await session.execute(
                        select(UserSession).where(
                            UserSession.id == uuid.UUID(session_id)
                        )
                    )
                    user_session = result.scalar_one_or_none()
                    
                    if user_session:
                        user_session.is_active = False
                        user_session.revoked_at = datetime.now(timezone.utc)
                        user_session.revocation_reason = "user_logout"
                        
                        await session.commit()
            
            except JWTError:
                pass  # Token invalid, but continue with logout
        
        # Create audit log
        background_tasks.add_task(
            create_audit_log,
            AsyncSessionLocal(),
            user.id,
            user.tenant_id,
            "sso_logout",
            "User logged out via SSO",
            request
        )
        
        return {"status": "success", "message": "Logout successful"}
        
    except Exception as e:
        await logger.aerror(
            "SSO logout failed",
            user_id=str(user.id),
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )

@app.get("/auth/me", response_model=dict, tags=["auth:user"])
async def get_current_user_info(
    user: User = Depends(current_active_user)
):
    """Get current user information with tenant and permissions"""
    return {
        "user": UserRead.model_validate(user),
        "tenant": TenantRead.model_validate(user.tenant),
        "permissions": {
            "role": user.role.value,
            "allowed_platforms": user.allowed_platforms,
            "tenant_platforms": user.tenant.allowed_platforms,
            "is_super_admin": user.role == UserRole.SUPER_ADMIN,
            "is_tenant_admin": user.role == UserRole.TENANT_ADMIN,
            "permissions": user.permissions or []
        },
        "session_info": {
            "last_login": user.last_login_at.isoformat() if user.last_login_at else None,
            "login_count": user.login_count,
            "last_activity": user.last_activity_at.isoformat() if user.last_activity_at else None
        }
    }

@app.get("/auth/authorize/{platform}", tags=["auth:authorization"])
async def authorize_platform_access(
    platform: str,
    user: User = Depends(current_active_user)
):
    """Check platform authorization"""
    has_access = (
        user.role == UserRole.SUPER_ADMIN or
        platform in user.allowed_platforms or
        platform in user.tenant.allowed_platforms
    )
    
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied to platform: {platform}"
        )
    
    return {
        "authorized": True,
        "platform": platform,
        "user": {
            "id": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "tenant_id": str(user.tenant_id)
        },
        "tenant": {
            "id": str(user.tenant.id),
            "slug": user.tenant.slug,
            "name": user.tenant.name,
            "status": user.tenant.status.value
        }
    }

# Tenant management endpoints
@app.post("/tenants", response_model=TenantRead, tags=["tenants"])
async def create_tenant(
    tenant_data: TenantCreate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    admin_user: User = Depends(require_role(UserRole.SUPER_ADMIN))
):
    """Create new tenant (Super Admin only)"""
    try:
        # Check if slug is unique
        result = await session.execute(
            select(Tenant).where(Tenant.slug == tenant_data.slug)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Tenant slug already exists"
            )
        
        # Create tenant
        tenant = Tenant(
            name=tenant_data.name,
            slug=tenant_data.slug,
            domain=tenant_data.domain,
            subscription_plan=tenant_data.subscription_plan,
            allowed_platforms=tenant_data.allowed_platforms,
            max_users=tenant_data.max_users,
            trial_ends_at=datetime.now(timezone.utc) + timedelta(days=30)  # 30-day trial
        )
        
        session.add(tenant)
        await session.commit()
        await session.refresh(tenant)
        
        # Create audit log
        background_tasks.add_task(
            create_audit_log,
            AsyncSessionLocal(),
            admin_user.id,
            admin_user.tenant_id,
            "tenant_created",
            f"Created tenant: {tenant.name} ({tenant.slug})",
            None,
            {"tenant_id": str(tenant.id)}
        )
        
        return TenantRead.model_validate(tenant)
        
    except HTTPException:
        raise
    except Exception as e:
        await logger.aerror(
            "Failed to create tenant",
            tenant_slug=tenant_data.slug,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create tenant"
        )

@app.get("/tenants", response_model=List[TenantRead], tags=["tenants"])
async def list_tenants(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session),
    admin_user: User = Depends(require_role(UserRole.SUPER_ADMIN))
):
    """List all tenants (Super Admin only)"""
    result = await session.execute(
        select(Tenant).offset(skip).limit(limit).order_by(Tenant.created_at.desc())
    )
    tenants = result.scalars().all()
    return [TenantRead.model_validate(tenant) for tenant in tenants]

@app.get("/tenants/me", response_model=TenantRead, tags=["tenants"])
async def get_my_tenant(
    user: User = Depends(current_active_user)
):
    """Get current user's tenant information"""
    return TenantRead.model_validate(user.tenant)

# Import standalone exchange router
from auth_exchange import router as exchange_router, get_db_session

# Include the exchange router
app.include_router(exchange_router)

# Override dependency to use the main session
app.dependency_overrides[get_db_session] = get_async_session

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.port, reload=True)