#!/usr/bin/env python3
"""
Unified Dashboard Service - Connected ONLY to FastAPI Brain
This dashboard service acts as a proxy/interface to the FastAPI Brain
ALL business logic and data flows through the central brain
"""

from fastapi import FastAPI, HTTPException, Depends, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
import json
import httpx
from pydantic import BaseModel

# Create FastAPI app for unified dashboard
app = FastAPI(
    title="BizOSaaS Unified Admin Dashboard",
    description="Administrative interface connected to FastAPI Brain",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates for HTML responses
templates = Jinja2Templates(directory="templates")
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# CRITICAL: Only connect to FastAPI Brain
BRAIN_API = {
    "url": os.getenv("BRAIN_API_URL", "http://localhost:8001"),
    "version": "2.0.0",
    "timeout": 10.0
}

# ========================================================================================
# HEALTH CHECK - Only check brain connectivity
# ========================================================================================

@app.get("/health")
async def health_check():
    """Health check - only verifies brain connectivity"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BRAIN_API['url']}/health", 
                timeout=BRAIN_API["timeout"]
            )
            
            if response.status_code == 200:
                brain_data = response.json()
                return {
                    "status": "healthy",
                    "service": "Unified Admin Dashboard",
                    "brain_connection": "healthy",
                    "brain_version": brain_data.get("version", "unknown"),
                    "timestamp": datetime.now().isoformat()
                }
    except Exception as e:
        return {
            "status": "unhealthy", 
            "service": "Unified Admin Dashboard",
            "brain_connection": "failed",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# ========================================================================================
# BRAIN PROXY ENDPOINTS - All requests forwarded to brain
# ========================================================================================

@app.get("/api/dashboard/overview")
async def dashboard_overview(host: str = Header(default="localhost")):
    """Get dashboard overview through brain"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BRAIN_API['url']}/api/dashboard",
                headers={"Host": host},
                timeout=BRAIN_API["timeout"]
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Brain API error")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Brain unavailable: {str(e)}")

@app.get("/api/directory/categories")
async def get_directory_categories(host: str = Header(default="localhost")):
    """Get directory categories through brain"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BRAIN_API['url']}/api/directory/categories",
                headers={"Host": host},
                timeout=BRAIN_API["timeout"]
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Brain API error")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Brain unavailable: {str(e)}")

@app.get("/api/directory/clients/{client_id}/listings")
async def get_client_listings(client_id: str, host: str = Header(default="localhost")):
    """Get client business listings through brain"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BRAIN_API['url']}/api/directory/clients/{client_id}/listings",
                headers={"Host": host},
                timeout=BRAIN_API["timeout"]
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Brain API error")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Brain unavailable: {str(e)}")

@app.post("/api/directory/clients/{client_id}/listings")
async def create_client_listing(client_id: str, listing_data: dict, host: str = Header(default="localhost")):
    """Create business listing through brain"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BRAIN_API['url']}/api/directory/clients/{client_id}/listings",
                json=listing_data,
                headers={"Host": host},
                timeout=BRAIN_API["timeout"]
            )
            if response.status_code in [200, 201]:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Brain API error")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Brain unavailable: {str(e)}")

@app.get("/api/cms/branding")
async def get_tenant_branding(host: str = Header(default="localhost")):
    """Get tenant branding through brain"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BRAIN_API['url']}/api/cms/branding",
                headers={"Host": host},
                timeout=BRAIN_API["timeout"]
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Brain API error")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Brain unavailable: {str(e)}")

@app.put("/api/cms/branding")
async def update_tenant_branding(branding_data: dict, host: str = Header(default="localhost")):
    """Update tenant branding through brain"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(
                f"{BRAIN_API['url']}/api/cms/branding",
                json=branding_data,
                headers={"Host": host},
                timeout=BRAIN_API["timeout"]
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Brain API error")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Brain unavailable: {str(e)}")

@app.get("/api/ecommerce/products")
async def get_ecommerce_products(host: str = Header(default="localhost")):
    """Get e-commerce products through brain"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BRAIN_API['url']}/api/ecommerce/products",
                headers={"Host": host},
                timeout=BRAIN_API["timeout"]
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Brain API error")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Brain unavailable: {str(e)}")

@app.get("/api/clients")
async def get_clients(host: str = Header(default="localhost")):
    """Get tenant clients through brain"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BRAIN_API['url']}/api/clients",
                headers={"Host": host},
                timeout=BRAIN_API["timeout"]
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Brain API error")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Brain unavailable: {str(e)}")

@app.post("/api/clients")
async def create_client(client_data: dict, host: str = Header(default="localhost")):
    """Create new client through brain"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BRAIN_API['url']}/api/clients",
                json=client_data,
                headers={"Host": host},
                timeout=BRAIN_API["timeout"]
            )
            if response.status_code in [200, 201]:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Brain API error")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Brain unavailable: {str(e)}")

# ========================================================================================
# ADMIN DASHBOARD HTML INTERFACE
# ========================================================================================

@app.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Unified Admin Dashboard Interface"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>BizOSaaS Unified Admin Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            .container { 
                max-width: 1400px; 
                margin: 0 auto; 
                padding: 20px;
            }
            .header {
                background: rgba(255,255,255,0.95);
                padding: 20px;
                border-radius: 12px;
                margin-bottom: 30px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
            }
            .dashboard-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .card {
                background: rgba(255,255,255,0.95);
                padding: 25px;
                border-radius: 12px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .card:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            }
            .card h3 {
                color: #4a5568;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .status-indicator {
                display: inline-block;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #48bb78;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }
            .api-endpoint {
                display: inline-block;
                background: #4299e1;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                text-decoration: none;
                font-size: 14px;
                margin: 5px 5px 5px 0;
                transition: background 0.2s;
            }
            .api-endpoint:hover {
                background: #3182ce;
            }
            .tenant-info {
                background: rgba(72, 187, 120, 0.1);
                border: 1px solid rgba(72, 187, 120, 0.3);
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
            }
            .brain-status {
                background: rgba(66, 153, 225, 0.1);
                border: 1px solid rgba(66, 153, 225, 0.3);
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
            }
            .architecture-note {
                background: rgba(237, 137, 54, 0.1);
                border: 1px solid rgba(237, 137, 54, 0.3);
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠 BizOSaaS Unified Admin Dashboard</h1>
                <p>Centralized administration through FastAPI Brain</p>
                <div class="brain-status">
                    <strong>🔗 Architecture:</strong> All business logic handled by FastAPI Brain (Port 8001)<br>
                    <strong>📊 Data Flow:</strong> Admin Dashboard → FastAPI Brain → Storage Services<br>
                    <strong>🏢 Multi-tenant:</strong> Domain-based tenant resolution active
                </div>
            </div>
            
            <div class="dashboard-grid">
                <div class="card">
                    <h3><span class="status-indicator"></span> Brain Connection</h3>
                    <p>Connected to FastAPI Brain on port 8001</p>
                    <div class="tenant-info">
                        <strong>Current Mode:</strong> Unified Admin<br>
                        <strong>Brain Version:</strong> 2.0.0<br>
                        <strong>Connection:</strong> Active
                    </div>
                    <a href="/health" class="api-endpoint">Health Check</a>
                </div>
                
                <div class="card">
                    <h3>🏢 Business Directory</h3>
                    <p>Manage business listings through brain</p>
                    <a href="/api/directory/categories" class="api-endpoint">Categories</a>
                    <a href="/api/dashboard/overview" class="api-endpoint">Overview</a>
                </div>
                
                <div class="card">
                    <h3>🎨 CMS & Branding</h3>
                    <p>Content management through brain</p>
                    <a href="/api/cms/branding" class="api-endpoint">Get Branding</a>
                    <a href="/brain/docs" class="api-endpoint">Brain API Docs</a>
                </div>
                
                <div class="card">
                    <h3>🛒 E-commerce</h3>
                    <p>Saleor integration through brain</p>
                    <a href="/api/ecommerce/products" class="api-endpoint">Products</a>
                    <a href="/api/clients" class="api-endpoint">Clients</a>
                </div>
            </div>
            
            <div class="architecture-note">
                <strong>🏗️ Architecture Note:</strong> This dashboard connects ONLY to the FastAPI Brain (port 8001). 
                All business logic is centralized in the brain. Backend services (Wagtail, Saleor, Directory) 
                are pure storage layers with no direct business logic access.
            </div>
            
            <div class="card">
                <h3>🔧 Available API Endpoints</h3>
                <p>All endpoints proxy through FastAPI Brain:</p>
                <a href="/api/dashboard/overview" class="api-endpoint">Dashboard Overview</a>
                <a href="/api/directory/categories" class="api-endpoint">Directory Categories</a>
                <a href="/api/cms/branding" class="api-endpoint">CMS Branding</a>
                <a href="/api/ecommerce/products" class="api-endpoint">E-commerce Products</a>
                <a href="/api/clients" class="api-endpoint">Client Management</a>
            </div>
        </div>
        
        <script>
            // Simple status check
            fetch('/health')
                .then(res => res.json())
                .then(data => {
                    console.log('Admin Dashboard Status:', data);
                    if (data.status === 'healthy') {
                        document.querySelector('.status-indicator').style.background = '#48bb78';
                    } else {
                        document.querySelector('.status-indicator').style.background = '#f56565';
                    }
                })
                .catch(err => {
                    console.error('Health check failed:', err);
                    document.querySelector('.status-indicator').style.background = '#f56565';
                });
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5004, reload=True)