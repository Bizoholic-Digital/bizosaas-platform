"""
Saleor Storage Layer API
IMPORTANT: This contains NO business logic - only data storage/retrieval
All business logic is handled by FastAPI Brain (port 8001)
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
import json
import asyncio
import httpx

# Create FastAPI app for Saleor storage layer
app = FastAPI(
    title="Saleor Storage Layer",
    description="Storage-only API for e-commerce data (no business logic)",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock database for demonstration (in real implementation, connect to Saleor's PostgreSQL)
MOCK_PRODUCTS = [
    {
        "id": "1",
        "tenant_id": "coreldove",
        "name": "Premium Gaming Laptop",
        "slug": "premium-gaming-laptop",
        "description": "High-performance laptop for gaming and professional work",
        "price": 1299.99,
        "currency": "USD",
        "category": "Electronics",
        "is_published": True,
        "created_at": "2024-01-15T10:00:00Z"
    },
    {
        "id": "2", 
        "tenant_id": "coreldove",
        "name": "Wireless Bluetooth Headphones",
        "slug": "wireless-bluetooth-headphones",
        "description": "Premium noise-cancelling headphones",
        "price": 299.99,
        "currency": "USD", 
        "category": "Audio",
        "is_published": True,
        "created_at": "2024-01-16T14:30:00Z"
    }
]

MOCK_ORDERS = [
    {
        "id": "order_001",
        "tenant_id": "coreldove",
        "customer_email": "customer@example.com",
        "total_amount": 1299.99,
        "currency": "USD",
        "status": "fulfilled",
        "created_at": "2024-01-20T09:15:00Z"
    }
]

# ========================================================================================
# STORAGE LAYER - Data operations only (no business logic)
# ========================================================================================

@app.get("/health")
def health_check():
    """Storage layer health check"""
    return {
        "status": "healthy",
        "service": "Saleor Storage Layer",
        "mode": "storage_only",
        "business_logic": "handled_by_brain",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/products")
def list_products(tenant_id: Optional[str] = None):
    """List products - STORAGE ONLY (no business validation)"""
    products = MOCK_PRODUCTS
    
    if tenant_id:
        products = [p for p in products if p.get("tenant_id") == tenant_id]
    
    return {
        "products": products,
        "count": len(products),
        "storage_mode": True
    }

@app.get("/api/products/{product_id}")
def get_product(product_id: str):
    """Get product by ID - STORAGE ONLY"""
    for product in MOCK_PRODUCTS:
        if product["id"] == product_id:
            return product
    
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/api/products")
def store_product(product_data: Dict[str, Any]):
    """Store product data - STORAGE ONLY (no business validation)"""
    try:
        # Just store the data - no business logic validation
        new_product = {
            "id": str(len(MOCK_PRODUCTS) + 1),
            "tenant_id": product_data.get("tenant_id", "default"),
            "name": product_data.get("name", ""),
            "slug": product_data.get("slug", ""),
            "description": product_data.get("description", ""),
            "price": product_data.get("price", 0.0),
            "currency": product_data.get("currency", "USD"),
            "category": product_data.get("category", ""),
            "is_published": product_data.get("is_published", False),
            "created_at": datetime.now().isoformat()
        }
        
        MOCK_PRODUCTS.append(new_product)
        
        return {
            "success": True,
            "product": new_product,
            "created": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/orders")
def list_orders(tenant_id: Optional[str] = None):
    """List orders - STORAGE ONLY"""
    orders = MOCK_ORDERS
    
    if tenant_id:
        orders = [o for o in orders if o.get("tenant_id") == tenant_id]
    
    return {
        "orders": orders,
        "count": len(orders),
        "storage_mode": True
    }

@app.get("/api/orders/{order_id}")
def get_order(order_id: str):
    """Get order by ID - STORAGE ONLY"""
    for order in MOCK_ORDERS:
        if order["id"] == order_id:
            return order
    
    raise HTTPException(status_code=404, detail="Order not found")

@app.post("/api/orders")
def store_order(order_data: Dict[str, Any]):
    """Store order data - STORAGE ONLY (no business validation)"""
    try:
        # Just store the data - no business logic
        new_order = {
            "id": f"order_{len(MOCK_ORDERS) + 1:03d}",
            "tenant_id": order_data.get("tenant_id", "default"),
            "customer_email": order_data.get("customer_email", ""),
            "total_amount": order_data.get("total_amount", 0.0),
            "currency": order_data.get("currency", "USD"),
            "status": order_data.get("status", "pending"),
            "created_at": datetime.now().isoformat()
        }
        
        MOCK_ORDERS.append(new_order)
        
        return {
            "success": True,
            "order": new_order,
            "created": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/categories")
def list_categories():
    """List product categories - STORAGE ONLY"""
    categories = [
        {"id": "electronics", "name": "Electronics", "slug": "electronics"},
        {"id": "audio", "name": "Audio", "slug": "audio"},
        {"id": "computing", "name": "Computing", "slug": "computing"},
        {"id": "gaming", "name": "Gaming", "slug": "gaming"}
    ]
    
    return {
        "categories": categories,
        "count": len(categories),
        "storage_mode": True
    }

@app.get("/api/inventory/{product_id}")
def get_inventory(product_id: str):
    """Get product inventory - STORAGE ONLY"""
    # Mock inventory data
    inventory = {
        "product_id": product_id,
        "quantity_available": 25,
        "quantity_allocated": 5,
        "warehouse_id": "warehouse_001",
        "last_updated": datetime.now().isoformat()
    }
    
    return inventory

@app.put("/api/inventory/{product_id}")
def update_inventory(product_id: str, inventory_data: Dict[str, Any]):
    """Update inventory - STORAGE ONLY (no business validation)"""
    return {
        "success": True,
        "product_id": product_id,
        "updated_fields": list(inventory_data.keys()),
        "timestamp": datetime.now().isoformat()
    }

# ========================================================================================
# TENANT ISOLATION - Storage level data filtering
# ========================================================================================

@app.get("/api/tenant/{tenant_id}/products")
def get_tenant_products(tenant_id: str):
    """Get products for specific tenant - STORAGE ONLY"""
    tenant_products = [p for p in MOCK_PRODUCTS if p.get("tenant_id") == tenant_id]
    
    return {
        "tenant_id": tenant_id,
        "products": tenant_products,
        "count": len(tenant_products),
        "storage_mode": True
    }

@app.get("/api/tenant/{tenant_id}/orders")
def get_tenant_orders(tenant_id: str):
    """Get orders for specific tenant - STORAGE ONLY"""
    tenant_orders = [o for o in MOCK_ORDERS if o.get("tenant_id") == tenant_id]
    
    return {
        "tenant_id": tenant_id,
        "orders": tenant_orders,
        "count": len(tenant_orders),
        "storage_mode": True
    }

@app.get("/api/tenant/{tenant_id}/analytics")
def get_tenant_analytics(tenant_id: str):
    """Get basic analytics for tenant - STORAGE ONLY"""
    tenant_products = [p for p in MOCK_PRODUCTS if p.get("tenant_id") == tenant_id]
    tenant_orders = [o for o in MOCK_ORDERS if o.get("tenant_id") == tenant_id]
    
    total_revenue = sum(o.get("total_amount", 0) for o in tenant_orders)
    
    return {
        "tenant_id": tenant_id,
        "analytics": {
            "total_products": len(tenant_products),
            "published_products": len([p for p in tenant_products if p.get("is_published")]),
            "total_orders": len(tenant_orders),
            "total_revenue": total_revenue,
            "currency": "USD"
        },
        "storage_mode": True,
        "note": "Raw data only - business logic handled by brain"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4003, reload=True)