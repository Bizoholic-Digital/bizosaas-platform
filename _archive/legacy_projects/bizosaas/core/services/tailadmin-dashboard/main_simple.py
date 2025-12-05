#!/usr/bin/env python3

"""
TailAdmin v2 Dashboard - Simple Secured Version
Basic authentication until auth-service-v2 integration is complete
"""

import os
import json
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import FastAPI, Request, HTTPException, Depends, status, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
STATIC_FILES_PATH = os.getenv("STATIC_FILES_PATH", "/app/html")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
SESSION_SECRET = os.getenv("SESSION_SECRET", secrets.token_hex(32))

app = FastAPI(
    title="TailAdmin v2 Dashboard - Secured",
    description="Secured business operations dashboard",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer(auto_error=False)

# Templates and static files
templates = Jinja2Templates(directory=STATIC_FILES_PATH)
app.mount("/static", StaticFiles(directory=f"{STATIC_FILES_PATH}/static"), name="static")

# Simple session storage (in production, use Redis)
active_sessions = {}

# Pydantic models
class LoginRequest(BaseModel):
    email: str
    password: str
    remember_me: bool = False

class UserSession(BaseModel):
    user_id: str
    email: str
    role: str
    expires_at: datetime

# Authentication functions
def create_session_token() -> str:
    """Create a secure session token"""
    return secrets.token_urlsafe(32)

def verify_credentials(email: str, password: str) -> bool:
    """Verify user credentials (simple implementation)"""
    return email == ADMIN_USERNAME and password == ADMIN_PASSWORD

def create_user_session(email: str, remember_me: bool = False) -> tuple:
    """Create a new user session"""
    session_token = create_session_token()
    expires_at = datetime.utcnow() + timedelta(hours=24 if remember_me else 1)
    
    user_session = UserSession(
        user_id="admin",
        email=email,
        role="super_admin",
        expires_at=expires_at
    )
    
    active_sessions[session_token] = user_session
    return session_token, user_session

def verify_session_token(token: str) -> Optional[UserSession]:
    """Verify session token and return user session"""
    if token not in active_sessions:
        return None
    
    session = active_sessions[token]
    if datetime.utcnow() > session.expires_at:
        del active_sessions[token]
        return None
    
    return session

async def get_current_user(request: Request) -> Optional[UserSession]:
    """Get current user from session"""
    # Try to get session token from cookie
    session_token = request.cookies.get("session_token")
    
    if not session_token:
        # Try Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            session_token = auth_header[7:]
    
    if not session_token:
        return None
    
    return verify_session_token(session_token)

async def require_authentication(request: Request) -> UserSession:
    """Dependency to require authentication"""
    user = await get_current_user(request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return user

# Routes

@app.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request):
    """Main dashboard - requires authentication"""
    user = await get_current_user(request)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # Load the TailAdmin v2 dashboard and inject user info
    try:
        dashboard_config = {
            "user": {
                "id": user.user_id,
                "email": user.email,
                "role": user.role,
                "permissions": ["admin:*"] if user.role == "super_admin" else []
            },
            "features": get_features_for_role(user.role),
            "navigation": get_navigation_for_role(user.role)
        }
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "user": dashboard_config["user"],
            "features": dashboard_config["features"],
            "navigation": dashboard_config["navigation"]
        })
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        # Fallback to simple success page
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head><title>BizOSaaS Admin Dashboard</title></head>
        <body>
            <h1>Welcome to BizOSaaS Admin Dashboard</h1>
            <p>User: {user.email} ({user.role})</p>
            <p>Authenticated successfully at {datetime.utcnow()}</p>
            <p><a href="/api/auth/logout">Logout</a></p>
        </body>
        </html>
        """)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    user = await get_current_user(request)
    if user:
        return RedirectResponse(url="/", status_code=302)
    
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/api/auth/login")
async def login(login_data: LoginRequest, response: Response):
    """Login endpoint"""
    try:
        if not verify_credentials(login_data.email, login_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        session_token, user_session = create_user_session(
            login_data.email, 
            login_data.remember_me
        )
        
        # Create response
        response_data = JSONResponse(content={
            "success": True,
            "user": {
                "id": user_session.user_id,
                "email": user_session.email,
                "role": user_session.role
            }
        })
        
        # Set session cookie
        response_data.set_cookie(
            key="session_token",
            value=session_token,
            max_age=86400 if login_data.remember_me else 3600,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax"
        )
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/auth/logout")
async def logout(request: Request):
    """Logout endpoint"""
    try:
        session_token = request.cookies.get("session_token")
        if session_token and session_token in active_sessions:
            del active_sessions[session_token]
        
        response = JSONResponse(content={"success": True})
        response.delete_cookie(key="session_token")
        return response
        
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/user/profile")
async def get_user_profile(user: UserSession = Depends(require_authentication)):
    """Get current user profile"""
    return {
        "user_id": user.user_id,
        "email": user.email,
        "role": user.role,
        "expires_at": user.expires_at.isoformat()
    }

@app.get("/api/system/health")
async def system_health():
    """System health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "dashboard": "operational",
            "authentication": "operational"
        },
        "active_sessions": len(active_sessions)
    }

# Helper functions
def get_features_for_role(role: str) -> Dict[str, Any]:
    """Get available features based on user role"""
    if role == "super_admin":
        return {
            "infrastructure": True,
            "ai_agents": True,
            "system_monitoring": True,
            "user_management": True,
            "tenant_management": True,
            "saleor_access": True,
            "analytics": True,
            "chat_ai": True
        }
    else:
        return {
            "infrastructure": False,
            "ai_agents": False,
            "system_monitoring": False,
            "user_management": False,
            "tenant_management": False,
            "saleor_access": True,
            "analytics": True,
            "chat_ai": True
        }

def get_navigation_for_role(role: str) -> list:
    """Get navigation menu based on user role"""
    base_nav = [
        {"name": "Dashboard", "url": "/", "icon": "dashboard"},
        {"name": "Analytics", "url": "/analytics", "icon": "analytics"}
    ]
    
    if role == "super_admin":
        base_nav.extend([
            {"name": "Infrastructure", "url": "/infrastructure", "icon": "settings"},
            {"name": "AI Agents", "url": "/ai-agents", "icon": "robot"},
            {"name": "System Monitor", "url": "/monitor", "icon": "monitor"},
            {"name": "Users", "url": "/users", "icon": "users"},
            {"name": "Tenants", "url": "/tenants", "icon": "building"}
        ])
    
    base_nav.append({"name": "AI Assistant", "url": "/chat", "icon": "message-circle"})
    return base_nav

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")