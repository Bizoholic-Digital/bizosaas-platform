import logging
from typing import Dict, Any, Optional
from app.ports.secret_port import SecretPort

logger = logging.getLogger(__name__)

class SecretService:
    """
    Domain service for managing secrets.
    Encapsulates business logic for secret management.
    """
    
    def __init__(self, secret_adapter: SecretPort):
        self.secret_adapter = secret_adapter
    
    def _build_connector_path(self, tenant_id: str, connector_id: str) -> str:
        """Build standardized path for connector credentials"""
        return f"tenants/{tenant_id}/connectors/{connector_id}"
    
    async def store_connector_credentials(
        self,
        tenant_id: str,
        connector_id: str,
        credentials: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Store connector credentials securely.
        
        Args:
            tenant_id: Tenant identifier
            connector_id: Connector identifier
            credentials: Credential data
            metadata: Optional metadata (created_at, created_by, etc.)
            
        Returns:
            True if successful
        """
        path = self._build_connector_path(tenant_id, connector_id)
        
        # Add default metadata
        full_metadata = metadata or {}
        full_metadata.update({
            "tenant_id": tenant_id,
            "connector_id": connector_id,
            "type": "connector_credentials"
        })
        
        success = await self.secret_adapter.store_secret(
            path=path,
            secret_data=credentials,
            metadata=full_metadata
        )
        
        if success:
            logger.info(f"Stored credentials for {connector_id} (tenant: {tenant_id})")
        else:
            logger.error(f"Failed to store credentials for {connector_id} (tenant: {tenant_id})")
        
        return success
    
    async def get_connector_credentials(
        self,
        tenant_id: str,
        connector_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve connector credentials.
        
        Args:
            tenant_id: Tenant identifier
            connector_id: Connector identifier
            
        Returns:
            Credentials or None if not found
        """
        path = self._build_connector_path(tenant_id, connector_id)
        credentials = await self.secret_adapter.get_secret(path)
        
        if credentials:
            logger.info(f"Retrieved credentials for {connector_id} (tenant: {tenant_id})")
        else:
            logger.warning(f"No credentials found for {connector_id} (tenant: {tenant_id})")
        
        return credentials
    
    async def delete_connector_credentials(
        self,
        tenant_id: str,
        connector_id: str
    ) -> bool:
        """
        Delete connector credentials.
        
        Args:
            tenant_id: Tenant identifier
            connector_id: Connector identifier
            
        Returns:
            True if successful
        """
        path = self._build_connector_path(tenant_id, connector_id)
        success = await self.secret_adapter.delete_secret(path)
        
        if success:
            logger.info(f"Deleted credentials for {connector_id} (tenant: {tenant_id})")
        else:
            logger.error(f"Failed to delete credentials for {connector_id} (tenant: {tenant_id})")
        
        return success
    
    async def list_tenant_connectors(self, tenant_id: str) -> list[str]:
        """
        List all connectors for a tenant.
        
        Args:
            tenant_id: Tenant identifier
            
        Returns:
            List of connector IDs
        """
        path_prefix = f"tenants/{tenant_id}/connectors/"
        paths = await self.secret_adapter.list_secrets(path_prefix)
        
        # Extract connector IDs from paths
        connector_ids = [
            path.replace(path_prefix, "").split("/")[0]
            for path in paths
        ]
        
        return list(set(connector_ids))  # Remove duplicates
    
    async def rotate_connector_credentials(
        self,
        tenant_id: str,
        connector_id: str,
        new_credentials: Dict[str, Any]
    ) -> bool:
        """
        Rotate connector credentials.
        
        Args:
            tenant_id: Tenant identifier
            connector_id: Connector identifier
            new_credentials: New credential data
            
        Returns:
            True if successful
        """
        path = self._build_connector_path(tenant_id, connector_id)
        success = await self.secret_adapter.rotate_secret(path, new_credentials)
        
        if success:
            logger.info(f"Rotated credentials for {connector_id} (tenant: {tenant_id})")
        else:
            logger.error(f"Failed to rotate credentials for {connector_id} (tenant: {tenant_id})")
        
        return success
