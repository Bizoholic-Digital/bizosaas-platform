#!/usr/bin/env python3
"""
BizOSaaS Integration Monitoring Service [P5]
Third-Party API Health Monitoring & Automatic Failover System

Monitors 40+ external integrations with 99.9% availability target:
- Payment Gateways (Stripe, PayPal, Razorpay, PayU, CCAvenue)
- Marketing Platforms (Google Ads, Facebook, LinkedIn, TikTok)
- Communication APIs (SMTP, SMS, WhatsApp Business)
- E-commerce APIs (Saleor, Amazon SP-API)
- Analytics (Google Analytics, Facebook Pixel)
- Infrastructure (AWS S3, CloudFlare)
- AI Services (OpenAI, Anthropic, Synthesia, Midjourney)
"""

import asyncio
import logging
import signal
import sys
from contextlib import asynccontextmanager
from typing import Dict, Any

import uvicorn
from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from core.monitor_engine import IntegrationMonitorEngine
from core.failover_controller import FailoverController
from core.alert_manager import AlertManager
from core.dashboard_api import DashboardAPI
from core.websocket_manager import WebSocketManager
from routers import health, integrations, alerts, metrics, configuration
from database.connection import init_database
from config.settings import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('integration_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Global instances
monitor_engine: IntegrationMonitorEngine = None
failover_controller: FailoverController = None
alert_manager: AlertManager = None
dashboard_api: DashboardAPI = None
websocket_manager: WebSocketManager = None
background_tasks: set = set()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global monitor_engine, failover_controller, alert_manager, dashboard_api, websocket_manager
    
    logger.info("🚀 Starting BizOSaaS Integration Monitoring Service")
    
    try:
        # Initialize database
        await init_database()
        logger.info("✅ Database initialized")
        
        # Initialize core components
        websocket_manager = WebSocketManager()
        alert_manager = AlertManager(websocket_manager)
        failover_controller = FailoverController(alert_manager)
        dashboard_api = DashboardAPI()
        monitor_engine = IntegrationMonitorEngine(
            failover_controller=failover_controller,
            alert_manager=alert_manager,
            websocket_manager=websocket_manager
        )
        
        # Start monitoring engine
        monitoring_task = asyncio.create_task(monitor_engine.start_monitoring())
        background_tasks.add(monitoring_task)
        monitoring_task.add_done_callback(background_tasks.discard)
        
        logger.info("✅ Integration monitoring started")
        logger.info(f"📊 Dashboard available at: http://localhost:{settings.SERVICE_PORT}/dashboard")
        logger.info(f"🔗 API docs available at: http://localhost:{settings.SERVICE_PORT}/docs")
        
        # Store instances for route access
        app.state.monitor_engine = monitor_engine
        app.state.failover_controller = failover_controller
        app.state.alert_manager = alert_manager
        app.state.dashboard_api = dashboard_api
        app.state.websocket_manager = websocket_manager
        
        yield
        
    except Exception as e:
        logger.error(f"❌ Failed to start monitoring service: {e}")
        raise
    finally:
        logger.info("🛑 Shutting down Integration Monitoring Service")
        
        # Cancel background tasks
        for task in background_tasks:
            task.cancel()
        
        # Wait for tasks to complete
        if background_tasks:
            await asyncio.gather(*background_tasks, return_exceptions=True)
        
        # Stop monitoring engine
        if monitor_engine:
            await monitor_engine.stop_monitoring()
        
        logger.info("✅ Integration monitoring stopped gracefully")


# Create FastAPI application
app = FastAPI(
    title="BizOSaaS Integration Monitor",
    description="Third-Party API Health Monitoring & Automatic Failover System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(integrations.router, prefix="/integrations", tags=["Integrations"])
app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])
app.include_router(configuration.router, prefix="/config", tags=["Configuration"])

# Mount static files for dashboard
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with service information"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>BizOSaaS Integration Monitor</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
            .status { display: flex; gap: 20px; margin: 20px 0; }
            .status-card { flex: 1; padding: 20px; border-radius: 8px; text-align: center; color: white; }
            .online { background: #27ae60; }
            .warning { background: #f39c12; }
            .offline { background: #e74c3c; }
            .links { margin: 30px 0; }
            .link { display: inline-block; margin: 10px 15px 10px 0; padding: 12px 24px; background: #3498db; color: white; text-decoration: none; border-radius: 6px; transition: background 0.3s; }
            .link:hover { background: #2980b9; }
            .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }
            .feature { padding: 20px; border: 1px solid #ddd; border-radius: 8px; background: #f9f9f9; }
            .feature h3 { margin-top: 0; color: #2c3e50; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 BizOSaaS Integration Monitor</h1>
            <p>Third-Party API Health Monitoring & Automatic Failover System</p>
            
            <div class="status">
                <div class="status-card online">
                    <h3>✅ ONLINE</h3>
                    <p>Monitoring Active</p>
                </div>
                <div class="status-card online">
                    <h3>🔄 FAILOVER</h3>
                    <p>Ready</p>
                </div>
                <div class="status-card online">
                    <h3>📊 METRICS</h3>
                    <p>Collecting</p>
                </div>
            </div>
            
            <div class="links">
                <a href="/dashboard" class="link">📊 Live Dashboard</a>
                <a href="/docs" class="link">📚 API Documentation</a>
                <a href="/health" class="link">🏥 Health Check</a>
                <a href="/metrics/status" class="link">📈 System Metrics</a>
            </div>
            
            <div class="features">
                <div class="feature">
                    <h3>🎯 40+ Integrations</h3>
                    <p>Payment gateways, marketing platforms, AI services, and more</p>
                </div>
                <div class="feature">
                    <h3>⚡ Real-time Monitoring</h3>
                    <p>Sub-second health checks with instant failover</p>
                </div>
                <div class="feature">
                    <h3>🚨 Smart Alerts</h3>
                    <p>Multi-channel notifications with escalation</p>
                </div>
                <div class="feature">
                    <h3>📊 Analytics</h3>
                    <p>Performance metrics and cost optimization</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Integration monitoring dashboard"""
    with open("templates/dashboard.html", "r") as f:
        return f.read()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await app.state.websocket_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle any incoming messages
            data = await websocket.receive_text()
            # Echo back for now, can be extended for client commands
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        app.state.websocket_manager.disconnect(websocket)


@app.get("/status")
async def service_status():
    """Get service status"""
    try:
        return {
            "service": "integration-monitor",
            "status": "healthy",
            "version": "1.0.0",
            "timestamp": asyncio.get_event_loop().time(),
            "components": {
                "monitor_engine": "active" if app.state.monitor_engine else "inactive",
                "failover_controller": "ready" if app.state.failover_controller else "not_ready",
                "alert_manager": "ready" if app.state.alert_manager else "not_ready",
                "websocket_manager": "ready" if app.state.websocket_manager else "not_ready"
            }
        }
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "service": "integration-monitor",
                "status": "unhealthy",
                "error": str(e)
            }
        )


def handle_shutdown(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}, shutting down...")
    sys.exit(0)


if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    
    # Start the service
    uvicorn.run(
        "main:app",
        host=settings.SERVICE_HOST,
        port=settings.SERVICE_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )