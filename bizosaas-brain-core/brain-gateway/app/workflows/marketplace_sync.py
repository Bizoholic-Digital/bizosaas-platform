from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any, List

# Import activities
with workflow.unsafe.imports_passed_through():
    from app.activities.marketplace import fetch_shopify_products, sync_product_to_marketplace

@workflow.defn
class MarketplaceCatalogSyncWorkflow:
    @workflow.run
    async def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Marketplace Catalog Sync Workflow:
        1. Fetch products from Shopify Hub.
        2. Iterate and sync to each active marketplace (Flipkart, Meesho).
        """
        tenant_id = params.get("tenant_id")
        marketplaces = params.get("marketplaces", ["meesho", "flipkart"])
        
        # Step 1: Fetch Products from Shopify
        products = await workflow.execute_activity(
            fetch_shopify_products,
            tenant_id,
            start_to_close_timeout=timedelta(minutes=10)
        )
        
        sync_results = []
        
        # Step 2: Iterate through products and sync to all marketplaces
        # We could use workflow.gather for parallel sync, but sequential is safer for rate limits
        for product in products:
            for marketplace in marketplaces:
                res = await workflow.execute_activity(
                    sync_product_to_marketplace,
                    {
                        "marketplace_slug": marketplace, 
                        "product": product, 
                        "tenant_id": tenant_id
                    },
                    start_to_close_timeout=timedelta(minutes=2)
                )
                sync_results.append(res)
        
        return {
            "status": "completed",
            "products_processed": len(products),
            "sync_details": sync_results
        }
