from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from app.middleware.auth import get_current_user
from domain.ports.identity_port import AuthenticatedUser
from app.store import active_connectors
from app.connectors.registry import ConnectorRegistry
from app.connectors.base import ConnectorType, ConnectorStatus
from app.connectors.ports.ecommerce_port import ECommercePort

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
                description=p.description,
                price=p.price,
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
                number=o.number,
                status=o.status,
                total=o.total,
                currency=o.currency,
                customer_id=o.customer_id,
                created_at=o.created_at,
                line_items=o.line_items
            ) for o in orders
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"E-commerce Error: {str(e)}")
