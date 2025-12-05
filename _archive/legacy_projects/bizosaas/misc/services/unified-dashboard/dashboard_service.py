#!/usr/bin/env python3
"""
Unified Dashboard Service for BizOSaaS Platform
Provides centralized management for all services:
- Business Directory Management
- CRM Integration
- Wagtail CMS Settings
- Saleor E-commerce
- AI Agents Monitoring
"""

from fastapi import FastAPI, HTTPException, Depends, Request, Form, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio
import os
import json
import uuid
import httpx
from dataclasses import dataclass
from pydantic import BaseModel

# Create FastAPI app for unified dashboard
app = FastAPI(
    title="BizOSaaS Unified Dashboard",
    description="Centralized management dashboard for all BizOSaaS platform services",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3003", "http://localhost:5001", "http://localhost:5002", "http://localhost:5003"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates for HTML responses (if needed)
templates = Jinja2Templates(directory="templates")
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# IMPORTANT: Unified Admin now connects ONLY to FastAPI Brain
# All business logic goes through the central brain, not direct to services
BRAIN_API = {
    "url": os.getenv("BRAIN_API_URL", "http://localhost:8001"),
    "version": "2.0.0"
}

# Data Models
class ServiceStatus(BaseModel):
    name: str
    url: str
    status: str = "unknown"
    response_time: float = 0.0
    last_check: datetime = None

class BusinessListingSummary(BaseModel):
    business_id: str
    name: str
    category: str
    status: str
    premium_status: str
    client_id: str
    created_at: str

class TenantSummary(BaseModel):
    tenant_id: str
    name: str
    domain: str
    services_enabled: Dict[str, bool]
    active_listings: int = 0
    
# Health Check - Only check FastAPI Brain
@app.get("/health")
async def health_check():
    """Health check for unified admin - connects only to FastAPI Brain"""
    try:
        async with httpx.AsyncClient() as client:
            start_time = datetime.now()
            response = await client.get(f"{BRAIN_API['url']}/health", timeout=5.0)
            response_time = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                brain_data = response.json()
                return {
                    "status": "healthy",
                    "service": "Unified Admin Dashboard",
                    "brain_connection": {
                        "status": "healthy",
                        "response_time": response_time,
                        "brain_version": brain_data.get("version", "unknown")
                    },
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "degraded",
                    "service": "Unified Admin Dashboard", 
                    "brain_connection": {
                        "status": "unhealthy",
                        "error": f"Brain API returned HTTP {response.status_code}"
                    },
                    "timestamp": datetime.now().isoformat()
                }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "Unified Admin Dashboard",
            "brain_connection": {
                "status": "unreachable",
                "error": str(e)
            },
            "timestamp": datetime.now().isoformat()
        }

# All API endpoints now go through FastAPI Brain
@app.get("/api/business-directory/categories")
async def get_directory_categories(host: str = Header(default="localhost")):
    """Get available business categories through FastAPI Brain"""
    try:
        async with httpx.AsyncClient() as client:
            # Pass domain to brain for tenant resolution
            response = await client.get(
                f"{BRAIN_API['url']}/api/directory/categories",
                headers={"Host": host}
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch categories from brain")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"FastAPI Brain unavailable: {str(e)}")

@app.get("/api/business-directory/platforms")
async def get_directory_platforms():
    """Get available listing platforms from directory service"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{SERVICES['business_directory']}/api/platforms")
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch platforms")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Business directory service unavailable: {str(e)}")

@app.get("/api/business-directory/listings/{client_id}")
async def get_client_listings(client_id: str):
    """Get business listings for a specific client"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{SERVICES['business_directory']}/api/client/{client_id}/listings")
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch client listings")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Business directory service unavailable: {str(e)}")

@app.post("/api/business-directory/listings/{client_id}")
async def create_business_listing(client_id: str, listing_data: dict):
    """Create a new business listing for a client through the directory service"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['business_directory']}/api/client/{client_id}/listings",
                json=listing_data
            )
            if response.status_code in [200, 201]:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to create listing")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Business directory service unavailable: {str(e)}")

@app.put("/api/business-directory/listings/{client_id}/{business_id}")
async def update_business_listing(client_id: str, business_id: str, listing_data: dict):
    """Update a business listing for a client"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{SERVICES['business_directory']}/api/client/{client_id}/listings/{business_id}",
                json=listing_data
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to update listing")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Business directory service unavailable: {str(e)}")

@app.delete("/api/business-directory/listings/{client_id}/{business_id}")
async def delete_business_listing(client_id: str, business_id: str):
    """Delete a business listing for a client"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{SERVICES['business_directory']}/api/client/{client_id}/listings/{business_id}"
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to delete listing")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Business directory service unavailable: {str(e)}")

@app.get("/api/business-directory/seo-analysis/{client_id}")
async def get_seo_analysis(client_id: str):
    """Get SEO analysis for a client's business listings"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{SERVICES['business_directory']}/api/client/{client_id}/seo-analysis")
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch SEO analysis")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Business directory service unavailable: {str(e)}")

# Wagtail CMS Integration
@app.get("/api/cms/tenants")
async def get_cms_tenants():
    """Get all CMS tenants from Wagtail"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{SERVICES['wagtail_cms']}/api/tenants/")
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch tenants")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Wagtail CMS service unavailable: {str(e)}")

@app.get("/api/cms/tenants/{tenant_id}/branding")
async def get_tenant_branding(tenant_id: str):
    """Get branding settings for a tenant"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{SERVICES['wagtail_cms']}/api/tenants/{tenant_id}/branding/")
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch tenant branding")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Wagtail CMS service unavailable: {str(e)}")

@app.put("/api/cms/tenants/{tenant_id}/branding")
async def update_tenant_branding(tenant_id: str, branding_data: dict):
    """Update branding settings for a tenant"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{SERVICES['wagtail_cms']}/api/tenants/{tenant_id}/branding/update/",
                json=branding_data
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to update tenant branding")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Wagtail CMS service unavailable: {str(e)}")

# Saleor E-commerce Integration
@app.get("/api/ecommerce/products")
async def get_ecommerce_products():
    """Get products from Saleor API"""
    try:
        # GraphQL query for products
        query = """
        query GetProducts {
          products(first: 20) {
            edges {
              node {
                id
                name
                description
                pricing {
                  priceRange {
                    start {
                      gross {
                        amount
                        currency
                      }
                    }
                  }
                }
              }
            }
          }
        }
        """
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['saleor_api']}/graphql/",
                json={"query": query}
            )
            if response.status_code == 200:
                data = response.json()
                products = []
                for edge in data.get("data", {}).get("products", {}).get("edges", []):
                    node = edge["node"]
                    products.append({
                        "id": node["id"],
                        "name": node["name"],
                        "description": node.get("description", ""),
                        "price": node["pricing"]["priceRange"]["start"]["gross"]["amount"]
                    })
                return {"products": products}
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch products")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Saleor API service unavailable: {str(e)}")

# Dashboard Overview
@app.get("/api/dashboard/overview")
async def dashboard_overview():
    """Get comprehensive dashboard overview"""
    overview = {
        "timestamp": datetime.now().isoformat(),
        "services_status": {},
        "business_directory": {"total_listings": 0, "active_listings": 0},
        "cms": {"total_tenants": 0, "active_sites": 0},
        "ecommerce": {"total_products": 0, "active_products": 0},
        "recent_activity": []
    }
    
    # Check services health
    health_data = await health_check()
    overview["services_status"] = health_data["services"]
    
    # Get business directory stats
    try:
        directory_data = await get_all_business_listings()
        overview["business_directory"]["total_listings"] = directory_data["count"]
        # Count active listings
        active_count = sum(1 for listing in directory_data["listings"] if listing.get("verification_status") == "verified")
        overview["business_directory"]["active_listings"] = active_count
    except Exception as e:
        overview["business_directory"]["error"] = str(e)
    
    # Get CMS stats  
    try:
        cms_data = await get_cms_tenants()
        overview["cms"]["total_tenants"] = cms_data.get("count", 0)
    except Exception as e:
        overview["cms"]["error"] = str(e)
    
    # Get e-commerce stats
    try:
        products_data = await get_ecommerce_products()
        overview["ecommerce"]["total_products"] = len(products_data.get("products", []))
        overview["ecommerce"]["active_products"] = len(products_data.get("products", []))
    except Exception as e:
        overview["ecommerce"]["error"] = str(e)
    
    return overview

# Multi-tenant client management
@app.get("/api/clients")
async def get_all_clients():
    """Get all clients across all services with their associated resources"""
    clients_data = {}
    
    # Get directory listings grouped by client
    try:
        directory_data = await get_all_business_listings()
        for listing in directory_data["listings"]:
            client_id = listing.get("client_id")
            if client_id:
                if client_id not in clients_data:
                    clients_data[client_id] = {
                        "client_id": client_id,
                        "business_listings": [],
                        "cms_sites": [],
                        "ecommerce_enabled": False
                    }
                clients_data[client_id]["business_listings"].append({
                    "business_id": listing.get("business_id"),
                    "name": listing.get("name"),
                    "status": listing.get("verification_status")
                })
    except Exception as e:
        pass  # Continue even if directory service is down
    
    # Get CMS tenants
    try:
        cms_data = await get_cms_tenants()
        for tenant in cms_data.get("tenants", []):
            client_id = tenant.get("id")  # Using tenant ID as client ID
            if client_id not in clients_data:
                clients_data[client_id] = {
                    "client_id": client_id,
                    "business_listings": [],
                    "cms_sites": [],
                    "ecommerce_enabled": False
                }
            clients_data[client_id]["cms_sites"].append({
                "site_name": tenant.get("name"),
                "domain": tenant.get("domain")
            })
    except Exception as e:
        pass  # Continue even if CMS service is down
    
    return {"clients": list(clients_data.values()), "count": len(clients_data)}

@app.get("/api/clients/{client_id}/summary")
async def get_client_summary(client_id: str):
    """Get comprehensive summary for a specific client"""
    summary = {
        "client_id": client_id,
        "business_listings": [],
        "cms_sites": [],
        "ecommerce_products": [],
        "services_enabled": {
            "directory": False,
            "cms": False,
            "ecommerce": False
        }
    }
    
    # Get client's business listings
    try:
        listings = await get_client_listings(client_id)
        summary["business_listings"] = listings.get("businesses", [])
        summary["services_enabled"]["directory"] = len(listings.get("businesses", [])) > 0
    except Exception as e:
        summary["directory_error"] = str(e)
    
    # Get client's CMS branding
    try:
        branding = await get_tenant_branding(client_id)
        if "branding" in branding:
            summary["cms_branding"] = branding["branding"]
            summary["services_enabled"]["cms"] = True
    except Exception as e:
        summary["cms_error"] = str(e)
    
    return summary

# HTML Dashboard (optional - for testing)
@app.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request):
    """Simple HTML dashboard for testing"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>BizOSaaS Unified Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .services { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 30px; }
            .service { padding: 20px; border: 1px solid #ddd; border-radius: 6px; background: #fafafa; }
            .status-healthy { border-left: 4px solid #4CAF50; }
            .status-unhealthy { border-left: 4px solid #f44336; }
            .status-unreachable { border-left: 4px solid #ff9800; }
            h1 { color: #333; margin-bottom: 10px; }
            h2 { color: #555; margin-bottom: 15px; }
            .api-link { display: inline-block; margin: 5px 10px 5px 0; padding: 8px 16px; background: #2196F3; color: white; text-decoration: none; border-radius: 4px; font-size: 14px; }
            .api-link:hover { background: #1976D2; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 BizOSaaS Unified Dashboard</h1>
            <p>Centralized management for all platform services</p>
            
            <h2>🔗 API Endpoints</h2>
            <div>
                <a href="/docs" class="api-link">📖 API Documentation</a>
                <a href="/api/dashboard/overview" class="api-link">📊 Dashboard Overview</a>
                <a href="/api/business-directory/listings" class="api-link">🏢 Business Listings</a>
                <a href="/api/cms/tenants" class="api-link">🎨 CMS Tenants</a>
                <a href="/api/clients" class="api-link">👥 All Clients</a>
                <a href="/health" class="api-link">❤️ Health Check</a>
            </div>
            
            <h2>📋 Integrated Services</h2>
            <div class="services">
                <div class="service">
                    <h3>🏢 Business Directory</h3>
                    <p>Port 4001 - Professional directory management</p>
                    <a href="http://localhost:4001/docs" class="api-link">API Docs</a>
                </div>
                <div class="service">
                    <h3>🎨 Wagtail CMS</h3>
                    <p>Port 4000 (API) / 5000 (Admin) - Content management</p>
                    <a href="http://localhost:5000" class="api-link">Admin</a>
                </div>
                <div class="service">
                    <h3>🛒 Saleor E-commerce</h3>
                    <p>Port 4003 (API) / 5003 (Dashboard) - Online store</p>
                    <a href="http://localhost:5003" class="api-link">Dashboard</a>
                </div>
                <div class="service">
                    <h3>📊 Django CRM</h3>
                    <p>Port 4004 - Customer relationship management</p>
                    <a href="#" class="api-link">Coming Soon</a>
                </div>
            </div>
            
            <p style="margin-top: 40px; color: #666; font-size: 14px;">
                💡 Use the API endpoints above to integrate with your applications.
            </p>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5004, reload=True)