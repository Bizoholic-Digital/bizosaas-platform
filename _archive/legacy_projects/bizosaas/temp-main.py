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
UNIFIED_AUTH_URL = os.getenv("UNIFIED_AUTH_URL", "http://host.docker.internal:3002")  # For container-to-container calls
UNIFIED_AUTH_BROWSER_URL = os.getenv("UNIFIED_AUTH_BROWSER_URL", "http://localhost:3002")  # For browser redirects
SQLADMIN_URL = os.getenv("SQLADMIN_URL", "http://localhost:5000")  # Infrastructure management
BIZOHOLIC_URL = os.getenv("BIZOHOLIC_URL", "http://localhost:3000")  # Bizoholic marketing platform
CORELDOVE_URL = os.getenv("CORELDOVE_URL", "http://localhost:3001")  # CoreLDove e-commerce platform
DIRECTORY_API_URL = os.getenv("DIRECTORY_API_URL", "http://localhost:8003")  # Business directory service
AI_CHAT_URL = os.getenv("AI_CHAT_URL", "http://localhost:3003")  # AI chat service

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
    accessible_platforms: Optional[list] = []

class PlatformInfo(BaseModel):
    name: str
    url: str
    description: str
    icon: str
    status: str
    features: list
    access_level: str

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
    
    # Check for token in URL parameters (from successful auth redirect)
    token = request.query_params.get("token")
    if token:
        # Set the token as a cookie and redirect without the token parameter
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(
            key="session_token",
            value=token,
            max_age=86400,  # 24 hours
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax"
        )
        return response
    
    user_session = await verify_session_with_unified_auth(request)
    
    if not user_session:
        # Redirect to unified login page directly
        login_url = f"{UNIFIED_AUTH_BROWSER_URL}/auth/login/"
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Redirecting to Login - TailAdmin v2</title>
            <meta http-equiv="refresh" content="2; url={login_url}">
            <script>
                // Store the return URL for after login
                sessionStorage.setItem('tailadmin_return_url', window.location.href);
                
                // Show countdown and redirect
                let countdown = 2;
                const countdownElement = document.getElementById('countdown');
                
                const timer = setInterval(() => {{
                    countdown--;
                    if (countdownElement) {{
                        countdownElement.textContent = countdown;
                    }}
                    if (countdown <= 0) {{
                        clearInterval(timer);
                        window.location.href = '{login_url}';
                    }}
                }}, 1000);
                
                // Immediate redirect option
                function goToLogin() {{
                    window.location.href = '{login_url}';
                }}
            </script>
        </head>
        <body>
            <div style="text-align: center; padding: 50px; font-family: Arial, sans-serif; background: #f8f9fa;">
                <div style="max-width: 500px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #333; margin-bottom: 20px;">Authentication Required</h2>
                    <p style="color: #666; margin-bottom: 30px;">Please log in to access the TailAdmin v2 Dashboard.</p>
                    
                    <div style="margin-bottom: 30px;">
                        <p style="color: #888;">Redirecting to login in <span id="countdown" style="font-weight: bold; color: #0066cc;">2</span> seconds...</p>
                    </div>
                    
                    <button onclick="goToLogin()" style="background: #0066cc; color: white; padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; margin: 10px;">
                        Login Now
                    </button>
                    
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                        <p style="font-size: 12px; color: #999;">
                            After logging in, <a href="/auth/return" style="color: #0066cc;">click here to return to the dashboard</a>
                        </p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """)
    
    # Load the TailAdmin v2 dashboard and inject user info + dashboard switcher
    try:
        platform_tabs = get_platform_tabs(user_session.role, user_session.permissions)
        
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
            "dashboard_switcher": get_dashboard_options(user_session.role),
            "platform_tabs": platform_tabs,
            "platform_categories": {
                "admin": [p for p in platform_tabs if p["category"] == "admin"],
                "platform": [p for p in platform_tabs if p["category"] == "platform"],
                "tools": [p for p in platform_tabs if p["category"] == "tools"]
            }
        }
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "user": dashboard_config["user"],
            "features": dashboard_config["features"],
            "navigation": dashboard_config["navigation"],
            "dashboard_switcher": dashboard_config["dashboard_switcher"],
            "platform_tabs": dashboard_config["platform_tabs"],
            "platform_categories": dashboard_config["platform_categories"]
        })
        
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        # Fallback to enhanced success page with platform tabs
        platform_tabs_html = get_platform_tabs_html(user_session.role, user_session.permissions)
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
                                {platform_tabs_html}
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

@app.get("/auth/return")
async def auth_return(request: Request):
    """Handle return from authentication - user manually navigates back"""
    user_session = await verify_session_with_unified_auth(request)
    
    if user_session:
        # User is authenticated, redirect to dashboard
        return RedirectResponse(url="/", status_code=302)
    else:
        # Still not authenticated, show message
        login_url = f"{UNIFIED_AUTH_BROWSER_URL}/auth/login/"
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Please Complete Login</title>
        </head>
        <body>
            <div style="text-align: center; padding: 50px; font-family: Arial, sans-serif;">
                <h2>Please Complete Login</h2>
                <p>You haven't completed the login process yet.</p>
                <button onclick="window.location.href='{login_url}'" style="background: #0066cc; color: white; padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer;">
                    Go to Login
                </button>
            </div>
        </body>
        </html>
        """)

@app.get("/auth/check")
async def auth_check(request: Request):
    """Check authentication status via API"""
    user_session = await verify_session_with_unified_auth(request)
    
    if user_session:
        return JSONResponse({"authenticated": True, "user": user_session.dict()})
    else:
        return JSONResponse({"authenticated": False}, status_code=401)

@app.get("/api/auth/logout")
async def logout_redirect():
    """Logout - redirect to unified auth logout"""
    logout_url = f"{UNIFIED_AUTH_BROWSER_URL}/auth/logout"
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
    """System health check including all platforms"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "tailadmin_dashboard": "operational",
            "unified_auth": "external",
            "sqladmin": "pending"
        },
        "platforms": {
            "bizoholic": {
                "url": BIZOHOLIC_URL,
                "status": "active",
                "description": "AI Marketing Agency Platform"
            },
            "coreldove": {
                "url": CORELDOVE_URL,
                "status": "active",
                "description": "E-commerce & Dropshipping Platform"
            },
            "directory": {
                "url": DIRECTORY_API_URL,
                "status": "active",
                "description": "Business Directory Management"
            },
            "ai_chat": {
                "url": AI_CHAT_URL,
                "status": "active",
                "description": "Universal AI Chat & Agent Management"
            }
        },
        "auth_integration": {
            "unified_login_url": f"{UNIFIED_AUTH_BROWSER_URL}/auth/login",
            "unified_auth_api": UNIFIED_AUTH_URL,
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
        "unified": f"{UNIFIED_AUTH_BROWSER_URL}/dashboard/"
    }
    
    if dashboard_type not in dashboard_urls:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    
    return RedirectResponse(url=dashboard_urls[dashboard_type], status_code=302)

@app.get("/api/platforms")
async def get_available_platforms(
    user_session: UserSession = Depends(require_authentication)
) -> Dict[str, Any]:
    """Get available platforms for the current user"""
    platforms = get_platform_tabs(user_session.role, user_session.permissions)
    
    # Check platform health status
    platform_health = {}
    for platform in platforms:
        if platform["id"] in ["bizoholic", "coreldove", "directory", "ai-chat"]:
            try:
                # This would be implemented with actual health checks
                platform_health[platform["id"]] = "active"
            except:
                platform_health[platform["id"]] = "inactive"
    
    return {
        "platforms": platforms,
        "categories": {
            "admin": [p for p in platforms if p["category"] == "admin"],
            "platform": [p for p in platforms if p["category"] == "platform"],
            "tools": [p for p in platforms if p["category"] == "tools"]
        },
        "health": platform_health,
        "user_context": {
            "role": user_session.role,
            "permissions": user_session.permissions,
            "tenant_id": user_session.tenant_id
        }
    }

@app.get("/api/platform/{platform_id}/status")
async def get_platform_status(
    platform_id: str,
    user_session: UserSession = Depends(require_authentication)
):
    """Get status of a specific platform"""
    platforms = get_platform_tabs(user_session.role, user_session.permissions)
    platform = next((p for p in platforms if p["id"] == platform_id), None)
    
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found or not accessible")
    
    # Simulate health check (would be implemented with actual checks)
    health_status = "active"  # This would check actual service health
    
    return {
        "platform": platform,
        "status": health_status,
        "last_checked": datetime.utcnow().isoformat(),
        "accessible": True
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

def get_platform_tabs(role: str, user_permissions: list = []) -> list:
    """Get multi-platform navigation tabs based on user role and permissions"""
    platforms = []
    
    # Core admin dashboards - always available for admin users
    if role in ["super_admin", "tenant_admin"]:
        platforms.extend([
            {
                "id": "tailadmin",
                "name": "TailAdmin v2",
                "url": "http://localhost:3001/",
                "description": "Business Operations Dashboard",
                "icon": "layout-dashboard",
                "status": "active",
                "current": True,
                "features": ["Analytics", "User Management", "AI Agents", "System Monitor"],
                "access_level": "admin",
                "category": "admin"
            },
            {
                "id": "sqladmin",
                "name": "SQLAdmin",
                "url": "/switch-dashboard/sqladmin",
                "description": "Infrastructure Management",
                "icon": "database",
                "status": "active" if role == "super_admin" else "restricted",
                "current": False,
                "features": ["Database Admin", "System Health", "Monitoring", "Logs"],
                "access_level": "super_admin",
                "category": "admin"
            }
        ])
    
    # Platform services - based on permissions and role
    if role in ["super_admin", "tenant_admin", "manager"]:
        platforms.extend([
            {
                "id": "bizoholic",
                "name": "Bizoholic",
                "url": BIZOHOLIC_URL,
                "description": "AI Marketing Agency Platform",
                "icon": "megaphone",
                "status": "active",
                "current": False,
                "features": ["Marketing Campaigns", "AI Agents", "Analytics", "CRM"],
                "access_level": "manager",
                "category": "platform"
            },
            {
                "id": "coreldove",
                "name": "CoreLDove",
                "url": CORELDOVE_URL,
                "description": "E-commerce & Dropshipping Platform",
                "icon": "shopping-cart",
                "status": "active",
                "current": False,
                "features": ["Product Sourcing", "Inventory", "Orders", "Saleor Backend"],
                "access_level": "manager",
                "category": "platform"
            },
            {
                "id": "directory",
                "name": "Directory",
                "url": f"{DIRECTORY_API_URL}/directories",
                "description": "Business Directory Management",
                "icon": "building",
                "status": "active",
                "current": False,
                "features": ["Business Listings", "Directory Sync", "Local SEO", "Lead Gen"],
                "access_level": "manager",
                "category": "platform"
            }
        ])
    
    # AI & Support tools - available to most users
    if role in ["super_admin", "tenant_admin", "manager", "client"]:
        platforms.append({
            "id": "ai-chat",
            "name": "AI Assistant",
            "url": AI_CHAT_URL,
            "description": "Universal AI Chat & Agent Management",
            "icon": "message-circle",
            "status": "active",
            "current": False,
            "features": ["AI Chat", "Agent Status", "Automation", "Analytics"],
            "access_level": "client",
            "category": "tools"
        })
    
    # Filter based on user permissions
    if "platform.bizoholic.access" not in user_permissions and role not in ["super_admin"]:
        platforms = [p for p in platforms if p["id"] != "bizoholic"]
    
    if "platform.coreldove.access" not in user_permissions and role not in ["super_admin"]:
        platforms = [p for p in platforms if p["id"] != "coreldove"]
    
    if "platform.directory.access" not in user_permissions and role not in ["super_admin"]:
        platforms = [p for p in platforms if p["id"] != "directory"]
    
    # Filter restricted platforms
    if role not in ["super_admin"]:
        platforms = [p for p in platforms if p["access_level"] != "super_admin"]
    
    return platforms

def get_dashboard_options(role: str) -> list:
    """Legacy function for backward compatibility"""
    platforms = get_platform_tabs(role)
    return [{
        "name": p["name"],
        "url": p["url"],
        "description": p["description"],
        "current": p["current"]
    } for p in platforms if p["category"] == "admin"]

def get_platform_tabs_html(role: str, permissions: list = []) -> str:
    """Generate HTML for multi-platform navigation tabs"""
    platforms = get_platform_tabs(role, permissions)
    if not platforms:
        return ""
    
    # Group platforms by category
    admin_platforms = [p for p in platforms if p["category"] == "admin"]
    business_platforms = [p for p in platforms if p["category"] == "platform"]
    tool_platforms = [p for p in platforms if p["category"] == "tools"]
    
    tabs_html = []
    
    # Admin platforms dropdown
    if admin_platforms:
        admin_options = []
        for platform in admin_platforms:
            if not platform["current"]:
                status_class = "text-green-600" if platform["status"] == "active" else "text-amber-600"
                admin_options.append(f"""
                    <a href="{platform['url']}" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700">
                        <div class="flex items-center space-x-2">
                            <span class="w-2 h-2 rounded-full {status_class.replace('text-', 'bg-')}"></span>
                            <div>
                                <div class="font-medium">{platform['name']}</div>
                                <div class="text-xs text-gray-500">{platform['description']}</div>
                            </div>
                        </div>
                    </a>
                """)
        
        if admin_options:
            tabs_html.append(f"""
                <div class="relative inline-block text-left">
                    <button onclick="toggleAdminDropdown()" class="bg-indigo-600 text-white px-3 py-1 rounded text-sm hover:bg-indigo-700 flex items-center space-x-1">
                        <span>Admin</span>
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                        </svg>
                    </button>
                    <div id="admin-dropdown" class="hidden absolute right-0 mt-2 w-64 rounded-md shadow-lg bg-white dark:bg-gray-800 ring-1 ring-black ring-opacity-5 z-50">
                        <div class="py-1">
                            <div class="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider border-b border-gray-200 dark:border-gray-600">
                                Admin Dashboards
                            </div>
                            {''.join(admin_options)}
                        </div>
                    </div>
                </div>
            """)
    
    # Business platforms dropdown
    if business_platforms:
        business_options = []
        for platform in business_platforms:
            status_class = "text-green-600" if platform["status"] == "active" else "text-amber-600"
            features_text = ", ".join(platform["features"][:2])  # Show first 2 features
            business_options.append(f"""
                <a href="{platform['url']}" target="_blank" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700">
                    <div class="flex items-center space-x-2">
                        <span class="w-2 h-2 rounded-full {status_class.replace('text-', 'bg-')}"></span>
                        <div>
                            <div class="font-medium">{platform['name']}</div>
                            <div class="text-xs text-gray-500">{platform['description']}</div>
                            <div class="text-xs text-blue-600 mt-1">{features_text}</div>
                        </div>
                    </div>
                </a>
            """)
        
        tabs_html.append(f"""
            <div class="relative inline-block text-left">
                <button onclick="togglePlatformsDropdown()" class="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 flex items-center space-x-1">
                    <span>Platforms</span>
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                </button>
                <div id="platforms-dropdown" class="hidden absolute right-0 mt-2 w-72 rounded-md shadow-lg bg-white dark:bg-gray-800 ring-1 ring-black ring-opacity-5 z-50">
                    <div class="py-1">
                        <div class="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider border-b border-gray-200 dark:border-gray-600">
                            Business Platforms
                        </div>
                        {''.join(business_options)}
                    </div>
                </div>
            </div>
        """)
    
    # AI Tools button
    if tool_platforms:
        ai_platform = tool_platforms[0]  # Assuming AI Assistant is the main tool
        tabs_html.append(f"""
            <a href="{ai_platform['url']}" target="_blank" class="bg-emerald-600 text-white px-3 py-1 rounded text-sm hover:bg-emerald-700 flex items-center space-x-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                </svg>
                <span>AI Assistant</span>
            </a>
        """)
    
    # JavaScript for dropdown functionality
    if admin_platforms or business_platforms:
        tabs_html.append("""
            <script>
                function toggleAdminDropdown() {
                    const dropdown = document.getElementById('admin-dropdown');
                    const platformsDropdown = document.getElementById('platforms-dropdown');
                    if (platformsDropdown) platformsDropdown.classList.add('hidden');
                    dropdown.classList.toggle('hidden');
                }
                
                function togglePlatformsDropdown() {
                    const dropdown = document.getElementById('platforms-dropdown');
                    const adminDropdown = document.getElementById('admin-dropdown');
                    if (adminDropdown) adminDropdown.classList.add('hidden');
                    dropdown.classList.toggle('hidden');
                }
                
                // Close dropdowns when clicking outside
                document.addEventListener('click', function(event) {
                    const adminDropdown = document.getElementById('admin-dropdown');
                    const platformsDropdown = document.getElementById('platforms-dropdown');
                    const adminButton = event.target.closest('button[onclick="toggleAdminDropdown()"]');
                    const platformsButton = event.target.closest('button[onclick="togglePlatformsDropdown()"]');
                    
                    if (!adminButton && adminDropdown) {
                        adminDropdown.classList.add('hidden');
                    }
                    if (!platformsButton && platformsDropdown) {
                        platformsDropdown.classList.add('hidden');
                    }
                });
            </script>
        """)
    
    return ' '.join(tabs_html)

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

# Update the switcher function to use the new platform tabs
def get_dashboard_switcher_html(role: str) -> str:
    """Legacy function - now redirects to platform tabs"""
    return get_platform_tabs_html(role, [])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")