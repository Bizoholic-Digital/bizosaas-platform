#!/usr/bin/env python3
"""
Superset Analytics Dashboard Proxy Service
Routes analytics dashboard requests to Superset container and provides API integration
"""

import os
import asyncio
import logging
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import httpx
from typing import Optional, Dict, Any
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Superset container configuration
SUPERSET_CONTAINER_URL = "http://localhost:8088"  # Default Superset port
SUPERSET_CONTAINER_ID = "398c12ce95b2"  # Superset container ID

app = FastAPI(
    title="Superset Analytics Dashboard Proxy",
    description="Analytics Dashboard proxy service routing to Apache Superset",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if Superset is accessible
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{SUPERSET_CONTAINER_URL}/health", timeout=5.0)
            superset_healthy = response.status_code == 200
    except Exception as e:
        logger.warning(f"Superset health check failed: {e}")
        superset_healthy = False
    
    return {
        "status": "healthy",
        "service": "superset-analytics-proxy",
        "port": 3009,
        "superset_connection": "healthy" if superset_healthy else "disconnected",
        "superset_url": SUPERSET_CONTAINER_URL
    }

@app.get("/")
async def analytics_dashboard():
    """Main analytics dashboard page"""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Analytics Dashboard - BizOSaaS</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50">
        <div class="min-h-screen">
            <header class="bg-white shadow-sm border-b">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="flex justify-between items-center py-4">
                        <h1 class="text-2xl font-bold text-gray-900">Analytics Dashboard</h1>
                        <div class="text-sm text-gray-500">Powered by Apache Superset</div>
                    </div>
                </div>
            </header>
            <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div class="bg-white rounded-lg shadow p-6 mb-6">
                    <h2 class="text-xl font-semibold text-gray-900 mb-4">Business Intelligence Dashboard</h2>
                    <p class="text-gray-600 mb-4">Access your comprehensive analytics and campaign performance data.</p>
                    <div class="flex space-x-4">
                        <a href="/admin" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                            Access Analytics Dashboard →
                        </a>
                        <a href="/api/analytics/dashboard" class="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors">
                            API Dashboard Data →
                        </a>
                    </div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="bg-white rounded-lg shadow p-6">
                        <h3 class="text-lg font-medium text-gray-900 mb-2">Campaign Performance</h3>
                        <p class="text-gray-600">Real-time campaign metrics and ROI analysis</p>
                    </div>
                    <div class="bg-white rounded-lg shadow p-6">
                        <h3 class="text-lg font-medium text-gray-900 mb-2">Lead Analytics</h3>
                        <p class="text-gray-600">Lead generation and conversion tracking</p>
                    </div>
                    <div class="bg-white rounded-lg shadow p-6">
                        <h3 class="text-lg font-medium text-gray-900 mb-2">Revenue Insights</h3>
                        <p class="text-gray-600">Revenue tracking and forecasting</p>
                    </div>
                </div>
            </main>
        </div>
    </body>
    </html>
    """)

@app.get("/admin")
@app.get("/admin/{path:path}")
async def proxy_to_superset_admin(request: Request, path: str = ""):
    """Proxy admin requests to Superset dashboard"""
    try:
        # Forward request to Superset
        async with httpx.AsyncClient() as client:
            superset_url = f"{SUPERSET_CONTAINER_URL}/superset/dashboard/list/"
            
            # Forward headers
            headers = dict(request.headers)
            headers.pop('host', None)  # Remove host header to avoid conflicts
            
            response = await client.get(
                superset_url,
                headers=headers,
                timeout=30.0
            )
            
            # Return the Superset response
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
            
    except Exception as e:
        logger.error(f"Error proxying to Superset: {e}")
        return HTMLResponse(
            content=f"""
            <div class="p-8">
                <h1>Analytics Dashboard - Connection Error</h1>
                <p>Unable to connect to Superset analytics backend.</p>
                <p>Error: {str(e)}</p>
                <p>Trying to connect to: {SUPERSET_CONTAINER_URL}</p>
                <a href="/" class="text-blue-600 hover:underline">← Back to Dashboard</a>
            </div>
            """,
            status_code=503
        )

@app.api_route("/api/analytics/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_analytics_api(request: Request, path: str):
    """Proxy analytics API requests to Superset API"""
    try:
        async with httpx.AsyncClient() as client:
            # Forward to Superset API
            superset_url = f"{SUPERSET_CONTAINER_URL}/api/v1/{path}"
            
            # Get request body if present
            body = await request.body() if request.method in ["POST", "PUT"] else None
            
            # Forward headers
            headers = dict(request.headers)
            headers.pop('host', None)
            
            response = await client.request(
                method=request.method,
                url=superset_url,
                headers=headers,
                content=body,
                params=request.query_params,
                timeout=30.0
            )
            
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.headers.get("content-type", "application/json")
            )
            
    except Exception as e:
        logger.error(f"Error proxying analytics API: {e}")
        return JSONResponse(
            content={
                "error": "Analytics API connection failed",
                "details": str(e),
                "superset_url": SUPERSET_CONTAINER_URL
            },
            status_code=503
        )

@app.get("/api/analytics/dashboard")
async def get_dashboard_data():
    """Get consolidated dashboard data for frontend integration"""
    try:
        # Mock dashboard data that would normally come from Superset API
        dashboard_data = {
            "overview": {
                "total_campaigns": 24,
                "active_campaigns": 8,
                "total_leads": 1247,
                "conversion_rate": 24.5,
                "total_revenue": 89650,
                "roi": 340.2
            },
            "campaign_performance": [
                {
                    "campaign_id": "camp_001",
                    "name": "Google Ads - Q4 2024",
                    "channel": "google_ads",
                    "status": "active",
                    "spend": 5420,
                    "leads": 142,
                    "conversions": 34,
                    "revenue": 12890,
                    "roi": 237.6
                },
                {
                    "campaign_id": "camp_002", 
                    "name": "Facebook Marketing",
                    "channel": "facebook_ads",
                    "status": "active",
                    "spend": 3200,
                    "leads": 89,
                    "conversions": 23,
                    "revenue": 8760,
                    "roi": 273.8
                }
            ],
            "channel_performance": {
                "google_ads": {"leads": 142, "spend": 5420, "revenue": 12890},
                "facebook_ads": {"leads": 89, "spend": 3200, "revenue": 8760},
                "linkedin_ads": {"leads": 45, "spend": 2100, "revenue": 4500},
                "email_marketing": {"leads": 78, "spend": 800, "revenue": 3200}
            },
            "recent_activity": [
                {
                    "timestamp": "2024-09-23T15:30:00Z",
                    "type": "conversion",
                    "campaign": "Google Ads - Q4 2024",
                    "value": 425,
                    "description": "New lead converted to customer"
                }
            ],
            "last_updated": "2024-09-23T15:47:00Z"
        }
        
        return JSONResponse(content=dashboard_data)
        
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        return JSONResponse(
            content={"error": "Failed to fetch dashboard data", "details": str(e)},
            status_code=500
        )

if __name__ == "__main__":
    logger.info("Starting Superset Analytics Dashboard Proxy on port 3009")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=3009,
        log_level="info"
    )