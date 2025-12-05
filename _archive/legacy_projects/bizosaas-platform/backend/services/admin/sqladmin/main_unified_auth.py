#!/usr/bin/env python3

"""
BizOSaaS SQLAdmin Dashboard with Unified Authentication
Integrates with the unified auth service for secure super_admin access
"""

import os
import json
import httpx
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from sqlalchemy import create_engine, MetaData, inspect, text, Column, String, DateTime, Boolean, Integer, Text, JSON, ForeignKey, UUID
from sqlalchemy.orm import sessionmaker, declarative_base
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:Bizoholic2024Alagiri@bizosaas-postgres-unified:5432/bizosaas')
SECRET_KEY = os.getenv('SECRET_KEY', 'sqladmin-secret-key-production')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')
AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://bizosaas-mock-auth-8008-cors:8007')

# FastAPI app
app = FastAPI(
    title="BizOSaaS SuperAdmin Dashboard - Unified Auth",
    description="Platform management with unified authentication",
    version="3.0.0-unified-auth"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy Base
Base = declarative_base()

class UnifiedAuthBackend(AuthenticationBackend):
    """Authentication backend that integrates with unified auth service"""

    async def login(self, request: Request) -> bool:
        """Handle login by redirecting to unified auth portal"""
        form = await request.form()
        email = form.get("username")  # SQLAdmin uses 'username' field
        password = form.get("password")

        if not email or not password:
            return False

        try:
            # Call unified auth service
            async with httpx.AsyncClient() as client:
                auth_response = await client.post(
                    f"{AUTH_SERVICE_URL}/auth/login",
                    json={"email": email, "password": password},
                    timeout=10.0
                )

                if auth_response.status_code == 200:
                    auth_data = auth_response.json()
                    user_role = auth_data.get("user", {}).get("role")

                    # Only allow super_admin role
                    if user_role == "super_admin":
                        # Store user info in session
                        request.session["user"] = auth_data["user"]
                        request.session["access_token"] = auth_data["access_token"]
                        return True
                    else:
                        logger.warning(f"Non-super_admin user attempted access: {email} (role: {user_role})")
                        return False
                else:
                    logger.warning(f"Auth failed for user: {email}")
                    return False

        except Exception as e:
            logger.error(f"Auth service error: {e}")
            return False

    async def logout(self, request: Request) -> bool:
        """Logout by clearing session"""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Check if user is authenticated and has super_admin role"""
        user = request.session.get("user")
        if user and user.get("role") == "super_admin":
            return True
        return False

# Initialize SQLAdmin with unified authentication
authentication_backend = UnifiedAuthBackend(secret_key=SECRET_KEY)
admin = Admin(app, engine, authentication_backend=authentication_backend)

# Define models with proper primary key configuration
class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(100))
    slug = Column(String(50))
    status = Column(String(20))
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    subscription_plan = Column(String(50))
    subscription_status = Column(String(20))

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String(255))
    first_name = Column(String(50))
    last_name = Column(String(50))
    role = Column(String(20))
    tenant_id = Column(UUID(as_uuid=True))
    is_active = Column(Boolean)
    is_superuser = Column(Boolean)
    is_verified = Column(Boolean)
    created_at = Column(DateTime(timezone=True))
    last_login_at = Column(DateTime(timezone=True))

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True))
    name = Column(String(200))
    type = Column(String(50))
    status = Column(String(20))
    budget = Column(JSON)
    targeting = Column(JSON)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))

class Lead(Base):
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True))
    email = Column(String(255))
    name = Column(String(200))
    company = Column(String(200))
    status = Column(String(20))
    source = Column(String(50))
    score = Column(Integer)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))

# Admin Views
class TenantAdmin(ModelView, model=Tenant):
    name = "Tenant"
    name_plural = "Tenants"
    icon = "fa-solid fa-building"
    column_list = [Tenant.id, Tenant.name, Tenant.slug, Tenant.status, Tenant.subscription_plan, Tenant.created_at]
    column_searchable_list = [Tenant.name, Tenant.slug]
    column_sortable_list = [Tenant.name, Tenant.created_at]

class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-users"
    column_list = [User.id, User.email, User.first_name, User.last_name, User.role, User.tenant_id, User.is_active, User.created_at]
    column_searchable_list = [User.email, User.first_name, User.last_name]
    column_sortable_list = [User.email, User.created_at]

class CampaignAdmin(ModelView, model=Campaign):
    name = "Campaign"
    name_plural = "Campaigns"
    icon = "fa-solid fa-bullhorn"
    column_list = [Campaign.id, Campaign.name, Campaign.type, Campaign.status, Campaign.tenant_id, Campaign.created_at]
    column_searchable_list = [Campaign.name]
    column_sortable_list = [Campaign.name, Campaign.created_at]

class LeadAdmin(ModelView, model=Lead):
    name = "Lead"
    name_plural = "Leads"
    icon = "fa-solid fa-user-plus"
    column_list = [Lead.id, Lead.name, Lead.email, Lead.company, Lead.status, Lead.score, Lead.tenant_id, Lead.created_at]
    column_searchable_list = [Lead.name, Lead.email, Lead.company]
    column_sortable_list = [Lead.name, Lead.created_at, Lead.score]

# Register admin views
admin.add_view(TenantAdmin)
admin.add_view(UserAdmin)
admin.add_view(CampaignAdmin)
admin.add_view(LeadAdmin)

# Health check endpoint
@app.get("/health")
async def health():
    """Health check endpoint"""
    try:
        # Test database connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "service": "sqladmin-unified-auth",
            "version": "3.0.0",
            "database": "connected",
            "auth_service": AUTH_SERVICE_URL,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

# Custom login redirect for non-authenticated users
@app.get("/")
async def root():
    """Root endpoint - redirect to admin or unified auth"""
    return RedirectResponse(url="/admin")

if __name__ == "__main__":
    uvicorn.run(
        "main_unified_auth:app",
        host="0.0.0.0",
        port=8005,
        reload=True
    )