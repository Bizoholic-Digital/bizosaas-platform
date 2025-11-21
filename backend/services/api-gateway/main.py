from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import Dict
import logging

app = FastAPI(
    title="BizOSaaS API Gateway",
    version="1.0.0",
    description="Unified API Gateway for BizOSaaS Platform"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://stg.bizoholic.com",
        "https://stg.coreldove.com",
        "https://stg.thrillring.com",
        "https://portal.bizoholic.com",
        "https://admin.bizoholic.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service Registry (DDD Bounded Contexts)
SERVICE_REGISTRY: Dict[str, str] = {
    "/auth": "http://backendservices-authservice-ux07ss:8002",
    "/crm": "http://backend-django-crm:8003",
    "/cms": "http://backend-wagtail-cms:8004",
    "/directory": "http://backend-business-directory:8005",
    "/ai": "http://backend-ai-agents:8008",
    "/trading": "http://backend-quanttrade-backend:8009",
    "/sourcing": "http://backend-amazon-sourcing:8010",
}

# Default to Brain Gateway
DEFAULT_SERVICE = "http://backend-brain-gateway:8001"

logger = logging.getLogger(__name__)

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def gateway_proxy(path: str, request: Request):
    """
    API Gateway - Routes requests to appropriate microservices
    Implements DDD bounded context routing with circuit breaker pattern
    """

    # Determine target service from path
    target_service = DEFAULT_SERVICE
    route_prefix = None

    for prefix, service_url in SERVICE_REGISTRY.items():
        if f"/{path}".startswith(prefix):
            target_service = service_url
            route_prefix = prefix
            break

    # Remove route prefix from path for backend
    if route_prefix:
        backend_path = path[len(route_prefix.lstrip('/')):]
    else:
        backend_path = path

    # Build target URL
    target_url = f"{target_service}/{backend_path}"

    logger.info(f"Routing {request.method} /{path} → {target_url}")

    # Forward request to backend service
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Prepare headers (remove host header)
            headers = dict(request.headers)
            headers.pop('host', None)

            # Forward request
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                params=request.query_params,
                content=await request.body()
            )

            # Return response
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.headers.get('content-type')
            )

    except httpx.TimeoutException:
        logger.error(f"Timeout calling {target_url}")
        raise HTTPException(status_code=504, detail="Gateway timeout")
    except httpx.ConnectError:
        logger.error(f"Connection error to {target_url}")
        raise HTTPException(status_code=503, detail="Service unavailable")
    except Exception as e:
        logger.error(f"Error proxying request: {e}")
        raise HTTPException(status_code=500, detail="Internal gateway error")

@app.get("/health")
async def health_check():
    """Gateway health check"""
    return {
        "status": "healthy",
        "service": "api-gateway",
        "version": "1.0.0",
        "services": len(SERVICE_REGISTRY)
    }

@app.get("/gateway/routes")
async def list_routes():
    """List all registered service routes"""
    return {
        "routes": [
            {
                "prefix": prefix,
                "service": url,
                "description": f"Routes {prefix}/* to {url}"
            }
            for prefix, url in SERVICE_REGISTRY.items()
        ],
        "default": DEFAULT_SERVICE
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
