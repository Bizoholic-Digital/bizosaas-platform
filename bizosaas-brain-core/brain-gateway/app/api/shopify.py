from fastapi import APIRouter, Request, HTTPException, Depends, Header
from typing import Dict, Any, List
import hmac
import hashlib
import json
import logging
from base64 import b64encode
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_secret_service
from app.domain.services.secret_service import SecretService
from app.models.mcp import MarketplaceProductMap
from app.services.marketplace_service import MarketplaceService
from app.services.inventory_service import InventoryService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/webhooks/shopify", tags=["shopify-webhooks"])

def verify_shopify_webhook(data: bytes, hmac_header: str, secret: str) -> bool:
    if not hmac_header:
        return False
    digest = hmac.new(secret.encode('utf-8'), data, hashlib.sha256).digest()
    computed_hmac = b64encode(digest).decode('utf-8')
    return hmac.compare_digest(computed_hmac, hmac_header)

@router.post("/products/update")
async def shopify_product_update(
    request: Request,
    x_shopify_hmac_sha256: str = Header(None),
    x_shopify_topic: str = Header(None),
    x_shopify_shop_domain: str = Header(None),
    db: Session = Depends(get_db)
):
    """Handle Shopify product update webhooks"""
    data = await request.body()
    # In production, verify HMAC here using shop-specific secret from Vault
    
    payload = json.loads(data)
    product_id = str(payload.get("id"))
    logger.info(f"Received Shopify product update: {product_id} from {x_shopify_shop_domain}")
    
    # Trigger marketplace sync
    try:
        # Using shop domain as tenant_id for simplicity in POC
        await MarketplaceService.trigger_catalog_sync(tenant_id=x_shopify_shop_domain)
    except Exception as e:
        logger.error(f"Failed to trigger sync: {e}")

    return {"status": "received"}

@router.post("/orders/create")
async def shopify_order_create(
    request: Request,
   db: Session = Depends(get_db)
):
    """Handle Shopify order creation webhooks"""
    data = await request.json()
    logger.info(f"Received Shopify order: {data.get('id')}")
    
    # Logic to route to fulfillment (DeoDap) if necessary
    return {"status": "received"}

@router.post("/inventory/update")
async def shopify_inventory_update(
    request: Request,
    x_shopify_shop_domain: str = Header(None),
    db: Session = Depends(get_db)
):
    """Handle Shopify inventory update webhooks"""
    data = await request.json()
    sku = data.get("sku")
    available = data.get("available")
    
    logger.info(f"Received Shopify inventory update for {sku}: {available} from {x_shopify_shop_domain}")
    
    if sku and available is not None:
        try:
            await InventoryService.reconcile_inventory(
                tenant_id=x_shopify_shop_domain, 
                sku=sku, 
                current_stock=available
            )
        except Exception as e:
            logger.error(f"Inventory reconciliation failed: {e}")

    return {"status": "received"}
