from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any

# Import activities (interface definitions)
# In a real app, these would be in a shared library or defined in an activities module

@workflow.defn
class ConnectorSetupWorkflow:
    @workflow.run
    async def run(self, connector_id: str, tenant_id: str, credentials: Dict[str, Any]) -> Dict[str, Any]:
        
        # 1. Validate Credentials
        # We assume there's an activity 'validate_connector_credentials' registered
        validation_result = await workflow.execute_activity(
            "validate_connector_credentials",
            args=[connector_id, tenant_id, credentials],
            start_to_close_timeout=timedelta(seconds=10)
        )
        
        if not validation_result.get("valid"):
            raise ApplicationError("Invalid credentials provided.")
            
        # 2. Save Credentials to Vault
        await workflow.execute_activity(
            "save_connector_credentials",
            args=[connector_id, tenant_id, credentials],
            start_to_close_timeout=timedelta(seconds=5)
        )
        
        # 3. Initial Sync
        sync_result = await workflow.execute_activity(
            "sync_connector_data",
            args=[connector_id, tenant_id, "initial_sync"],
            start_to_close_timeout=timedelta(minutes=5)
        )
        
        # 4. Update Status
        await workflow.execute_activity(
            "update_connector_status",
            args=[connector_id, tenant_id, "connected"],
            start_to_close_timeout=timedelta(seconds=5)
        )
        
        return {"status": "success", "sync_summary": sync_result}

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
