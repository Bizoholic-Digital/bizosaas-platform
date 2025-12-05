#!/usr/bin/env python3

"""
BizOSaaS SQLAdmin Dashboard with Token-based Authentication
Simple authentication using mock tokens from unified auth service
"""

import os
import json
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

# FastAPI app
app = FastAPI(
    title="BizOSaaS SuperAdmin Dashboard - Token Auth",
    description="Platform management with token-based authentication",
    version="3.0.0-token-auth"
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

# Test users and their tokens (matching our mock auth service)
VALID_TOKENS = {
    "superadmin@bizosaas.com": {
        "token": "mock_access_token_550e8400-e29b-41d4-a716-446655440000",
        "role": "super_admin",
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Super Admin"
    }
}

class TokenAuthBackend(AuthenticationBackend):
    """Simple token-based authentication backend"""

    async def login(self, request: Request) -> bool:
        """Handle login using email/password and validate against known users"""
        form = await request.form()
        email = form.get("username")  # SQLAdmin uses 'username' field
        password = form.get("password")

        if not email or not password:
            return False

        # Check if this is the super admin with correct credentials
        if (email == "superadmin@bizosaas.com" and
            password == "BizoSaaS2025!Admin"):

            # Store user info in session
            user_info = VALID_TOKENS[email]
            request.session["user"] = {
                "email": email,
                "role": user_info["role"],
                "user_id": user_info["user_id"],
                "name": user_info["name"]
            }
            request.session["access_token"] = user_info["token"]
            logger.info(f"Super admin logged in: {email}")
            return True
        else:
            logger.warning(f"Invalid login attempt: {email}")
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

# Initialize SQLAdmin with token authentication
authentication_backend = TokenAuthBackend(secret_key=SECRET_KEY)
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
            "service": "sqladmin-token-auth",
            "version": "3.0.0",
            "database": "connected",
            "auth_method": "token-based",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

# Custom login redirect for non-authenticated users
@app.get("/")
async def root():
    """Root endpoint - redirect to admin"""
    return RedirectResponse(url="/admin")

if __name__ == "__main__":
    uvicorn.run(
        "main_token_auth:app",
        host="0.0.0.0",
        port=8005,
        reload=True
    )