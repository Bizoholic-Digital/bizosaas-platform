"""
Amazon Sourcing Workflow Service - Main Application
Comprehensive Temporal-based product sourcing integrated with BizOSaaS platform
"""

import asyncio
import logging
import os
import sys
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

# Add path for shared modules
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas')

# Import our modules
from amazon_sourcing_api import router as amazon_sourcing_router
from dashboard_integration import (
    get_dashboard_manager, 
    DashboardManager, 
    DASHBOARD_HTML_TEMPLATE
)
from amazon_sourcing_workflow import get_amazon_sourcing_manager
from temporal_client import get_temporal_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Application lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown"""
    
    logger.info("🚀 Starting Amazon Sourcing Workflow Service")
    
    try:
        # Initialize Temporal client
        temporal_client = await get_temporal_client()
        await temporal_client.initialize()
        logger.info("✅ Temporal client initialized")
        
        # Initialize workflow manager
        workflow_manager = await get_amazon_sourcing_manager()
        logger.info("✅ Workflow manager initialized")
        
        # Initialize dashboard manager
        dashboard_manager = await get_dashboard_manager()
        logger.info("✅ Dashboard manager initialized")
        
        # Store in app state
        app.state.temporal_client = temporal_client
        app.state.workflow_manager = workflow_manager
        app.state.dashboard_manager = dashboard_manager
        
        logger.info("🎉 Amazon Sourcing Workflow Service started successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to start service: {e}")
        raise
    
    yield
    
    logger.info("🔄 Shutting down Amazon Sourcing Workflow Service")
    
    try:
        # Cleanup resources
        if hasattr(app.state, 'temporal_client'):
            # Close temporal client if needed
            pass
        
        logger.info("✅ Service shutdown completed")
        
    except Exception as e:
        logger.error(f"❌ Error during shutdown: {e}")

# Create FastAPI application
app = FastAPI(
    title="Amazon Sourcing Workflow Service",
    description="Comprehensive Amazon product sourcing using Temporal workflows",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(amazon_sourcing_router, prefix="/api")

# Dashboard routes
@app.get("/", response_class=HTMLResponse)
async def dashboard_home():
    """Main dashboard page"""
    return HTMLResponse(DASHBOARD_HTML_TEMPLATE)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page():
    """Dashboard page"""
    return HTMLResponse(DASHBOARD_HTML_TEMPLATE)

@app.get("/api/dashboard-data")
async def get_dashboard_data(dashboard_manager: DashboardManager = Depends(get_dashboard_manager)):
    """Get comprehensive dashboard data"""
    try:
        data = await dashboard_manager.get_dashboard_data()
        return JSONResponse(data)
    except Exception as e:
        logger.error(f"Failed to get dashboard data: {e}")
        return JSONResponse(
            {"error": "Failed to get dashboard data"}, 
            status_code=500
        )

@app.get("/api/dashboard/workflow/{workflow_id}")
async def get_workflow_details(
    workflow_id: str,
    dashboard_manager: DashboardManager = Depends(get_dashboard_manager)
):
    """Get detailed workflow information"""
    try:
        details = await dashboard_manager.get_workflow_details(workflow_id)
        if details is None:
            return JSONResponse(
                {"error": "Workflow not found"}, 
                status_code=404
            )
        return JSONResponse(details)
    except Exception as e:
        logger.error(f"Failed to get workflow details: {e}")
        return JSONResponse(
            {"error": "Failed to get workflow details"}, 
            status_code=500
        )

@app.post("/api/dashboard/workflow/start")
async def start_workflow_from_dashboard(
    request: Request,
    dashboard_manager: DashboardManager = Depends(get_dashboard_manager)
):
    """Start workflow from dashboard"""
    try:
        data = await request.json()
        
        amazon_url = data.get('amazon_url')
        if not amazon_url:
            return JSONResponse(
                {"error": "Amazon URL is required"}, 
                status_code=400
            )
        
        config = data.get('config', {})
        user_info = data.get('user_info', {})
        
        result = await dashboard_manager.start_workflow_from_dashboard(
            amazon_url, config, user_info
        )
        
        return JSONResponse(result)
        
    except Exception as e:
        logger.error(f"Failed to start workflow from dashboard: {e}")
        return JSONResponse(
            {"error": "Failed to start workflow"}, 
            status_code=500
        )

@app.post("/api/dashboard/workflow/{workflow_id}/cancel")
async def cancel_workflow_from_dashboard(
    workflow_id: str,
    request: Request,
    dashboard_manager: DashboardManager = Depends(get_dashboard_manager)
):
    """Cancel workflow from dashboard"""
    try:
        data = await request.json() if request.headers.get('content-type') == 'application/json' else {}
        user_info = data.get('user_info', {})
        
        result = await dashboard_manager.cancel_workflow_from_dashboard(
            workflow_id, user_info
        )
        
        return JSONResponse(result)
        
    except Exception as e:
        logger.error(f"Failed to cancel workflow from dashboard: {e}")
        return JSONResponse(
            {"error": "Failed to cancel workflow"}, 
            status_code=500
        )

# WebSocket endpoint for real-time dashboard updates
@app.websocket("/ws/dashboard")
async def dashboard_websocket(
    websocket: WebSocket,
    dashboard_manager: DashboardManager = Depends(get_dashboard_manager)
):
    """WebSocket endpoint for real-time dashboard updates"""
    client_info = {
        "connected_at": datetime.now(timezone.utc),
        "client_ip": websocket.client.host if websocket.client else "unknown"
    }
    
    await dashboard_manager.websocket_manager.connect(websocket, client_info)
    
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            
            # Handle client messages (ping, requests, etc.)
            try:
                import json
                message = json.loads(data) if data else {}
                
                if message.get('type') == 'ping':
                    await dashboard_manager.websocket_manager.send_personal_message(
                        websocket, 
                        {"type": "pong", "timestamp": datetime.now(timezone.utc).isoformat()}
                    )
                
            except Exception as e:
                logger.warning(f"Failed to handle client message: {e}")
                
    except WebSocketDisconnect:
        logger.info("Dashboard client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        dashboard_manager.websocket_manager.disconnect(websocket)

# Health check endpoints
@app.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "service": "amazon_sourcing_workflow",
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0"
    }

@app.get("/health/detailed")
async def detailed_health_check(
    dashboard_manager: DashboardManager = Depends(get_dashboard_manager)
):
    """Detailed health check including all dependencies"""
    try:
        # Check system health
        system_health = await dashboard_manager.get_system_health()
        
        # Get basic metrics
        workflow_manager = await get_amazon_sourcing_manager()
        metrics = await workflow_manager.get_workflow_metrics()
        
        health_data = {
            "service": "amazon_sourcing_workflow",
            "status": system_health["overall"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0",
            "system_health": system_health,
            "metrics": {
                "total_workflows": metrics.get("total_workflows", 0),
                "active_workflows": metrics.get("active_workflows", 0),
                "success_rate": metrics.get("success_rate", 0)
            },
            "websocket_connections": len(dashboard_manager.websocket_manager.active_connections)
        }
        
        return health_data
        
    except Exception as e:
        logger.error(f"Detailed health check failed: {e}")
        return JSONResponse(
            {
                "service": "amazon_sourcing_workflow",
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            },
            status_code=503
        )

# Metrics endpoint for monitoring
@app.get("/metrics")
async def get_metrics():
    """Prometheus-style metrics endpoint"""
    try:
        workflow_manager = await get_amazon_sourcing_manager()
        dashboard_manager = await get_dashboard_manager()
        
        metrics = await workflow_manager.get_workflow_metrics()
        system_metrics = await dashboard_manager.get_performance_statistics()
        
        # Format as Prometheus metrics
        prometheus_metrics = f"""
# HELP amazon_sourcing_workflows_total Total number of workflows
# TYPE amazon_sourcing_workflows_total counter
amazon_sourcing_workflows_total {metrics.get('total_workflows', 0)}

# HELP amazon_sourcing_workflows_active Currently active workflows
# TYPE amazon_sourcing_workflows_active gauge
amazon_sourcing_workflows_active {metrics.get('active_workflows', 0)}

# HELP amazon_sourcing_success_rate Workflow success rate percentage
# TYPE amazon_sourcing_success_rate gauge
amazon_sourcing_success_rate {metrics.get('success_rate', 0)}

# HELP amazon_sourcing_duration_seconds Average workflow duration
# TYPE amazon_sourcing_duration_seconds gauge
amazon_sourcing_duration_seconds {metrics.get('average_duration_seconds', 0)}

# HELP system_cpu_usage_percent CPU usage percentage
# TYPE system_cpu_usage_percent gauge
system_cpu_usage_percent {system_metrics.get('cpu_usage', 0)}

# HELP system_memory_usage_percent Memory usage percentage  
# TYPE system_memory_usage_percent gauge
system_memory_usage_percent {system_metrics.get('memory_usage', 0)}

# HELP websocket_connections_active Active WebSocket connections
# TYPE websocket_connections_active gauge
websocket_connections_active {len(dashboard_manager.websocket_manager.active_connections)}
"""
        
        return Response(
            prometheus_metrics.strip(),
            media_type="text/plain; version=0.0.4"
        )
        
    except Exception as e:
        logger.error(f"Failed to get metrics: {e}")
        return JSONResponse({"error": "Failed to get metrics"}, status_code=500)

# API documentation endpoints
@app.get("/api/schema")
async def get_api_schema():
    """Get OpenAPI schema"""
    return app.openapi()

@app.get("/api/info")
async def get_api_info():
    """Get API information"""
    return {
        "name": "Amazon Sourcing Workflow API",
        "version": "1.0.0",
        "description": "Comprehensive Amazon product sourcing using Temporal workflows",
        "endpoints": {
            "start_workflow": "POST /api/amazon-sourcing/start",
            "get_workflow_status": "GET /api/amazon-sourcing/status/{workflow_id}",
            "list_workflows": "GET /api/amazon-sourcing/workflows",
            "cancel_workflow": "POST /api/amazon-sourcing/cancel/{workflow_id}",
            "batch_start": "POST /api/amazon-sourcing/batch/start",
            "metrics": "GET /api/amazon-sourcing/metrics",
            "health": "GET /api/amazon-sourcing/health"
        },
        "dashboard": {
            "url": "/dashboard",
            "websocket": "/ws/dashboard"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/api/schema"
        }
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        {
            "error": "Not Found",
            "message": f"The requested path {request.url.path} was not found",
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        status_code=404
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        {
            "error": "Internal Server Error",
            "message": "An internal server error occurred",
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        status_code=500
    )

# Main execution
if __name__ == "__main__":
    # Configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    workers = int(os.getenv("WORKERS", "1"))
    
    # Log configuration
    log_level = "debug" if debug else "info"
    
    logger.info(f"Starting Amazon Sourcing Workflow Service on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"Workers: {workers}")
    
    # Development vs Production configuration
    if debug:
        # Development mode - single worker with auto-reload
        uvicorn.run(
            "amazon_sourcing_main:app",
            host=host,
            port=port,
            log_level=log_level,
            reload=True,
            reload_dirs=["./"],
            access_log=True
        )
    else:
        # Production mode - multiple workers
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level=log_level,
            workers=workers,
            access_log=True,
            server_header=False,
            date_header=False
        )