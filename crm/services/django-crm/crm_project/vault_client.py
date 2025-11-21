"""
HashiCorp Vault Client for Django CRM
Handles secure secrets management and dynamic configuration
"""
import os
import json
import logging
from typing import Dict, Any, Optional
import hvac
from functools import lru_cache

logger = logging.getLogger(__name__)

class VaultClient:
    """
    Secure Vault client for BizOSaaS services
    Provides centralized secrets management and configuration
    """
    
    def __init__(self, vault_addr: str = None, vault_token: str = None):
        self.vault_addr = vault_addr or os.getenv('VAULT_ADDR', 'http://vault:8200')
        self.vault_token = vault_token or os.getenv('VAULT_TOKEN', 'bizosaas-vault-dev-token-2025')
        self.mount_path = os.getenv('VAULT_MOUNT_PATH', 'secret')
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Vault client with authentication"""
        try:
            self.client = hvac.Client(url=self.vault_addr, token=self.vault_token)
            
            # Verify authentication
            if not self.client.is_authenticated():
                logger.error("Failed to authenticate with Vault")
            else:
                logger.info(f"Successfully connected to Vault at {self.vault_addr}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Vault client: {e}")
    
    @lru_cache(maxsize=128)
    def get_secret(self, path: str) -> Dict[str, Any]:
        """
        Retrieve secret from Vault with caching
        """
        if not self.client or not self.client.is_authenticated():
            return {}

        try:
            full_path = f"{self.mount_path}/data/{path}"
            response = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                mount_point=self.mount_path
            )
            
            if response and 'data' in response and 'data' in response['data']:
                secret_data = response['data']['data']
                logger.info(f"Retrieved secret from path: {path}")
                return secret_data
            else:
                logger.warning(f"No data found at Vault path: {path}")
                return {}
                
        except Exception as e:
            logger.error(f"Failed to retrieve secret from {path}: {e}")
            return {}
    
    def get_django_config(self) -> Dict[str, str]:
        """Get Django configuration from Vault"""
        return self.get_secret('bizosaas/django')

# Global Vault client instance
vault_client: Optional[VaultClient] = None

def get_vault_client() -> VaultClient:
    """Get global Vault client instance"""
    global vault_client
    if vault_client is None:
        vault_client = VaultClient()
    return vault_client
