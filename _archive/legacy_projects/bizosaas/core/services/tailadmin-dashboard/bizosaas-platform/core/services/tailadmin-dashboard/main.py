#!/usr/bin/env python3

"""
TailAdmin v2 Dashboard - Secured FastAPI Backend
Integrates with existing auth-service-v2 for comprehensive authentication and RBAC
"""

import os
import json
import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import redis.asyncio as redis
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service-v2:8005")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
STATIC_FILES_PATH = os.getenv("STATIC_FILES_PATH", "/app/html")

app = FastAPI(
    title="TailAdmin v2 Dashboard",
    description="Secured business operations dashboard with RBAC",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on your domain requirements
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer(auto_error=False)

# Templates and static files
templates = Jinja2Templates(directory=STATIC_FILES_PATH)
app.mount("/static", StaticFiles(directory=f"{STATIC_FILES_PATH}/static"), name="static")

# Redis connection
redis_client = None

# Pydantic models
class UserSession(BaseModel):
    user_id: str
    tenant_id: Optional[str]
    role: str
    permissions: list
    email: str
    expires_at: datetime

class LoginRequest(BaseModel):
    email: str
    password: str
    remember_me: bool = False

# Authentication middleware
async def get_redis_client():
    global redis_client
    if not redis_client:
        redis_client = await redis.from_url(REDIS_URL)
    return redis_client

async def verify_session(request: Request) -> Optional[UserSession]:
    """Verify user session with auth-service-v2"""
    try:
        # Get session token from cookie or Authorization header
        session_token = request.cookies.get("session_token")
        
        if not session_token:
            # Try Authorization header
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                session_token = auth_header[7:]
        
        if not session_token:
            return None
        
        # Verify session with auth-service-v2
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {session_token}"}
            async with session.get(f"{AUTH_SERVICE_URL}/auth/verify", headers=headers) as response:
                if response.status == 200:
                    user_data = await response.json()
                    return UserSession(**user_data)
                else:
                    logger.warning(f"Session verification failed: {response.status}")
                    return None
    
    except Exception as e:
        logger.error(f"Session verification error: {e}")
        return None

async def require_authentication(request: Request) -> UserSession:
    """Dependency to require authentication"""
    user_session = await verify_session(request)
    if not user_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return user_session

async def require_role(required_roles: list):
    """Dependency factory to require specific roles"""
    async def role_checker(user_session: UserSession = Depends(require_authentication)) -> UserSession:
        if user_session.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {required_roles}"
            )
        return user_session
    return role_checker

async def require_permission(required_permissions: list):
    """Dependency factory to require specific permissions"""
    async def permission_checker(user_session: UserSession = Depends(require_authentication)) -> UserSession:
        user_permissions = user_session.permissions
        
        # Check if user has admin:* (super admin) or required permissions
        if "admin:*" not in user_permissions:
            has_permissions = all(perm in user_permissions for perm in required_permissions)
            if not has_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions. Required: {required_permissions}"
                )
        return user_session
    return permission_checker

# Routes

@app.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request):
    """Main dashboard - requires authentication"""
    user_session = await verify_session(request)
    
    if not user_session:
        # Redirect to login if not authenticated
        return RedirectResponse(url="/login", status_code=302)
    
    # Serve dashboard based on user role
    dashboard_config = {
        "user": {
            "id": user_session.user_id,
            "email": user_session.email,
            "role": user_session.role,
            "permissions": user_session.permissions,
            "tenant_id": user_session.tenant_id
        },
        "features": get_features_for_role(user_session.role),
        "navigation": get_navigation_for_role(user_session.role)
    }
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "user": dashboard_config["user"],
        "features": dashboard_config["features"],
        "navigation": dashboard_config["navigation"]
    })

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/api/auth/login")
async def login(request: Request, login_data: LoginRequest):
    """Login endpoint - proxies to auth-service-v2"""
    try:
        async with aiohttp.ClientSession() as session:
            login_payload = {
                "email": login_data.email,
                "password": login_data.password,
                "remember_me": login_data.remember_me
            }
            
            async with session.post(f"{AUTH_SERVICE_URL}/auth/login", json=login_payload) as response:
                result = await response.json()
                
                if response.status == 200:
                    # Set session cookie
                    response_data = JSONResponse(content={"success": True, "user": result["user"]})
                    response_data.set_cookie(
                        key="session_token",
                        value=result["session_token"],
                        max_age=86400 if login_data.remember_me else 3600,  # 24h or 1h
                        httponly=True,
                        secure=True,
                        samesite="lax"
                    )
                    return response_data
                else:
                    raise HTTPException(status_code=response.status, detail=result.get("detail", "Login failed"))
    
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/auth/logout")
async def logout(request: Request, user_session: UserSession = Depends(require_authentication)):
    """Logout endpoint"""
    try:
        session_token = request.cookies.get("session_token")
        if session_token:
            # Invalidate session in auth-service-v2
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {session_token}"}
                await session.post(f"{AUTH_SERVICE_URL}/auth/logout", headers=headers)
        
        # Clear session cookie
        response = JSONResponse(content={"success": True})
        response.delete_cookie(key="session_token")
        return response
    
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/user/profile")
async def get_user_profile(user_session: UserSession = Depends(require_authentication)):
    """Get current user profile"""
    return {
        "user_id": user_session.user_id,
        "email": user_session.email,
        "role": user_session.role,
        "permissions": user_session.permissions,
        "tenant_id": user_session.tenant_id
    }

# Role-specific endpoints

@app.get("/admin")
async def admin_dashboard(
    request: Request,
    user_session: UserSession = Depends(require_role(["super_admin", "tenant_admin"]))
):
    """Admin dashboard - Super Admin and Tenant Admin only"""
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "user": user_session
    })

@app.get("/manager")
async def manager_dashboard(
    request: Request,
    user_session: UserSession = Depends(require_role(["super_admin", "tenant_admin", "manager"]))
):
    """Manager dashboard"""
    return templates.TemplateResponse("manager.html", {
        "request": request,
        "user": user_session
    })

@app.get("/api/system/health")
async def system_health(
    user_session: UserSession = Depends(require_permission(["system:read"]))
):
    """System health check - requires system permissions"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "auth_service": "operational",
            "dashboard": "operational"
        }
    }

# Helper functions

def get_features_for_role(role: str) -> Dict[str, Any]:
    """Get available features based on user role"""
    feature_map = {
        "super_admin": {
            "infrastructure": True,
            "ai_agents": True,
            "system_monitoring": True,
            "user_management": True,
            "tenant_management": True,
            "saleor_access": True,
            "analytics": True,
            "chat_ai": True
        },
        "tenant_admin": {
            "infrastructure": False,
            "ai_agents": True,
            "system_monitoring": False,
            "user_management": True,
            "tenant_management": True,
            "saleor_access": True,
            "analytics": True,
            "chat_ai": True
        },
        "manager": {
            "infrastructure": False,
            "ai_agents": False,
            "system_monitoring": False,
            "user_management": False,
            "tenant_management": False,
            "saleor_access": True,
            "analytics": True,
            "chat_ai": True
        },
        "staff": {
            "infrastructure": False,
            "ai_agents": False,
            "system_monitoring": False,
            "user_management": False,
            "tenant_management": False,
            "saleor_access": False,
            "analytics": False,
            "chat_ai": False
        },
        "client": {
            "infrastructure": False,
            "ai_agents": False,
            "system_monitoring": False,
            "user_management": False,
            "tenant_management": False,
            "saleor_access": False,
            "analytics": True,
            "chat_ai": True
        }
    }
    
    return feature_map.get(role, feature_map["client"])

def get_navigation_for_role(role: str) -> list:
    """Get navigation menu based on user role"""
    base_nav = [
        {"name": "Dashboard", "url": "/", "icon": "dashboard"},
        {"name": "Analytics", "url": "/analytics", "icon": "analytics"}
    ]
    
    if role in ["super_admin"]:
        base_nav.extend([
            {"name": "Infrastructure", "url": "/infrastructure", "icon": "settings"},
            {"name": "AI Agents", "url": "/ai-agents", "icon": "robot"},
            {"name": "System Monitor", "url": "/monitor", "icon": "monitor"},
            {"name": "Users", "url": "/users", "icon": "users"},
            {"name": "Tenants", "url": "/tenants", "icon": "building"}
        ])
    
    elif role in ["tenant_admin"]:
        base_nav.extend([
            {"name": "Users", "url": "/users", "icon": "users"},
            {"name": "Settings", "url": "/settings", "icon": "settings"}
        ])
    
    elif role in ["manager"]:
        base_nav.extend([
            {"name": "Products", "url": "/products", "icon": "package"},
            {"name": "Orders", "url": "/orders", "icon": "shopping-cart"}
        ])
    
    # Add chat for eligible roles
    if role in ["super_admin", "tenant_admin", "manager", "client"]:
        base_nav.append({"name": "AI Assistant", "url": "/chat", "icon": "message-circle"})
    
    return base_nav

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")