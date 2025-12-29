import logging
import os
from typing import Dict, Any, Optional, List
import hvac
from app.ports.secret_port import SecretPort

logger = logging.getLogger(__name__)

class VaultAdapter(SecretPort):
    """
    HashiCorp Vault adapter for secure secret storage.
    Implements the SecretPort interface using Vault KV v2 engine.
    """
    
    def __init__(
        self,
        vault_url: Optional[str] = None,
        vault_token: Optional[str] = None,
        mount_point: str = "secret"
    ):
        self.vault_url = vault_url or os.getenv("VAULT_URL", "http://vault:8200")
        self.vault_token = vault_token or os.getenv("VAULT_TOKEN")
        self.mount_point = mount_point
        
        if not self.vault_token:
            logger.warning("VAULT_TOKEN not set - Vault operations will fail")
        
        try:
            self.client = hvac.Client(
                url=self.vault_url,
                token=self.vault_token
            )
            
            # Set a default timeout for all requests
            # hvac uses requests.Session internally via RequestAdapter
            if hasattr(self.client, 'adapter'):
                self.client.adapter.timeout = 5.0
            
            if self.client.is_authenticated():
                logger.info(f"Successfully authenticated with Vault at {self.vault_url}")
            else:
                logger.error("Failed to authenticate with Vault")
        except Exception as e:
            logger.error(f"Failed to initialize Vault client: {e}")
            self.client = None
    
    async def store_secret(
        self,
        path: str,
        secret_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Store a secret in Vault KV v2.
        
        Args:
            path: Secret path (e.g., "tenants/tenant-123/connectors/wordpress")
            secret_data: The secret data to store
            metadata: Optional metadata
            
        Returns:
            True if successful
        """
        if not self.client or not self.client.is_authenticated():
            logger.error("Vault client not authenticated")
            return False
        
        try:
            # KV v2 requires 'data' wrapper
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=secret_data,
                mount_point=self.mount_point
            )
            logger.info(f"Stored secret at {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to store secret at {path}: {e}")
            return False
    
    async def get_secret(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a secret from Vault.
        
        Args:
            path: Secret path
            
        Returns:
            Secret data or None if not found
        """
        if not self.client or not self.client.is_authenticated():
            logger.error("Vault client not authenticated")
            return None
        
        try:
            response = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                mount_point=self.mount_point
            )
            return response['data']['data']
        except hvac.exceptions.InvalidPath:
            logger.warning(f"Secret not found at {path}")
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve secret from {path}: {e}")
            return None
    
    async def delete_secret(self, path: str) -> bool:
        """
        Delete a secret from Vault.
        
        Args:
            path: Secret path
            
        Returns:
            True if successful
        """
        if not self.client or not self.client.is_authenticated():
            logger.error("Vault client not authenticated")
            return False
        
        try:
            self.client.secrets.kv.v2.delete_metadata_and_all_versions(
                path=path,
                mount_point=self.mount_point
            )
            logger.info(f"Deleted secret at {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete secret at {path}: {e}")
            return False
    
    async def list_secrets(self, path_prefix: str) -> List[str]:
        """
        List all secrets under a path prefix.
        
        Args:
            path_prefix: Path prefix to list
            
        Returns:
            List of secret paths
        """
        if not self.client or not self.client.is_authenticated():
            logger.error("Vault client not authenticated")
            return []
        
        try:
            response = self.client.secrets.kv.v2.list_secrets(
                path=path_prefix,
                mount_point=self.mount_point
            )
            keys = response['data']['keys']
            return [f"{path_prefix}{key}" for key in keys]
        except hvac.exceptions.InvalidPath:
            logger.warning(f"No secrets found under {path_prefix}")
            return []
        except Exception as e:
            logger.error(f"Failed to list secrets under {path_prefix}: {e}")
            return []
    
    async def rotate_secret(
        self,
        path: str,
        new_secret_data: Dict[str, Any]
    ) -> bool:
        """
        Rotate a secret (create new version).
        
        Args:
            path: Secret path
            new_secret_data: New secret data
            
        Returns:
            True if successful
        """
        # In Vault KV v2, rotation is just creating a new version
        return await self.store_secret(path, new_secret_data)
