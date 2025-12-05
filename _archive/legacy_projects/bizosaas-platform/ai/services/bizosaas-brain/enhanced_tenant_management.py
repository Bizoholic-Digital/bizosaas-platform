#!/usr/bin/env python3
"""
Enhanced Tenant Management for BizOSaaS Central Brain
Comprehensive tenant management based on Django CRM features
"""

from fastapi import FastAPI, HTTPException, Depends, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
from enum import Enum
from uuid import UUID, uuid4
from pydantic import BaseModel
import asyncio
import json
import httpx

# ========================================================================================
# ENHANCED TENANT MODELS - Based on Django CRM comprehensive features
# ========================================================================================

class SubscriptionTier(str, Enum):
    FREE = "free"
    STARTER = "starter" 
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"

class TenantStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    TRIAL = "trial"

class UserRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    READONLY = "readonly"

class Domain(BaseModel):
    domain_id: str = str(uuid4())
    domain: str
    is_primary: bool = False
    is_verified: bool = False
    ssl_enabled: bool = False
    created_at: datetime = datetime.utcnow()

class TenantMembership(BaseModel):
    membership_id: str = str(uuid4())
    user_email: str
    role: UserRole = UserRole.USER
    is_active: bool = True
    permissions: Dict[str, Any] = {}
    invited_at: datetime = datetime.utcnow()
    joined_at: Optional[datetime] = None

class APIKey(BaseModel):
    key_id: str = str(uuid4())
    name: str
    key_hash: str  # Hashed API key
    permissions: List[str] = []
    is_active: bool = True
    rate_limit: int = 1000  # requests per hour
    usage_count: int = 0
    last_used_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    created_at: datetime = datetime.utcnow()

class AuditLog(BaseModel):
    log_id: str = str(uuid4())
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    description: str
    metadata: Dict[str, Any] = {}
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    user_email: Optional[str] = None
    created_at: datetime = datetime.utcnow()

class EnhancedTenant(BaseModel):
    # Core Identity (Enhanced from Django CRM)
    tenant_id: str = str(uuid4())
    name: str
    slug: str  # URL-friendly identifier
    description: Optional[str] = None
    
    # Contact Information
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    
    # Address
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    
    # Subscription and Billing
    subscription_tier: SubscriptionTier = SubscriptionTier.FREE
    subscription_status: TenantStatus = TenantStatus.ACTIVE
    billing_email: Optional[str] = None
    
    # Settings
    timezone: str = "UTC"
    currency: str = "USD"
    language: str = "en"
    
    # Status
    is_active: bool = True
    is_verified: bool = False
    
    # Resource Limits (from Django CRM)
    max_users: int = 5
    max_leads: int = 1000
    max_customers: int = 500
    max_storage_mb: int = 100
    
    # Domain Management
    primary_domain: str
    domains: List[Domain] = []
    subdomain: Optional[str] = None
    
    # Service Configuration
    services_enabled: Dict[str, bool] = {
        "cms": True,
        "directory": False,
        "ecommerce": False,
        "crm": True,
        "ai_agents": False
    }
    
    # Integration Settings
    integrations_config: Dict[str, Any] = {}
    
    # Multi-Service Integration IDs
    django_crm_tenant_id: Optional[str] = None
    wagtail_tenant_id: Optional[str] = None
    
    # Branding & Theme (Enhanced)
    branding: Dict[str, Any] = {
        "primary_color": "#0ea5e9",
        "secondary_color": "#64748b",
        "logo_url": None,
        "company_name": None
    }
    theme_settings: Dict[str, Any] = {}
    seo_settings: Dict[str, Any] = {}
    
    # User Management
    memberships: List[TenantMembership] = []
    api_keys: List[APIKey] = []
    
    # Audit & Compliance
    audit_logs: List[AuditLog] = []
    
    # Timestamps
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    
    @property
    def current_users_count(self) -> int:
        """Get current active users count"""
        return len([m for m in self.memberships if m.is_active])
    
    @property
    def full_domain(self) -> str:
        """Get the full domain including subdomain if applicable"""
        if self.subdomain and self.subdomain != 'www':
            return f"{self.subdomain}.{self.primary_domain}"
        return self.primary_domain
    
    def has_service_enabled(self, service: str) -> bool:
        """Check if a service is enabled for this tenant"""
        return self.services_enabled.get(service, False)
    
    def add_audit_log(self, action: str, resource_type: str, description: str, 
                     user_email: Optional[str] = None, metadata: Dict[str, Any] = None):
        """Add audit log entry"""
        log = AuditLog(
            action=action,
            resource_type=resource_type,
            description=description,
            user_email=user_email,
            metadata=metadata or {}
        )
        self.audit_logs.append(log)
        self.updated_at = datetime.utcnow()
    
    def add_membership(self, user_email: str, role: UserRole = UserRole.USER) -> TenantMembership:
        """Add user membership"""
        membership = TenantMembership(
            user_email=user_email,
            role=role
        )
        self.memberships.append(membership)
        
        self.add_audit_log(
            action="membership_added",
            resource_type="membership", 
            description=f"User {user_email} added with role {role.value}",
            user_email=user_email
        )
        
        return membership
    
    def create_api_key(self, name: str, permissions: List[str] = None) -> APIKey:
        """Create new API key"""
        api_key = APIKey(
            name=name,
            key_hash=f"sk_live_{str(uuid4()).replace('-', '')}",  # Generate secure key
            permissions=permissions or []
        )
        self.api_keys.append(api_key)
        
        self.add_audit_log(
            action="api_key_created",
            resource_type="api_key",
            description=f"API key '{name}' created"
        )
        
        return api_key
    
    def get_resource_usage(self) -> Dict[str, Any]:
        """Get current resource usage"""
        return {
            "users": {
                "current": self.current_users_count,
                "limit": self.max_users,
                "percentage": (self.current_users_count / self.max_users) * 100 if self.max_users > 0 else 0
            },
            "api_keys": {
                "current": len([k for k in self.api_keys if k.is_active]),
                "limit": 10,  # Default limit
            },
            "storage": {
                "current_mb": 0,  # TODO: Calculate actual usage
                "limit_mb": self.max_storage_mb,
                "percentage": 0
            }
        }

# ========================================================================================
# TENANT REGISTRY SERVICE - Centralized tenant management
# ========================================================================================

class TenantRegistry:
    """Centralized tenant management service"""
    
    def __init__(self):
        # In-memory storage for development (replace with database)
        self._tenants: Dict[str, EnhancedTenant] = {}
        self._initialize_default_tenants()
    
    def _initialize_default_tenants(self):
        """Initialize default tenants for development"""
        # Bizoholic Tenant
        bizoholic_tenant = EnhancedTenant(
            tenant_id="bizoholic-main",
            name="Bizoholic Digital Marketing",
            slug="bizoholic",
            description="AI-powered marketing automation platform",
            email="admin@bizoholic.com",
            primary_domain="bizoholic.com",
            subdomain="www",
            subscription_tier=SubscriptionTier.ENTERPRISE,
            subscription_status=TenantStatus.ACTIVE,
            services_enabled={
                "cms": True,
                "directory": True,
                "ecommerce": False,
                "crm": True,
                "ai_agents": True
            },
            branding={
                "primary_color": "#0ea5e9",
                "secondary_color": "#64748b",
                "logo_url": "/assets/bizoholic-logo.png",
                "company_name": "Bizoholic Digital"
            },
            max_users=50,
            max_leads=10000,
            max_customers=5000,
            max_storage_mb=10000,
            django_crm_tenant_id="bizoholic-main",
            wagtail_tenant_id="bizoholic-main"
        )
        
        # Add default admin membership
        bizoholic_tenant.add_membership("admin@bizoholic.com", UserRole.OWNER)
        
        # CoreLDove Tenant
        coreldove_tenant = EnhancedTenant(
            tenant_id="coreldove-main",
            name="CoreLDove E-commerce",
            slug="coreldove",
            description="Premium e-commerce platform",
            email="admin@coreldove.com",
            primary_domain="coreldove.com",
            subscription_tier=SubscriptionTier.PROFESSIONAL,
            subscription_status=TenantStatus.ACTIVE,
            services_enabled={
                "cms": True,
                "directory": False,
                "ecommerce": True,
                "crm": True,
                "ai_agents": False
            },
            branding={
                "primary_color": "#10b981",
                "secondary_color": "#374151",
                "logo_url": "/assets/coreldove-logo.png",
                "company_name": "CoreLDove"
            },
            max_users=25,
            max_leads=5000,
            max_customers=2500,
            max_storage_mb=5000,
            django_crm_tenant_id="coreldove-main",
            wagtail_tenant_id="coreldove-main"
        )
        
        # Add default admin membership
        coreldove_tenant.add_membership("admin@coreldove.com", UserRole.OWNER)
        
        # Development Tenant
        dev_tenant = EnhancedTenant(
            tenant_id="bizoholic-dev",
            name="Bizoholic Digital (Development)",
            slug="bizoholic-dev",
            description="Development environment",
            email="dev@bizoholic.com",
            primary_domain="localhost",
            subscription_tier=SubscriptionTier.ENTERPRISE,
            subscription_status=TenantStatus.ACTIVE,
            services_enabled={
                "cms": True,
                "directory": True,
                "ecommerce": True,
                "crm": True,
                "ai_agents": True
            },
            branding={
                "primary_color": "#0ea5e9",
                "secondary_color": "#64748b",
                "logo_url": "/assets/bizoholic-logo.png",
                "company_name": "Bizoholic Digital (Dev)"
            },
            django_crm_tenant_id="bizoholic-dev",
            wagtail_tenant_id="bizoholic-dev"
        )
        
        # Add default dev user
        dev_tenant.add_membership("dev@bizoholic.com", UserRole.OWNER)
        
        self._tenants["bizoholic-main"] = bizoholic_tenant
        self._tenants["coreldove-main"] = coreldove_tenant
        self._tenants["bizoholic-dev"] = dev_tenant
    
    def get_tenant_by_id(self, tenant_id: str) -> Optional[EnhancedTenant]:
        """Get tenant by ID"""
        return self._tenants.get(tenant_id)
    
    def get_tenant_by_domain(self, domain: str) -> Optional[EnhancedTenant]:
        """Get tenant by domain"""
        for tenant in self._tenants.values():
            if tenant.primary_domain == domain:
                return tenant
            # Check additional domains
            for domain_obj in tenant.domains:
                if domain_obj.domain == domain and domain_obj.is_verified:
                    return tenant
        return None
    
    def get_tenant_by_subdomain(self, subdomain: str, parent_domain: str) -> Optional[EnhancedTenant]:
        """Get tenant by subdomain"""
        for tenant in self._tenants.values():
            if (tenant.subdomain == subdomain and 
                parent_domain in tenant.primary_domain):
                return tenant
        return None
    
    def create_tenant(self, tenant_data: Dict[str, Any]) -> EnhancedTenant:
        """Create new tenant"""
        tenant = EnhancedTenant(**tenant_data)
        self._tenants[tenant.tenant_id] = tenant
        
        # Add audit log
        tenant.add_audit_log(
            action="tenant_created",
            resource_type="tenant",
            description=f"Tenant {tenant.name} created"
        )
        
        return tenant
    
    def update_tenant(self, tenant_id: str, updates: Dict[str, Any]) -> Optional[EnhancedTenant]:
        """Update existing tenant"""
        tenant = self._tenants.get(tenant_id)
        if not tenant:
            return None
        
        # Update fields
        for key, value in updates.items():
            if hasattr(tenant, key):
                setattr(tenant, key, value)
        
        tenant.updated_at = datetime.utcnow()
        
        # Add audit log
        tenant.add_audit_log(
            action="tenant_updated",
            resource_type="tenant",
            description=f"Tenant {tenant.name} updated",
            metadata=updates
        )
        
        return tenant
    
    def list_tenants(self, active_only: bool = True) -> List[EnhancedTenant]:
        """List all tenants"""
        tenants = list(self._tenants.values())
        if active_only:
            tenants = [t for t in tenants if t.is_active]
        return tenants
    
    def get_tenant_statistics(self) -> Dict[str, Any]:
        """Get platform-wide tenant statistics"""
        all_tenants = list(self._tenants.values())
        active_tenants = [t for t in all_tenants if t.is_active]
        
        return {
            "total_tenants": len(all_tenants),
            "active_tenants": len(active_tenants),
            "subscription_breakdown": {
                tier.value: len([t for t in active_tenants if t.subscription_tier == tier])
                for tier in SubscriptionTier
            },
            "total_users": sum(t.current_users_count for t in active_tenants),
            "total_api_keys": sum(len(t.api_keys) for t in active_tenants)
        }

# Global tenant registry instance
tenant_registry = TenantRegistry()

# ========================================================================================
# TENANT RESOLUTION MIDDLEWARE - Enhanced domain-based routing logic
# ========================================================================================

async def resolve_tenant_from_domain(request: Request) -> Optional[EnhancedTenant]:
    """
    ENHANCED CORE BUSINESS LOGIC: Resolve tenant from domain/subdomain
    Uses centralized tenant registry with comprehensive tenant management
    """
    host = request.headers.get("host", "").lower()
    
    # Extract domain and subdomain
    if ":" in host:
        host = host.split(":")[0]  # Remove port
    
    parts = host.split(".")
    
    # Business Logic: Determine tenant based on domain structure
    if len(parts) >= 2:
        if len(parts) == 2:
            # Direct domain: bizoholic.com, coreldove.com
            domain = host
            subdomain = None
        else:
            # Subdomain: client1.bizoholic.com
            subdomain = parts[0]
            domain = ".".join(parts[1:])
    else:
        # localhost or single word domain
        domain = host
        subdomain = None
    
    # Try to resolve tenant from registry
    tenant = None
    
    # 1. Try direct domain match
    tenant = tenant_registry.get_tenant_by_domain(domain)
    if tenant:
        return tenant
    
    # 2. Try subdomain match
    if subdomain:
        tenant = tenant_registry.get_tenant_by_subdomain(subdomain, domain)
        if tenant:
            return tenant
    
    # 3. Development/localhost fallback
    if "localhost" in domain or domain.startswith("127.0.0.1") or domain.startswith("192.168"):
        return tenant_registry.get_tenant_by_id("bizoholic-dev")
    
    # 4. Pattern-based fallback for known domains
    if "bizoholic" in domain:
        return tenant_registry.get_tenant_by_id("bizoholic-main")
    elif "coreldove" in domain:
        return tenant_registry.get_tenant_by_id("coreldove-main")
    
    return None

def get_current_tenant(request: Request) -> Optional[EnhancedTenant]:
    """Dependency injection for current tenant"""
    return getattr(request.state, "current_tenant", None)

# ========================================================================================
# TENANT MANAGEMENT API ENDPOINTS
# ========================================================================================

tenant_management_app = FastAPI(
    title="Tenant Management API",
    description="Comprehensive tenant management system",
    version="1.0.0"
)

@tenant_management_app.get("/tenants", response_model=List[EnhancedTenant])
async def list_tenants(active_only: bool = True):
    """List all tenants"""
    return tenant_registry.list_tenants(active_only=active_only)

@tenant_management_app.get("/tenants/{tenant_id}", response_model=EnhancedTenant)
async def get_tenant(tenant_id: str):
    """Get tenant by ID"""
    tenant = tenant_registry.get_tenant_by_id(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

@tenant_management_app.post("/tenants", response_model=EnhancedTenant)
async def create_tenant(tenant_data: Dict[str, Any]):
    """Create new tenant"""
    try:
        return tenant_registry.create_tenant(tenant_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@tenant_management_app.put("/tenants/{tenant_id}", response_model=EnhancedTenant)
async def update_tenant(tenant_id: str, updates: Dict[str, Any]):
    """Update existing tenant"""
    tenant = tenant_registry.update_tenant(tenant_id, updates)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

@tenant_management_app.get("/tenants/{tenant_id}/usage")
async def get_tenant_usage(tenant_id: str):
    """Get tenant resource usage"""
    tenant = tenant_registry.get_tenant_by_id(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant.get_resource_usage()

@tenant_management_app.get("/platform/statistics")
async def get_platform_statistics():
    """Get platform-wide statistics"""
    return tenant_registry.get_tenant_statistics()

@tenant_management_app.post("/tenants/{tenant_id}/memberships")
async def add_tenant_membership(tenant_id: str, user_email: str, role: UserRole = UserRole.USER):
    """Add user membership to tenant"""
    tenant = tenant_registry.get_tenant_by_id(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    membership = tenant.add_membership(user_email, role)
    return membership

@tenant_management_app.post("/tenants/{tenant_id}/api-keys")
async def create_tenant_api_key(tenant_id: str, name: str, permissions: List[str] = None):
    """Create API key for tenant"""
    tenant = tenant_registry.get_tenant_by_id(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    api_key = tenant.create_api_key(name, permissions)
    return api_key

@tenant_management_app.get("/tenants/{tenant_id}/audit-logs")
async def get_tenant_audit_logs(tenant_id: str, limit: int = 100):
    """Get tenant audit logs"""
    tenant = tenant_registry.get_tenant_by_id(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Return most recent logs
    return tenant.audit_logs[-limit:] if len(tenant.audit_logs) > limit else tenant.audit_logs