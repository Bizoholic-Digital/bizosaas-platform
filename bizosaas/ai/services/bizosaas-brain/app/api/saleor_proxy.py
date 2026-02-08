"""
Saleor GraphQL Proxy Routes
Proxies all Saleor GraphQL requests through Brain Gateway for centralized control
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import Response, JSONResponse
import httpx
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/saleor", tags=["saleor-proxy"])

# Saleor backend configuration
SALEOR_API_URL = os.getenv("SALEOR_API_URL", "http://10.0.1.47:8000/graphql/")
SALEOR_TIMEOUT = 30.0  # 30 second timeout for GraphQL queries


@router.post("/graphql")
async def proxy_graphql(request: Request):
    """
    Proxy GraphQL requests to Saleor backend

    This endpoint maintains the Brain Gateway as the central API gateway,
    routing all Saleor GraphQL requests through it for:
    - Centralized authentication
    - Request/response logging
    - Future AI feature injection
    - Consistent platform architecture

    Usage:
    POST /api/saleor/graphql
    Content-Type: application/json

    Body: Standard GraphQL query/mutation
    {
      "query": "{ products { edges { node { name } } } }",
      "variables": {}
    }
    """
    try:
        # Get the request body
        body = await request.body()

        # Prepare headers to forward
        headers = {
            "Content-Type": "application/json",
        }

        # Forward authorization header if present
        if auth_header := request.headers.get("Authorization"):
            headers["Authorization"] = auth_header

        # Forward Saleor-specific headers
        if channel_header := request.headers.get("Saleor-Channel"):
            headers["Saleor-Channel"] = channel_header

        if locale_header := request.headers.get("Saleor-Locale"):
            headers["Saleor-Locale"] = locale_header

        # Log the request (optional - can be disabled in production)
        logger.info(f"Proxying GraphQL request to Saleor: {len(body)} bytes")

        # Make request to Saleor backend
        async with httpx.AsyncClient(timeout=SALEOR_TIMEOUT) as client:
            response = await client.post(
                SALEOR_API_URL,
                content=body,
                headers=headers
            )

        # Log response status
        logger.info(f"Saleor GraphQL response: {response.status_code}")

        # Return the response
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers={
                "Content-Type": "application/json",
                # Add CORS headers if needed
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization, Saleor-Channel, Saleor-Locale",
            }
        )

    except httpx.TimeoutException:
        logger.error("Saleor GraphQL request timed out")
        raise HTTPException(
            status_code=504,
            detail="Saleor backend request timed out"
        )

    except httpx.RequestError as e:
        logger.error(f"Error connecting to Saleor backend: {str(e)}")
        raise HTTPException(
            status_code=502,
            detail=f"Error connecting to Saleor backend: {str(e)}"
        )

    except Exception as e:
        logger.error(f"Unexpected error in Saleor proxy: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal proxy error: {str(e)}"
        )


@router.options("/graphql")
async def graphql_options():
    """
    Handle CORS preflight requests for GraphQL endpoint
    """
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, Saleor-Channel, Saleor-Locale",
            "Access-Control-Max-Age": "3600",
        }
    )


@router.get("/health")
async def saleor_proxy_health():
    """
    Health check for Saleor proxy
    Verifies connectivity to Saleor backend
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Simple introspection query to check if Saleor is responding
            response = await client.post(
                SALEOR_API_URL,
                json={
                    "query": "{ __schema { queryType { name } } }"
                },
                headers={"Content-Type": "application/json"}
            )

        if response.status_code == 200:
            return {
                "status": "healthy",
                "service": "saleor-proxy",
                "saleor_backend": SALEOR_API_URL,
                "saleor_status": "connected",
                "response_time_ms": int(response.elapsed.total_seconds() * 1000)
            }
        else:
            return JSONResponse(
                status_code=503,
                content={
                    "status": "unhealthy",
                    "service": "saleor-proxy",
                    "saleor_backend": SALEOR_API_URL,
                    "saleor_status": "error",
                    "error": f"Saleor returned status {response.status_code}"
                }
            )

    except Exception as e:
        logger.error(f"Saleor health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "saleor-proxy",
                "saleor_backend": SALEOR_API_URL,
                "saleor_status": "unreachable",
                "error": str(e)
            }
        )


@router.post("/media")
async def proxy_media_upload(request: Request):
    """
    Proxy media upload requests to Saleor backend

    Handles file uploads for product images, etc.
    """
    try:
        # Get form data
        form = await request.form()

        # Prepare headers
        headers = {}
        if auth_header := request.headers.get("Authorization"):
            headers["Authorization"] = auth_header

        # Forward to Saleor media endpoint
        saleor_media_url = SALEOR_API_URL.replace("/graphql/", "/media/")

        async with httpx.AsyncClient(timeout=60.0) as client:  # Longer timeout for uploads
            response = await client.post(
                saleor_media_url,
                files=form,
                headers=headers
            )

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers={"Content-Type": response.headers.get("Content-Type", "application/json")}
        )

    except Exception as e:
        logger.error(f"Error proxying media upload: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Media upload error: {str(e)}"
        )


# Future enhancement: AI-powered features
async def inject_ai_recommendations(graphql_response: dict, query: str) -> dict:
    """
    Future: Inject AI-powered recommendations into GraphQL responses

    This can be used to enhance product listings with:
    - AI-generated descriptions
    - Personalized recommendations
    - Dynamic pricing
    - SEO metadata

    Currently a placeholder for Phase 2 implementation.
    """
    # TODO: Implement AI feature injection
    # Example: If query is for products, add AI recommendations
    # if "products" in query:
    #     response["data"]["aiRecommendations"] = get_ai_recommendations()

    return graphql_response
