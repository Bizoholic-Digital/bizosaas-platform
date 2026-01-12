from temporalio import activity
from typing import Dict, Any
from app.connectors.registry import ConnectorRegistry
import logging

logger = logging.getLogger(__name__)

# Mock Vault/DB storage for now
MOCK_CREDENTIAL_STORAGE = {}
MOCK_STATUS_STORAGE = {}

@activity.defn
async def validate_connector_credentials(connector_id: str, tenant_id: str, credentials: Dict[str, Any]) -> Dict[str, Any]:
    try:
        connector = ConnectorRegistry.create_connector(connector_id, tenant_id, credentials)
        is_valid = await connector.validate_credentials()
        return {"valid": is_valid}
    except Exception as e:
        logger.error(f"Validation activity failed: {e}")
        return {"valid": False, "error": str(e)}

@activity.defn
async def save_connector_credentials(connector_id: str, tenant_id: str, credentials: Dict[str, Any]) -> bool:
    key = f"{tenant_id}:{connector_id}"
    MOCK_CREDENTIAL_STORAGE[key] = credentials
    logger.info(f"Saved credentials for {key}")
    return True

@activity.defn
async def sync_connector_data(connector_id: str, tenant_id: str, resource_type: str) -> Dict[str, Any]:
    try:
        # Retrieve credentials (mock)
        key = f"{tenant_id}:{connector_id}"
        credentials = MOCK_CREDENTIAL_STORAGE.get(key, {})
        
        connector = ConnectorRegistry.create_connector(connector_id, tenant_id, credentials)
        data = await connector.sync_data(resource_type)
        
        # In real world, save 'data' to data warehouse / DB
        logger.info(f"Synced {resource_type} for {key}: {len(data) if isinstance(data, list) else 'success'}")
        
        return {"status": "success", "items_synced": 10} # Mock count
    except Exception as e:
        logger.error(f"Sync activity failed: {e}")
        raise

@activity.defn
async def update_connector_status(connector_id: str, tenant_id: str, status: str) -> bool:
    key = f"{tenant_id}:{connector_id}"
    MOCK_STATUS_STORAGE[key] = status
    logger.info(f"Updated status for {key} to {status}")
    return True
