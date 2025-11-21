"""
HashiCorp Vault Client for BizOSaaS Brain API
Handles secure secrets management and dynamic configuration
"""
import os
import json
import logging
from typing import Dict, Any, Optional
import hvac
from functools import lru_cache
import asyncio
from contextlib import asynccontextmanager

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
                raise Exception("Vault authentication failed")
            
            logger.info(f"Successfully connected to Vault at {self.vault_addr}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Vault client: {e}")
            raise
    
    @lru_cache(maxsize=128)
    def get_secret(self, path: str) -> Dict[str, Any]:
        """
        Retrieve secret from Vault with caching
        
        Args:
            path: Secret path (e.g., 'bizosaas/database')
            
        Returns:
            Secret data dictionary
        """
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
    
    def put_secret(self, path: str, secret_data: Dict[str, Any]) -> bool:
        """
        Store secret in Vault
        
        Args:
            path: Secret path
            secret_data: Data to store
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=secret_data,
                mount_point=self.mount_path
            )
            
            logger.info(f"Successfully stored secret at path: {path}")
            
            # Clear cache for this path
            cache_key = path
            if cache_key in self.get_secret.cache_info():
                self.get_secret.cache_clear()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to store secret at {path}: {e}")
            return False
    
    def delete_secret(self, path: str) -> bool:
        """
        Delete secret from Vault
        
        Args:
            path: Secret path to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.secrets.kv.v2.delete_metadata_and_all_versions(
                path=path,
                mount_point=self.mount_path
            )
            
            logger.info(f"Successfully deleted secret at path: {path}")
            
            # Clear cache
            self.get_secret.cache_clear()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete secret at {path}: {e}")
            return False
    
    def get_service_config(self, service_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific service
        
        Args:
            service_name: Name of the service (e.g., 'crm', 'saleor', 'wagtail')
            
        Returns:
            Configuration dictionary
        """
        return self.get_secret(f'bizosaas/{service_name}')

    def get_database_config(self) -> Dict[str, str]:
        """Get database configuration from Vault"""
        return self.get_secret('bizosaas/database')
    
    def get_django_config(self) -> Dict[str, str]:
        """Get Django configuration from Vault"""
        return self.get_secret('bizosaas/django')
    
    def get_wagtail_config(self) -> Dict[str, str]:
        """Get Wagtail configuration from Vault"""
        return self.get_secret('bizosaas/wagtail')
    
    def get_saleor_config(self) -> Dict[str, str]:
        """Get Saleor configuration from Vault"""
        return self.get_secret('bizosaas/saleor')

    def get_redis_config(self) -> Dict[str, str]:
        """Get Redis configuration from Vault"""
        return self.get_secret('bizosaas/redis')
    
    def get_ai_config(self) -> Dict[str, str]:
        """Get AI services configuration from Vault"""
        return self.get_secret('bizosaas/ai-agents')
    
    def get_tenant_secrets(self, tenant_id: str) -> Dict[str, Any]:
        """
        Get tenant-specific secrets
        
        Args:
            tenant_id: Tenant identifier
            
        Returns:
            Tenant secrets dictionary
        """
        return self.get_secret(f'tenants/{tenant_id}')
    
    def store_tenant_secrets(self, tenant_id: str, secrets: Dict[str, Any]) -> bool:
        """
        Store tenant-specific secrets
        
        Args:
            tenant_id: Tenant identifier
            secrets: Secrets to store
            
        Returns:
            True if successful
        """
        return self.put_secret(f'tenants/{tenant_id}', secrets)
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on Vault connection
        
        Returns:
            Health status dictionary
        """
        try:
            # Check if client is authenticated
            is_authenticated = self.client.is_authenticated()
            
            # Check Vault status
            status = self.client.sys.read_health_status()
            
            return {
                'vault_connected': True,
                'vault_authenticated': is_authenticated,
                'vault_status': status,
                'vault_addr': self.vault_addr
            }
            
        except Exception as e:
            logger.error(f"Vault health check failed: {e}")
            return {
                'vault_connected': False,
                'vault_authenticated': False,
                'error': str(e),
                'vault_addr': self.vault_addr
            }
    
    def rotate_service_token(self, service_name: str) -> Optional[str]:
        """
        Rotate service token for enhanced security
        
        Args:
            service_name: Name of the service
            
        Returns:
            New token if successful, None otherwise
        """
        try:
            policy_name = f"{service_name}-policy"
            
            # Create new token with same policy
            response = self.client.auth.token.create(
                policies=[policy_name],
                ttl='24h',  # 24 hour TTL for tokens
                renewable=True
            )
            
            if 'auth' in response and 'client_token' in response['auth']:
                new_token = response['auth']['client_token']
                logger.info(f"Successfully rotated token for service: {service_name}")
                return new_token
            
        except Exception as e:
            logger.error(f"Failed to rotate token for {service_name}: {e}")
            
        return None

# Global Vault client instance
vault_client: Optional[VaultClient] = None

def get_vault_client() -> VaultClient:
    """Get global Vault client instance"""
    global vault_client
    if vault_client is None:
        vault_client = VaultClient()
    return vault_client

@asynccontextmanager
async def vault_context():
    """Async context manager for Vault operations"""
    client = get_vault_client()
    try:
        yield client
    except Exception as e:
        logger.error(f"Vault operation failed: {e}")
        raise
    finally:
        # Cleanup if needed
        pass

def load_config_from_vault() -> Dict[str, Any]:
    """
    Load all configuration from Vault for Brain API
    
    Returns:
        Complete configuration dictionary
    """
    try:
        vault = get_vault_client()
        
        config = {
            'database': vault.get_database_config(),
            'django': vault.get_django_config(),
            'wagtail': vault.get_wagtail_config(),
            'saleor': vault.get_saleor_config(),
            'redis': vault.get_redis_config(),
            'ai_agents': vault.get_ai_config(),
        }
        
        logger.info("Successfully loaded configuration from Vault")
        return config
        
    except Exception as e:
        logger.error(f"Failed to load configuration from Vault: {e}")
        
        # Fallback to environment variables (Logged as warning)
        logger.warning("Falling back to environment variables for configuration")
        return {
            'database': {
                'host': os.getenv('POSTGRES_HOST', 'localhost'),
                'port': os.getenv('POSTGRES_PORT', '5432'),
                'database': os.getenv('POSTGRES_DB', 'bizosaas'),
                'username': os.getenv('POSTGRES_USER', 'admin'),
                'password': os.getenv('POSTGRES_PASSWORD', 'fallback_password')
            }
        }