from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

class SecretPort(ABC):
    """
    Port for secret management following hexagonal architecture.
    Implementations can use HashiCorp Vault, AWS Secrets Manager, etc.
    """
    
    @abstractmethod
    async def store_secret(
        self,
        path: str,
        secret_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Store a secret at the given path.
        
        Args:
            path: Secret path (e.g., "tenants/tenant-123/connectors/google-analytics")
            secret_data: The secret data to store
            metadata: Optional metadata (tags, expiry, etc.)
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def get_secret(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a secret from the given path.
        
        Args:
            path: Secret path
            
        Returns:
            Secret data or None if not found
        """
        pass
    
    @abstractmethod
    async def delete_secret(self, path: str) -> bool:
        """
        Delete a secret at the given path.
        
        Args:
            path: Secret path
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def list_secrets(self, path_prefix: str) -> list[str]:
        """
        List all secret paths under the given prefix.
        
        Args:
            path_prefix: Path prefix to search under
            
        Returns:
            List of secret paths
        """
        pass
    
    @abstractmethod
    async def rotate_secret(
        self,
        path: str,
        new_secret_data: Dict[str, Any]
    ) -> bool:
        """
        Rotate a secret (store new version, keep old for grace period).
        
        Args:
            path: Secret path
            new_secret_data: New secret data
            
        Returns:
            True if successful
        """
        pass
