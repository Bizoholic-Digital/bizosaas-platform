import os
import logging
from typing import List, Optional
from temporalio.client import Client
from app.workflows.marketplace_sync import MarketplaceCatalogSyncWorkflow

logger = logging.getLogger(__name__)

class MarketplaceService:
    @staticmethod
    async def trigger_catalog_sync(tenant_id: str, marketplaces: Optional[List[str]] = None):
        """
        Trigger a Temporal workflow to sync catalog from Shopify to marketplaces.
        """
        if marketplaces is None:
            marketplaces = ["meesho", "flipkart"]
            
        temporal_url = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
        
        try:
            client = await Client.connect(temporal_url)
            
            workflow_id = f"marketplace-sync-{tenant_id}"
            
            await client.start_workflow(
                MarketplaceCatalogSyncWorkflow.run,
                {
                    "tenant_id": tenant_id,
                    "marketplaces": marketplaces
                },
                id=workflow_id,
                task_queue="brain-tasks"
            )
            
            logger.info(f"Started marketplace sync workflow {workflow_id} for tenant {tenant_id}")
            return {"status": "workflow_started", "workflow_id": workflow_id}
            
        except Exception as e:
            logger.error(f"Failed to start marketplace sync workflow: {e}")
            raise
