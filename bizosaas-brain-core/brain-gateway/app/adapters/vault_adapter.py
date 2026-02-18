import hvac
import logging
from typing import Dict, Any, Optional
from app.ports.secret_port import SecretPort

logger = logging.getLogger(__name__)

class VaultAdapter(SecretPort):
    """
    Production adapter for HashiCorp Vault.
    Use this in staging and production environments.
    """
    
    def __init__(
        self,
        vault_url: str,
        vault_token: Optional[str] = None,
        vault_role_id: Optional[str] = None,
        vault_secret_id: Optional[str] = None,
        mount_point: str = "secret"
    ):
        """
        Initialize Vault client.
        
        Args:
            vault_url: Vault server URL (e.g., "http://vault:8200")
            vault_token: Vault token (for token auth)
            vault_role_id: AppRole role ID (for AppRole auth)
            vault_secret_id: AppRole secret ID (for AppRole auth)
            mount_point: KV secrets engine mount point
        """
        self.client = hvac.Client(url=vault_url)
        self.mount_point = mount_point
        
        # Authenticate
        if vault_token:
            self.client.token = vault_token
            logger.info("Authenticated to Vault using token")
        elif vault_role_id and vault_secret_id:
            self.client.auth.approle.login(
                role_id=vault_role_id,
                secret_id=vault_secret_id
            )
            logger.info("Authenticated to Vault using AppRole")
        else:
            raise ValueError("Must provide either vault_token or both vault_role_id and vault_secret_id")
        
        if not self.client.is_authenticated():
            raise ConnectionError("Failed to authenticate to Vault")
    
    async def store_secret(
        self,
        path: str,
        secret_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Store secret in Vault KV v2"""
        try:
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=secret_data,
                mount_point=self.mount_point
            )
            
            # Add metadata if provided
            if metadata:
                self.client.secrets.kv.v2.update_metadata(
                    path=path,
                    custom_metadata=metadata,
                    mount_point=self.mount_point
                )
            
            logger.info(f"Stored secret in Vault: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to store secret in Vault: {e}")
            return False
    
    async def get_secret(self, path: str) -> Optional[Dict[str, Any]]:
        """Retrieve secret from Vault KV v2"""
        try:
            response = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                mount_point=self.mount_point
            )
            return response['data']['data']
        except hvac.exceptions.InvalidPath:
            logger.warning(f"Secret not found: {path}")
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve secret from Vault: {e}")
            return None
    
    async def delete_secret(self, path: str) -> bool:
        """Delete secret from Vault (soft delete)"""
        try:
            self.client.secrets.kv.v2.delete_latest_version_of_secret(
                path=path,
                mount_point=self.mount_point
            )
            logger.info(f"Deleted secret from Vault: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete secret from Vault: {e}")
            return False
    
    async def list_secrets(self, path_prefix: str) -> list[str]:
        """List secrets under path prefix"""
        try:
            response = self.client.secrets.kv.v2.list_secrets(
                path=path_prefix,
                mount_point=self.mount_point
            )
            return response['data']['keys']
        except Exception as e:
            logger.error(f"Failed to list secrets from Vault: {e}")
            return []
    
    async def rotate_secret(
        self,
        path: str,
        new_secret_data: Dict[str, Any]
    ) -> bool:
        """Rotate secret (creates new version in Vault)"""
        return await self.store_secret(path, new_secret_data)
