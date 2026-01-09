import os
import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(name)s:%(message)s'
)
logger = logging.getLogger(__name__)


from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.api import connectors, agents, cms, onboarding, support, crm, ecommerce, billing, admin, mcp, marketing, campaigns
import app.connectors # Trigger registration

app = FastAPI(title="Brain API Gateway")

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
    otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

trace.set_tracer_provider(tracer_provider)
FastAPIInstrumentor.instrument_app(app)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.seeds.connectors import seed_connectors

@app.on_event("startup")
async def startup_event():
    # Auto-Migration & Seeding
    try:
        from init_db import init_db
        from seed_mcp import seed_mcp_registry
        print("Running database initialization...")
        init_db()
        print("Running MCP registry seeding...")
        seed_mcp_registry()
    except Exception as e:
        print(f"Startup migration failed: {e}")

    # Vault Integration for API Keys
    try:
        import hvac
        vault_addr = os.getenv('VAULT_ADDR')
        vault_token = os.getenv('VAULT_TOKEN')
        
        if vault_addr and vault_token:
            client = hvac.Client(url=vault_addr, token=vault_token)
            if client.is_authenticated():
                print("Connected to Vault for API keys")
                
                # Fetch Platform Secrets
                try:
                    secret = client.secrets.kv.v2.read_secret_version(path='platform/brain-gateway', mount_point='bizosaas')
                    data = secret['data']['data']
                    
                    if 'openai_api_key' in data:
                        os.environ['OPENAI_API_KEY'] = data['openai_api_key']
                    if 'vector_db_url' in data:
                        os.environ['VECTOR_DB_URL'] = data['vector_db_url']
                except Exception as e:
                    print(f"Failed to fetch platform secrets: {e}")

                # Fetch Clerk Secrets
                try:
                    clerk_secret = client.secrets.kv.v2.read_secret_version(path='clerk', mount_point='bizosaas')
                    clerk_data = clerk_secret['data']['data']
                    if 'secret_key' in clerk_data:
                        os.environ['CLERK_SECRET_KEY'] = clerk_data['secret_key']
                        print("Clerk Secret Key loaded from Vault")
                except Exception as e:
                    print(f"Failed to fetch Clerk secrets (Key might not be stored yet): {e}")

                # Re-initialize RAG service with new env vars
                from app.core import rag
                rag.rag_service.__init__()
                print("RAG Service re-initialized with Vault secrets")
    except Exception as e:
        print(f"Failed to connect to Vault: {e}")

    seed_connectors()

app.include_router(connectors.router)
app.include_router(agents.router)
app.include_router(cms.router, prefix="/api/cms", tags=["cms"])
app.include_router(crm.router, prefix="/api/crm", tags=["crm"])
app.include_router(ecommerce.router, prefix="/api/ecommerce", tags=["ecommerce"])
app.include_router(marketing.router, prefix="/api/marketing", tags=["marketing"])
app.include_router(campaigns.router, prefix="/api/campaigns", tags=["campaigns"])
app.include_router(billing.router, prefix="/api/billing", tags=["billing"])
app.include_router(onboarding.router)
app.include_router(support.router)
# app.include_router(auth.router) # Deprecated
app.include_router(admin.router)
app.include_router(mcp.router, prefix="/api/mcp", tags=["MCP Marketplace"])

from app.routers import oauth
from app.api import rag
app.include_router(oauth.router)
app.include_router(rag.router)

from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Configuration
CMS_URL = os.getenv("CMS_URL", "http://cms:8002")
CRM_URL = os.getenv("CRM_URL", "http://crm:8003")
# AUTH_URL = os.getenv("AUTH_URL", "http://auth-service:8006") # Deprecated
SALEOR_URL = os.getenv("SALEOR_URL", "http://saleor:8000")


@app.get("/health")
async def health_check():
    from app.dependencies import engine
    from sqlalchemy import text
    import time

    health = {
        "status": "healthy",
        "service": "brain-gateway",
        "timestamp": time.time(),
        "dependencies": {}
    }

    # Check Database
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        health["dependencies"]["database"] = "ok"
    except Exception as e:
        health["dependencies"]["database"] = f"error: {str(e)}"
        health["status"] = "unhealthy"

    # Check Vault (Optional)
    vault_addr = os.getenv('VAULT_ADDR')
    if vault_addr:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(f"{vault_addr}/v1/sys/health", timeout=2.0)
                health["dependencies"]["vault"] = "ok" if res.status_code == 200 else f"status: {res.status_code}"
        except:
            health["dependencies"]["vault"] = "unreachable"

    # Check Services (Basic ping)
    services = {
        "cms": CMS_URL,
        "crm": CRM_URL,
        "ai-agents": "http://ai-agents:8000"
    }
    
    for name, url in services.items():
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(f"{url}/health" if name == "ai-agents" else url, timeout=1.0)
                health["dependencies"][name] = "ok" if res.status_code < 500 else f"status: {res.status_code}"
        except:
            health["dependencies"][name] = "unreachable"

    status_code = 200 if health["status"] == "healthy" else 503
    return JSONResponse(content=health, status_code=status_code)

@app.api_route("/api/brain/wagtail/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_wagtail(request: Request, path: str):
    url = f"{CMS_URL}/api/v2/{path}"
    return await proxy_request(request, url)

@app.api_route("/api/brain/django-crm/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_crm(request: Request, path: str):
    url = f"{CRM_URL}/api/{path}"
    return await proxy_request(request, url)

@app.api_route("/api/brain/integrations/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_integrations(request: Request, path: str = ""):
    """Proxy for frontend integrations calls"""
    # Simply forward to the connectors router logic
    url = f"http://ai-agents:8000/api/connectors/{path}"
    return await proxy_request(request, url)

# @app.api_route("/api/brain/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
# async def proxy_auth(request: Request, path: str):
#     url = f"{AUTH_URL}/{path}"
#     return await proxy_request(request, url)

@app.api_route("/api/brain/agents/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
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

@app.api_route("/api/brain/tasks/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
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
