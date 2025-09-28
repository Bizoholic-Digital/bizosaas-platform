"""
API Gateway Service - BizoholicSaaS Enhanced Multi-Tenant Edition
Central routing, authentication, and load balancing for all microservices with three-tier client model
Port: 8080
"""

from fastapi import FastAPI, HTTPException, Depends, status, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
from typing import Dict, Any, Optional, List
import logging
import time
from datetime import datetime
import asyncio
import json
import uuid
from urllib.parse import urlparse

# Shared imports
import sys
import os
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas')

from shared.auth.jwt_auth import get_current_user, UserContext, ServiceAuthToken
from shared.database.connection import get_redis_client, init_database
from tenant_context_service import tenant_context_service, TenantContext

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API Gateway - BizoholicSaaS Multi-Tenant",
    description="Enhanced Central API Gateway with multi-tenant routing and three-tier client model",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
redis_client = None
http_client = None

# Enhanced service configuration with multi-tenant support
SERVICES_CONFIG = {
    "user-management": {
        "base_url": "http://localhost:8005",
        "health_endpoint": "/health",
        "routes": ["/auth", "/users", "/tenants", "/sessions"],
        "public_routes": ["/auth/login", "/auth/register"],
        "timeout": 30,
        "multi_tenant": True
    },
    "campaign-management": {
        "base_url": "http://localhost:8002", 
        "health_endpoint": "/health",
        "routes": ["/campaigns", "/executions", "/ai-tasks", "/funnels"],
        "public_routes": [],
        "timeout": 60,
        "multi_tenant": True
    },
    "analytics": {
        "base_url": "http://localhost:8004",
        "health_endpoint": "/health", 
        "routes": ["/metrics", "/reports", "/dashboards", "/kpis"],
        "public_routes": [],
        "timeout": 45,
        "multi_tenant": True
    },
    "integration": {
        "base_url": "http://localhost:8008",
        "health_endpoint": "/health",
        "routes": ["/integrations", "/webhooks", "/sync"],
        "public_routes": ["/webhooks"],  # Webhooks need to be public
        "timeout": 30,
        "multi_tenant": True
    },
    "notification": {
        "base_url": "http://localhost:8009",
        "health_endpoint": "/health",
        "routes": ["/send", "/templates", "/preferences"],
        "public_routes": [],
        "timeout": 30,
        "multi_tenant": True
    },
    "ai-agents": {
        "base_url": "http://localhost:8001",
        "health_endpoint": "/health",
        "routes": ["/agents", "/tasks", "/workflows", "/api/agents"],
        "public_routes": [],
        "timeout": 120,  # AI tasks can take longer
        "multi_tenant": False
    },
    "wagtail-cms": {
        "base_url": "http://localhost:8006",
        "health_endpoint": "/",
        "routes": ["/api/v2/pages", "/api/v2/documents", "/api/v2/images", "/admin", "/cms"],
        "public_routes": ["/api/v2/pages"],  # Public content API
        "timeout": 30,
        "multi_tenant": True
    },
    "saleor-commerce": {
        "base_url": "http://localhost:8000",
        "health_endpoint": "/health/",
        "routes": ["/graphql/", "/media/", "/dashboard/"],
        "public_routes": ["/graphql/"],  # Public GraphQL API
        "timeout": 45,
        "multi_tenant": True
    },
    "business-directory": {
        "base_url": "http://localhost:8003",
        "health_endpoint": "/health",
        "routes": ["/directory", "/search", "/listings", "/api/directory"],
        "public_routes": ["/directory", "/search", "/listings"],
        "timeout": 30,
        "multi_tenant": True
    },
    "django-crm": {
        "base_url": "http://localhost:8007",
        "health_endpoint": "/health/",
        "routes": ["/api/leads", "/api/customers", "/api/orders", "/api/contacts", "/admin", "/crm"],
        "public_routes": [],
        "timeout": 30,
        "multi_tenant": True
    },
    "vault-service": {
        "base_url": "http://localhost:8201",
        "health_endpoint": "/",
        "routes": ["/api/credentials", "/api/vault", "/v1/secret", "/vault"],
        "public_routes": [],
        "timeout": 30,
        "multi_tenant": True
    },
    "temporal-integration": {
        "base_url": "http://localhost:8202",
        "health_endpoint": "/health",
        "routes": ["/api/workflows", "/api/temporal", "/workflows", "/temporal"],
        "public_routes": [],
        "timeout": 60,  # Workflow operations can take longer
        "multi_tenant": True
    }
}

# Enhanced rate limiting configuration
RATE_LIMITS = {
    "default": {"requests": 100, "window": 60},  # 100 requests per minute
    "auth": {"requests": 10, "window": 60},      # 10 auth requests per minute  
    "ai-agents": {"requests": 20, "window": 60}, # 20 AI requests per minute
    "webhooks": {"requests": 1000, "window": 60}, # Higher limit for webhooks
    "wagtail-cms": {"requests": 200, "window": 60}, # CMS requests
    "saleor-commerce": {"requests": 500, "window": 60}, # E-commerce requests
    "django-crm": {"requests": 300, "window": 60}, # CRM requests
    "vault-service": {"requests": 50, "window": 60}, # Vault security requests
    "temporal-integration": {"requests": 100, "window": 60} # Workflow requests
}

# Client tier configuration for three-tier model ($97/$297/$997)
CLIENT_TIERS = {
    "tier_1": {  # $97/month - Basic Marketing Starter
        "name": "Marketing Starter",
        "price": 97,
        "allowed_services": ["wagtail-cms", "business-directory", "django-crm"],
        "allowed_routes": [
            "/api/v2/pages", "/cms/pages", "/cms/*",
            "/directory/listings", "/directory/search",
            "/api/leads", "/api/customers", "/crm/*"
        ],
        "rate_limit": {"requests": 1000, "window": 3600},  # 1000/hour
        "features": ["static_sites", "basic_cms", "directory_listing", "basic_crm"],
        "description": "Essential marketing tools: website, business directory, and lead management"
    },
    "tier_2": {  # $297/month - Dynamic CMS + AI access
        "name": "Dynamic CMS Tier", 
        "price": 297,
        "allowed_services": ["wagtail-cms", "ai-agents", "business-directory", "django-crm"],
        "allowed_routes": [
            "/api/v2/pages", "/api/v2/documents", "/api/v2/images", 
            "/cms/*", "/agents/*", "/directory/*",
            "/api/leads", "/api/customers", "/crm/*"
        ],
        "rate_limit": {"requests": 5000, "window": 3600},  # 5000/hour
        "features": ["dynamic_cms", "ai_content", "seo_tools", "directory_listing", "basic_crm"],
        "description": "Dynamic websites with AI-powered content, SEO tools, and basic CRM"
    },
    "tier_3": {  # $997/month - Full platform access
        "name": "Full Platform Tier",
        "price": 997,
        "allowed_services": [
            "wagtail-cms", "saleor-commerce", "ai-agents", "business-directory", 
            "analytics", "integration", "campaign-management", "notification",
            "django-crm", "vault-service", "temporal-integration", "user-management"
        ],
        "allowed_routes": ["*"],  # Full access
        "rate_limit": {"requests": 20000, "window": 3600},  # 20000/hour
        "features": [
            "full_cms", "ecommerce", "ai_agents", "analytics", "integrations", 
            "custom_domains", "campaign_management", "advanced_notifications",
            "full_crm", "secure_vault", "workflow_automation", "user_management"
        ],
        "description": "Complete marketing automation platform with e-commerce, CRM, workflows, and secure credential management"
    }
}

# Default tier for new users
DEFAULT_TIER = "tier_1"

# Default tenant UUID (consistent across restarts)
DEFAULT_TENANT_UUID = "00000000-0000-4000-8000-000000000001"  # Special UUID for default tenant

# Circuit breaker configuration
CIRCUIT_BREAKER_CONFIG = {
    "failure_threshold": 5,  # Number of failures before opening circuit
    "recovery_timeout": 30,  # Seconds before trying to close circuit
    "success_threshold": 3   # Successful requests needed to close circuit
}

class CircuitBreakerState:
    """Circuit breaker state management"""
    
    def __init__(self):
        self.states = {}  # service_name -> {state, failures, last_failure, successes}
    
    def get_state(self, service_name: str) -> str:
        """Get current circuit breaker state for service"""
        if service_name not in self.states:
            self.states[service_name] = {
                "state": "closed",
                "failures": 0,
                "last_failure": None,
                "successes": 0
            }
        
        state_info = self.states[service_name]
        
        # Check if we should move from open to half-open
        if (state_info["state"] == "open" and 
            state_info["last_failure"] and
            time.time() - state_info["last_failure"] > CIRCUIT_BREAKER_CONFIG["recovery_timeout"]):
            state_info["state"] = "half-open"
            state_info["successes"] = 0
        
        return state_info["state"]
    
    def record_success(self, service_name: str):
        """Record successful request"""
        if service_name not in self.states:
            return
        
        state_info = self.states[service_name]
        state_info["failures"] = 0
        
        if state_info["state"] == "half-open":
            state_info["successes"] += 1
            if state_info["successes"] >= CIRCUIT_BREAKER_CONFIG["success_threshold"]:
                state_info["state"] = "closed"
                state_info["successes"] = 0
    
    def record_failure(self, service_name: str):
        """Record failed request"""
        if service_name not in self.states:
            self.states[service_name] = {
                "state": "closed",
                "failures": 0,
                "last_failure": None,
                "successes": 0
            }
        
        state_info = self.states[service_name]
        state_info["failures"] += 1
        state_info["last_failure"] = time.time()
        
        if state_info["failures"] >= CIRCUIT_BREAKER_CONFIG["failure_threshold"]:
            state_info["state"] = "open"

circuit_breaker = CircuitBreakerState()

# Tenant context extraction functions
def extract_tenant_id(request: Request) -> Optional[str]:
    """Extract tenant ID from request headers, subdomain, or JWT token"""
    
    # Method 1: Check X-Tenant-ID header
    tenant_id = request.headers.get("x-tenant-id")
    if tenant_id:
        return tenant_id
    
    # Method 2: Extract from subdomain
    host = request.headers.get("host", "")
    if "." in host:
        subdomain = host.split(".")[0]
        # Skip common subdomains
        if subdomain not in ["www", "api", "admin", "localhost"]:
            return subdomain
    
    # Method 3: Extract from JWT token if available
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        try:
            token = auth_header.replace("Bearer ", "")
            from shared.auth.jwt_auth import jwt_manager
            token_data = jwt_manager.verify_token(token)
            return token_data.tenant_id
        except Exception:
            pass
    
    # Method 4: Check tenant parameter in query string
    tenant_id = request.query_params.get("tenant_id")
    if tenant_id:
        return tenant_id
        
    return None

def get_user_tier_from_request(request: Request) -> str:
    """Get user tier from JWT token or default to tier_1"""
    
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        try:
            token = auth_header.replace("Bearer ", "")
            from shared.auth.jwt_auth import jwt_manager
            token_data = jwt_manager.verify_token(token)
            
            # Check if user context has tier information (could be stored in permissions or custom claims)
            # For now, determine tier based on role
            if token_data.role.value in ["super_admin", "tenant_admin"]:
                return "tier_3"
            elif token_data.role.value == "manager":
                return "tier_2" 
            else:
                return "tier_1"
        except Exception:
            pass
    
    return DEFAULT_TIER

async def get_user_tier(user_context: Optional[UserContext]) -> str:
    """Get user tier based on user context or subscription info"""
    
    if not user_context:
        return DEFAULT_TIER
    
    # TODO: Query database for user's subscription tier
    # For now, determine based on role
    if user_context.role.value in ["super_admin", "tenant_admin"]:
        return "tier_3"
    elif user_context.role.value == "manager":
        return "tier_2"
    else:
        return "tier_1"

def is_tier_allowed(user_tier: str, service_name: str, path: str) -> bool:
    """Check if user's tier allows access to service and path"""
    
    tier_config = CLIENT_TIERS.get(user_tier, CLIENT_TIERS[DEFAULT_TIER])
    
    # Debug logging
    logger.debug(f"Tier check: user_tier={user_tier}, service={service_name}, path={path}")
    logger.debug(f"Allowed services: {tier_config['allowed_services']}")
    logger.debug(f"Allowed routes: {tier_config['allowed_routes']}")
    
    # Check if service is allowed
    if service_name not in tier_config["allowed_services"]:
        logger.debug(f"Service {service_name} not in allowed services")
        return False
    
    # Check if route is allowed
    allowed_routes = tier_config["allowed_routes"]
    
    # If "*" is in allowed routes, allow everything
    if "*" in allowed_routes:
        logger.debug("Full access granted via * route")
        return True
    
    # Check if path matches any allowed route
    for allowed_route in allowed_routes:
        logger.debug(f"Checking route: {allowed_route} against path: {path}")
        if allowed_route.endswith("*"):
            # Wildcard match
            prefix = allowed_route[:-1]
            logger.debug(f"Wildcard match: checking if '{path}' starts with '{prefix}'")
            if path.startswith(prefix):
                logger.debug(f"Wildcard match SUCCESS: {path} matches {allowed_route}")
                return True
        else:
            # Exact match
            logger.debug(f"Exact match: checking if '{path}' starts with '{allowed_route}'")
            if path.startswith(allowed_route):
                logger.debug(f"Exact match SUCCESS: {path} matches {allowed_route}")
                return True
    
    logger.debug(f"No route match found for path: {path}")
    return False

# Tenant isolation middleware
@app.middleware("http")
async def tenant_isolation_middleware(request: Request, call_next):
    """Extract tenant context and add to request state"""
    
    # Extract tenant ID from request
    tenant_id = extract_tenant_id(request)
    request.state.tenant_id = tenant_id or DEFAULT_TENANT_UUID
    
    # Extract user tier from request
    user_tier = get_user_tier_from_request(request)
    request.state.user_tier = user_tier
    
    # Add request ID for tracing
    request.state.request_id = str(uuid.uuid4())
    
    logger.info(f"Request: {request.method} {request.url.path} | Tenant: {request.state.tenant_id} | Tier: {request.state.user_tier} | ID: {request.state.request_id}")
    
    response = await call_next(request)
    
    # Add tenant context headers to response
    response.headers["x-tenant-id"] = request.state.tenant_id
    response.headers["x-user-tier"] = request.state.user_tier
    response.headers["x-request-id"] = request.state.request_id
    
    return response

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize connections and services"""
    global redis_client, http_client
    
    try:
        # Initialize HTTP client for service requests (always needed)
        http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(60.0),
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
        )
        
        # Try to initialize database connections (optional for basic functionality)
        try:
            await init_database()
            redis_client = await get_redis_client()
            logger.info("Database connections initialized successfully")
        except Exception as db_error:
            logger.warning(f"Database initialization failed, continuing without it: {db_error}")
            redis_client = None
        
        # Initialize tenant context service
        try:
            await tenant_context_service.initialize()
            logger.info("Tenant context service initialized successfully")
        except Exception as tenant_error:
            logger.warning(f"Tenant context service initialization failed: {tenant_error}")
        
        logger.info("Multi-tenant API Gateway initialized successfully")
        
        # Start health check background task
        asyncio.create_task(health_check_services())
        
    except Exception as e:
        logger.error(f"API Gateway startup failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Clean shutdown"""
    global http_client
    
    if http_client:
        await http_client.aclose()
    
    logger.info("API Gateway shutdown complete")

# Health check endpoints
@app.get("/health")
async def health_check():
    """API Gateway health check"""
    return {
        "status": "healthy",
        "service": "api-gateway-multitenant",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health/services")
async def services_health_check():
    """Check health of all downstream services"""
    
    health_status = {}
    
    for service_name, config in SERVICES_CONFIG.items():
        try:
            circuit_state = circuit_breaker.get_state(service_name)
            
            if circuit_state == "open":
                health_status[service_name] = {
                    "status": "circuit_open",
                    "available": False,
                    "circuit_state": circuit_state
                }
                continue
            
            # Check service health
            health_url = f"{config['base_url']}{config['health_endpoint']}"
            
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(health_url)
                
                if response.status_code == 200:
                    health_status[service_name] = {
                        "status": "healthy",
                        "available": True,
                        "circuit_state": circuit_state,
                        "response_time": response.elapsed.total_seconds(),
                        "multi_tenant": config.get("multi_tenant", False)
                    }
                    circuit_breaker.record_success(service_name)
                else:
                    health_status[service_name] = {
                        "status": "unhealthy",
                        "available": False,
                        "circuit_state": circuit_state,
                        "status_code": response.status_code
                    }
                    circuit_breaker.record_failure(service_name)
                    
        except Exception as e:
            health_status[service_name] = {
                "status": "error",
                "available": False,
                "circuit_state": circuit_breaker.get_state(service_name),
                "error": str(e)
            }
            circuit_breaker.record_failure(service_name)
    
    # Overall health
    all_healthy = all(service["available"] for service in health_status.values())
    
    return {
        "overall_status": "healthy" if all_healthy else "degraded",
        "services": health_status,
        "timestamp": datetime.utcnow().isoformat()
    }

# Multi-tenant health check
@app.get("/health/tenant/{tenant_id}")
async def tenant_health_check(tenant_id: str, request: Request):
    """Check health of services for a specific tenant"""
    
    # Set tenant context for this check
    request.state.tenant_id = tenant_id
    
    health_status = {}
    user_tier = getattr(request.state, 'user_tier', DEFAULT_TIER)
    tier_config = CLIENT_TIERS.get(user_tier, CLIENT_TIERS[DEFAULT_TIER])
    
    # Only check services available to this tier
    for service_name in tier_config["allowed_services"]:
        if service_name in SERVICES_CONFIG:
            config = SERVICES_CONFIG[service_name]
            try:
                circuit_state = circuit_breaker.get_state(service_name)
                
                if circuit_state == "open":
                    health_status[service_name] = {
                        "status": "circuit_open",
                        "available": False,
                        "circuit_state": circuit_state
                    }
                    continue
                
                # Check service health
                health_url = f"{config['base_url']}{config['health_endpoint']}"
                
                async with httpx.AsyncClient(timeout=5.0) as client:
                    headers = {
                        "X-Tenant-ID": tenant_id,
                        "X-User-Tier": user_tier
                    }
                    response = await client.get(health_url, headers=headers)
                    
                    if response.status_code == 200:
                        health_status[service_name] = {
                            "status": "healthy",
                            "available": True,
                            "circuit_state": circuit_state,
                            "response_time": response.elapsed.total_seconds()
                        }
                        circuit_breaker.record_success(service_name)
                    else:
                        health_status[service_name] = {
                            "status": "unhealthy",
                            "available": False,
                            "circuit_state": circuit_state,
                            "status_code": response.status_code
                        }
                        circuit_breaker.record_failure(service_name)
                        
            except Exception as e:
                health_status[service_name] = {
                    "status": "error",
                    "available": False,
                    "circuit_state": circuit_breaker.get_state(service_name),
                    "error": str(e)
                }
                circuit_breaker.record_failure(service_name)
    
    # Overall health
    all_healthy = all(service["available"] for service in health_status.values())
    
    return {
        "tenant_id": tenant_id,
        "user_tier": user_tier,
        "overall_status": "healthy" if all_healthy else "degraded",
        "services": health_status,
        "timestamp": datetime.utcnow().isoformat()
    }

# Rate limiting middleware
async def check_rate_limit(request: Request, service_name: str = "default") -> bool:
    """Check if request is within rate limits"""
    
    # If Redis is not available, allow all requests
    if not redis_client:
        return True
    
    try:
        # Get client identifier (IP or user ID)
        client_ip = request.client.host
        user_agent = request.headers.get("user-agent", "unknown")
        client_id = f"{client_ip}:{hash(user_agent) % 1000}"
        
        # Determine rate limit based on service and endpoint
        rate_limit_key = service_name
        if "auth" in str(request.url.path):
            rate_limit_key = "auth"
        elif "webhooks" in str(request.url.path):
            rate_limit_key = "webhooks"
        
        limits = RATE_LIMITS.get(rate_limit_key, RATE_LIMITS["default"])
        
        # Check rate limit in Redis
        redis_key = f"rate_limit:{rate_limit_key}:{client_id}"
        
        # Use Redis sliding window
        current_time = int(time.time())
        window_start = current_time - limits["window"]
        
        # Remove old entries
        await redis_client.zremrangebyscore(redis_key, 0, window_start)
        
        # Count current requests
        current_requests = await redis_client.zcard(redis_key)
        
        if current_requests >= limits["requests"]:
            return False
        
        # Add current request
        await redis_client.zadd(redis_key, {str(current_time): current_time})
        await redis_client.expire(redis_key, limits["window"])
        
        return True
        
    except Exception as e:
        logger.error(f"Rate limit check error: {e}")
        return True  # Allow request if rate limiting fails

# Authentication middleware
async def authenticate_request(request: Request) -> Optional[UserContext]:
    """Authenticate request and return user context"""
    
    try:
        # Check if route is public
        path = str(request.url.path)
        
        for service_name, config in SERVICES_CONFIG.items():
            for public_route in config.get("public_routes", []):
                if path.startswith(public_route):
                    return None  # Public route, no auth needed
        
        # Get authorization header
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        
        # Extract and validate token
        token = auth_header.replace("Bearer ", "")
        
        # Use shared JWT validation
        from shared.auth.jwt_auth import jwt_manager
        token_data = jwt_manager.verify_token(token)
        
        return UserContext(
            user_id=token_data.user_id,
            tenant_id=token_data.tenant_id,
            email=token_data.email,
            role=token_data.role,
            permissions=token_data.permissions
        )
        
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        return None

# Direct service routing without tier validation (assumes already validated)
async def route_to_service_directly(request: Request, service_name: str, path: str) -> Response:
    """Route request to service without tier validation (assumes already validated)"""
    
    try:
        tenant_id = getattr(request.state, 'tenant_id', DEFAULT_TENANT_UUID)
        user_tier = getattr(request.state, 'user_tier', DEFAULT_TIER)
        request_id = getattr(request.state, 'request_id', str(uuid.uuid4()))
        
        # Check circuit breaker
        circuit_state = circuit_breaker.get_state(service_name)
        if circuit_state == "open":
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Service {service_name} is temporarily unavailable"
            )
        
        config = SERVICES_CONFIG[service_name]
        target_url = f"{config['base_url']}{path}"
        
        # Get request body
        body = await request.body()
        
        # Prepare headers (remove hop-by-hop headers)
        headers = dict(request.headers)
        headers.pop("host", None)
        headers.pop("content-length", None)
        
        # Add tenant context headers for downstream services
        headers["X-Tenant-ID"] = tenant_id
        headers["X-User-Tier"] = user_tier
        headers["X-Request-ID"] = request_id
        
        # Add service-to-service authentication
        service_token = ServiceAuthToken.create_service_token(
            service_name="api-gateway",
            target_service=service_name
        )
        headers["x-service-auth"] = service_token
        
        # Make request to service
        start_time = time.time()
        
        async with httpx.AsyncClient(timeout=config.get("timeout", 30)) as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params=dict(request.query_params)
            )
        
        # Record metrics
        duration = time.time() - start_time
        await record_request_metrics(service_name, response.status_code, duration, tenant_id, user_tier)
        
        # Update circuit breaker
        if response.status_code < 500:
            circuit_breaker.record_success(service_name)
        else:
            circuit_breaker.record_failure(service_name)
        
        logger.info(f"Routed: {service_name}{path} | Status: {response.status_code} | Duration: {duration:.3f}s | Tenant: {tenant_id}")
        
        # Return response
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.headers.get("content-type")
        )
        
    except Exception as e:
        logger.error(f"Direct routing error for {service_name}: {str(e)}")
        return JSONResponse(
            status_code=502,
            content={"error": "Service routing failed", "service": service_name}
        )

# Multi-tenant service routing with tier validation using full path
async def route_request_with_tenant_full_path(request: Request, service_name: str, path: str, full_path: str) -> Response:
    """Route request to service with tenant context and tier validation using full path for tier checking"""
    
    try:
        tenant_id = getattr(request.state, 'tenant_id', DEFAULT_TENANT_UUID)
        user_tier = getattr(request.state, 'user_tier', DEFAULT_TIER)
        request_id = getattr(request.state, 'request_id', str(uuid.uuid4()))
        
        # Check tier permissions using full path
        if not is_tier_allowed(user_tier, service_name, full_path):
            tier_name = CLIENT_TIERS[user_tier]['name']
            logger.warning(f"Tier access denied: {user_tier} -> {service_name}{full_path}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"Your {tier_name} plan does not include access to {service_name}. Please upgrade your plan."
            )
        
        # Use direct service routing logic (without tier checking again)
        return await route_to_service_directly(request, service_name, path)
        
    except Exception as e:
        logger.error(f"Routing error for {service_name}: {str(e)}")
        return JSONResponse(
            status_code=502,
            content={"error": "Service routing failed", "service": service_name}
        )

# Multi-tenant service routing with tier validation
async def route_request_with_tenant(request: Request, service_name: str, path: str) -> Response:
    """Route request to service with tenant context and tier validation"""
    
    try:
        tenant_id = getattr(request.state, 'tenant_id', DEFAULT_TENANT_UUID)
        user_tier = getattr(request.state, 'user_tier', DEFAULT_TIER)
        request_id = getattr(request.state, 'request_id', str(uuid.uuid4()))
        
        # Check tier permissions
        if not is_tier_allowed(user_tier, service_name, path):
            tier_name = CLIENT_TIERS[user_tier]['name']
            logger.warning(f"Tier access denied: {user_tier} -> {service_name}{path}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"Your {tier_name} plan does not include access to {service_name}. Please upgrade your plan."
            )
        
        # Check circuit breaker
        circuit_state = circuit_breaker.get_state(service_name)
        if circuit_state == "open":
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Service {service_name} is temporarily unavailable"
            )
        
        config = SERVICES_CONFIG[service_name]
        target_url = f"{config['base_url']}{path}"
        
        # Get request body
        body = await request.body()
        
        # Prepare headers (remove hop-by-hop headers)
        headers = dict(request.headers)
        headers.pop("host", None)
        headers.pop("content-length", None)
        
        # Add tenant context headers for downstream services
        headers["X-Tenant-ID"] = tenant_id
        headers["X-User-Tier"] = user_tier
        headers["X-Request-ID"] = request_id
        
        # Add service-to-service authentication
        service_token = ServiceAuthToken.create_service_token(
            service_name="api-gateway",
            target_service=service_name
        )
        headers["x-service-auth"] = service_token
        
        # Make request to service
        start_time = time.time()
        
        async with httpx.AsyncClient(timeout=config.get("timeout", 30)) as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params=dict(request.query_params)
            )
        
        # Record metrics
        duration = time.time() - start_time
        await record_request_metrics(service_name, response.status_code, duration, tenant_id, user_tier)
        
        # Update circuit breaker
        if response.status_code < 500:
            circuit_breaker.record_success(service_name)
        else:
            circuit_breaker.record_failure(service_name)
        
        logger.info(f"Routed: {service_name}{path} | Status: {response.status_code} | Duration: {duration:.3f}s | Tenant: {tenant_id}")
        
        # Return response
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.headers.get("content-type")
        )
        
    except httpx.TimeoutException:
        circuit_breaker.record_failure(service_name)
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Request to {service_name} timed out"
        )
    except httpx.ConnectError:
        circuit_breaker.record_failure(service_name)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not connect to {service_name}"
        )
    except Exception as e:
        circuit_breaker.record_failure(service_name)
        logger.error(f"Routing error for {service_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error routing request to {service_name}"
        )

async def record_request_metrics(service_name: str, status_code: int, duration: float, tenant_id: str = None, user_tier: str = None):
    """Record request metrics in Redis with tenant and tier information"""
    
    # Skip metrics if Redis is not available
    if not redis_client:
        return
    
    try:
        current_time = int(time.time())
        
        # Record request count
        await redis_client.hincrby("gateway:metrics:requests", service_name, 1)
        
        # Record response time
        await redis_client.hset("gateway:metrics:response_times", service_name, duration)
        
        # Record status code
        status_key = f"{service_name}:{status_code}"
        await redis_client.hincrby("gateway:metrics:status_codes", status_key, 1)
        
        # Record tenant-specific metrics
        if tenant_id:
            await redis_client.hincrby(f"tenant:{tenant_id}:requests", service_name, 1)
            await redis_client.hset(f"tenant:{tenant_id}:response_times", service_name, duration)
        
        # Record tier-specific metrics
        if user_tier:
            await redis_client.hincrby(f"tier:{user_tier}:requests", service_name, 1)
            await redis_client.hset(f"tier:{user_tier}:response_times", service_name, duration)
        
        # Record in time series (for monitoring)
        ts_key = f"gateway:timeseries:{service_name}:{current_time // 60}"  # Per minute
        await redis_client.zadd(ts_key, {str(current_time): duration})
        await redis_client.expire(ts_key, 3600)  # Keep for 1 hour
        
    except Exception as e:
        logger.error(f"Record metrics error: {e}")

# Multi-tenant specific routes
@app.api_route("/cms/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def wagtail_proxy(request: Request, path: str):
    """Proxy requests to Wagtail CMS with multi-tenant routing"""
    
    # Ensure path starts with /api/v2/ for Wagtail API
    if not path.startswith("api/v2/"):
        path = f"api/v2/{path}"
    
    if not path.startswith("/"):
        path = "/" + path
        
    return await route_request_with_tenant(request, "wagtail-cms", path)

@app.api_route("/commerce/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def saleor_proxy(request: Request, path: str):
    """Proxy requests to Saleor E-commerce with multi-tenant routing"""
    
    if not path.startswith("/"):
        path = "/" + path
        
    return await route_request_with_tenant(request, "saleor-commerce", path)

@app.api_route("/directory/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def directory_proxy(request: Request, path: str):
    """Proxy requests to Business Directory with multi-tenant routing"""
    
    if not path.startswith("/"):
        path = "/" + path
        
    return await route_request_with_tenant(request, "business-directory", path)

@app.api_route("/crm/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def crm_proxy(request: Request, path: str):
    """Proxy requests to Django CRM with multi-tenant routing"""
    
    if not path.startswith("/"):
        path = "/" + path
    
    # For tier checking, use the full path including /crm prefix
    full_path = f"/crm{path}"
    
    return await route_request_with_tenant_full_path(request, "django-crm", path, full_path)

@app.api_route("/vault/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def vault_proxy(request: Request, path: str):
    """Proxy requests to Vault Service with multi-tenant routing"""
    
    if not path.startswith("/"):
        path = "/" + path
        
    return await route_request_with_tenant(request, "vault-service", path)

@app.api_route("/workflows/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def temporal_proxy(request: Request, path: str):
    """Proxy requests to Temporal Integration with multi-tenant routing"""
    
    if not path.startswith("/"):
        path = "/" + path
        
    return await route_request_with_tenant(request, "temporal-integration", path)

@app.api_route("/agents/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def agents_proxy(request: Request, path: str):
    """Proxy requests to AI Agents with multi-tenant routing"""
    
    if not path.startswith("/"):
        path = "/" + path
        
    return await route_request_with_tenant(request, "ai-agents", path)

# Client-specific static site generation
@app.get("/sites/{tenant_id}/{path:path}")
async def static_site_proxy(request: Request, tenant_id: str, path: str):
    """Route to tenant-specific static site generation"""
    
    # Verify tenant access
    if hasattr(request.state, 'tenant_id') and request.state.tenant_id != tenant_id:
        # Allow super admin to access any tenant
        user_context = await authenticate_request(request)
        if not user_context or user_context.role.value != "super_admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this tenant's site"
            )
    
    # For now, route to Wagtail CMS - in future this could be a dedicated static site service
    cms_path = f"/api/v2/pages/?site={tenant_id}&path={path}"
    return await route_request_with_tenant(request, "wagtail-cms", cms_path)

# Tier management endpoints
@app.get("/gateway/tiers")
async def get_tier_info():
    """Get information about available tiers"""
    
    return {
        "tiers": CLIENT_TIERS,
        "default_tier": DEFAULT_TIER,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/gateway/tier/{tier_name}")
async def get_tier_details(tier_name: str):
    """Get detailed information about a specific tier"""
    
    if tier_name not in CLIENT_TIERS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tier not found"
        )
    
    return {
        "tier": tier_name,
        "config": CLIENT_TIERS[tier_name],
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/gateway/user/tier")
async def get_user_current_tier(request: Request):
    """Get current user's tier information"""
    
    user_tier = getattr(request.state, 'user_tier', DEFAULT_TIER)
    tenant_id = getattr(request.state, 'tenant_id', 'default')
    
    return {
        "current_tier": user_tier,
        "tenant_id": tenant_id,
        "tier_config": CLIENT_TIERS.get(user_tier, CLIENT_TIERS[DEFAULT_TIER]),
        "timestamp": datetime.utcnow().isoformat()
    }

# Dynamic routing based on path (with multi-tenant support)
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def dynamic_router(request: Request, path: str):
    """Dynamic router for all service requests with multi-tenant support"""
    
    try:
        # Add leading slash if not present
        if not path.startswith("/"):
            path = "/" + path
        
        # Skip gateway management routes
        if path.startswith("/gateway/") or path.startswith("/health") or path.startswith("/docs") or path.startswith("/openapi.json"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
            )
        
        # Determine target service based on path
        service_name = None
        for svc_name, config in SERVICES_CONFIG.items():
            for route in config["routes"]:
                if path.startswith(route):
                    service_name = svc_name
                    break
            if service_name:
                break
        
        if not service_name:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found for this path"
            )
        
        # Check rate limits
        rate_limit_ok = await check_rate_limit(request, service_name)
        if not rate_limit_ok:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )
        
        # Authenticate request if needed
        user_context = await authenticate_request(request)
        
        # Check if authentication is required
        is_public = False
        for public_route in SERVICES_CONFIG[service_name].get("public_routes", []):
            if path.startswith(public_route):
                is_public = True
                break
        
        if not is_public and not user_context:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        # Route request to service with multi-tenant support
        response = await route_request_with_tenant(request, service_name, path)
        
        # Add headers
        response.headers["x-gateway-service"] = service_name
        response.headers["x-gateway-timestamp"] = str(int(time.time()))
        response.headers["x-gateway-version"] = "2.0.0"
        
        if user_context:
            response.headers["x-user-id"] = user_context.user_id
            response.headers["x-tenant-id"] = user_context.tenant_id
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Dynamic router error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal gateway error"
        )

# Enhanced metrics and monitoring endpoints
@app.get("/gateway/metrics")
async def get_gateway_metrics():
    """Get API Gateway metrics with tenant and tier breakdown"""
    
    try:
        if not redis_client:
            return {
                "total_requests": 0,
                "requests_by_service": {},
                "average_response_time": 0,
                "response_times_by_service": {},
                "status_codes": {},
                "circuit_breaker_states": {
                    service: circuit_breaker.get_state(service) 
                    for service in SERVICES_CONFIG.keys()
                },
                "redis_available": False,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Get request counts
        request_counts = await redis_client.hgetall("gateway:metrics:requests")
        
        # Get response times
        response_times = await redis_client.hgetall("gateway:metrics:response_times")
        
        # Get status codes
        status_codes = await redis_client.hgetall("gateway:metrics:status_codes")
        
        # Get tier metrics
        tier_metrics = {}
        for tier_name in CLIENT_TIERS.keys():
            tier_requests = await redis_client.hgetall(f"tier:{tier_name}:requests")
            tier_metrics[tier_name] = {k: int(v) for k, v in tier_requests.items()}
        
        # Calculate derived metrics
        total_requests = sum(int(count) for count in request_counts.values())
        avg_response_time = sum(float(time) for time in response_times.values()) / len(response_times) if response_times else 0
        
        return {
            "total_requests": total_requests,
            "requests_by_service": {k: int(v) for k, v in request_counts.items()},
            "average_response_time": round(avg_response_time, 3),
            "response_times_by_service": {k: float(v) for k, v in response_times.items()},
            "status_codes": {k: int(v) for k, v in status_codes.items()},
            "tier_metrics": tier_metrics,
            "circuit_breaker_states": {
                service: circuit_breaker.get_state(service) 
                for service in SERVICES_CONFIG.keys()
            },
            "redis_available": True,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Get gateway metrics error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get metrics"
        )

@app.get("/gateway/config")
async def get_gateway_config():
    """Get current gateway configuration including tier information"""
    
    return {
        "services": {
            service: {
                "base_url": config["base_url"],
                "routes": config["routes"],
                "public_routes": config.get("public_routes", []),
                "timeout": config.get("timeout", 30),
                "multi_tenant": config.get("multi_tenant", False)
            }
            for service, config in SERVICES_CONFIG.items()
        },
        "tiers": CLIENT_TIERS,
        "rate_limits": RATE_LIMITS,
        "circuit_breaker": CIRCUIT_BREAKER_CONFIG,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/gateway/circuit-breaker/{service_name}/reset")
async def reset_circuit_breaker(service_name: str):
    """Reset circuit breaker for a service"""
    
    if service_name not in SERVICES_CONFIG:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    # Reset circuit breaker state
    if service_name in circuit_breaker.states:
        circuit_breaker.states[service_name] = {
            "state": "closed",
            "failures": 0,
            "last_failure": None,
            "successes": 0
        }
    
    return {
        "message": f"Circuit breaker reset for {service_name}",
        "service": service_name,
        "new_state": "closed"
    }

# Load balancing (for future use with multiple service instances)
class LoadBalancer:
    """Simple round-robin load balancer"""
    
    def __init__(self):
        self.service_instances = {}  # service_name -> [list of instances]
        self.current_instance = {}   # service_name -> current_index
    
    def add_instance(self, service_name: str, instance_url: str):
        """Add service instance"""
        if service_name not in self.service_instances:
            self.service_instances[service_name] = []
            self.current_instance[service_name] = 0
        
        if instance_url not in self.service_instances[service_name]:
            self.service_instances[service_name].append(instance_url)
    
    def get_instance(self, service_name: str) -> str:
        """Get next instance using round-robin"""
        if service_name not in self.service_instances:
            return SERVICES_CONFIG[service_name]["base_url"]
        
        instances = self.service_instances[service_name]
        if not instances:
            return SERVICES_CONFIG[service_name]["base_url"]
        
        current = self.current_instance[service_name]
        instance = instances[current]
        
        # Move to next instance
        self.current_instance[service_name] = (current + 1) % len(instances)
        
        return instance

load_balancer = LoadBalancer()

# Background health check task
async def health_check_services():
    """Background task to continuously check service health"""
    
    while True:
        try:
            await asyncio.sleep(30)  # Check every 30 seconds
            
            for service_name, config in SERVICES_CONFIG.items():
                try:
                    health_url = f"{config['base_url']}{config['health_endpoint']}"
                    
                    async with httpx.AsyncClient(timeout=5.0) as client:
                        response = await client.get(health_url)
                        
                        if response.status_code == 200:
                            circuit_breaker.record_success(service_name)
                            
                            # Cache health status if Redis is available
                            if redis_client:
                                await redis_client.hset(
                                    "gateway:service_health",
                                    service_name,
                                    json.dumps({
                                        "status": "healthy",
                                        "last_check": datetime.utcnow().isoformat(),
                                        "response_time": response.elapsed.total_seconds(),
                                        "multi_tenant": config.get("multi_tenant", False)
                                    })
                                )
                        else:
                            circuit_breaker.record_failure(service_name)
                            
                            if redis_client:
                                await redis_client.hset(
                                    "gateway:service_health", 
                                    service_name,
                                    json.dumps({
                                        "status": "unhealthy",
                                        "last_check": datetime.utcnow().isoformat(),
                                        "status_code": response.status_code
                                    })
                                )
                            
                except Exception as e:
                    circuit_breaker.record_failure(service_name)
                    
                    if redis_client:
                        await redis_client.hset(
                            "gateway:service_health",
                            service_name, 
                            json.dumps({
                                "status": "error",
                                "last_check": datetime.utcnow().isoformat(),
                                "error": str(e)
                            })
                        )
                    
        except Exception as e:
            logger.error(f"Health check background task error: {e}")

# Request/Response logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests and responses with tenant context"""
    
    start_time = time.time()
    tenant_id = getattr(request.state, 'tenant_id', 'unknown')
    user_tier = getattr(request.state, 'user_tier', 'unknown')
    
    # Log request
    logger.info(f"Request: {request.method} {request.url.path} | Tenant: {tenant_id} | Tier: {user_tier}")
    
    try:
        response = await call_next(request)
        
        # Log response
        duration = time.time() - start_time
        logger.info(f"Response: {response.status_code} ({duration:.3f}s) | Tenant: {tenant_id}")
        
        # Add performance headers
        response.headers["x-response-time"] = f"{duration:.3f}s"
        
        return response
        
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Request failed: {request.method} {request.url.path} - {str(e)} ({duration:.3f}s)")
        raise

# WebSocket proxy (for real-time features with multi-tenant support)
@app.websocket("/ws/{path:path}")
async def websocket_proxy(websocket, path: str):
    """Proxy WebSocket connections to appropriate services with tenant context"""
    
    # Determine target service
    service_name = None
    for svc_name, config in SERVICES_CONFIG.items():
        for route in config["routes"]:
            if f"/{path}".startswith(route):
                service_name = svc_name
                break
        if service_name:
            break
    
    if not service_name:
        await websocket.close(code=1000, reason="Service not found")
        return
    
    # For now, just accept and close - full WebSocket proxy would require more complex implementation
    await websocket.accept()
    await websocket.send_text(json.dumps({
        "message": "WebSocket proxy not fully implemented",
        "service": service_name,
        "path": path,
        "multi_tenant_support": "coming_soon"
    }))
    await websocket.close()


# Unified Tenant Context Management Endpoints
@app.get("/api/tenant/context")
async def get_tenant_context(request: Request, user: Optional[UserContext] = Depends(get_current_user)):
    """
    Get unified tenant context for current domain
    Coordinates information from Wagtail, Saleor, and CRM services
    """
    try:
        # Extract domain from request
        domain = request.headers.get("host", "").split(":")[0]
        if not domain:
            raise HTTPException(status_code=400, detail="Invalid domain")
        
        # Get user ID if authenticated
        user_id = user.user_id if user else None
        
        # Resolve tenant context
        context = await tenant_context_service.resolve_tenant_context(
            domain=domain,
            user_id=user_id,
            force_refresh=False
        )
        
        if not context:
            raise HTTPException(status_code=404, detail="Tenant not found for this domain")
        
        return {
            "success": True,
            "tenant_context": context.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting tenant context: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/tenant/context/refresh")
async def refresh_tenant_context(request: Request, user: Optional[UserContext] = Depends(get_current_user)):
    """
    Force refresh of tenant context from all services
    """
    try:
        # Extract domain from request
        domain = request.headers.get("host", "").split(":")[0]
        if not domain:
            raise HTTPException(status_code=400, detail="Invalid domain")
        
        # Get user ID if authenticated
        user_id = user.user_id if user else None
        
        # Force refresh tenant context
        context = await tenant_context_service.resolve_tenant_context(
            domain=domain,
            user_id=user_id,
            force_refresh=True
        )
        
        if not context:
            raise HTTPException(status_code=404, detail="Tenant not found for this domain")
        
        return {
            "success": True,
            "message": "Tenant context refreshed",
            "tenant_context": context.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error refreshing tenant context: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/tenant/sync")
async def sync_tenant_across_services(
    request: Request, 
    user: UserContext = Depends(get_current_user)
):
    """
    Synchronize tenant information across all services
    Requires authenticated user
    """
    try:
        # Extract domain from request
        domain = request.headers.get("host", "").split(":")[0]
        if not domain:
            raise HTTPException(status_code=400, detail="Invalid domain")
        
        # Get current tenant context
        context = await tenant_context_service.resolve_tenant_context(
            domain=domain,
            user_id=user.user_id,
            force_refresh=True
        )
        
        if not context:
            raise HTTPException(status_code=404, detail="Tenant not found for this domain")
        
        # Synchronize across services
        sync_results = await tenant_context_service.sync_tenant_across_services(context)
        
        return {
            "success": True,
            "message": "Tenant synchronization completed",
            "sync_results": sync_results,
            "tenant_context": context.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error syncing tenant: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/tenant/features")
async def get_tenant_features(request: Request, user: Optional[UserContext] = Depends(get_current_user)):
    """
    Get available features for current tenant based on subscription tier
    """
    try:
        # Extract domain from request
        domain = request.headers.get("host", "").split(":")[0]
        if not domain:
            raise HTTPException(status_code=400, detail="Invalid domain")
        
        # Get user ID if authenticated
        user_id = user.user_id if user else None
        
        # Resolve tenant context
        context = await tenant_context_service.resolve_tenant_context(
            domain=domain,
            user_id=user_id
        )
        
        if not context:
            raise HTTPException(status_code=404, detail="Tenant not found for this domain")
        
        return {
            "success": True,
            "tenant_id": context.tenant_id,
            "subscription_tier": context.subscription_tier,
            "features": context.features,
            "tier_limits": context.tier_limits,
            "branding": context.branding
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting tenant features: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.delete("/api/tenant/context/cache")
async def invalidate_tenant_cache(request: Request, user: UserContext = Depends(get_current_user)):
    """
    Invalidate cached tenant context (requires authentication)
    """
    try:
        # Extract domain from request
        domain = request.headers.get("host", "").split(":")[0]
        if not domain:
            raise HTTPException(status_code=400, detail="Invalid domain")
        
        # Invalidate cache
        await tenant_context_service.invalidate_cache(domain, user.user_id)
        
        return {
            "success": True,
            "message": "Tenant context cache invalidated"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error invalidating cache: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)