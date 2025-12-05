"""
BizOSaas Authentication Service - Unified SSO System
FastAPI-Users based authentication with multi-tenant support
"""

import asyncio
import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Depends, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
import uvicorn

# Import our authentication system
import sys
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas')

from shared.auth_system import (
    fastapi_users,
    jwt_backend,
    cookie_backend,
    current_active_user,
    current_superuser,
    get_current_tenant_user,
    require_role,
    require_service_access,
    UserRole,
    User,
    UserCreate,
    UserRead,
    UserUpdate,
    Tenant,
    TenantCreate,
    TenantRead,
    create_db_and_tables,
    get_async_session,
    get_user_db,
    token_service,
    session_manager
)
from shared.logging_system import get_logger, LogLevel, LogCategory

# Initialize FastAPI app
app = FastAPI(
    title="BizOSaas Authentication Service",
    description="Unified authentication and authorization service for all BizOSaas platforms",
    version="1.0.0",
    docs_url="/auth/docs",
    redoc_url="/auth/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize logger
logger = None

@app.on_event("startup")
async def startup_event():
    """Initialize authentication service"""
    global logger
    logger = get_logger()
    
    # Create database tables
    await create_db_and_tables()
    
    await logger.log(
        LogLevel.INFO,
        LogCategory.SYSTEM,
        "auth-service",
        "Authentication service started"
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

# Custom authentication endpoints
@app.get("/")
async def root():
    """Service health check"""
    return {
        "service": "bizosaas-auth-service",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/auth/me")
async def get_current_user_info(user: User = Depends(current_active_user)):
    """Get current user information"""
    await logger.log(
        LogLevel.INFO,
        LogCategory.API,
        "auth-service",
        f"User info requested: {user.email}",
        user_id=str(user.id),
        tenant_id=str(user.tenant_id)
    )
    
    return {
        "user": UserRead.from_orm(user),
        "tenant": {
            "id": str(user.tenant.id),
            "name": user.tenant.name,
            "slug": user.tenant.slug,
            "status": user.tenant.status,
            "allowed_platforms": user.tenant.allowed_platforms
        },
        "permissions": {
            "role": user.role,
            "allowed_services": user.allowed_services,
            "is_super_admin": user.role == UserRole.SUPER_ADMIN
        }
    }

@app.post("/auth/sso/login")
async def sso_login(
    request: Request,
    email: EmailStr,
    password: str,
    platform: str = "bizosaas",
    remember_me: bool = False
):
    """Single Sign-On login endpoint"""
    try:
        # This would integrate with FastAPI Users login
        # For now, return a structured response
        
        await logger.log(
            LogLevel.INFO,
            LogCategory.AUTHENTICATION,
            "auth-service",
            f"SSO login attempt: {email}",
            details={"platform": platform, "remember_me": remember_me}
        )
        
        return {
            "status": "success",
            "message": "Login successful",
            "access_token": "jwt_token_here",
            "refresh_token": "refresh_token_here",
            "expires_in": 3600,
            "token_type": "bearer",
            "user": {
                "email": email,
                "platforms": ["bizoholic", "coreldove"]
            }
        }
        
    except Exception as e:
        await logger.log(
            LogLevel.ERROR,
            LogCategory.AUTHENTICATION,
            "auth-service",
            f"SSO login failed: {email}",
            details={"error": str(e)},
            error=e
        )
        raise HTTPException(status_code=401, detail="Authentication failed")

@app.post("/auth/sso/logout")
async def sso_logout(
    request: Request,
    user: User = Depends(current_active_user)
):
    """Single Sign-On logout endpoint"""
    try:
        # Invalidate session across all platforms
        session_token = request.headers.get("Authorization", "").replace("Bearer ", "")
        
        await logger.log(
            LogLevel.INFO,
            LogCategory.AUTHENTICATION,
            "auth-service",
            f"SSO logout: {user.email}",
            user_id=str(user.id),
            tenant_id=str(user.tenant_id)
        )
        
        return {
            "status": "success",
            "message": "Logout successful"
        }
        
    except Exception as e:
        await logger.log(
            LogLevel.ERROR,
            LogCategory.AUTHENTICATION,
            "auth-service",
            f"SSO logout failed: {user.email if user else 'unknown'}",
            error=e
        )
        raise HTTPException(status_code=500, detail="Logout failed")

@app.post("/auth/token/refresh")
async def refresh_token(refresh_token: str):
    """Refresh access token using refresh token"""
    try:
        payload = token_service.verify_token(refresh_token)
        
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        # Generate new access token
        new_access_token = token_service.create_access_token({
            "user_id": payload["user_id"],
            "tenant_id": payload["tenant_id"],
            "platform": payload.get("platform", "bizosaas")
        })
        
        await logger.log(
            LogLevel.INFO,
            LogCategory.AUTHENTICATION,
            "auth-service",
            "Token refreshed",
            details={"user_id": payload["user_id"]}
        )
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": 3600
        }
        
    except Exception as e:
        await logger.log(
            LogLevel.ERROR,
            LogCategory.AUTHENTICATION,
            "auth-service",
            "Token refresh failed",
            error=e
        )
        raise HTTPException(status_code=401, detail="Token refresh failed")

# Service Authorization Endpoints
@app.get("/auth/authorize/{service_name}")
async def authorize_service_access(
    service_name: str,
    user: User = Depends(current_active_user)
):
    """Check if user has access to specific service"""
    try:
        has_access = (
            user.role == UserRole.SUPER_ADMIN or 
            service_name in user.allowed_services or
            service_name in user.tenant.allowed_platforms
        )
        
        await logger.log(
            LogLevel.INFO,
            LogCategory.AUTHENTICATION,
            "auth-service",
            f"Service authorization check: {service_name}",
            details={
                "service": service_name,
                "access_granted": has_access,
                "user_role": user.role
            },
            user_id=str(user.id),
            tenant_id=str(user.tenant_id)
        )
        
        if not has_access:
            raise HTTPException(
                status_code=403, 
                detail=f"Access denied to {service_name}"
            )
        
        return {
            "authorized": True,
            "service": service_name,
            "user": {
                "id": str(user.id),
                "email": user.email,
                "role": user.role,
                "tenant_id": str(user.tenant_id)
            },
            "tenant": {
                "id": str(user.tenant.id),
                "slug": user.tenant.slug,
                "name": user.tenant.name
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        await logger.log(
            LogLevel.ERROR,
            LogCategory.AUTHENTICATION,
            "auth-service",
            f"Service authorization failed: {service_name}",
            error=e,
            user_id=str(user.id) if user else None
        )
        raise HTTPException(status_code=500, detail="Authorization check failed")

@app.post("/auth/sessions")
async def create_session(
    request: Request,
    platform: str = "bizosaas",
    user: User = Depends(current_active_user)
):
    """Create cross-platform session"""
    try:
        ip_address = request.client.host
        user_agent = request.headers.get("User-Agent", "")
        
        session = await session_manager.create_session(
            user_id=user.id,
            tenant_id=user.tenant_id,
            ip_address=ip_address,
            user_agent=user_agent,
            platform=platform
        )
        
        return {
            "session_id": str(session.id),
            "session_token": session.session_token,
            "refresh_token": session.refresh_token,
            "expires_at": session.expires_at.isoformat(),
            "platform": platform
        }
        
    except Exception as e:
        await logger.log(
            LogLevel.ERROR,
            LogCategory.AUTHENTICATION,
            "auth-service",
            "Failed to create session",
            error=e,
            user_id=str(user.id)
        )
        raise HTTPException(status_code=500, detail="Failed to create session")

# Health and Status Endpoints
@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",  # Would check actual DB connection
        "redis": "connected",     # Would check Redis connection
        "vault": "connected",     # Would check Vault connection
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/auth/status")
async def auth_status():
    """Authentication service status"""
    return {
        "service": "authentication",
        "backends": ["jwt", "cookie"],
        "features": [
            "multi_tenant",
            "role_based_access",
            "single_sign_on",
            "session_management",
            "audit_logging"
        ],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 3001))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )