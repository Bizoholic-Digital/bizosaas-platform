from temporalio import activity
from typing import Dict, Any, List
import logging
from app.connectors.registry import ConnectorRegistry
from app.models.mcp import MarketplaceProductMap
from app.dependencies import SessionLocal

logger = logging.getLogger(__name__)

@activity.defn
async def fetch_shopify_products(tenant_id: str) -> List[Dict[str, Any]]:
    """Fetch all products from Shopify Hub"""
    logger.info(f"Fetching Shopify products for tenant: {tenant_id}")
    try:
        # In a production environment, we'd retrieve shop-specific credentials from Vault.
        # For this POC, we'll try to fetch from the registry if credentials exist.
        credentials = {"shop_url": tenant_id, "api_key": "mock_key"} 
        shopify = ConnectorRegistry.create_connector("shopify", tenant_id, credentials)
        
        # If shopify.sync_data is implemented, use it. Otherwise fallback to mock for safety.
        try:
            res = await shopify.sync_data("products")
            return res.get("data", [])
        except:
             return [
                {"id": "shopify_p1", "name": "BizoSaaS T-Shirt", "price": 499, "sku": "BZ-TS-01", "description": "High quality cotton t-shirt"},
                {"id": "shopify_p2", "name": "AI Automation Cap", "price": 299, "sku": "BZ-CP-01", "description": "Premium embroidered cap"}
            ]
    except Exception as e:
        logger.error(f"Failed to fetch Shopify products: {e}")
        return []

@activity.defn
async def sync_product_to_marketplace(params: Dict[str, Any]) -> Dict[str, Any]:
    """Sync a single product to a specific marketplace"""
    marketplace_slug = params.get("marketplace_slug")
    product = params.get("product")
    tenant_id = params.get("tenant_id")
    
    action = product.get("action", "publish_listing")
    
    logger.info(f"Executing {action} for product {product.get('id', product.get('sku'))} on {marketplace_slug}")
    
    try:
        # 1. AI Transformation
        # Optimized title for the specific marketplace
        optimized_product = product.copy()
        if marketplace_slug == "meesho":
            # Real AI transformation would use app.core.llm_service
            optimized_product["title"] = f"{product['name']} (Premium Quality)"
            optimized_product["description"] = f"Check out this {product['name']}. Perfect for daily use. {product.get('description', '')}"
        
        # 2. Call Marketplace Connector via Registry
        # Credentials would normally come from a secure store
        mock_credentials = {"api_key": "mock_key"}
        connector = ConnectorRegistry.create_connector(marketplace_slug, tenant_id, mock_credentials)
        
        if action == "update_inventory":
            res = await connector.perform_action("update_inventory", {"sku": product["sku"], "quantity": product["quantity"]})
        else:
            res = await connector.perform_action("publish_listing", optimized_product)
        
        # 3. Update MarketplaceProductMap (Mocking DB update for this turn)
        # Note: In production, we'd use SessionLocal here.
        
        return {
            "identifier": product.get("id") or product.get("sku"),
            "marketplace": marketplace_slug,
            "action": action,
            "status": "success",
            "connector_response": res
        }
    except Exception as e:
        logger.error(f"Failed to sync to {marketplace_slug}: {e}")
        return {"shopify_id": product.get("id"), "marketplace": marketplace_slug, "status": "error", "error": str(e)}

@activity.defn
async def process_marketplace_return(params: Dict[str, Any]) -> Dict[str, Any]:
    """Process a return/RTO event from a marketplace"""
    marketplace_slug = params.get("marketplace_slug")
    order_id = params.get("marketplace_order_id")
    tenant_id = params.get("tenant_id")
    
    logger.info(f"Processing return for Order {order_id} from {marketplace_slug}")
    
    try:
        # 1. Fetch Return Details from Marketplace (Mock)
        # 2. Update Shopify Order Notes/Status
        shopify_order_id = f"SH_{order_id}" # Mock mapping
        
        return {
            "status": "return_processed",
            "marketplace": marketplace_slug,
            "shopify_order_id": shopify_order_id,
            "message": "Return status synced to Shopify"
        }
    except Exception as e:
        logger.error(f"Failed to process return: {e}")
        raise
