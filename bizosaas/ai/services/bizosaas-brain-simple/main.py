#!/usr/bin/env python3

"""
BizOSaaS Brain Gateway - Simplified FastAPI Service
Centralized API gateway for BizOSaaS platform
"""

import os
import asyncio
import logging
import httpx
from datetime import datetime
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException, Depends, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import redis
import asyncpg
import uvicorn

# Import the integrated e-commerce module
from ecommerce_module import create_ecommerce_router, BizOSaaSEcommerce

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===========================================
# FASTAPI APPLICATION SETUP
# ===========================================

app = FastAPI(
    title="BizOSaaS Brain Gateway",
    description="Centralized AI-powered API gateway for BizOSaaS platform",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================================
# CONFIGURATION
# ===========================================

class Settings:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "postgresql://admin:securepassword@localhost:5432/bizosaas")
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.jwt_secret = os.getenv("JWT_SECRET", "dev-secret-key")
        self.environment = os.getenv("ENVIRONMENT", "development")
        
        # Service URLs
        self.django_crm_url = os.getenv("DJANGO_CRM_URL", "http://bizosaas-django-crm:8008")
        self.wagtail_url = os.getenv("WAGTAIL_URL", "http://localhost:8006")
        self.superset_url = os.getenv("SUPERSET_URL", "http://localhost:8088")
        self.vault_url = os.getenv("VAULT_URL", "http://localhost:8200")
        self.auth_service_url = os.getenv("AUTH_SERVICE_URL", "http://bizosaas-auth-v2:8007")
        
settings = Settings()

# ===========================================
# DATABASE AND REDIS CONNECTIONS
# ===========================================

redis_client = None
db_pool = None

async def init_redis():
    """Initialize Redis connection"""
    global redis_client
    try:
        redis_client = redis.from_url(settings.redis_url, decode_responses=True)
        redis_client.ping()
        logger.info("✅ Redis connection established")
    except Exception as e:
        logger.error(f"❌ Redis connection failed: {e}")
        redis_client = None

async def init_database():
    """Initialize PostgreSQL connection pool"""
    global db_pool
    try:
        db_pool = await asyncpg.create_pool(settings.database_url)
        logger.info("✅ PostgreSQL connection pool established")
    except Exception as e:
        logger.error(f"❌ PostgreSQL connection failed: {e}")
        db_pool = None

# ===========================================
# PYDANTIC MODELS
# ===========================================

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    environment: str
    services: Dict[str, str]

class PlatformStatsResponse(BaseModel):
    active_users: int
    total_tenants: int
    api_calls_today: int
    system_health: str

# ===========================================
# HEALTH CHECK ENDPOINTS
# ===========================================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring"""
    services_status = {}
    
    # Check Redis
    try:
        if redis_client:
            redis_client.ping()
            services_status["redis"] = "healthy"
        else:
            services_status["redis"] = "disconnected"
    except:
        services_status["redis"] = "unhealthy"
    
    # Check PostgreSQL
    try:
        if db_pool:
            async with db_pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            services_status["postgresql"] = "healthy"
        else:
            services_status["postgresql"] = "disconnected"
    except:
        services_status["postgresql"] = "unhealthy"
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        environment=settings.environment,
        services=services_status
    )

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "BizOSaaS Brain Gateway API",
        "version": "2.0.0",
        "environment": settings.environment,
        "docs": "/docs"
    }

# ===========================================
# PLATFORM ANALYTICS ENDPOINTS
# ===========================================

@app.get("/analytics/dashboard", response_model=PlatformStatsResponse)
async def get_dashboard_stats():
    """Get platform analytics for dashboard"""
    try:
        # Mock data for now - will be replaced with real queries
        return PlatformStatsResponse(
            active_users=156,
            total_tenants=23,
            api_calls_today=12847,
            system_health="excellent"
        )
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch dashboard statistics")

@app.get("/analytics/superset")
async def superset_proxy():
    """Proxy to Apache Superset analytics (placeholder)"""
    return {
        "message": "Apache Superset integration",
        "status": "available",
        "url": "/analytics/superset/dashboard"
    }

# ===========================================
# TENANT MANAGEMENT ENDPOINTS
# ===========================================

@app.get("/tenants")
async def get_tenants():
    """Get all tenants"""
    try:
        if not db_pool:
            raise HTTPException(status_code=503, detail="Database not available")
            
        async with db_pool.acquire() as conn:
            tenants = await conn.fetch("""
                SELECT tenant_id, name, subscription_tier, status, created_at
                FROM tenants 
                WHERE status = 'active'
                ORDER BY created_at DESC
                LIMIT 50
            """)
            
        return {"tenants": [dict(tenant) for tenant in tenants]}
    except Exception as e:
        logger.error(f"Error fetching tenants: {e}")
        return {"tenants": [], "error": str(e)}

# ===========================================
# PLATFORM INTEGRATION ENDPOINTS
# ===========================================

@app.get("/integrations/status")
async def get_integrations_status():
    """Get status of all platform integrations"""
    integrations = {
        "django_crm": {"status": "containerized", "url": settings.django_crm_url, "port": "8008"},
        "wagtail_cms": {"status": "containerized", "url": settings.wagtail_url, "port": "8006"},
        "auth_service": {"status": "containerized", "url": settings.auth_service_url, "port": "8007"},
        "superset": {"status": "containerized", "url": settings.superset_url, "port": "8088"},
        "vault": {"status": "containerized", "url": settings.vault_url, "port": "8200"},
        "saleor": {"status": "pending_containerization", "url": "http://localhost:8010", "port": "8010"},
        "temporal": {"status": "pending_containerization", "url": "http://localhost:8202", "port": "8202"}
    }
    
    return {"integrations": integrations}

# ===========================================
# DJANGO CRM API GATEWAY ROUTES
# ===========================================

def create_django_crm_router():
    """Create Django CRM proxy router"""
    router = APIRouter(prefix="/api/brain/django-crm", tags=["Django CRM"])
    
    @router.get("/leads")
    async def get_leads(request: Request):
        """Proxy to Django CRM leads endpoint"""
        try:
            query_params = str(request.url.query)
            url = f"{settings.django_crm_url}/api/leads/"
            if query_params:
                url += f"?{query_params}"
                
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=dict(request.headers))
                return response.json()
        except Exception as e:
            logger.error(f"Django CRM leads proxy error: {e}")
            raise HTTPException(status_code=503, detail="Django CRM service unavailable")
    
    @router.post("/leads")
    async def create_lead(request: Request):
        """Proxy to Django CRM create lead endpoint"""
        try:
            body = await request.json()
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.django_crm_url}/api/leads/",
                    json=body,
                    headers=dict(request.headers)
                )
                return response.json()
        except Exception as e:
            logger.error(f"Django CRM create lead proxy error: {e}")
            raise HTTPException(status_code=503, detail="Django CRM service unavailable")
    
    @router.get("/contacts")
    async def get_contacts(request: Request):
        """Proxy to Django CRM contacts endpoint"""
        try:
            query_params = str(request.url.query)
            url = f"{settings.django_crm_url}/api/contacts/"
            if query_params:
                url += f"?{query_params}"
                
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=dict(request.headers))
                return response.json()
        except Exception as e:
            logger.error(f"Django CRM contacts proxy error: {e}")
            raise HTTPException(status_code=503, detail="Django CRM service unavailable")
    
    @router.post("/contacts")
    async def create_contact(request: Request):
        """Proxy to Django CRM create contact endpoint"""
        try:
            body = await request.json()
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.django_crm_url}/api/contacts/",
                    json=body,
                    headers=dict(request.headers)
                )
                return response.json()
        except Exception as e:
            logger.error(f"Django CRM create contact proxy error: {e}")
            raise HTTPException(status_code=503, detail="Django CRM service unavailable")
    
    @router.get("/deals")
    async def get_deals(request: Request):
        """Proxy to Django CRM deals endpoint"""
        try:
            query_params = str(request.url.query)
            url = f"{settings.django_crm_url}/api/deals/"
            if query_params:
                url += f"?{query_params}"
                
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=dict(request.headers))
                return response.json()
        except Exception as e:
            logger.error(f"Django CRM deals proxy error: {e}")
            raise HTTPException(status_code=503, detail="Django CRM service unavailable")
    
    @router.post("/deals")
    async def create_deal(request: Request):
        """Proxy to Django CRM create deal endpoint"""
        try:
            body = await request.json()
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.django_crm_url}/api/deals/",
                    json=body,
                    headers=dict(request.headers)
                )
                return response.json()
        except Exception as e:
            logger.error(f"Django CRM create deal proxy error: {e}")
            raise HTTPException(status_code=503, detail="Django CRM service unavailable")
    
    @router.get("/activities")
    async def get_activities(request: Request):
        """Proxy to Django CRM activities endpoint"""
        try:
            query_params = str(request.url.query)
            url = f"{settings.django_crm_url}/api/activities/"
            if query_params:
                url += f"?{query_params}"
                
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=dict(request.headers))
                return response.json()
        except Exception as e:
            logger.error(f"Django CRM activities proxy error: {e}")
            raise HTTPException(status_code=503, detail="Django CRM service unavailable")
    
    @router.post("/activities")
    async def create_activity(request: Request):
        """Proxy to Django CRM create activity endpoint"""
        try:
            body = await request.json()
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.django_crm_url}/api/activities/",
                    json=body,
                    headers=dict(request.headers)
                )
                return response.json()
        except Exception as e:
            logger.error(f"Django CRM create activity proxy error: {e}")
            raise HTTPException(status_code=503, detail="Django CRM service unavailable")
    
    return router

# ===========================================
# SUPERSET ANALYTICS API GATEWAY ROUTES
# ===========================================

def create_superset_router():
    """Create Apache Superset proxy router"""
    router = APIRouter(prefix="/api/brain/superset", tags=["Apache Superset"])
    
    @router.get("/dashboards")
    async def get_dashboards(request: Request):
        """Proxy to Superset dashboards endpoint"""
        try:
            query_params = str(request.url.query)
            url = f"{settings.superset_url}/api/v1/dashboard/"
            if query_params:
                url += f"?{query_params}"
                
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=dict(request.headers))
                return response.json()
        except Exception as e:
            logger.error(f"Superset dashboards proxy error: {e}")
            raise HTTPException(status_code=503, detail="Superset service unavailable")
    
    @router.get("/reports")
    async def get_reports(request: Request):
        """Proxy to Superset reports endpoint"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.superset_url}/api/v1/report/",
                    headers=dict(request.headers)
                )
                return response.json()
        except Exception as e:
            logger.error(f"Superset reports proxy error: {e}")
            raise HTTPException(status_code=503, detail="Superset service unavailable")
    
    @router.get("/metrics")
    async def get_metrics(request: Request):
        """Proxy to Superset metrics endpoint"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.superset_url}/api/v1/chart/",
                    headers=dict(request.headers)
                )
                return response.json()
        except Exception as e:
            logger.error(f"Superset metrics proxy error: {e}")
            raise HTTPException(status_code=503, detail="Superset service unavailable")
    
    return router

# ===========================================
# WAGTAIL CMS API GATEWAY ROUTES
# ===========================================

def create_wagtail_router():
    """Create Wagtail CMS proxy router"""
    router = APIRouter(prefix="/api/brain/wagtail", tags=["Wagtail CMS"])
    
    @router.get("/pages")
    async def get_pages(request: Request):
        """Proxy to Wagtail pages endpoint"""
        try:
            query_params = str(request.url.query)
            url = f"{settings.wagtail_url}/api/v2/pages/"
            if query_params:
                url += f"?{query_params}"
                
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=dict(request.headers))
                return response.json()
        except Exception as e:
            logger.error(f"Wagtail pages proxy error: {e}")
            raise HTTPException(status_code=503, detail="Wagtail CMS service unavailable")
    
    @router.post("/pages")
    async def create_page(request: Request):
        """Proxy to Wagtail create page endpoint"""
        try:
            body = await request.json()
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.wagtail_url}/api/v2/pages/",
                    json=body,
                    headers=dict(request.headers)
                )
                return response.json()
        except Exception as e:
            logger.error(f"Wagtail create page proxy error: {e}")
            raise HTTPException(status_code=503, detail="Wagtail CMS service unavailable")
    
    @router.get("/media")
    async def get_media(request: Request):
        """Proxy to Wagtail media endpoint"""
        try:
            query_params = str(request.url.query)
            url = f"{settings.wagtail_url}/api/v2/images/"
            if query_params:
                url += f"?{query_params}"
                
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=dict(request.headers))
                return response.json()
        except Exception as e:
            logger.error(f"Wagtail media proxy error: {e}")
            raise HTTPException(status_code=503, detail="Wagtail CMS service unavailable")
    
    @router.get("/forms")
    async def get_forms(request: Request):
        """Proxy to Wagtail forms endpoint"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.wagtail_url}/admin/forms/",
                    headers=dict(request.headers)
                )
                return response.json()
        except Exception as e:
            logger.error(f"Wagtail forms proxy error: {e}")
            raise HTTPException(status_code=503, detail="Wagtail CMS service unavailable")
    
    @router.get("/collections")
    async def get_collections(request: Request):
        """Proxy to Wagtail collections endpoint"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.wagtail_url}/api/v2/documents/",
                    headers=dict(request.headers)
                )
                return response.json()
        except Exception as e:
            logger.error(f"Wagtail collections proxy error: {e}")
            raise HTTPException(status_code=503, detail="Wagtail CMS service unavailable")
    
    return router

# ===========================================
# VAULT SECRETS API GATEWAY ROUTES
# ===========================================

def create_vault_router():
    """Create HashiCorp Vault proxy router"""
    router = APIRouter(prefix="/api/brain/vault", tags=["HashiCorp Vault"])
    
    @router.get("/keys")
    async def get_keys(request: Request):
        """Proxy to Vault keys endpoint"""
        try:
            query_params = str(request.url.query)
            url = f"{settings.vault_url}/v1/secret/metadata/"
            if query_params:
                url += f"?{query_params}"
                
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=dict(request.headers))
                return response.json()
        except Exception as e:
            logger.error(f"Vault keys proxy error: {e}")
            raise HTTPException(status_code=503, detail="Vault service unavailable")
    
    @router.post("/keys")
    async def create_secret(request: Request):
        """Proxy to Vault create secret endpoint"""
        try:
            body = await request.json()
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.vault_url}/v1/secret/data/",
                    json=body,
                    headers=dict(request.headers)
                )
                return response.json()
        except Exception as e:
            logger.error(f"Vault create secret proxy error: {e}")
            raise HTTPException(status_code=503, detail="Vault service unavailable")
    
    @router.get("/secrets")
    async def get_secrets(request: Request):
        """Proxy to Vault secrets endpoint"""
        try:
            query_params = str(request.url.query)
            url = f"{settings.vault_url}/v1/secret/data/"
            if query_params:
                url += f"?{query_params}"
                
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=dict(request.headers))
                return response.json()
        except Exception as e:
            logger.error(f"Vault secrets proxy error: {e}")
            raise HTTPException(status_code=503, detail="Vault service unavailable")
    
    @router.get("/integrations")
    async def get_integrations(request: Request):
        """Proxy to Vault integrations endpoint"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.vault_url}/v1/auth/",
                    headers=dict(request.headers)
                )
                return response.json()
        except Exception as e:
            logger.error(f"Vault integrations proxy error: {e}")
            raise HTTPException(status_code=503, detail="Vault service unavailable")
    
    return router

# ===========================================
# BILLING & SUBSCRIPTION API GATEWAY ROUTES
# ===========================================

def create_billing_router():
    """Create Billing & Subscription Management proxy router"""
    router = APIRouter(prefix="/api/brain/billing", tags=["Billing & Subscriptions"])
    
    @router.get("/invoices")
    async def get_invoices(request: Request, limit: int = 10, offset: int = 0, status: str = None):
        """Get billing invoices with pagination and filtering"""
        try:
            # Mock billing service integration
            logger.info(f"Fetching invoices: limit={limit}, offset={offset}, status={status}")
            
            # Sample invoice data - replace with actual billing service integration
            invoices_data = {
                "invoices": [
                    {
                        "id": "INV-2025-001",
                        "date": "2025-01-01",
                        "amount": 2847.00,
                        "status": "paid",
                        "description": "Enterprise Plan - January 2025"
                    }
                ],
                "total": 1,
                "pagination": {"limit": limit, "offset": offset, "hasMore": False}
            }
            return invoices_data
        except Exception as e:
            logger.error(f"Billing invoices proxy error: {e}")
            raise HTTPException(status_code=503, detail="Billing service unavailable")

    @router.post("/invoices")
    async def create_invoice(request: Request):
        """Create a new invoice"""
        try:
            body = await request.json()
            logger.info(f"Creating invoice: {body}")
            
            # Mock invoice creation
            new_invoice = {
                "id": f"INV-{datetime.now().year}-{datetime.now().month:03d}",
                "status": "draft",
                "created": datetime.now().isoformat()
            }
            return {"success": True, "invoice": new_invoice}
        except Exception as e:
            logger.error(f"Billing create invoice proxy error: {e}")
            raise HTTPException(status_code=503, detail="Billing service unavailable")

    @router.get("/payments")
    async def get_payments(request: Request, type: str = "methods"):
        """Get payment methods or transaction history"""
        try:
            logger.info(f"Fetching payment data: type={type}")
            
            if type == "transactions":
                payment_data = {
                    "transactions": [
                        {
                            "id": "txn_2025001",
                            "amount": 2847.00,
                            "status": "succeeded",
                            "date": "2025-01-02T10:30:00Z"
                        }
                    ],
                    "total": 1
                }
            else:
                payment_data = {
                    "paymentMethods": [
                        {
                            "id": "pm_1234567890",
                            "type": "card",
                            "card": {"brand": "visa", "last4": "4242"},
                            "isDefault": True
                        }
                    ],
                    "total": 1
                }
            return payment_data
        except Exception as e:
            logger.error(f"Billing payments proxy error: {e}")
            raise HTTPException(status_code=503, detail="Billing service unavailable")

    @router.post("/payments")
    async def process_payment_action(request: Request):
        """Process payment actions (add/update/delete payment methods, process payments)"""
        try:
            body = await request.json()
            action = body.get("action")
            logger.info(f"Processing payment action: {action}")
            
            return {"success": True, "message": f"Payment action '{action}' processed successfully"}
        except Exception as e:
            logger.error(f"Billing payment action proxy error: {e}")
            raise HTTPException(status_code=503, detail="Billing service unavailable")

    @router.get("/subscriptions")
    async def get_subscriptions(request: Request, type: str = "subscriptions"):
        """Get subscription information or available plans"""
        try:
            logger.info(f"Fetching subscription data: type={type}")
            
            if type == "plans":
                subscription_data = {
                    "plans": [
                        {
                            "id": "plan_enterprise_monthly",
                            "name": "Enterprise Plan",
                            "amount": 2847.00,
                            "interval": "monthly",
                            "features": ["Unlimited Users", "5TB Storage", "24/7 Support"]
                        }
                    ],
                    "total": 1
                }
            else:
                subscription_data = {
                    "subscriptions": [
                        {
                            "id": "sub_enterprise_2024",
                            "planName": "Enterprise Plan",
                            "status": "active",
                            "amount": 34164.00,
                            "nextBillingDate": "2025-01-15T00:00:00Z"
                        }
                    ],
                    "total": 1,
                    "activeSubscription": {
                        "id": "sub_enterprise_2024",
                        "planName": "Enterprise Plan",
                        "status": "active"
                    }
                }
            return subscription_data
        except Exception as e:
            logger.error(f"Billing subscriptions proxy error: {e}")
            raise HTTPException(status_code=503, detail="Billing service unavailable")

    @router.post("/subscriptions")
    async def manage_subscription(request: Request):
        """Manage subscriptions (create, change plan, cancel, reactivate)"""
        try:
            body = await request.json()
            action = body.get("action")
            logger.info(f"Managing subscription: {action}")
            
            return {"success": True, "message": f"Subscription action '{action}' processed successfully"}
        except Exception as e:
            logger.error(f"Billing subscription management proxy error: {e}")
            raise HTTPException(status_code=503, detail="Billing service unavailable")

    @router.get("/usage")
    async def get_usage_analytics(request: Request, metric: str = "all", period: str = "current"):
        """Get usage analytics and billing insights"""
        try:
            logger.info(f"Fetching usage analytics: metric={metric}, period={period}")
            
            usage_data = {
                "currentPeriod": {
                    "start": "2025-01-15T00:00:00Z",
                    "end": "2025-02-15T00:00:00Z",
                    "usage": {
                        "users": {"current": 12, "limit": -1, "percentage": 0},
                        "storage": {"current": 245, "limit": 5120, "percentage": 4.8},
                        "apiCalls": {"current": 8432, "limit": 1000000, "percentage": 0.8}
                    }
                },
                "costBreakdown": {
                    "currentMonth": {
                        "basePlan": 2400.00,
                        "storage": 250.00,
                        "support": 197.00,
                        "total": 2847.00
                    }
                }
            }
            
            if metric != "all":
                # Return specific metric data
                metric_data = usage_data["currentPeriod"]["usage"].get(metric)
                return {"metric": metric, "period": period, "data": metric_data}
            
            return usage_data
        except Exception as e:
            logger.error(f"Billing usage analytics proxy error: {e}")
            raise HTTPException(status_code=503, detail="Billing service unavailable")

    @router.post("/usage")
    async def manage_usage(request: Request):
        """Manage usage settings (alerts, exports, cost calculations)"""
        try:
            body = await request.json()
            action = body.get("action")
            logger.info(f"Managing usage: {action}")
            
            return {"success": True, "message": f"Usage action '{action}' processed successfully"}
        except Exception as e:
            logger.error(f"Billing usage management proxy error: {e}")
            raise HTTPException(status_code=503, detail="Billing service unavailable")

    return router

# ===========================================
# WEBSOCKET ENDPOINTS (PLACEHOLDER)
# ===========================================

@app.get("/ws/realtime")
async def websocket_info():
    """WebSocket information endpoint"""
    return {
        "message": "WebSocket endpoint for real-time updates",
        "path": "/ws/realtime",
        "protocols": ["websocket"]
    }

# ===========================================
# STARTUP AND SHUTDOWN EVENTS
# ===========================================

@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup"""
    logger.info("🚀 Starting BizOSaaS Brain Gateway...")
    await init_redis()
    await init_database()
    
    # Initialize e-commerce module
    if db_pool and redis_client:
        ecommerce = BizOSaaSEcommerce(db_pool, redis_client)
        await ecommerce.initialize_tables()
        
        # Include e-commerce router
        ecommerce_router = create_ecommerce_router(db_pool, redis_client)
        app.include_router(ecommerce_router)
        
        logger.info("✅ E-commerce module initialized")
    
    # Include Django CRM router
    django_crm_router = create_django_crm_router()
    app.include_router(django_crm_router)
    logger.info("✅ Django CRM proxy router initialized")
    
    # Include Superset Analytics router
    superset_router = create_superset_router()
    app.include_router(superset_router)
    logger.info("✅ Apache Superset proxy router initialized")
    
    # Include Wagtail CMS router
    wagtail_router = create_wagtail_router()
    app.include_router(wagtail_router)
    logger.info("✅ Wagtail CMS proxy router initialized")
    
    # Include Vault secrets router
    vault_router = create_vault_router()
    app.include_router(vault_router)
    logger.info("✅ HashiCorp Vault proxy router initialized")
    
    # Include Billing & Subscription router
    billing_router = create_billing_router()
    app.include_router(billing_router)
    logger.info("✅ Billing & Subscription proxy router initialized")
    
    logger.info("✅ BizOSaaS Brain Gateway started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up connections on shutdown"""
    logger.info("🔄 Shutting down BizOSaaS Brain Gateway...")
    if redis_client:
        redis_client.close()
    if db_pool:
        await db_pool.close()
    logger.info("✅ BizOSaaS Brain Gateway shutdown complete")

# ===========================================
# ERROR HANDLERS
# ===========================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

# ===========================================
# MAIN ENTRY POINT
# ===========================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True if settings.environment == "development" else False,
        log_level="info"
    )