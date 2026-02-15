from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any

# Import activities (interface definitions)
# In a real app, these would be in a shared library or defined in an activities module

@workflow.defn
class ConnectorSetupWorkflow:
    @workflow.run
    async def run(self, connector_id: str, tenant_id: str, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive Connector Setup:
        1. Validate Credentials
        2. Save to Vault
        3. Initial Deep Sync (specialized per connector)
        4. Update Health Status
        """
        # 1. Validate Credentials
        validation_result = await workflow.execute_activity(
            "validate_connector_credentials",
            args=[connector_id, tenant_id, credentials],
            start_to_close_timeout=timedelta(minutes=2)
        )
        
        if not validation_result.get("valid"):
            error_msg = validation_result.get("error", "Invalid credentials provided.")
            raise workflow.ApplicationError(f"Connector setup failed: {error_msg}")
            
        # 2. Save Credentials to Vault
        await workflow.execute_activity(
            "save_connector_credentials",
            args=[connector_id, tenant_id, credentials],
            start_to_close_timeout=timedelta(seconds=30)
        )
        
        # 3. Initial Sync
        # Specialized sync depth for GA4/GSC
        resource_types = ["initial_sync"]
        if connector_id in ["google_analytics_4", "google_search_console"]:
            resource_types = ["metadata", "historical_30d"]
        elif connector_id == "hubspot":
            resource_types = ["contacts", "deals", "pipelines"]

        sync_summaries = {}
        for resource in resource_types:
            sync_result = await workflow.execute_activity(
                "sync_connector_data",
                args=[connector_id, tenant_id, resource],
                start_to_close_timeout=timedelta(minutes=10)
            )
            sync_summaries[resource] = sync_result
        
        # 4. Update Status
        await workflow.execute_activity(
            "update_connector_status",
            args=[connector_id, tenant_id, "connected"],
            start_to_close_timeout=timedelta(seconds=30)
        )
        
        return {
            "status": "success", 
            "connector_id": connector_id,
            "sync_summaries": sync_summaries
        }

@workflow.defn
class ConnectorSyncWorkflow:
    @workflow.run
    async def run(self, connector_id: str, tenant_id: str, resource_types: list) -> Dict[str, Any]:
        results = {}
        for resource in resource_types:
            result = await workflow.execute_activity(
                "sync_connector_data",
                args=[connector_id, tenant_id, resource],
                start_to_close_timeout=timedelta(minutes=10)
            )
            results[resource] = result
            
        return results
