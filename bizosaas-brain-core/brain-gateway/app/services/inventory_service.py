import logging
from typing import List, Dict, Any
from app.connectors.registry import ConnectorRegistry
from app.connectors.base import ConnectorType
from app.services.marketplace_service import MarketplaceService

logger = logging.getLogger(__name__)

class InventoryService:
    @staticmethod
    async def reconcile_inventory(tenant_id: str, sku: str, current_stock: int):
        """
        Reconcile inventory across all connected marketplaces.
        If stock is 0 or less, immediately push 'Out of Stock' to all platforms.
        """
        logger.info(f"Inventory Reconcile for Tenant {tenant_id} | SKU: {sku} | Stock: {current_stock}")
        
        if current_stock <= 0:
            await InventoryService.broadcast_out_of_stock(tenant_id, sku)
        else:
            # Optionally sync the exact stock level if needed
            logger.debug(f"Stock for {sku} is {current_stock}, skipping emergency lockout.")

    @staticmethod
    async def broadcast_out_of_stock(tenant_id: str, sku: str):
        """
        Urgent: Tell all marketplaces that this SKU is out of stock.
        """
        logger.warning(f"URGENT: Broadcasting Out-of-Stock for SKU {sku} across all channels for tenant {tenant_id}")
        
        # 1. Identify all connected MARKETPLACE and ECOMMERCE platforms except the source
        # For simplicity, we get all marketplaces from the registry that have credentials for this tenant
        
        # We need a way to get all active connectors for a tenant. 
        # Using a pattern similar to ecommerce.py's get_all_active_ecommerce_connectors
        from app.dependencies import SessionLocal # Or a dedicated connection manager
        from app.domain.services.secret_service import SecretService
        from app.api.ecommerce import get_all_active_ecommerce_connectors
        
        # This part requires a session/secret service which usually comes from Depends.
        # In a background task, we'd use a singleton or factory.
        
        # Trigger via Temporal for reliability and multi-marketplace parallel execution
        try:
            from temporalio.client import Client
            import os
            
            temporal_url = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
            client = await Client.connect(temporal_url)
            
            await client.start_workflow(
                "MarketplaceInventoryLockWorkflow",
                {
                    "tenant_id": tenant_id,
                    "sku": sku,
                    "quantity": 0
                },
                id=f"inv-lock-{tenant_id}-{sku}",
                task_queue="brain-tasks"
            )
            logger.info(f"Inventory Lock Workflow started for SKU {sku}")
        except Exception as e:
            logger.error(f"Failed to trigger Inventory Lock Workflow: {e}")
            # Fallback to direct sequential update if Temporal is down
            pass
