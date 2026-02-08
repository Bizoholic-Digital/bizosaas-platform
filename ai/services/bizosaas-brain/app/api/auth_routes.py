"""
Authentication Proxy Routes for BizOSaaS Brain Gateway
Proxies authentication requests to the dedicated Auth Service
"""
from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import JSONResponse
import httpx
import logging
import os

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Auth Service Configuration
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://backendservices-authservice-ux07ss:8007")

logger = logging.getLogger(__name__)

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_auth_request(path: str, request: Request):
    """
    Proxy all auth requests to the Auth Service
    Preserves headers, cookies, and request body
    """
    try:
        # Build target URL
        target_url = f"{AUTH_SERVICE_URL}/{path}"
        
        # Get request body
        body = await request.body()
        
        # Prepare headers (exclude host header)
        headers = dict(request.headers)
        headers.pop("host", None)
        
        # Make request to auth service
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params=request.query_params,
                cookies=request.cookies
            )
            
            # Return response with same status code, headers, and body
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.headers.get("content-type")
            )
            
    except httpx.HTTPStatusError as e:
        logger.error(f"Auth service HTTP error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Auth service error: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"Auth service connection error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Auth service unavailable: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error proxying auth request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/health")
async def auth_health_check():
    """Check auth service connectivity"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{AUTH_SERVICE_URL}/health")
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "auth_service": "connected",
                "auth_service_url": AUTH_SERVICE_URL,
                "auth_service_status": response.status_code
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "auth_service": "disconnected",
            "auth_service_url": AUTH_SERVICE_URL,
            "error": str(e)
        }
