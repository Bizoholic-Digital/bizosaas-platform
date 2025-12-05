#!/usr/bin/env python3

"""
SQLAdmin Dashboard - Infrastructure Management Service
Integrates with localhost:3002 auth system for SUPER_ADMIN only access
Provides database administration and system monitoring interface
"""

import os
import json
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import logging
from sqlalchemy import create_engine, MetaData, inspect, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
import uvicorn

# Import enhanced authentication middleware
from auth_middleware import (
    UserSession, 
    AuthenticationError,
    verify_session, 
    require_authentication, 
    require_super_admin,
    get_login_redirect_url,
    get_logout_url
)

# Import monitoring models and views
from monitoring_models import *
from monitoring_views import (
    # AI Monitoring Views
    AIAgentMonitoringView, WorkflowExecutionView, AgentErrorLogView,
    # Infrastructure Views
    DatabaseHealthMetricsView, RedisHealthMetricsView, ContainerMetricsView, APIEndpointMetricsView,
    # Business Operations Views
    TenantActivityMetricsView, UserSessionAnalyticsView, PlatformUsageStatsView,
    # Security & Compliance Views
    SecurityEventLogView, AuthenticationLogView, RateLimitStatusView, AdminActionAuditView,
    # Integration Monitoring Views
    ExternalAPIHealthView, WebhookDeliveryStatusView, DataSyncStatusView, IntegrationConnectivityView,
    # Alerts
    SystemAlertView,
    # Dashboard
    InfrastructureDashboardView
)

# Import comprehensive admin views
from admin_views import *

# Import monitoring service
from monitoring_service import MonitoringService, create_monitoring_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
UNIFIED_AUTH_URL = os.getenv("UNIFIED_AUTH_URL", "http://host.docker.internal:3002")
UNIFIED_AUTH_BROWSER_URL = os.getenv("UNIFIED_AUTH_BROWSER_URL", "http://localhost:3002")
TAILADMIN_URL = os.getenv("TAILADMIN_URL", "http://localhost:3001")
# Multi-platform URLs
BIZOHOLIC_URL = os.getenv("BIZOHOLIC_URL", "http://localhost:3000")
CORELDOVE_URL = os.getenv("CORELDOVE_URL", "http://localhost:3001")
DIRECTORY_API_URL = os.getenv("DIRECTORY_API_URL", "http://localhost:8003")
AI_CHAT_URL = os.getenv("AI_CHAT_URL", "http://localhost:3003")

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://bizosaas:bizosaas@host.docker.internal:5432/bizosaas")
DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL", "postgresql://bizosaas:bizosaas@host.docker.internal:5432/bizosaas")

# Create FastAPI app
app = FastAPI(
    title="SQLAdmin Dashboard - Infrastructure Management",
    description="Database administration and system monitoring for SUPER_ADMIN users",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
engine = create_engine(DATABASE_SYNC_URL)
async_engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)

# Additional models for system health
class SystemHealthResponse(BaseModel):
    status: str
    timestamp: str
    database: Dict[str, Any]
    services: Dict[str, str]
    user: Dict[str, str]
    platforms: Optional[Dict[str, Any]] = {}

class PlatformInfo(BaseModel):
    name: str
    url: str
    description: str
    icon: str
    status: str
    features: list
    access_level: str
    category: str

class SystemHealth(BaseModel):
    database: str
    redis: str
    vault: str
    ai_agents: str
    disk_usage: Dict[str, Any]
    memory_usage: Dict[str, Any]
    active_connections: int

# Authentication error handler
@app.exception_handler(AuthenticationError)
async def auth_exception_handler(request: Request, exc: AuthenticationError):
    """Handle authentication errors with appropriate redirects"""
    if exc.status_code == 401:
        # Redirect to login page
        redirect_url = get_login_redirect_url(str(request.url))
        return RedirectResponse(url=redirect_url, status_code=302)
    else:
        # Return error response for other auth errors
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )

# SQLAdmin Authentication Backend
class UnifiedAuthBackend(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        """Check authentication status"""
        try:
            user_session = await verify_session(request)
            if user_session and user_session.is_super_admin:
                request.session["user"] = user_session.dict()
                return True
            return False
        except Exception as e:
            logger.error(f"Login check error: {e}")
            return False

    async def logout(self, request: Request) -> bool:
        """Logout - clear session"""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Verify current authentication"""
        try:
            user_data = request.session.get("user")
            if user_data:
                # Verify session is still valid
                user_session = await verify_session(request)
                return user_session and user_session.is_super_admin
            return False
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return False

# Initialize SQLAdmin
authentication_backend = UnifiedAuthBackend(secret_key="your-secret-key-here")
admin = Admin(app, engine, authentication_backend=authentication_backend)

# Database Models for SQLAdmin (simplified for admin interface)
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, JSON, ForeignKey, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class TenantAdmin(Base):
    __tablename__ = "tenants"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(100))
    slug = Column(String(50))
    status = Column(String(20))
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    subscription_plan = Column(String(50))
    subscription_status = Column(String(20))
    allowed_platforms = Column(JSON)
    settings = Column(JSON)

class UserAdmin(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String(255))
    first_name = Column(String(50))
    last_name = Column(String(50))
    role = Column(String(20))
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    is_active = Column(Boolean)
    is_superuser = Column(Boolean)
    is_verified = Column(Boolean)
    created_at = Column(DateTime(timezone=True))
    last_login_at = Column(DateTime(timezone=True))
    login_count = Column(Integer)
    allowed_services = Column(JSON)

class UserSessionAdmin(Base):
    __tablename__ = "user_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    session_token = Column(String(255))
    refresh_token = Column(String(255))
    created_at = Column(DateTime(timezone=True))
    expires_at = Column(DateTime(timezone=True))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    platform = Column(String(50))
    is_active = Column(Boolean)

# Admin Views
class TenantAdminView(ModelView, model=TenantAdmin):
    column_list = [TenantAdmin.id, TenantAdmin.name, TenantAdmin.slug, TenantAdmin.status, TenantAdmin.created_at]
    column_details_list = [
        TenantAdmin.id, TenantAdmin.name, TenantAdmin.slug, TenantAdmin.status,
        TenantAdmin.subscription_plan, TenantAdmin.subscription_status,
        TenantAdmin.allowed_platforms, TenantAdmin.created_at, TenantAdmin.updated_at
    ]
    column_searchable_list = [TenantAdmin.name, TenantAdmin.slug]
    column_sortable_list = [TenantAdmin.name, TenantAdmin.created_at, TenantAdmin.status]

class UserAdminView(ModelView, model=UserAdmin):
    column_list = [UserAdmin.id, UserAdmin.email, UserAdmin.role, UserAdmin.is_active, UserAdmin.created_at]
    column_details_list = [
        UserAdmin.id, UserAdmin.email, UserAdmin.first_name, UserAdmin.last_name,
        UserAdmin.role, UserAdmin.tenant_id, UserAdmin.is_active, UserAdmin.is_superuser,
        UserAdmin.is_verified, UserAdmin.last_login_at, UserAdmin.login_count,
        UserAdmin.allowed_services
    ]
    column_searchable_list = [UserAdmin.email, UserAdmin.first_name, UserAdmin.last_name]
    column_sortable_list = [UserAdmin.email, UserAdmin.created_at, UserAdmin.role]

class UserSessionAdminView(ModelView, model=UserSessionAdmin):
    column_list = [UserSessionAdmin.id, UserSessionAdmin.user_id, UserSessionAdmin.platform, UserSessionAdmin.created_at, UserSessionAdmin.is_active]
    column_details_list = [
        UserSessionAdmin.id, UserSessionAdmin.user_id, UserSessionAdmin.tenant_id,
        UserSessionAdmin.created_at, UserSessionAdmin.expires_at, UserSessionAdmin.ip_address,
        UserSessionAdmin.user_agent, UserSessionAdmin.platform, UserSessionAdmin.is_active
    ]
    column_sortable_list = [UserSessionAdminView.created_at, UserSessionAdminView.expires_at]

# Register all comprehensive admin views

# Core Platform Views
admin.add_view(TenantAdminView)
admin.add_view(UserAdminView)
admin.add_view(UserSessionAdminView)
admin.add_view(OrganizationAdminView)

# CRM Views
admin.add_view(ContactAdminView)
admin.add_view(LeadAdminView)
admin.add_view(DealAdminView)
admin.add_view(ActivityAdminView)
admin.add_view(CampaignAdminView)

# E-commerce Views
admin.add_view(ProductAdminView)
admin.add_view(CategoryAdminView)
admin.add_view(OrderAdminView)
admin.add_view(CustomerAdminView)
admin.add_view(InventoryAdminView)

# CMS Views
admin.add_view(PageAdminView)
admin.add_view(MediaAdminView)
admin.add_view(FormAdminView)
admin.add_view(CollectionAdminView)
admin.add_view(MenuAdminView)

# Billing Views
admin.add_view(PlanAdminView)
admin.add_view(SubscriptionAdminView)
admin.add_view(InvoiceAdminView)
admin.add_view(PaymentAdminView)

# Analytics Views
admin.add_view(EventAdminView)
admin.add_view(MetricAdminView)
admin.add_view(AnalyticsReportAdminView)
admin.add_view(DashboardAdminView)

# Integration Views
admin.add_view(IntegrationAdminView)
admin.add_view(WebhookAdminView)
admin.add_view(ExternalServiceAdminView)
admin.add_view(APIKeyAdminView)

# Security Views
admin.add_view(SecurityEventAdminView)
admin.add_view(AuditLogAdminView)
admin.add_view(RoleAdminView)
admin.add_view(PermissionAdminView)

# Custom Dashboard Views
admin.add_view(PlatformOverviewView)
admin.add_view(SystemHealthView)

# Register monitoring views
# AI Monitoring
admin.add_view(AIAgentMonitoringView)
admin.add_view(WorkflowExecutionView)
admin.add_view(AgentErrorLogView)

# Infrastructure Monitoring
admin.add_view(DatabaseHealthMetricsView)
admin.add_view(RedisHealthMetricsView)
admin.add_view(ContainerMetricsView)
admin.add_view(APIEndpointMetricsView)

# Business Operations
admin.add_view(TenantActivityMetricsView)
admin.add_view(UserSessionAnalyticsView)
admin.add_view(PlatformUsageStatsView)

# Security & Compliance
admin.add_view(SecurityEventLogView)
admin.add_view(AuthenticationLogView)
admin.add_view(RateLimitStatusView)
admin.add_view(AdminActionAuditView)

# Integration Monitoring
admin.add_view(ExternalAPIHealthView)
admin.add_view(WebhookDeliveryStatusView)
admin.add_view(DataSyncStatusView)
admin.add_view(IntegrationConnectivityView)

# System Alerts
admin.add_view(SystemAlertView)

# Custom Dashboards
admin.add_view(InfrastructureDashboardView)

# Custom routes
@app.get("/")
async def dashboard_home(request: Request):
    """Redirect to admin interface or show login requirement"""
    user_session = await verify_session(request)
    
    if not user_session:
        # Redirect to unified login with return URL
        redirect_url = get_login_redirect_url("http://localhost:5000/")
        return RedirectResponse(url=redirect_url, status_code=302)
    
    if not user_session.is_super_admin:
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Access Denied - SQLAdmin</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-50 dark:bg-gray-900">
            <div class="min-h-screen flex items-center justify-center">
                <div class="max-w-md w-full bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6">
                    <div class="text-center">
                        <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
                            <svg class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                            </svg>
                        </div>
                        <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">Access Denied</h3>
                        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                            SUPER_ADMIN role required for infrastructure management
                        </p>
                        <p class="mt-2 text-xs text-gray-400 dark:text-gray-500">
                            Current role: {user_session.role} | Required: SUPER_ADMIN
                        </p>
                        <div class="mt-6 flex space-x-3">
                            <a href="{TAILADMIN_URL}" 
                               class="w-full bg-blue-600 text-white py-2 px-4 rounded-md text-sm hover:bg-blue-700 transition-colors">
                                Go to TailAdmin
                            </a>
                            <a href="{get_logout_url()}" 
                               class="w-full bg-gray-600 text-white py-2 px-4 rounded-md text-sm hover:bg-gray-700 transition-colors">
                                Logout
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """, status_code=403)
    
    # Redirect to admin interface for super admins
    return RedirectResponse(url="/admin", status_code=302)

@app.get("/dashboard-switcher")
async def dashboard_switcher(user_session: UserSession = Depends(require_super_admin)):
    """Enhanced multi-platform dashboard switcher for super admins"""
    platforms = get_platform_tabs(user_session.role, user_session.permissions)
    
    # Create cards for each platform category
    admin_cards = ""
    platform_cards = ""
    tool_cards = ""
    
    for platform in platforms:
        status_color = "green" if platform["status"] == "active" else "amber"
        border_class = "border-2 border-green-200" if platform["current"] else ""
        button_class = "bg-green-50 text-green-700 border-green-200" if platform["current"] else "bg-blue-600 text-white hover:bg-blue-700"
        button_text = "Current Dashboard" if platform["current"] else "Open Platform"
        
        card_html = f"""
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6 {border_class}">
            <div class="flex items-center">
                <div class="flex-shrink-0">
                    <div class="w-12 h-12 bg-{status_color}-100 rounded-lg flex items-center justify-center">
                        <div class="w-6 h-6 bg-{status_color}-600 rounded"></div>
                    </div>
                </div>
                <div class="ml-4 flex-1">
                    <h3 class="text-lg font-medium text-gray-900 dark:text-white">{platform['name']}</h3>
                    <p class="text-sm text-gray-500 dark:text-gray-400">{platform['description']}</p>
                    <p class="text-xs text-blue-600 mt-1">{', '.join(platform['features'][:3])}</p>
                    <div class="mt-3">
                        {'<span class="inline-flex items-center px-4 py-2 border text-sm font-medium rounded-md " + button_class + "">' + button_text + '</span>' if platform['current'] else '<a href="' + platform['url'] + '" target="_blank" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md ' + button_class + '">' + button_text + '</a>'}
                    </div>
                </div>
            </div>
        </div>
        """
        
        if platform["category"] == "admin":
            admin_cards += card_html
        elif platform["category"] == "platform":
            platform_cards += card_html
        elif platform["category"] == "tools":
            tool_cards += card_html
    
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Multi-Platform Dashboard - BizOSaaS</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50 dark:bg-gray-900">
        <div class="min-h-screen">
            <header class="bg-white dark:bg-gray-800 shadow">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="flex justify-between h-16">
                        <div class="flex items-center">
                            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
                                BizOSaaS Multi-Platform Dashboard
                            </h1>
                        </div>
                        <div class="flex items-center space-x-4">
                            {get_platform_tabs_html(user_session.role, user_session.permissions)}
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
            <main class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
                        <div class="flex items-center">
                            <div class="flex-shrink-0">
                                <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                                    <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H9z"></path>
                                    </svg>
                                </div>
                            </div>
                            <div class="ml-4 flex-1">
                                <h3 class="text-lg font-medium text-gray-900 dark:text-white">TailAdmin v2</h3>
                                <p class="text-sm text-gray-500 dark:text-gray-400">Business Operations Dashboard</p>
                                <a href="{TAILADMIN_URL}" class="mt-3 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
                                    Open Dashboard
                                </a>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6 border-2 border-green-200">
                        <div class="flex items-center">
                            <div class="flex-shrink-0">
                                <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                                    <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4"></path>
                                    </svg>
                                </div>
                            </div>
                            <div class="ml-4 flex-1">
                                <h3 class="text-lg font-medium text-gray-900 dark:text-white">SQLAdmin</h3>
                                <p class="text-sm text-gray-500 dark:text-gray-400">Infrastructure Management (Current)</p>
                                <span class="mt-3 inline-flex items-center px-4 py-2 border border-green-200 text-sm font-medium rounded-md text-green-700 bg-green-50">
                                    Current Dashboard
                                </span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
                        <div class="flex items-center">
                            <div class="flex-shrink-0">
                                <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                                    <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                                    </svg>
                                </div>
                            </div>
                            <div class="ml-4 flex-1">
                                <h3 class="text-lg font-medium text-gray-900 dark:text-white">Unified Platform</h3>
                                <p class="text-sm text-gray-500 dark:text-gray-400">Main BizOSaaS Platform</p>
                                <a href="{UNIFIED_AUTH_BROWSER_URL}/dashboard/" class="mt-3 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700">
                                    Open Platform
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="mt-12">
                    <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-6">System Status</h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                        <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-4">
                            <div class="flex items-center justify-between">
                                <div class="text-sm font-medium text-gray-500 dark:text-gray-400">Database</div>
                                <div class="text-xs text-green-600 bg-green-100 px-2 py-1 rounded">Online</div>
                            </div>
                            <div class="mt-1 text-lg font-semibold text-gray-900 dark:text-white">PostgreSQL</div>
                        </div>
                        <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-4">
                            <div class="flex items-center justify-between">
                                <div class="text-sm font-medium text-gray-500 dark:text-gray-400">Cache</div>
                                <div class="text-xs text-green-600 bg-green-100 px-2 py-1 rounded">Online</div>
                            </div>
                            <div class="mt-1 text-lg font-semibold text-gray-900 dark:text-white">Redis</div>
                        </div>
                        <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-4">
                            <div class="flex items-center justify-between">
                                <div class="text-sm font-medium text-gray-500 dark:text-gray-400">AI Agents</div>
                                <div class="text-xs text-green-600 bg-green-100 px-2 py-1 rounded">Active</div>
                            </div>
                            <div class="mt-1 text-lg font-semibold text-gray-900 dark:text-white">28 Agents</div>
                        </div>
                        <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-4">
                            <div class="flex items-center justify-between">
                                <div class="text-sm font-medium text-gray-500 dark:text-gray-400">Sessions</div>
                                <div class="text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded">Active</div>
                            </div>
                            <div class="mt-1 text-lg font-semibold text-gray-900 dark:text-white">Active Users</div>
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
    logout_url = get_logout_url()
    return RedirectResponse(url=logout_url, status_code=302)

@app.get("/api/system/health")
async def system_health(user_session: UserSession = Depends(require_super_admin)):
    """System health check for super admins"""
    try:
        # Check database connection
        async with async_session() as session:
            result = await session.execute(text("SELECT 1"))
            db_status = "healthy" if result.scalar() == 1 else "unhealthy"
        
        # Check active database connections
        async with async_session() as session:
            result = await session.execute(text("""
                SELECT count(*) FROM pg_stat_activity 
                WHERE state = 'active' AND datname = current_database()
            """))
            active_connections = result.scalar() or 0
        
        return {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "database": {
                "status": db_status,
                "active_connections": active_connections,
                "url": DATABASE_URL.split("@")[1] if "@" in DATABASE_URL else "configured"
            },
            "redis": {"status": "external", "note": "Redis monitoring not implemented"},
            "vault": {"status": "external", "note": "Vault monitoring not implemented"},
            "ai_agents": {"status": "external", "note": "AI agent monitoring not implemented"},
            "services": {
                "sqladmin": "operational",
                "tailadmin": "external",
                "unified_auth": "external"
            },
            "user": {
                "id": user_session.user_id,
                "email": user_session.email,
                "role": user_session.role
            }
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

@app.get("/api/system/stats")
async def system_stats(user_session: UserSession = Depends(require_super_admin)):
    """Detailed system statistics"""
    try:
        async with async_session() as session:
            # Get tenant count
            tenant_result = await session.execute(text("SELECT COUNT(*) FROM tenants"))
            tenant_count = tenant_result.scalar() or 0
            
            # Get user count
            user_result = await session.execute(text("SELECT COUNT(*) FROM users"))
            user_count = user_result.scalar() or 0
            
            # Get active sessions
            session_result = await session.execute(text("""
                SELECT COUNT(*) FROM user_sessions 
                WHERE is_active = true AND expires_at > NOW()
            """))
            active_sessions = session_result.scalar() or 0
            
            # Get database size
            db_size_result = await session.execute(text("""
                SELECT pg_size_pretty(pg_database_size(current_database()))
            """))
            db_size = db_size_result.scalar() or "unknown"
            
            # Get AI agent stats
            agent_stats = await session.execute(text("""
                SELECT 
                    COUNT(*) as total_agents,
                    COUNT(*) FILTER (WHERE status = 'active') as active_agents,
                    AVG(response_time_ms) as avg_response_time,
                    AVG(success_rate) as avg_success_rate
                FROM ai_agent_monitoring
                WHERE updated_at > NOW() - INTERVAL '1 hour'
            """))
            agent_data = agent_stats.fetchone() or (0, 0, 0, 0)
            
            # Get recent alerts
            alert_stats = await session.execute(text("""
                SELECT 
                    severity,
                    COUNT(*) as count
                FROM system_alerts 
                WHERE is_active = true 
                GROUP BY severity
            """))
            alert_data = {row[0]: row[1] for row in alert_stats.fetchall()}
            
            return {
                "tenants": tenant_count,
                "users": user_count,
                "active_sessions": active_sessions,
                "database_size": db_size,
                "ai_agents": {
                    "total": agent_data[0] or 0,
                    "active": agent_data[1] or 0,
                    "avg_response_time": round(agent_data[2] or 0, 1),
                    "avg_success_rate": round(agent_data[3] or 0, 1)
                },
                "alerts": alert_data,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
    except Exception as e:
        logger.error(f"Stats collection failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to collect system statistics")

@app.get("/api/monitoring/dashboard")
async def monitoring_dashboard_data(user_session: UserSession = Depends(require_super_admin)):
    """Get real-time monitoring dashboard data"""
    try:
        async with async_session() as session:
            # Latest database metrics
            db_metrics = await session.execute(text("""
                SELECT 
                    active_connections,
                    cache_hit_ratio,
                    cpu_usage_percent,
                    memory_usage_percent,
                    slow_query_count
                FROM database_health_metrics 
                ORDER BY timestamp DESC 
                LIMIT 1
            """))
            db_data = db_metrics.fetchone()
            
            # Latest Redis metrics
            redis_metrics = await session.execute(text("""
                SELECT 
                    connected_clients,
                    hit_rate_percent,
                    used_memory_mb,
                    operations_per_second
                FROM redis_health_metrics 
                ORDER BY timestamp DESC 
                LIMIT 1
            """))
            redis_data = redis_metrics.fetchone()
            
            # Active alerts by severity
            alert_summary = await session.execute(text("""
                SELECT severity, COUNT(*) as count
                FROM system_alerts 
                WHERE is_active = true 
                GROUP BY severity
                ORDER BY 
                    CASE severity 
                        WHEN 'critical' THEN 1
                        WHEN 'error' THEN 2
                        WHEN 'warning' THEN 3
                        WHEN 'info' THEN 4
                    END
            """))
            alerts = {row[0]: row[1] for row in alert_summary.fetchall()}
            
            # Recent AI agent performance
            agent_performance = await session.execute(text("""
                SELECT 
                    agent_name,
                    status,
                    response_time_ms,
                    success_rate,
                    error_count
                FROM ai_agent_monitoring 
                WHERE updated_at > NOW() - INTERVAL '1 hour'
                ORDER BY response_time_ms DESC
                LIMIT 10
            """))
            agents = [{
                "name": row[0],
                "status": row[1],
                "response_time": row[2],
                "success_rate": row[3],
                "error_count": row[4]
            } for row in agent_performance.fetchall()]
            
            return {
                "database": {
                    "active_connections": db_data[0] if db_data else 0,
                    "cache_hit_ratio": db_data[1] if db_data else 0,
                    "cpu_usage": db_data[2] if db_data else 0,
                    "memory_usage": db_data[3] if db_data else 0,
                    "slow_queries": db_data[4] if db_data else 0
                },
                "redis": {
                    "connected_clients": redis_data[0] if redis_data else 0,
                    "hit_rate": redis_data[1] if redis_data else 0,
                    "memory_usage_mb": redis_data[2] if redis_data else 0,
                    "operations_per_second": redis_data[3] if redis_data else 0
                },
                "alerts": alerts,
                "ai_agents": agents,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
    except Exception as e:
        logger.error(f"Dashboard data collection failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to collect dashboard data")

@app.post("/api/monitoring/start")
async def start_monitoring(user_session: UserSession = Depends(require_super_admin)):
    """Start the monitoring service"""
    try:
        # Initialize monitoring service
        config = create_monitoring_config()
        monitoring_service = MonitoringService(config)
        
        # Start monitoring in background
        asyncio.create_task(monitoring_service.start())
        
        return {"status": "success", "message": "Monitoring service started"}
        
    except Exception as e:
        logger.error(f"Failed to start monitoring service: {e}")
        raise HTTPException(status_code=500, detail="Failed to start monitoring service")

@app.post("/api/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str, user_session: UserSession = Depends(require_super_admin)):
    """Acknowledge a system alert"""
    try:
        async with async_session() as session:
            await session.execute(text("""
                UPDATE system_alerts 
                SET acknowledged_at = NOW(),
                    acknowledged_by = :user_id
                WHERE id = :alert_id
            """), {"alert_id": alert_id, "user_id": user_session.user_id})
            await session.commit()
            
            # Log admin action
            await session.execute(text("""
                INSERT INTO admin_action_audit (
                    admin_user_id, action_type, resource_type, resource_id,
                    action_details, ip_address
                ) VALUES (
                    :admin_user_id, 'alert_acknowledgment', 'system_alert', :alert_id,
                    :action_details, :ip_address
                )
            """), {
                "admin_user_id": user_session.user_id,
                "alert_id": alert_id,
                "action_details": json.dumps({"action": "acknowledge_alert", "alert_id": alert_id}),
                "ip_address": "127.0.0.1"  # Would get from request in real implementation
            })
            await session.commit()
            
        return {"status": "success", "message": "Alert acknowledged"}
        
    except Exception as e:
        logger.error(f"Failed to acknowledge alert: {e}")
        raise HTTPException(status_code=500, detail="Failed to acknowledge alert")

@app.post("/api/alerts/{alert_id}/resolve")
async def resolve_alert(alert_id: str, resolution_notes: str = "", user_session: UserSession = Depends(require_super_admin)):
    """Resolve a system alert"""
    try:
        async with async_session() as session:
            await session.execute(text("""
                UPDATE system_alerts 
                SET resolved_at = NOW(),
                    resolved_by = :user_id,
                    resolution_notes = :notes,
                    is_active = false
                WHERE id = :alert_id
            """), {
                "alert_id": alert_id, 
                "user_id": user_session.user_id,
                "notes": resolution_notes
            })
            await session.commit()
            
            # Log admin action
            await session.execute(text("""
                INSERT INTO admin_action_audit (
                    admin_user_id, action_type, resource_type, resource_id,
                    action_details, ip_address
                ) VALUES (
                    :admin_user_id, 'alert_resolution', 'system_alert', :alert_id,
                    :action_details, :ip_address
                )
            """), {
                "admin_user_id": user_session.user_id,
                "alert_id": alert_id,
                "action_details": json.dumps({
                    "action": "resolve_alert", 
                    "alert_id": alert_id,
                    "resolution_notes": resolution_notes
                }),
                "ip_address": "127.0.0.1"
            })
            await session.commit()
            
        return {"status": "success", "message": "Alert resolved"}
        
    except Exception as e:
        logger.error(f"Failed to resolve alert: {e}")
        raise HTTPException(status_code=500, detail="Failed to resolve alert")

# Multi-platform integration functions

def get_platform_tabs(role: str, user_permissions: list = []) -> list:
    """Get multi-platform navigation tabs based on user role and permissions"""
    platforms = []
    
    # SQLAdmin is current platform for super admin only
    if role in ["super_admin"]:
        platforms.append({
            "id": "sqladmin",
            "name": "SQLAdmin",
            "url": "http://localhost:5000/",
            "description": "Infrastructure Management Dashboard",
            "icon": "database",
            "status": "active",
            "current": True,
            "features": ["Database Admin", "System Health", "Monitoring", "Logs"],
            "access_level": "super_admin",
            "category": "admin"
        })
        
        # Other admin dashboards
        platforms.append({
            "id": "tailadmin",
            "name": "TailAdmin v2",
            "url": TAILADMIN_URL,
            "description": "Business Operations Dashboard",
            "icon": "layout-dashboard",
            "status": "active",
            "current": False,
            "features": ["Analytics", "User Management", "AI Agents", "System Monitor"],
            "access_level": "admin",
            "category": "admin"
        })
        
        # Business platforms - super admin has access to all
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
        
        # AI tools
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
    
    return platforms

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
    
    # Admin platforms dropdown (excluding current)
    available_admin = [p for p in admin_platforms if not p["current"]]
    if available_admin:
        admin_options = []
        for platform in available_admin:
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
        
        tabs_html.append(f"""
            <div class="relative inline-block text-left">
                <button onclick="toggleAdminDropdown()" class="bg-indigo-600 text-white px-3 py-1 rounded text-sm hover:bg-indigo-700 flex items-center space-x-1">
                    <span>Admin Dashboards</span>
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                </button>
                <div id="admin-dropdown" class="hidden absolute right-0 mt-2 w-64 rounded-md shadow-lg bg-white dark:bg-gray-800 ring-1 ring-black ring-opacity-5 z-50">
                    <div class="py-1">
                        <div class="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider border-b border-gray-200 dark:border-gray-600">
                            Switch Admin Dashboard
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
            features_text = ", ".join(platform["features"][:2])
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
                    <span>Business Platforms</span>
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                </button>
                <div id="platforms-dropdown" class="hidden absolute right-0 mt-2 w-72 rounded-md shadow-lg bg-white dark:bg-gray-800 ring-1 ring-black ring-opacity-5 z-50">
                    <div class="py-1">
                        <div class="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider border-b border-gray-200 dark:border-gray-600">
                            Access Business Platforms
                        </div>
                        {''.join(business_options)}
                    </div>
                </div>
            </div>
        """)
    
    # AI Tools button
    if tool_platforms:
        ai_platform = tool_platforms[0]
        tabs_html.append(f"""
            <a href="{ai_platform['url']}" target="_blank" class="bg-emerald-600 text-white px-3 py-1 rounded text-sm hover:bg-emerald-700 flex items-center space-x-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                </svg>
                <span>AI Assistant</span>
            </a>
        """)
    
    # JavaScript for dropdown functionality
    if available_admin or business_platforms:
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

@app.get("/api/platforms")
async def get_available_platforms(
    user_session: UserSession = Depends(require_super_admin)
) -> Dict[str, Any]:
    """Get available platforms for the current user"""
    platforms = get_platform_tabs(user_session.role, user_session.permissions)
    
    return {
        "platforms": platforms,
        "categories": {
            "admin": [p for p in platforms if p["category"] == "admin"],
            "platform": [p for p in platforms if p["category"] == "platform"],
            "tools": [p for p in platforms if p["category"] == "tools"]
        },
        "user_context": {
            "role": user_session.role,
            "permissions": user_session.permissions,
            "tenant_id": user_session.tenant_id
        }
    }

@app.get("/api/platform/{platform_id}/health")
async def check_platform_health(platform_id: str):
    """Check the health status of a specific platform"""
    # This would implement actual health checks for each platform
    platform_health = {
        "bizoholic": "active",
        "coreldove": "active",
        "directory": "active",
        "ai-chat": "active",
        "tailadmin": "active",
        "sqladmin": "active"
    }
    
    return {
        "platform_id": platform_id,
        "status": platform_health.get(platform_id, "unknown"),
        "last_checked": datetime.utcnow().isoformat(),
        "accessible": True
    }

# Global monitoring service instance
monitoring_service = None

@app.on_event("startup")
async def startup_event():
    """Initialize monitoring service on startup"""
    global monitoring_service
    try:
        # Initialize and start monitoring service
        config = create_monitoring_config()
        monitoring_service = MonitoringService(config)
        
        # Start monitoring in background
        asyncio.create_task(monitoring_service.start())
        logger.info("Monitoring service started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start monitoring service: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global monitoring_service
    if monitoring_service:
        await monitoring_service.stop()
        logger.info("Monitoring service stopped")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")