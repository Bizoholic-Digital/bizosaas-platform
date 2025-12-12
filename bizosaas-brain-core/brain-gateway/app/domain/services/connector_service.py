import logging
from typing import Dict, Any, Optional
from app.connectors.registry import ConnectorRegistry
from app.domain.services.secret_service import SecretService

logger = logging.getLogger(__name__)

class ConnectorService:
    """
    Domain service for managing connectors.
    Orchestrates connector operations following hexagonal architecture.
    """
    
    def __init__(self, secret_service: SecretService):
        self.secret_service = secret_service
        self.registry = ConnectorRegistry
    
    async def connect_connector(
        self,
        tenant_id: str,
        connector_id: str,
        credentials: Dict[str, Any],
        validate: bool = True
    ) -> Dict[str, Any]:
        """
        Connect a connector for a tenant.
        
        Args:
            tenant_id: Tenant identifier
            connector_id: Connector identifier
            credentials: Connector credentials
            validate: Whether to validate credentials before storing
            
        Returns:
            Result dictionary with status and message
        """
        try:
            # Validate credentials if requested
            if validate:
                connector = self.registry.create_connector(
                    connector_id,
                    tenant_id,
                    credentials
                )
                is_valid = await connector.validate_credentials()
                
                if not is_valid:
                    return {
                        "status": "error",
                        "message": "Invalid credentials"
                    }
            
            # Store credentials securely
            success = await self.secret_service.store_connector_credentials(
                tenant_id=tenant_id,
                connector_id=connector_id,
                credentials=credentials
            )
            
            if not success:
                return {
                    "status": "error",
                    "message": "Failed to store credentials"
                }
            
            logger.info(f"Connected {connector_id} for tenant {tenant_id}")
            
            return {
                "status": "success",
                "message": f"Successfully connected {connector_id}",
                "connector_id": connector_id
            }
            
        except Exception as e:
            logger.error(f"Error connecting connector: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def disconnect_connector(
        self,
        tenant_id: str,
        connector_id: str
    ) -> Dict[str, Any]:
        """
        Disconnect a connector for a tenant.
        
        Args:
            tenant_id: Tenant identifier
            connector_id: Connector identifier
            
        Returns:
            Result dictionary with status and message
        """
        try:
            success = await self.secret_service.delete_connector_credentials(
                tenant_id=tenant_id,
                connector_id=connector_id
            )
            
            if not success:
                return {
                    "status": "error",
                    "message": "Failed to delete credentials"
                }
            
            logger.info(f"Disconnected {connector_id} for tenant {tenant_id}")
            
            return {
                "status": "success",
                "message": f"Successfully disconnected {connector_id}"
            }
            
        except Exception as e:
            logger.error(f"Error disconnecting connector: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def get_connector_status(
        self,
        tenant_id: str,
        connector_id: str
    ) -> Dict[str, Any]:
        """
        Get connector connection status.
        
        Args:
            tenant_id: Tenant identifier
            connector_id: Connector identifier
            
        Returns:
            Status dictionary
        """
        try:
            credentials = await self.secret_service.get_connector_credentials(
                tenant_id=tenant_id,
                connector_id=connector_id
            )
            
            if not credentials:
                return {
                    "connector_id": connector_id,
                    "status": "disconnected",
                    "message": "No credentials found"
                }
            
            # Test connection
            connector = self.registry.create_connector(
                connector_id,
                tenant_id,
                credentials
            )
            
            is_valid = await connector.validate_credentials()
            
            return {
                "connector_id": connector_id,
                "status": "connected" if is_valid else "error",
                "message": "Connection valid" if is_valid else "Connection failed"
            }
            
        except Exception as e:
            logger.error(f"Error checking connector status: {e}")
            return {
                "connector_id": connector_id,
                "status": "error",
                "message": str(e)
            }
    
    async def list_connected_connectors(
        self,
        tenant_id: str
    ) -> list[Dict[str, Any]]:
        """
        List all connected connectors for a tenant.
        
        Args:
            tenant_id: Tenant identifier
            
        Returns:
            List of connector status dictionaries
        """
        try:
            connector_ids = await self.secret_service.list_tenant_connectors(tenant_id)
            
            statuses = []
            for connector_id in connector_ids:
                status = await self.get_connector_status(tenant_id, connector_id)
                statuses.append(status)
            
            return statuses
            
        except Exception as e:
            logger.error(f"Error listing connectors: {e}")
            return []
    
    async def sync_connector_data(
        self,
        tenant_id: str,
        connector_id: str,
        resource_type: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Sync data from a connector.
        
        Args:
            tenant_id: Tenant identifier
            connector_id: Connector identifier
            resource_type: Type of resource to sync
            params: Optional parameters for sync
            
        Returns:
            Sync result dictionary
        """
        try:
            credentials = await self.secret_service.get_connector_credentials(
                tenant_id=tenant_id,
                connector_id=connector_id
            )
            
            if not credentials:
                return {
                    "status": "error",
                    "message": "Connector not connected"
                }
            
            connector = self.registry.create_connector(
                connector_id,
                tenant_id,
                credentials
            )
            
            data = await connector.sync_data(resource_type, params)
            
            return {
                "status": "success",
                "connector_id": connector_id,
                "resource_type": resource_type,
                "data": data
            }
            
        except Exception as e:
            logger.error(f"Error syncing connector data: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
