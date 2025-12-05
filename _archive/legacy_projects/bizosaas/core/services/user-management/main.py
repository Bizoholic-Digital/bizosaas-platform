"""
User Management Service - BizoholicSaaS
Handles authentication, authorization, user management, and multi-tenant operations
Port: 8001
"""

from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime, timedelta
import logging

# Shared imports
import sys
import os
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas')

from shared.database.connection import get_postgres_session, get_redis_client, init_database
from shared.database.models import User, Tenant, UserSession
from shared.events.event_bus import EventBus, EventFactory, EventType, event_handler
from shared.auth.jwt_auth import (
    jwt_manager, PasswordManager, get_current_user, UserContext, UserRole,
    require_admin, require_permission, Permission, set_redis_client
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="User Management Service",
    description="Authentication, authorization, and user management for BizoholicSaaS",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
event_bus: EventBus = None
redis_client = None

# Pydantic models
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole = UserRole.USER
    tenant_id: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    permissions: Optional[List[str]] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    tenant_domain: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    role: UserRole
    tenant_id: str
    is_active: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 1800  # 30 minutes

class TenantCreate(BaseModel):
    name: str
    domain: str
    billing_email: EmailStr
    subscription_plan: str = "starter"
    admin_user: UserCreate

class TenantResponse(BaseModel):
    id: str
    name: str
    domain: str
    subscription_status: str
    subscription_plan: str
    max_users: int
    max_campaigns: int
    created_at: datetime
    is_active: bool

class SessionResponse(BaseModel):
    id: str
    user_id: str
    ip_address: Optional[str]
    user_agent: Optional[str]
    last_activity: datetime
    expires_at: datetime

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database and event bus connections"""
    global event_bus, redis_client
    
    try:
        # Initialize database
        await init_database()
        logger.info("Database connections initialized")
        
        # Initialize Redis client
        redis_client = await get_redis_client()
        set_redis_client(redis_client)
        
        # Initialize event bus
        event_bus = EventBus(redis_client, "user-management")
        await event_bus.initialize()
        await event_bus.start()
        logger.info("Event bus initialized")
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Clean shutdown of connections"""
    global event_bus
    
    if event_bus:
        await event_bus.stop()
    logger.info("User Management Service shutdown complete")

# Health check endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "user-management",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    try:
        # Check database connection
        async with get_postgres_session("user_management") as session:
            await session.execute("SELECT 1")
        
        # Check Redis connection
        await redis_client.ping()
        
        return {
            "status": "ready",
            "service": "user-management",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service not ready: {str(e)}"
        )

# Authentication endpoints
@app.post("/auth/login", response_model=TokenResponse)
async def login(login_data: UserLogin):
    """Authenticate user and return JWT tokens"""
    
    try:
        async with get_postgres_session("user_management") as session:
            # Find user by email
            from sqlalchemy import select
            stmt = select(User).where(User.email == login_data.email, User.is_active == True)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            
            # Verify password
            if not PasswordManager.verify_password(login_data.password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            
            # Check tenant domain if provided
            if login_data.tenant_domain:
                tenant_stmt = select(Tenant).where(
                    Tenant.id == user.tenant_id,
                    Tenant.domain == login_data.tenant_domain,
                    Tenant.is_active == True
                )
                tenant_result = await session.execute(tenant_stmt)
                tenant = tenant_result.scalar_one_or_none()
                
                if not tenant:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid tenant domain"
                    )
            
            # Create JWT tokens
            access_token = jwt_manager.create_access_token(
                user_id=str(user.id),
                tenant_id=str(user.tenant_id),
                email=user.email,
                role=UserRole(user.role)
            )
            
            refresh_token = jwt_manager.create_refresh_token(
                user_id=str(user.id),
                tenant_id=str(user.tenant_id)
            )
            
            # Update last login
            user.last_login = datetime.utcnow()
            await session.commit()
            
            # Create user session
            session_token = str(uuid.uuid4())
            user_session = UserSession(
                id=uuid.uuid4(),
                user_id=user.id,
                tenant_id=user.tenant_id,
                session_token=session_token,
                expires_at=datetime.utcnow() + timedelta(hours=24),
                last_activity=datetime.utcnow()
            )
            session.add(user_session)
            await session.commit()
            
            # Publish user login event
            event = EventFactory.user_login(
                tenant_id=str(user.tenant_id),
                user_id=str(user.id),
                user_data={
                    "email": user.email,
                    "role": user.role,
                    "login_time": datetime.utcnow().isoformat()
                }
            )
            await event_bus.publish(event)
            
            return TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=1800
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed"
        )

@app.post("/auth/logout")
async def logout(current_user: UserContext = Depends(get_current_user)):
    """Logout user and revoke tokens"""
    
    try:
        # Revoke current token
        # Note: In a real implementation, you'd extract token_data from the request
        # For now, we'll just log the logout
        
        # Publish user logout event
        event = EventFactory.user_logout(
            tenant_id=current_user.tenant_id,
            user_id=current_user.user_id,
            user_data={
                "email": current_user.email,
                "logout_time": datetime.utcnow().isoformat()
            }
        )
        await event_bus.publish(event)
        
        return {"message": "Logged out successfully"}
        
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )

@app.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserContext = Depends(get_current_user)):
    """Get current user information"""
    
    try:
        async with get_postgres_session("user_management") as session:
            from sqlalchemy import select
            stmt = select(User).where(User.id == uuid.UUID(current_user.user_id))
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            return UserResponse(
                id=str(user.id),
                email=user.email,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                role=UserRole(user.role),
                tenant_id=str(user.tenant_id),
                is_active=user.is_active,
                last_login=user.last_login,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get current user error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information"
        )

# User management endpoints
@app.post("/users", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    current_user: UserContext = Depends(require_permission(Permission.USER_CREATE))
):
    """Create a new user"""
    
    try:
        async with get_postgres_session("user_management") as session:
            # Check if user already exists
            from sqlalchemy import select
            existing_user = await session.execute(
                select(User).where(User.email == user_data.email)
            )
            if existing_user.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with this email already exists"
                )
            
            # Hash password
            hashed_password = PasswordManager.hash_password(user_data.password)
            
            # Create user
            new_user = User(
                id=uuid.uuid4(),
                email=user_data.email,
                username=user_data.username,
                hashed_password=hashed_password,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                role=user_data.role.value,
                tenant_id=uuid.UUID(user_data.tenant_id),
                is_active=True
            )
            
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            
            # Publish user created event
            event = EventFactory.user_created(
                tenant_id=str(new_user.tenant_id),
                user_id=str(new_user.id),
                user_data={
                    "email": new_user.email,
                    "username": new_user.username,
                    "role": new_user.role,
                    "created_by": current_user.user_id
                }
            )
            await event_bus.publish(event)
            
            return UserResponse(
                id=str(new_user.id),
                email=new_user.email,
                username=new_user.username,
                first_name=new_user.first_name,
                last_name=new_user.last_name,
                role=UserRole(new_user.role),
                tenant_id=str(new_user.tenant_id),
                is_active=new_user.is_active,
                last_login=new_user.last_login,
                created_at=new_user.created_at,
                updated_at=new_user.updated_at
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create user error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

@app.get("/users", response_model=List[UserResponse])
async def list_users(
    current_user: UserContext = Depends(require_permission(Permission.USER_READ)),
    skip: int = 0,
    limit: int = 100
):
    """List users in current tenant"""
    
    try:
        async with get_postgres_session("user_management") as session:
            from sqlalchemy import select
            
            # Filter by tenant for non-super-admin users
            if current_user.role != UserRole.SUPER_ADMIN:
                stmt = select(User).where(
                    User.tenant_id == uuid.UUID(current_user.tenant_id),
                    User.is_active == True
                ).offset(skip).limit(limit)
            else:
                stmt = select(User).where(User.is_active == True).offset(skip).limit(limit)
            
            result = await session.execute(stmt)
            users = result.scalars().all()
            
            return [
                UserResponse(
                    id=str(user.id),
                    email=user.email,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    role=UserRole(user.role),
                    tenant_id=str(user.tenant_id),
                    is_active=user.is_active,
                    last_login=user.last_login,
                    created_at=user.created_at,
                    updated_at=user.updated_at
                ) for user in users
            ]
            
    except Exception as e:
        logger.error(f"List users error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list users"
        )

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: UserContext = Depends(require_permission(Permission.USER_READ))
):
    """Get user by ID"""
    
    try:
        async with get_postgres_session("user_management") as session:
            from sqlalchemy import select
            stmt = select(User).where(User.id == uuid.UUID(user_id), User.is_active == True)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Check tenant access
            if (current_user.role != UserRole.SUPER_ADMIN and 
                str(user.tenant_id) != current_user.tenant_id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            
            return UserResponse(
                id=str(user.id),
                email=user.email,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                role=UserRole(user.role),
                tenant_id=str(user.tenant_id),
                is_active=user.is_active,
                last_login=user.last_login,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get user error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user"
        )

# Tenant management endpoints
@app.post("/tenants", response_model=TenantResponse)
async def create_tenant(
    tenant_data: TenantCreate,
    current_user: UserContext = Depends(require_permission(Permission.TENANT_MANAGE))
):
    """Create a new tenant with admin user"""
    
    try:
        async with get_postgres_session("user_management") as session:
            # Check if tenant domain already exists
            from sqlalchemy import select
            existing_tenant = await session.execute(
                select(Tenant).where(Tenant.domain == tenant_data.domain)
            )
            if existing_tenant.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Tenant with this domain already exists"
                )
            
            # Create tenant
            new_tenant = Tenant(
                id=uuid.uuid4(),
                name=tenant_data.name,
                domain=tenant_data.domain,
                billing_email=tenant_data.billing_email,
                subscription_plan=tenant_data.subscription_plan,
                subscription_status='trial',
                is_active=True
            )
            
            session.add(new_tenant)
            await session.flush()  # Get tenant ID
            
            # Create admin user for tenant
            admin_password_hash = PasswordManager.hash_password(tenant_data.admin_user.password)
            admin_user = User(
                id=uuid.uuid4(),
                email=tenant_data.admin_user.email,
                username=tenant_data.admin_user.username,
                hashed_password=admin_password_hash,
                first_name=tenant_data.admin_user.first_name,
                last_name=tenant_data.admin_user.last_name,
                role=UserRole.TENANT_ADMIN.value,
                tenant_id=new_tenant.id,
                is_active=True
            )
            
            session.add(admin_user)
            await session.commit()
            
            return TenantResponse(
                id=str(new_tenant.id),
                name=new_tenant.name,
                domain=new_tenant.domain,
                subscription_status=new_tenant.subscription_status,
                subscription_plan=new_tenant.subscription_plan,
                max_users=new_tenant.max_users,
                max_campaigns=new_tenant.max_campaigns,
                created_at=new_tenant.created_at,
                is_active=new_tenant.is_active
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create tenant error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create tenant"
        )

# Session management endpoints
@app.get("/sessions", response_model=List[SessionResponse])
async def list_user_sessions(current_user: UserContext = Depends(get_current_user)):
    """List active sessions for current user"""
    
    try:
        async with get_postgres_session("user_management") as session:
            from sqlalchemy import select
            stmt = select(UserSession).where(
                UserSession.user_id == uuid.UUID(current_user.user_id),
                UserSession.expires_at > datetime.utcnow()
            )
            result = await session.execute(stmt)
            sessions = result.scalars().all()
            
            return [
                SessionResponse(
                    id=str(session.id),
                    user_id=str(session.user_id),
                    ip_address=session.ip_address,
                    user_agent=session.user_agent,
                    last_activity=session.last_activity,
                    expires_at=session.expires_at
                ) for session in sessions
            ]
            
    except Exception as e:
        logger.error(f"List sessions error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list sessions"
        )

# Event handlers
@event_handler(EventType.CAMPAIGN_STARTED)
async def handle_campaign_started(event):
    """Handle campaign started event - could trigger user notifications"""
    logger.info(f"Campaign started for tenant {event.tenant_id}: {event.data}")

@event_handler(EventType.INTEGRATION_CONNECTED)
async def handle_integration_connected(event):
    """Handle integration connected event"""
    logger.info(f"Integration connected for tenant {event.tenant_id}: {event.data}")

# Metrics endpoint
@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    # In a real implementation, you'd return Prometheus-formatted metrics
    return {
        "service": "user-management",
        "metrics": {
            "active_users": 0,  # Would be calculated from database
            "login_attempts": 0,
            "failed_logins": 0,
            "active_sessions": 0
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)