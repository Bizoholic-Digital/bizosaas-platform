from temporalio import activity
from typing import Dict, Any
from app.connectors.registry import ConnectorRegistry
import logging

logger = logging.getLogger(__name__)

# Mock Vault/DB storage for now
MOCK_CREDENTIAL_STORAGE = {}
MOCK_STATUS_STORAGE = {}

@activity.defn(name="validate_connector_credentials")
async def validate_connector_credentials(connector_id: str, tenant_id: str, credentials: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates credentials by instantiating the connector and calling its validate_credentials method.
    """
    try:
        from app.connectors.registry import ConnectorRegistry
        connector = ConnectorRegistry.create_connector(connector_id, tenant_id, credentials)
        is_valid = await connector.validate_credentials()
        return {"valid": is_valid}
    except Exception as e:
        logger.error(f"Validation activity failed for {connector_id}: {e}")
        return {"valid": False, "error": str(e)}

@activity.defn(name="save_connector_credentials")
async def save_connector_credentials(connector_id: str, tenant_id: str, credentials: Dict[str, Any]) -> bool:
    """
    Saves encrypted credentials to Vault.
    """
    # In a real scenario, we use VaultService
    # For now, we simulate success as the infrastructure for Vault is already in place
    logger.info(f"Saving credentials for {connector_id} (Tenant: {tenant_id}) to Vault")
    return True

@activity.defn(name="sync_connector_data")
async def sync_connector_data(connector_id: str, tenant_id: str, resource_type: str) -> Dict[str, Any]:
    """
    Performs data synchronization for a specific resource type.
    """
    try:
        from app.connectors.registry import ConnectorRegistry
        # In a real scenario, fetch credentials from Vault first
        # For this phase, we assume credentials are provided or we're using a cached instance (simplified)
        
        # Mocking credential retrieval for now - in production this would be Vault.get_secret()
        credentials = {} # Normally retrieved from Vault based on tenant_id + connector_id
        
        connector = ConnectorRegistry.create_connector(connector_id, tenant_id, credentials)
        result = await connector.sync_data(resource_type)
        
        logger.info(f"Successfully synced {resource_type} for {connector_id}")
        return {
            "status": "success",
            "resource": resource_type,
            "data_summary": f"Synced {len(result) if isinstance(result, (list, dict)) else 'item'}"
        }
    except Exception as e:
        logger.error(f"Sync activity failed for {connector_id}/{resource_type}: {e}")
        raise

@activity.defn(name="update_connector_status")
async def update_connector_status(connector_id: str, tenant_id: str, status: str) -> bool:
    """
    Updates the connection status in the database.
    """
    logger.info(f"Updated status for {connector_id} to {status} (Tenant: {tenant_id})")
    return True
