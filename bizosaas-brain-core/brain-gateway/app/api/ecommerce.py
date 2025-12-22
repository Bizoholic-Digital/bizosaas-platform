from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from app.middleware.auth import get_current_user
from domain.ports.identity_port import AuthenticatedUser
from app.store import active_connectors
from app.connectors.registry import ConnectorRegistry
from app.connectors.base import ConnectorType, ConnectorStatus
from app.ports.ecommerce_port import ECommercePort

router = APIRouter()

class ProductMessage(BaseModel):
    id: str
    name: str
    description: Optional[str] = ""
    price: str
    sku: Optional[str] = ""
    stock_quantity: Optional[int] = 0
    status: str
    images: List[str] = []

class OrderMessage(BaseModel):
    id: str
    number: str
    status: str
    total: str
    currency: str
    customer_id: int
    created_at: datetime
    line_items: List[Any] = []

async def get_active_ecommerce_connector(tenant_id: str) -> ECommercePort:
    # 1. Get all ECOM connector types
    configs = [c for c in ConnectorRegistry.get_all_configs() if c.type == ConnectorType.ECOMMERCE]
    
    # 2. Check connections
    for config in configs:
        key = f"{tenant_id}:{config.id}"
        if key in active_connectors:
            data = active_connectors[key]
            connector = ConnectorRegistry.create_connector(config.id, tenant_id, data["credentials"])
            return connector
            
    raise HTTPException(status_code=404, detail="No E-commerce connector configured.")

    raise HTTPException(status_code=404, detail="No E-commerce connector configured.")

@router.get("/status")
async def get_ecommerce_status(
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Check connectivity to the active store"""
    tenant_id = user.tenant_id or "default_tenant"
    try:
        connector = await get_active_ecommerce_connector(tenant_id)
        is_valid = await connector.validate_credentials()
        
        return {
            "connected": is_valid,
            "platform": connector.config.name if hasattr(connector, 'config') else "WooCommerce",
            "version": "Unknown" 
        }
    except HTTPException:
        return {"connected": False}
    except Exception as e:
         return {"connected": False, "error": str(e)}

@router.get("/stats")
async def get_ecommerce_stats(
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Get E-commerce statistics"""
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_ecommerce_connector(tenant_id)
    
    try:
        stats = await connector.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats Error: {str(e)}")

@router.get("/products", response_model=List[ProductMessage])
async def list_products(
    user: AuthenticatedUser = Depends(get_current_user)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_ecommerce_connector(tenant_id)
    
    try:
        products = await connector.get_products()
        return [
            ProductMessage(
                id=p.id,
                name=p.name,
                description=p.description or "",
                price=str(p.price),
                sku=p.sku,
                stock_quantity=p.stock_quantity,
                status=p.status,
                images=p.images
            ) for p in products
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"E-commerce Error: {str(e)}")

@router.get("/orders", response_model=List[OrderMessage])
async def list_orders(
    user: AuthenticatedUser = Depends(get_current_user)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_ecommerce_connector(tenant_id)
    
    try:
        orders = await connector.get_orders()
        return [
            OrderMessage(
                id=o.id,
                number=o.id, # Using ID as number for now
                status=o.status,
                total=str(o.total_amount),
                currency=o.currency,
                customer_id=int(o.customer_id) if o.customer_id and o.customer_id.isdigit() else 0,
                created_at=o.created_at or datetime.now(),
                line_items=o.items
            ) for o in orders
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"E-commerce Error: {str(e)}")
