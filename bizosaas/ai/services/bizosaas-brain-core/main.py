#!/usr/bin/env python3
"""
BizOSaaS Central Brain - CORE ROUTER ONLY
Lightweight routing and orchestration service

This service ONLY handles:
1. Domain routing & tenant resolution  
2. Authentication & authorization
3. Service orchestration & proxy
4. Business logic coordination
5. Multi-tenant data routing

All other concerns moved to specialized microservices.
"""

from fastapi import FastAPI, HTTPException, Depends, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
import asyncio
import os
import httpx
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple tenant resolution (simplified for core router)
from typing import NamedTuple

class SimpleTenant(NamedTuple):
    id: str
    domain: str
    name: str

def get_simple_tenant(domain: str) -> SimpleTenant:
    """Simple tenant resolution - can be enhanced later"""
    return SimpleTenant(
        id=domain.split('.')[0] if '.' in domain else "default",
        domain=domain,
        name=domain.replace('.', '_')
    )

app = FastAPI(
    title="BizOSaaS Central Brain - Core Router",
    description="Lightweight routing and orchestration service",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================================================================================
# SERVICE REGISTRY - Routes to specialized microservices
# ========================================================================================

SERVICE_REGISTRY = {
    "ai-agents": "http://ai-agent-service:8010",
    "payments": "http://payment-service:8014", 
    "documents": "http://document-service:8015",
    "conversations": "http://conversation-service:8016",
    "vault": "http://vault:8200",  # Official Vault service
    "events": "http://event-service:8018",
    "admin": "http://admin-service:8019",
    "analytics": "http://analytics-service:8013",
    "training": "http://ai-training-service:8020",
    "websocket": "http://websocket-service:8021",
    "wagtail": "http://wagtail-cms:8002",
    "django-crm": "http://django-crm:8000", 
    "saleor": "http://bizosaas-saleor-api-8003:8000"
}

# ========================================================================================
# CORE FUNCTIONS - Tenant Resolution & Routing
# ========================================================================================

def get_current_tenant(request: Request) -> Optional[SimpleTenant]:
    """Resolve tenant from domain/headers"""
    host = request.headers.get("host", "")
    domain = host.split(":")[0]
    return get_simple_tenant(domain)

async def proxy_to_service(service_name: str, path: str, method: str, headers: dict, body: dict = None) -> dict:
    """Proxy request to appropriate microservice"""
    service_url = SERVICE_REGISTRY.get(service_name)
    if not service_url:
        raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=method,
                url=f"{service_url}{path}",
                headers=headers,
                json=body,
                timeout=30.0
            )
            return response.json() if response.headers.get("content-type", "").startswith("application/json") else {"data": response.text}
        except Exception as e:
            logger.error(f"Service proxy error: {e}")
            raise HTTPException(status_code=503, detail=f"Service {service_name} unavailable")

# ========================================================================================
# CORE API ENDPOINTS - Health & Routing
# ========================================================================================

@app.get("/")
async def root():
    return {
        "service": "BizOSaaS Central Brain - Core Router",
        "version": "2.0.0",
        "status": "active",
        "architecture": "microservices",
        "services": len(SERVICE_REGISTRY),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Core health check"""
    return {
        "status": "healthy", 
        "service": "bizosaas-brain-core",
        "timestamp": datetime.now().isoformat(),
        "tenant_registry": "active",
        "services_registered": len(SERVICE_REGISTRY)
    }

@app.get("/services")
async def list_services():
    """List all registered microservices"""
    return {
        "services": SERVICE_REGISTRY,
        "count": len(SERVICE_REGISTRY),
        "timestamp": datetime.now().isoformat()
    }

# ========================================================================================
# SALEOR GRAPHQL ADAPTER - Convert REST to GraphQL
# ========================================================================================

async def saleor_graphql_request(query: str, variables: dict = None) -> dict:
    """Send GraphQL request to Saleor API"""
    saleor_url = "http://bizosaas-saleor-api-8003:8000/graphql/"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                saleor_url,
                json={
                    "query": query,
                    "variables": variables or {}
                },
                headers={"Content-Type": "application/json"},
                timeout=30.0
            )
            return response.json()
        except Exception as e:
            logger.error(f"Saleor GraphQL error: {e}")
            return {"errors": [{"message": str(e)}]}

@app.get("/api/brain/saleor/products")
async def saleor_products(
    request: Request,
    category: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 12
):
    """Get products from Saleor via GraphQL"""
    
    # Build GraphQL query for products
    query = """
    query GetProducts($first: Int, $filter: ProductFilterInput) {
        products(first: $first, filter: $filter) {
            edges {
                node {
                    id
                    name
                    description
                    slug
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
                    thumbnail {
                        url
                    }
                    category {
                        id
                        name
                    }
                    rating
                    variants {
                        id
                        name
                    }
                }
            }
            pageInfo {
                hasNextPage
                hasPreviousPage
            }
            totalCount
        }
    }
    """
    
    # Build variables
    variables = {"first": limit}
    filter_input = {}
    
    if search:
        filter_input["search"] = search
    if category:
        filter_input["categories"] = [category]
    
    if filter_input:
        variables["filter"] = filter_input
    
    # Make GraphQL request
    result = await saleor_graphql_request(query, variables)
    
    if "errors" in result:
        # Return fallback data if Saleor is unavailable
        return {
            "products": [
                {
                    "id": "fallback-1",
                    "name": "Premium Wireless Headphones",
                    "description": "High-quality wireless headphones with noise cancellation.",
                    "pricing": {
                        "priceRange": {
                            "start": {
                                "gross": {"amount": 149.99, "currency": "USD"}
                            }
                        }
                    },
                    "thumbnail": {"url": "/placeholder-product.jpg"},
                    "category": {"name": "Electronics"},
                    "rating": 4.5
                },
                {
                    "id": "fallback-2", 
                    "name": "Organic Cotton T-Shirt",
                    "description": "Comfortable and sustainable organic cotton t-shirt.",
                    "pricing": {
                        "priceRange": {
                            "start": {
                                "gross": {"amount": 29.99, "currency": "USD"}
                            }
                        }
                    },
                    "thumbnail": {"url": "/placeholder-product.jpg"},
                    "category": {"name": "Fashion"},
                    "rating": 4.2
                }
            ],
            "count": 2,
            "totalCount": 2,
            "hasNextPage": False,
            "source": "fallback"
        }
    
    # Transform GraphQL response to REST format
    products_data = result.get("data", {}).get("products", {})
    products = []
    
    for edge in products_data.get("edges", []):
        node = edge["node"]
        products.append({
            "id": node["id"],
            "name": node["name"],
            "description": node.get("description", ""),
            "slug": node.get("slug", ""),
            "pricing": node.get("pricing", {}),
            "thumbnail": node.get("thumbnail", {}),
            "category": node.get("category", {}),
            "rating": node.get("rating", 4.0),
            "variants": node.get("variants", [])
        })
    
    page_info = products_data.get("pageInfo", {})
    
    return {
        "products": products,
        "count": len(products),
        "totalCount": products_data.get("totalCount", 0),
        "hasNextPage": page_info.get("hasNextPage", False),
        "source": "saleor"
    }

@app.get("/api/brain/saleor/categories")
async def saleor_categories(request: Request):
    """Get categories from Saleor via GraphQL"""
    
    query = """
    query GetCategories {
        categories(first: 100) {
            edges {
                node {
                    id
                    name
                    slug
                    description
                    products {
                        totalCount
                    }
                }
            }
        }
    }
    """
    
    result = await saleor_graphql_request(query)
    
    if "errors" in result:
        return {
            "categories": [
                {"id": "fallback-1", "name": "Electronics", "slug": "electronics", "productCount": 25},
                {"id": "fallback-2", "name": "Fashion", "slug": "fashion", "productCount": 18},
                {"id": "fallback-3", "name": "Home & Garden", "slug": "home-garden", "productCount": 12}
            ],
            "source": "fallback"
        }
    
    categories_data = result.get("data", {}).get("categories", {})
    categories = []
    
    for edge in categories_data.get("edges", []):
        node = edge["node"]
        categories.append({
            "id": node["id"],
            "name": node["name"],
            "slug": node.get("slug", ""),
            "description": node.get("description", ""),
            "productCount": node.get("products", {}).get("totalCount", 0)
        })
    
    return {
        "categories": categories,
        "source": "saleor"
    }

# ========================================================================================
# ROUTING ENDPOINTS - Proxy to Microservices  
# ========================================================================================

@app.api_route("/api/brain/{service_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def route_to_service(service_name: str, path: str, request: Request):
    """Route all service requests to appropriate microservices"""
    
    # Skip Saleor routes - handled by specific endpoints above
    if service_name == "saleor" and path in ["products", "categories"]:
        raise HTTPException(status_code=404, detail="Use specific Saleor endpoints")
    
    # Get tenant context
    tenant = get_current_tenant(request)
    tenant_id = tenant.id if tenant else "default"
    
    # Prepare headers with tenant context
    headers = dict(request.headers)
    headers["x-tenant-id"] = tenant_id
    
    # Get request body if present
    body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.json()
        except:
            body = {}
    
    # Add tenant context to body
    if body:
        body["tenant_id"] = tenant_id
    
    # Proxy to appropriate service
    return await proxy_to_service(service_name, f"/{path}", request.method, headers, body)

# ========================================================================================
# LEGACY COMPATIBILITY - Direct endpoints for existing integrations
# ========================================================================================

@app.get("/api/dashboard")
async def dashboard_proxy(request: Request):
    """Proxy dashboard requests to admin service"""
    return await proxy_to_service("admin", "/dashboard", "GET", dict(request.headers))

@app.get("/api/directory/categories")
async def directory_categories_proxy(request: Request):
    """Proxy directory requests to business directory service"""
    return await proxy_to_service("admin", "/directory/categories", "GET", dict(request.headers))

# ========================================================================================
# STARTUP
# ========================================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)