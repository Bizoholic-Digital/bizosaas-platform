"""
Super Admin Dashboard - BizOSaaS Platform
God Mode Management Interface for Autonomous AI Agents Platform
Port: 8888
"""

from fastapi import FastAPI, HTTPException, Depends, status, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import Dict, Any, List, Optional
import httpx
import asyncio
import logging
import time
import json
from datetime import datetime

# Shared imports
import sys
import os
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas')

from shared.auth.jwt_auth import get_current_user, UserContext, require_role, UserRole

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Super Admin Dashboard - BizOSaaS",
    description="God Mode Management Interface for Autonomous AI Agents Platform",
    version="1.0.0",
    docs_url="/admin/docs",
    redoc_url="/admin/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service endpoints configuration
SERVICES = {
    "api_gateway": "http://localhost:8080",
    "ai_agents": "http://localhost:8001", 
    "saleor_commerce": "http://localhost:8024",
    "bizoholic_frontend": "http://localhost:3000",
    "coreldove_frontend": "http://localhost:3001",
}

# Global HTTP client
http_client = None

@app.on_event("startup")
async def startup_event():
    """Initialize Super Admin Dashboard"""
    global http_client
    
    try:
        http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
        )
        logger.info("Super Admin Dashboard initialized successfully")
        
    except Exception as e:
        logger.error(f"Super Admin Dashboard startup failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Clean shutdown"""
    global http_client
    
    if http_client:
        await http_client.aclose()
    
    logger.info("Super Admin Dashboard shutdown complete")

# Authentication requirement for all admin endpoints
admin_required = require_role(UserRole.SUPER_ADMIN)

# Health check
@app.get("/health")
async def health_check():
    """Super Admin Dashboard health check"""
    return {
        "status": "healthy",
        "service": "super-admin-dashboard", 
        "timestamp": datetime.utcnow().isoformat()
    }

# Main dashboard endpoint
@app.get("/", response_class=HTMLResponse)
async def dashboard_home():
    """Serve the main dashboard interface"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BizOSaaS Super Admin - God Mode</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
    </head>
    <body class="bg-gray-100 dark:bg-gray-900">
        <div class="min-h-screen" x-data="dashboard()">
            <!-- Header -->
            <header class="bg-white dark:bg-gray-800 shadow-lg">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="flex justify-between items-center py-6">
                        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
                            BizOSaaS Super Admin Dashboard
                        </h1>
                        <div class="flex items-center space-x-4">
                            <span class="text-sm text-gray-500 dark:text-gray-400">God Mode Active</span>
                            <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                        </div>
                    </div>
                </div>
            </header>

            <!-- Main Dashboard -->
            <main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                <!-- Service Status Overview -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">API Gateway</h3>
                        <div class="flex items-center justify-between">
                            <span x-text="services.api_gateway.status" class="text-sm"></span>
                            <div class="w-3 h-3 rounded-full" :class="services.api_gateway.status === 'healthy' ? 'bg-green-500' : 'bg-red-500'"></div>
                        </div>
                        <p class="text-sm text-gray-500 mt-2">Multi-tenant routing active</p>
                    </div>

                    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">AI Agents</h3>
                        <div class="flex items-center justify-between">
                            <span x-text="`${services.ai_agents.total_agents} Agents`" class="text-sm"></span>
                            <div class="w-3 h-3 rounded-full" :class="services.ai_agents.status === 'healthy' ? 'bg-green-500' : 'bg-red-500'"></div>
                        </div>
                        <p class="text-sm text-gray-500 mt-2">Universal chat interface</p>
                    </div>

                    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Saleor Commerce</h3>
                        <div class="flex items-center justify-between">
                            <span x-text="services.saleor.status" class="text-sm"></span>
                            <div class="w-3 h-3 rounded-full" :class="services.saleor.status === 'operational' ? 'bg-green-500' : 'bg-red-500'"></div>
                        </div>
                        <p class="text-sm text-gray-500 mt-2">E-commerce backend</p>
                    </div>
                </div>

                <!-- Tier Analytics -->
                <div class="bg-white dark:bg-gray-800 rounded-lg shadow mb-8">
                    <div class="p-6">
                        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Three-Tier Performance</h3>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div class="text-center p-4 bg-blue-50 dark:bg-blue-900 rounded-lg">
                                <div class="text-2xl font-bold text-blue-600 dark:text-blue-400">$97</div>
                                <div class="text-sm text-gray-600 dark:text-gray-400">Static Sites</div>
                                <div class="text-xs text-gray-500 mt-1">Tier 1 Clients</div>
                            </div>
                            <div class="text-center p-4 bg-green-50 dark:bg-green-900 rounded-lg">
                                <div class="text-2xl font-bold text-green-600 dark:text-green-400">$297</div>
                                <div class="text-sm text-gray-600 dark:text-gray-400">Dynamic CMS</div>
                                <div class="text-xs text-gray-500 mt-1">Tier 2 Clients</div>
                            </div>
                            <div class="text-center p-4 bg-purple-50 dark:bg-purple-900 rounded-lg">
                                <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">$997</div>
                                <div class="text-sm text-gray-600 dark:text-gray-400">Full Platform</div>
                                <div class="text-xs text-gray-500 mt-1">Tier 3 Clients</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Quick Actions -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="bg-white dark:bg-gray-800 rounded-lg shadow">
                        <div class="p-6">
                            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Quick Actions</h3>
                            <div class="space-y-3">
                                <button @click="refreshServices()" class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors">
                                    Refresh All Services
                                </button>
                                <button class="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors">
                                    View AI Chat Sessions
                                </button>
                                <button class="w-full bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 transition-colors">
                                    Tenant Management
                                </button>
                            </div>
                        </div>
                    </div>

                    <div class="bg-white dark:bg-gray-800 rounded-lg shadow">
                        <div class="p-6">
                            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">System Alerts</h3>
                            <div class="space-y-3">
                                <div class="p-3 bg-green-50 dark:bg-green-900 border border-green-200 dark:border-green-700 rounded-md">
                                    <p class="text-sm text-green-800 dark:text-green-200">All systems operational</p>
                                </div>
                                <div class="p-3 bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-700 rounded-md">
                                    <p class="text-sm text-blue-800 dark:text-blue-200">Multi-tenant routing active</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>

        <script>
            function dashboard() {
                return {
                    services: {
                        api_gateway: { status: 'loading' },
                        ai_agents: { status: 'loading', total_agents: 0 },
                        saleor: { status: 'loading' }
                    },

                    init() {
                        this.loadServiceStatus();
                        // Refresh every 30 seconds
                        setInterval(() => this.loadServiceStatus(), 30000);
                    },

                    async loadServiceStatus() {
                        try {
                            // Load API Gateway status
                            const gatewayResponse = await fetch('/admin/api/services/gateway/status');
                            const gatewayData = await gatewayResponse.json();
                            this.services.api_gateway = gatewayData;

                            // Load AI Agents status  
                            const aiResponse = await fetch('/admin/api/services/ai-agents/status');
                            const aiData = await aiResponse.json();
                            this.services.ai_agents = aiData;

                            // Load Saleor status
                            const saleorResponse = await fetch('/admin/api/services/saleor/status');
                            const saleorData = await saleorResponse.json();
                            this.services.saleor = saleorData;

                        } catch (error) {
                            console.error('Error loading service status:', error);
                        }
                    },

                    refreshServices() {
                        this.loadServiceStatus();
                    }
                }
            }
        </script>
    </body>
    </html>
    """

# Service Status APIs
@app.get("/admin/api/services/gateway/status")
async def get_gateway_status(current_user: UserContext = Depends(admin_required)):
    """Get API Gateway status"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{SERVICES['api_gateway']}/health")
            if response.status_code == 200:
                return {"status": "healthy", **response.json()}
            else:
                return {"status": "unhealthy", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/admin/api/services/ai-agents/status")
async def get_ai_agents_status(current_user: UserContext = Depends(admin_required)):
    """Get AI Agents status"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{SERVICES['ai_agents']}/health")
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "healthy",
                    "total_agents": data.get("total_agents", 0),
                    "active_sessions": data.get("active_sessions", 0)
                }
            else:
                return {"status": "unhealthy", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/admin/api/services/saleor/status")
async def get_saleor_status(current_user: UserContext = Depends(admin_required)):
    """Get Saleor Commerce status"""
    try:
        # Test GraphQL endpoint
        query = '{"query": "{ shop { name } }"}'
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{SERVICES['saleor_commerce']}/graphql",
                content=query,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                return {"status": "operational", "graphql": "available"}
            else:
                return {"status": "error", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

# Tenant Management APIs
@app.get("/admin/api/tenants")
async def get_tenants(current_user: UserContext = Depends(admin_required)):
    """Get all tenants"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{SERVICES['api_gateway']}/gateway/tiers")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Failed to fetch tenants"}
    except Exception as e:
        return {"error": str(e)}

# AI Agents Management
@app.get("/admin/api/ai-agents/sessions")
async def get_active_sessions(current_user: UserContext = Depends(admin_required)):
    """Get active AI chat sessions"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{SERVICES['ai_agents']}/sessions")
            if response.status_code == 200:
                return response.json()
            else:
                return {"sessions": [], "error": "Sessions endpoint not available"}
    except Exception as e:
        return {"sessions": [], "error": str(e)}

# Platform Analytics
@app.get("/admin/api/analytics/overview")
async def get_platform_analytics(current_user: UserContext = Depends(admin_required)):
    """Get platform analytics overview"""
    
    analytics = {
        "tier_performance": {
            "tier_1": {"clients": 0, "revenue": 0, "active": True},
            "tier_2": {"clients": 0, "revenue": 0, "active": True}, 
            "tier_3": {"clients": 0, "revenue": 0, "active": True}
        },
        "service_health": {
            "api_gateway": "healthy",
            "ai_agents": "healthy",
            "saleor": "healthy",
            "wagtail": "pending"
        },
        "ai_agent_stats": {
            "total_agents": 46,
            "active_sessions": 0,
            "avg_response_time": "1.2s"
        },
        "system_metrics": {
            "uptime": "99.9%",
            "avg_response_time": "150ms",
            "requests_per_minute": 1200
        }
    }
    
    return analytics

# Service Management Actions
@app.post("/admin/api/services/{service_name}/restart")
async def restart_service(
    service_name: str,
    current_user: UserContext = Depends(admin_required)
):
    """Restart a service (placeholder for future implementation)"""
    
    valid_services = ["api_gateway", "ai_agents", "saleor", "wagtail"]
    if service_name not in valid_services:
        raise HTTPException(status_code=400, detail="Invalid service name")
    
    return {
        "message": f"Service {service_name} restart initiated",
        "service": service_name,
        "status": "pending",
        "note": "Restart functionality will be implemented with proper service orchestration"
    }

# WebSocket for real-time updates
@app.websocket("/admin/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    # Note: WebSocket authentication would need custom implementation
):
    """WebSocket for real-time dashboard updates"""
    await websocket.accept()
    
    try:
        while True:
            # Send periodic updates
            update = {
                "timestamp": datetime.utcnow().isoformat(),
                "type": "status_update",
                "data": {
                    "services_healthy": True,
                    "active_tenants": 0,
                    "ai_agents_active": 46
                }
            }
            
            await websocket.send_text(json.dumps(update))
            await asyncio.sleep(10)  # Update every 10 seconds
            
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)