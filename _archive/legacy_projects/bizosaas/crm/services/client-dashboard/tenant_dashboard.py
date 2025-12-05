"""
Tenant-Aware Client Dashboard Service
IMPORTANT: This demonstrates how client dashboards interact with the FastAPI Brain
All business logic is handled by the brain - this is purely a UI/presentation layer
"""

import os
import httpx
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, Dict, Any
import asyncio

app = FastAPI(
    title="BizOSaaS Client Dashboard",
    description="Tenant-aware client dashboards connected to FastAPI Brain",
    version="2.0.0"
)

# Configuration
BRAIN_API_URL = os.getenv("BRAIN_API_URL", "http://localhost:8001")
templates = Jinja2Templates(directory="templates")

# ========================================================================================
# BRAIN API CLIENT - All business logic requests go through the brain
# ========================================================================================

class BrainAPIClient:
    """Client for communicating with FastAPI Brain (centralized business logic)"""
    
    def __init__(self, base_url: str = BRAIN_API_URL):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def get_tenant_info(self, domain: str) -> Optional[Dict]:
        """Get tenant information from brain based on domain"""
        try:
            response = await self.client.get(
                f"{self.base_url}/api/tenants/resolve",
                headers={"Host": domain}
            )
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error resolving tenant: {e}")
            return None
    
    async def get_tenant_dashboard_data(self, tenant_id: str) -> Dict:
        """Get comprehensive dashboard data for tenant"""
        try:
            response = await self.client.get(f"{self.base_url}/api/tenant/{tenant_id}/dashboard")
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            print(f"Error getting dashboard data: {e}")
            return {}
    
    async def get_tenant_directory_listings(self, tenant_id: str) -> Dict:
        """Get business directory listings for tenant"""
        try:
            response = await self.client.get(f"{self.base_url}/api/tenant/{tenant_id}/directory/listings")
            return response.json() if response.status_code == 200 else {"listings": [], "count": 0}
        except Exception as e:
            print(f"Error getting directory listings: {e}")
            return {"listings": [], "count": 0}
    
    async def get_tenant_branding(self, tenant_id: str) -> Dict:
        """Get tenant branding/theme settings"""
        try:
            response = await self.client.get(f"{self.base_url}/api/tenant/{tenant_id}/branding")
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            print(f"Error getting branding: {e}")
            return {}

brain_client = BrainAPIClient()

# ========================================================================================
# TENANT RESOLUTION MIDDLEWARE
# ========================================================================================

async def resolve_tenant_from_request(request: Request) -> Optional[Dict]:
    """Resolve tenant from request domain - delegates to brain"""
    host = request.headers.get("host", "").lower()
    return await brain_client.get_tenant_info(host)

# ========================================================================================
# CLIENT DASHBOARD ENDPOINTS
# ========================================================================================

@app.get("/", response_class=HTMLResponse)
async def client_dashboard_home(request: Request):
    """Main client dashboard - tenant-aware"""
    tenant = await resolve_tenant_from_request(request)
    
    if not tenant:
        return HTMLResponse("""
        <html><head><title>Domain Not Configured</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 100px;">
            <h1>🚫 Domain Not Configured</h1>
            <p>This domain is not configured in the BizOSaaS system.</p>
            <p>Please contact your administrator.</p>
        </body></html>
        """, status_code=404)
    
    # Get dashboard data through brain
    dashboard_data = await brain_client.get_tenant_dashboard_data(tenant["tenant_id"])
    branding = await brain_client.get_tenant_branding(tenant["tenant_id"])
    
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{tenant.get('name', 'Client Dashboard')} - Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0; padding: 0;
                background: linear-gradient(135deg, {branding.get('primary_color', '#0066cc')} 0%, {branding.get('secondary_color', '#004499')} 100%);
                color: #333;
            }}
            .header {{ 
                background: rgba(255,255,255,0.95); 
                padding: 1rem 2rem; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .container {{ max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }}
            .dashboard-grid {{ 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                gap: 2rem; 
            }}
            .dashboard-card {{ 
                background: white; 
                padding: 2rem; 
                border-radius: 12px; 
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                transition: transform 0.2s;
            }}
            .dashboard-card:hover {{ transform: translateY(-4px); }}
            .metric {{ font-size: 2.5rem; font-weight: bold; color: {branding.get('primary_color', '#0066cc')}; }}
            .metric-label {{ color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏢 {tenant.get('name', 'Client Dashboard')} Dashboard</h1>
            <p>Domain: <strong>{tenant.get('domain', 'Unknown')}</strong> | Tenant ID: <code>{tenant.get('tenant_id', 'Unknown')}</code></p>
        </div>
        
        <div class="container">
            <div class="dashboard-grid">
                <div class="dashboard-card">
                    <div class="metric">{dashboard_data.get('total_leads', 0)}</div>
                    <div class="metric-label">Total Leads</div>
                </div>
                
                <div class="dashboard-card">
                    <div class="metric">{dashboard_data.get('active_campaigns', 0)}</div>
                    <div class="metric-label">Active Campaigns</div>
                </div>
                
                <div class="dashboard-card">
                    <div class="metric">{dashboard_data.get('directory_listings', 0)}</div>
                    <div class="metric-label">Directory Listings</div>
                </div>
                
                <div class="dashboard-card">
                    <div class="metric">{dashboard_data.get('monthly_revenue', '$0')}</div>
                    <div class="metric-label">Monthly Revenue</div>
                </div>
            </div>
            
            <div style="margin-top: 3rem;">
                <div class="dashboard-card">
                    <h3>🧠 Powered by FastAPI Brain</h3>
                    <p><strong>Architecture:</strong> All business logic centralized in FastAPI Brain</p>
                    <p><strong>Data Source:</strong> Brain aggregates from Wagtail (CMS), PostgreSQL, and other storage layers</p>
                    <p><strong>Domain Resolution:</strong> Brain resolves {tenant.get('domain')} → Tenant {tenant.get('tenant_id')}</p>
                    <p><strong>This Dashboard:</strong> Pure presentation layer - no business logic</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """)

@app.get("/api/tenant/info")
async def get_tenant_info(request: Request):
    """API endpoint to get tenant info - proxies through brain"""
    tenant = await resolve_tenant_from_request(request)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return JSONResponse(tenant)

@app.get("/api/dashboard/data")
async def get_dashboard_data(request: Request):
    """API endpoint to get dashboard data - proxies through brain"""
    tenant = await resolve_tenant_from_request(request)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Get all dashboard data through brain
    data = await brain_client.get_tenant_dashboard_data(tenant["tenant_id"])
    listings = await brain_client.get_tenant_directory_listings(tenant["tenant_id"])
    branding = await brain_client.get_tenant_branding(tenant["tenant_id"])
    
    return JSONResponse({
        "tenant": tenant,
        "dashboard": data,
        "directory": listings,
        "branding": branding,
        "architecture": {
            "business_logic": "FastAPI Brain (port 8001)",
            "storage_layers": ["Wagtail CMS", "PostgreSQL", "Redis"],
            "presentation": "Client Dashboard (this service)"
        }
    })

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    # Test connection to brain
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BRAIN_API_URL}/health", timeout=5.0)
            brain_status = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception:
        brain_status = "unreachable"
    
    return JSONResponse({
        "status": "healthy",
        "service": "Client Dashboard",
        "brain_connection": brain_status,
        "brain_url": BRAIN_API_URL,
        "architecture": "tenant_aware_presentation_layer"
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3002, reload=True)