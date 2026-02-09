from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any, List

# Import activities
with workflow.unsafe.imports_passed_through():
    from app.activities.marketplace import sync_product_to_marketplace
    from app.api.ecommerce import get_all_active_ecommerce_connectors # This might need refactoring to a service
    
@workflow.defn
class MarketplaceInventoryLockWorkflow:
    @workflow.run
    async def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Urgent Inventory Lock Workflow:
        Broadcasts stock quantity (usually 0) to all active marketplaces.
        """
        tenant_id = params.get("tenant_id")
        sku = params.get("sku")
        quantity = params.get("quantity", 0)
        
        # In a real workflow, we'd fetch the list of active marketplaces as an activity
        # market_list = await workflow.execute_activity(get_active_marketplaces, tenant_id, ...)
        
        # For POC, we assume the list is passed or we broadcast to known Indian marketplaces
        marketplaces = ["meesho", "flipkart", "ajio", "myntra"]
        
        results = []
        for marketplace in marketplaces:
            res = await workflow.execute_activity(
                sync_product_to_marketplace,
                {
                    "marketplace_slug": marketplace,
                    "product": {"sku": sku, "quantity": quantity, "action": "update_inventory"},
                    "tenant_id": tenant_id
                },
                start_to_close_timeout=timedelta(minutes=1)
            )
            results.append(res)
            
        return {
            "status": "inventory_locked",
            "sku": sku,
            "details": results
        }
