#!/usr/bin/env python3

"""
TailAdmin v2 Dashboard - Unified Authentication
Integrates with localhost:3002 auth system and supports dashboard switching
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
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
STATIC_FILES_PATH = os.getenv("STATIC_FILES_PATH", "/app/html")
UNIFIED_AUTH_URL = os.getenv("UNIFIED_AUTH_URL", "http://localhost:3002")
SQLADMIN_URL = os.getenv("SQLADMIN_URL", "http://localhost:5000")  # Will be implemented

app = FastAPI(
    title="TailAdmin v2 Dashboard - Unified Auth",
    description="Secured business operations dashboard with unified authentication",
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

# Templates and static files
templates = Jinja2Templates(directory=STATIC_FILES_PATH)
app.mount("/static", StaticFiles(directory=f"{STATIC_FILES_PATH}/static"), name="static")

# Pydantic models
class UserSession(BaseModel):
    user_id: str
    email: str
    role: str
    permissions: list
    tenant_id: Optional[str] = None

# Authentication functions
async def verify_session_with_unified_auth(request: Request) -> Optional[UserSession]:
    """Verify session with the unified auth system at localhost:3002"""
    try:
        # Get session token from cookie
        session_token = request.cookies.get("session_token") or request.cookies.get("auth_token")
        
        if not session_token:
            # Try Authorization header
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                session_token = auth_header[7:]
        
        if not session_token:
            return None
        
        # Verify session with unified auth system
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {session_token}"}
            try:
                async with session.get(f"{UNIFIED_AUTH_URL}/api/auth/verify", headers=headers) as response:
                    if response.status == 200:
                        user_data = await response.json()
                        return UserSession(
                            user_id=user_data.get("id", "unknown"),
                            email=user_data.get("email", "unknown"),
                            role=user_data.get("role", "client"),
                            permissions=user_data.get("permissions", []),
                            tenant_id=user_data.get("tenant_id")
                        )
                    else:
                        logger.warning(f"Session verification failed: {response.status}")
                        return None
            except aiohttp.ClientError as e:
                logger.error(f"Auth service connection error: {e}")
                return None
    
    except Exception as e:
        logger.error(f"Session verification error: {e}")
        return None

async def require_authentication(request: Request) -> UserSession:
    """Dependency to require authentication"""
    user_session = await verify_session_with_unified_auth(request)
    if not user_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return user_session

# Routes

@app.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request):
    """Main TailAdmin v2 dashboard - requires authentication"""
    user_session = await verify_session_with_unified_auth(request)
    
    if not user_session:
        # Redirect to unified login with return URL
        redirect_url = f"{UNIFIED_AUTH_URL}/auth/login/?redirect=http://localhost:3001/"
        return RedirectResponse(url=redirect_url, status_code=302)
    
    # Load the TailAdmin v2 dashboard and inject user info + dashboard switcher
    try:
        dashboard_config = {
            "user": {
                "id": user_session.user_id,
                "email": user_session.email,
                "role": user_session.role,
                "permissions": user_session.permissions,
                "tenant_id": user_session.tenant_id
            },
            "features": get_features_for_role(user_session.role),
            "navigation": get_navigation_for_role(user_session.role),
            "dashboard_switcher": get_dashboard_options(user_session.role)
        }
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "user": dashboard_config["user"],
            "features": dashboard_config["features"],
            "navigation": dashboard_config["navigation"],
            "dashboard_switcher": dashboard_config["dashboard_switcher"]
        })
        
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        # Fallback to enhanced success page with dashboard switcher
        switcher_html = get_dashboard_switcher_html(user_session.role)
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>BizOSaaS - TailAdmin v2 Dashboard</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-50 dark:bg-gray-900">
            <div class="min-h-screen">
                <header class="bg-white dark:bg-gray-800 shadow">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div class="flex justify-between h-16">
                            <div class="flex items-center">
                                <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
                                    TailAdmin v2 Dashboard
                                </h1>
                            </div>
                            <div class="flex items-center space-x-4">
                                {switcher_html}
                                <div class="text-sm text-gray-600 dark:text-gray-300">
                                    {user_session.email} ({user_session.role})
                                </div>
                                <a href="/api/auth/logout" class="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700">
                                    Logout
                                </a>
                            </div>
                        </div>
                    </div>
                </header>
                <main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
                        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                            Welcome to TailAdmin v2 Dashboard
                        </h2>
                        <p class="text-gray-600 dark:text-gray-300 mb-4">
                            User: {user_session.email} | Role: {user_session.role} | Authenticated at {datetime.utcnow()}
                        </p>
                        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            <div class="bg-blue-50 dark:bg-blue-900 p-4 rounded-lg">
                                <h3 class="font-semibold text-blue-800 dark:text-blue-200">Analytics</h3>
                                <p class="text-blue-700 dark:text-blue-300 text-sm">Business performance metrics</p>
                            </div>
                            <div class="bg-green-50 dark:bg-green-900 p-4 rounded-lg">
                                <h3 class="font-semibold text-green-800 dark:text-green-200">AI Agents</h3>
                                <p class="text-green-700 dark:text-green-300 text-sm">28+ autonomous marketing agents</p>
                            </div>
                            <div class="bg-purple-50 dark:bg-purple-900 p-4 rounded-lg">
                                <h3 class="font-semibold text-purple-800 dark:text-purple-200">User Management</h3>
                                <p class="text-purple-700 dark:text-purple-300 text-sm">Team and access control</p>
                            </div>
                        </div>
                    </div>
                </main>
            </div>
        </body>
        </html>
        """)

@app.get("/api/auth/logout")
async def logout_redirect():
    """Logout - redirect to unified auth logout"""
    logout_url = f"{UNIFIED_AUTH_URL}/auth/logout"
    return RedirectResponse(url=logout_url, status_code=302)

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

@app.get("/api/system/health")
async def system_health():
    """System health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "tailadmin_dashboard": "operational",
            "unified_auth": "external",
            "sqladmin": "pending"
        },
        "auth_integration": {
            "unified_login_url": f"{UNIFIED_AUTH_URL}/auth/login",
            "sqladmin_url": SQLADMIN_URL
        }
    }

@app.get("/switch-dashboard/{dashboard_type}")
async def switch_dashboard(
    dashboard_type: str, 
    user_session: UserSession = Depends(require_authentication)
):
    """Switch between admin dashboards (super admin only)"""
    if user_session.role not in ["super_admin", "tenant_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to switch dashboards"
        )
    
    dashboard_urls = {
        "tailadmin": "http://localhost:3001/",
        "sqladmin": SQLADMIN_URL,
        "unified": f"{UNIFIED_AUTH_URL}/dashboard/"
    }
    
    if dashboard_type not in dashboard_urls:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    
    return RedirectResponse(url=dashboard_urls[dashboard_type], status_code=302)

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
            "chat_ai": True,
            "dashboard_switching": True
        },
        "tenant_admin": {
            "infrastructure": False,
            "ai_agents": True,
            "system_monitoring": False,
            "user_management": True,
            "tenant_management": True,
            "saleor_access": True,
            "analytics": True,
            "chat_ai": True,
            "dashboard_switching": True
        },
        "manager": {
            "infrastructure": False,
            "ai_agents": False,
            "system_monitoring": False,
            "user_management": False,
            "tenant_management": False,
            "saleor_access": True,
            "analytics": True,
            "chat_ai": True,
            "dashboard_switching": False
        }
    }
    
    return feature_map.get(role, {
        "infrastructure": False,
        "ai_agents": False,
        "system_monitoring": False,
        "user_management": False,
        "tenant_management": False,
        "saleor_access": False,
        "analytics": True,
        "chat_ai": True,
        "dashboard_switching": False
    })

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

def get_dashboard_options(role: str) -> list:
    """Get available dashboard options for role"""
    if role in ["super_admin"]:
        return [
            {
                "name": "TailAdmin v2",
                "url": "http://localhost:3001/",
                "description": "Business Operations Dashboard",
                "current": True
            },
            {
                "name": "SQLAdmin",
                "url": "/switch-dashboard/sqladmin",
                "description": "Infrastructure Management",
                "current": False
            },
            {
                "name": "Unified Platform",
                "url": "/switch-dashboard/unified",
                "description": "Main BizOSaaS Platform",
                "current": False
            }
        ]
    elif role in ["tenant_admin"]:
        return [
            {
                "name": "TailAdmin v2",
                "url": "http://localhost:3001/",
                "description": "Business Operations Dashboard",
                "current": True
            },
            {
                "name": "Unified Platform",
                "url": "/switch-dashboard/unified",
                "description": "Main BizOSaaS Platform",
                "current": False
            }
        ]
    else:
        return []

def get_dashboard_switcher_html(role: str) -> str:
    """Generate HTML for dashboard switcher"""
    options = get_dashboard_options(role)
    if not options:
        return ""
    
    switcher_options = []
    for option in options:
        if not option["current"]:
            switcher_options.append(f"""
                <a href="{option['url']}" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700">
                    <div class="font-medium">{option['name']}</div>
                    <div class="text-xs text-gray-500">{option['description']}</div>
                </a>
            """)
    
    if switcher_options:
        return f"""
        <div class="relative inline-block text-left">
            <button onclick="toggleDropdown()" class="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700">
                Switch Dashboard
            </button>
            <div id="dropdown" class="hidden absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white dark:bg-gray-800 ring-1 ring-black ring-opacity-5">
                <div class="py-1">
                    {''.join(switcher_options)}
                </div>
            </div>
        </div>
        <script>
            function toggleDropdown() {{
                const dropdown = document.getElementById('dropdown');
                dropdown.classList.toggle('hidden');
            }}
            // Close dropdown when clicking outside
            document.addEventListener('click', function(event) {{
                const dropdown = document.getElementById('dropdown');
                const button = event.target.closest('button');
                if (!button || button.textContent.trim() !== 'Switch Dashboard') {{
                    dropdown.classList.add('hidden');
                }}
            }});
        </script>
        """
    return ""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")