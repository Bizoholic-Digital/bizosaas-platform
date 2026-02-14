import os
import httpx
import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager
from app.observability.logging import setup_logging

# 1. Immediate Vault Initialization (Must happen before other app imports)
def load_vault_secrets_sync():
    """Synchronously load secrets from Vault into environment variables."""
    try:
        from app.adapters.vault_adapter import VaultAdapter
        mount_point = os.getenv("VAULT_MOUNT_POINT", "secret")
        vault = VaultAdapter(mount_point=mount_point)
        if vault.client and vault.client.is_authenticated():
            print("INFO: Connected to Vault. Loading secrets early...")
            
            # Load Platform Secrets
            platform_secrets = vault.get_secret_sync("platform/brain-gateway")
            if platform_secrets:
                os.environ.update(platform_secrets)
            
            # Load Infrastructure Secrets
            infra_secrets = vault.get_secret_sync("platform/infrastructure")
            if infra_secrets:
                os.environ.update(infra_secrets)
            
            # Load Integration Secrets
            for integration in ["openai", "anthropic", "google", "openrouter", "clerk", "stripe"]:
                int_secrets = vault.get_secret_sync(f"integrations/{integration}")
                if int_secrets:
                    os.environ.update(int_secrets)
            print("INFO: Vault secrets loaded successfully.")
            print(f"DEBUG: DATABASE_URL is {'set' if os.environ.get('DATABASE_URL') else 'NOT SET'}")
    except Exception as e:
        print(f"WARNING: Vault early loading failed: {e}. Falling back to environment variables.")

load_vault_secrets_sync()

# Configure structured logging after environment is potentially updated
setup_logging(level=os.getenv("LOG_LEVEL", "INFO"), json_format=os.getenv("LOG_JSON", "true").lower() == "true")
logger = logging.getLogger(__name__)


from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.api import connectors, agents, cms, onboarding, support, crm, ecommerce, billing, admin, mcp, marketing, campaigns, users, workflows, discovery, metrics as metrics_api, websockets, workflow_governance, workflow_metrics, admin_prime, feature_orchestrator, alerts, predictive_analytics, isolation_testing, cost_optimization, directory_admin, admin_mcp, tenant_management, billing_admin, cms_admin, analytics_admin, agent_admin, temporal_admin, triggers, domains, support_admin, reporting_admin, security_admin, shopify, shopify_oauth, gaming, monitoring, seo_dashboard, content, persona, social_content
from app.seeds.connectors import seed_connectors
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Brain Gateway (VERSION: c3eb_standardized)...")
    
    # Auto-Migration & Seeding
    try:
        from init_db import init_db
        from seed_mcp import seed_mcp_registry
        from seed_subscription_plans import seed_subscription_plans
        from migrate_mcp_columns import migrate as migrate_schema
        from migrate_missing_columns import migrate as migrate_missing_columns
        
        logger.info("Running database initialization...")
        init_db()
        
        logger.info("Running schema migrations...")
        migrate_schema()
        
        logger.info("Running missing columns migration...")
        migrate_missing_columns()
        
        logger.info("Running MCP registry seeding...")
        seed_mcp_registry()
        logger.info("Running subscription plans seeding...")
        seed_subscription_plans()

        # Start Alert Monitors
        from app.services.alert_system import start_alert_monitors
        await start_alert_monitors()
            
    except Exception as e:
        logger.error(f"Startup initialization failed: {e}")
        # Continue startup even if initialization fails, but log error

    seed_connectors()
    
    # Start metrics collector
    from app.observability.collectors import periodic_metric_collector
    asyncio.create_task(periodic_metric_collector())
    
    yield
    
    # Shutdown
    logger.info("Shutting down Brain Gateway...")

app = FastAPI(title="Brain API Gateway", lifespan=lifespan)

# ----------------------------------------------------------------------------
# Routers and Middleware
# ----------------------------------------------------------------------------

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all Routers
app.include_router(connectors.router)
app.include_router(agents.router)
app.include_router(cms.router, prefix="/api/cms", tags=["cms"])
app.include_router(crm.router, prefix="/api/crm", tags=["crm"])
app.include_router(ecommerce.router, prefix="/api/ecommerce", tags=["ecommerce"])
app.include_router(marketing.router, prefix="/api/marketing", tags=["marketing"])
app.include_router(campaigns.router, prefix="/api/campaigns", tags=["campaigns"])
app.include_router(billing.router, prefix="/api/billing", tags=["billing"])
app.include_router(onboarding.router)
app.include_router(shopify.router)
app.include_router(support.router)
app.include_router(admin.router)
app.include_router(mcp.router, prefix="/api/mcp", tags=["MCP Marketplace"])
app.include_router(users.router)
app.include_router(workflows.router)
app.include_router(workflow_governance.router)  # Workflow approval/rejection/refinement
app.include_router(workflow_metrics.router)  # Workflow monitoring and metrics
app.include_router(admin_prime.router)  # Admin Prime Copilot
app.include_router(feature_orchestrator.router)  # Centralized Feature Management
app.include_router(alerts.router)  # Real-time WebSocket Alerts
app.include_router(predictive_analytics.router)  # Predictive Insights
app.include_router(isolation_testing.router)  # Multi-tenant Isolation Testing
app.include_router(cost_optimization.router)  # Cost Optimization Engine
app.include_router(directory_admin.router)  # Directory Management & Fine-Tuning
app.include_router(admin_mcp.router)      # MCP Ecosystem Administration
app.include_router(tenant_management.router)  # Tenant Management Dashboard
app.include_router(billing_admin.router)     # Billing Administration
app.include_router(cms_admin.router)         # CMS & WordPress Administration
app.include_router(analytics_admin.router)   # Analytics & Intelligence Admin
app.include_router(agent_admin.router)       # AI Agent Management Admin
app.include_router(temporal_admin.router)     # Temporal & Workflow Administration
app.include_router(temporal_admin.router_sys) # System Configuration Admin
app.include_router(support_admin.router)      # Support & Debugging Admin
app.include_router(reporting_admin.router)    # Reporting & Exports Admin
app.include_router(security_admin.router)     # Security & Compliance Admin
app.include_router(triggers.router)           # Autonomous Triggers
app.include_router(shopify_oauth.router)      # Shopify OAuth & Proxy
app.include_router(domains.router)            # Domain Automation
app.include_router(discovery.router, prefix="/api/discovery", tags=["discovery"])
app.include_router(gaming.router, prefix="/api/brain/gaming", tags=["gaming"])
app.include_router(monitoring.router, prefix="/api/brain/monitoring", tags=["monitoring"])
app.include_router(seo_dashboard.router)
app.include_router(content.router)
app.include_router(persona.router)
app.include_router(social_content.router)
app.include_router(metrics_api.router)
app.include_router(websockets.router)
from app.api import directory
app.include_router(directory.router)

from app.routers import oauth
from app.api import rag
app.include_router(oauth.router)
app.include_router(rag.router)

from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# ----------------------------------------------------------------------------
# Instrumentation (After Routers)
# ----------------------------------------------------------------------------

# Add Prometheus metrics
Instrumentator().instrument(app).expose(app)

# OpenTelemetry Foundation
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Set up tracing
resource = Resource(attributes={
    SERVICE_NAME: "brain-gateway"
})

tracer_provider = TracerProvider(resource=resource)
# Only add OTLP exporter if endpoint is configured
otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
if otlp_endpoint:
    try:
        otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
        tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        logger.info(f"OTLP Exporter configured for {otlp_endpoint}")
    except Exception as e:
        logger.warning(f"Failed to initialize OTLP exporter: {e}")

trace.set_tracer_provider(tracer_provider)
FastAPIInstrumentor.instrument_app(app)

# ----------------------------------------------------------------------------


# Configuration
CMS_URL = os.getenv("CMS_URL", "http://cms:8002")
WORDPRESS_URL = os.getenv("WORDPRESS_URL", "http://bizoholicwebsite-wordpress-rbtyli")
CRM_URL = os.getenv("CRM_URL", "http://crm:8003")
# AUTH_URL = os.getenv("AUTH_URL", "http://auth-service:8006") # Deprecated
SALEOR_URL = os.getenv("SALEOR_URL", "http://saleor:8000")
AI_AGENTS_URL = os.getenv("AI_AGENTS_URL")


@app.get("/health")
async def health_check():
    import time
    from app.observability.health import get_dependency_health
    
    data = await get_dependency_health()
    
    # Check AI Agents service
    if AI_AGENTS_URL:
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                ai_res = await client.get(f"{AI_AGENTS_URL}/health")
                data["dependencies"]["ai_agents"] = {
                    "status": "healthy" if ai_res.status_code == 200 else "unhealthy",
                    "details": ai_res.json() if ai_res.status_code == 200 else ai_res.text
                }
        except Exception as e:
            data["dependencies"]["ai_agents"] = {"status": "error", "message": str(e)}
            data["status"] = "degraded"

    data.update({
        "service": "brain-gateway",
        "version": "1.0.0",
        "timestamp": time.time()
    })
    
    status_code = 200 if data["status"] == "healthy" else (503 if data["status"] == "unhealthy" else 200)
    return JSONResponse(content=data, status_code=status_code)

@app.api_route("/api/brain/wagtail/{path:path}", methods=["GET", "POST", "PUT", "DELETE"], include_in_schema=False)
async def proxy_wagtail(request: Request, path: str):
    url = f"{CMS_URL}/api/v2/{path}"
    return await proxy_request(request, url)

@app.api_route("/api/brain/wordpress/{path:path}", methods=["GET", "POST", "PUT", "DELETE"], include_in_schema=False)
async def proxy_wordpress(request: Request, path: str):
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/{path}"
    return await proxy_request(request, url)

@app.api_route("/api/brain/django-crm/{path:path}", methods=["GET", "POST", "PUT", "DELETE"], include_in_schema=False)
async def proxy_crm(request: Request, path: str):
    url = f"{CRM_URL}/api/{path}"
    return await proxy_request(request, url)

@app.api_route("/api/brain/integrations/{path:path}", methods=["GET", "POST", "PUT", "DELETE"], include_in_schema=False)
async def proxy_integrations(request: Request, path: str = ""):
    """Proxy for frontend integrations calls"""
    # Simply forward to the connectors router logic
    url = f"http://ai-agents:8000/api/connectors/{path}"
    return await proxy_request(request, url)

# @app.api_route("/api/brain/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
# async def proxy_auth(request: Request, path: str):
#     url = f"{AUTH_URL}/{path}"
#     return await proxy_request(request, url)

@app.api_route("/api/brain/agents/{path:path}", methods=["GET", "POST", "PUT", "DELETE"], include_in_schema=False)
async def proxy_agents(request: Request, path: str):
    """
    Proxy agents requests to the ai-agents service.
    Handles /task, /chat, and general agent info lookups.
    """
    # If path ends with /task, it's a direct task execution
    if path.endswith("/task"):
        # Transfrom agent_id to agent_type for ai-agents compatibility
        try:
            body = await request.json()
            if "agent_id" in body and "agent_type" not in body:
                body["agent_type"] = body["agent_id"]
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://ai-agents:8000/tasks",
                    json=body,
                    headers={k: v for k, v in request.headers.items() if k.lower() not in ('content-length', 'host')},
                    timeout=60.0
                )
                return JSONResponse(content=response.json(), status_code=response.status_code)
        except Exception as e:
            return JSONResponse(content={"error": f"Proxy transformation failed: {str(e)}"}, status_code=500)
    
    # Otherwise, map directly to ai-agents service
    url = f"http://ai-agents:8000/{path}"
    return await proxy_request(request, url)

@app.api_route("/api/brain/tasks/{path:path}", methods=["GET", "POST", "PUT", "DELETE"], include_in_schema=False)
async def proxy_tasks(request: Request, path: str):
    # Mapping to ai-agents service tasks
    url = f"http://ai-agents:8000/tasks/{path}"
    return await proxy_request(request, url)

# @app.post("/api/auth/login")
# async def auth_login(request: Request):
#     """Proxy login to Auth Service SSO"""
#     url = f"{AUTH_URL}/auth/sso/login"
#     return await proxy_request(request, url)

# @app.post("/api/auth/social-login")
# async def auth_social_login(request: Request):
#     """Proxy social login to Auth Service Token Exchange"""
#     url = f"{AUTH_URL}/auth/token/exchange"
#     return await proxy_request(request, url)

async def proxy_request(request: Request, url: str):
    async with httpx.AsyncClient() as client:
        try:
            # Forward headers, excluding hop-by-hop headers
            headers = {
                k: v for k, v in request.headers.items() 
                if k.lower() not in ('content-length', 'transfer-encoding', 'host')
            }
            
            content = await request.body()
            
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=content,
                params=request.query_params,
                timeout=30.0
            )
            
            # Try to parse as JSON, fall back to text
            try:
                response_content = response.json()
            except:
                response_content = response.text
            
            return JSONResponse(
                content=response_content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError as exc:
            return JSONResponse(
                content={"error": f"Service unavailable: {str(exc)}"},
                status_code=503
            )
        except Exception as exc:
            return JSONResponse(
                content={"error": f"Internal server error: {str(exc)}"},
                status_code=500
            )

@app.post("/api/auth/sso/wagtail")
async def sso_wagtail(request: Request):
    """
    Generate SSO login URL for Wagtail.
    1. Receives user info (should be from JWT in production)
    2. Calls Wagtail internal API to get signed token
    3. Returns magic link
    """
    try:
        body = await request.json()
        
        # Call Wagtail internal API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{CMS_URL}/api/internal/sso/token/",
                json=body,
                timeout=5.0
            )
            
            if response.status_code != 200:
                return JSONResponse(
                    content={"error": "Failed to generate SSO token"},
                    status_code=response.status_code
                )
                
            data = response.json()
            
            # Construct absolute URL for the frontend iframe
            # The token URL path is returned by Wagtail, e.g. /admin/sso/login/?token=...
            # We need to prepend the public Wagtail URL (proxied via Brain or direct)
            # Since Wagtail is embedded, we use the public URL routed through Brain or direct port
            # For now, let's assume direct access or proxied access.
            # If proxied: http://localhost:8000/api/brain/wagtail/... but that might not work for admin
            # The admin is accessed via http://localhost:8002/admin/ directly in the iframe usually
            # So we return the full URL using the public CMS URL (localhost:8002)
            
            # Use the login_url returned by Wagtail (relative path)
            # Prepend the public base URL
            public_cms_url = "http://localhost:8002" 
            full_url = f"{public_cms_url}{data['login_url']}"
            
            return JSONResponse({
                "sso_url": full_url,
                "expires_in": data.get("expires_in")
            })
            
    except Exception as exc:
        return JSONResponse(
            content={"error": f"SSO Error: {str(exc)}"},
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
