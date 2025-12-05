"""
Vault Integration Service
Securely retrieve secrets from HashiCorp Vault
"""

import os
import logging
from typing import Optional, Dict, Any
import hvac
from functools import lru_cache

logger = logging.getLogger(__name__)


class VaultClient:
    """HashiCorp Vault client for secure secrets management"""
    
    def __init__(
        self,
        vault_addr: Optional[str] = None,
        vault_token: Optional[str] = None,
        vault_namespace: Optional[str] = None
    ):
        self.vault_addr = vault_addr or os.getenv('VAULT_ADDR', 'http://localhost:8200')
        self.vault_token = vault_token or os.getenv('VAULT_TOKEN')
        self.vault_namespace = vault_namespace or os.getenv('VAULT_NAMESPACE', 'admin')
        
        if not self.vault_token:
            raise ValueError("VAULT_TOKEN environment variable is required")
        
        self.client = hvac.Client(
            url=self.vault_addr,
            token=self.vault_token,
            namespace=self.vault_namespace
        )
        
        if not self.client.is_authenticated():
            raise ValueError("Failed to authenticate with Vault")
        
        logger.info(f"Successfully connected to Vault at {self.vault_addr}")
    
    def get_secret(self, path: str, mount_point: str = 'secret') -> Dict[str, Any]:
        """
        Retrieve a secret from Vault
        
        Args:
            path: Secret path (e.g., 'quanttrade/deribit')
            mount_point: Vault mount point (default: 'secret')
        
        Returns:
            Dictionary containing secret data
        """
        try:
            response = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                mount_point=mount_point
            )
            return response['data']['data']
        except Exception as e:
            logger.error(f"Failed to retrieve secret from {path}: {e}")
            raise
    
    def set_secret(
        self,
        path: str,
        data: Dict[str, Any],
        mount_point: str = 'secret'
    ) -> None:
        """
        Store a secret in Vault
        
        Args:
            path: Secret path (e.g., 'quanttrade/deribit')
            data: Secret data to store
            mount_point: Vault mount point (default: 'secret')
        """
        try:
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=data,
                mount_point=mount_point
            )
            logger.info(f"Successfully stored secret at {path}")
        except Exception as e:
            logger.error(f"Failed to store secret at {path}: {e}")
            raise
    
    def get_exchange_credentials(self, exchange: str) -> Dict[str, str]:
        """
        Retrieve exchange API credentials from Vault
        
        Args:
            exchange: Exchange name ('deribit' or 'binance')
        
        Returns:
            Dictionary with 'api_key' and 'api_secret'
        """
        path = f"quanttrade/exchanges/{exchange}"
        try:
            credentials = self.get_secret(path)
            return {
                'api_key': credentials.get('api_key'),
                'api_secret': credentials.get('api_secret'),
                'testnet': credentials.get('testnet', True)
            }
        except Exception as e:
            logger.warning(f"Failed to get {exchange} credentials from Vault: {e}")
            # Fallback to environment variables
            return self._get_credentials_from_env(exchange)
    
    def _get_credentials_from_env(self, exchange: str) -> Dict[str, str]:
        """Fallback to environment variables if Vault is unavailable"""
        exchange_upper = exchange.upper()
        return {
            'api_key': os.getenv(f'{exchange_upper}_API_KEY', ''),
            'api_secret': os.getenv(f'{exchange_upper}_API_SECRET', ''),
            'testnet': os.getenv(f'{exchange_upper}_TESTNET', 'true').lower() == 'true'
        }
    
    def get_database_credentials(self) -> Dict[str, str]:
        """Retrieve database credentials from Vault"""
        try:
            credentials = self.get_secret('quanttrade/database')
            return {
                'host': credentials.get('host', 'localhost'),
                'port': credentials.get('port', 5432),
                'database': credentials.get('database', 'bizosaas'),
                'username': credentials.get('username', 'postgres'),
                'password': credentials.get('password')
            }
        except Exception as e:
            logger.warning(f"Failed to get database credentials from Vault: {e}")
            return {
                'host': os.getenv('DB_HOST', 'localhost'),
                'port': int(os.getenv('DB_PORT', '5432')),
                'database': os.getenv('DB_NAME', 'bizosaas'),
                'username': os.getenv('DB_USER', 'postgres'),
                'password': os.getenv('DB_PASSWORD', '')
            }
    
    def get_brain_api_credentials(self) -> Dict[str, str]:
        """Retrieve Brain API credentials from Vault"""
        try:
            credentials = self.get_secret('quanttrade/brain-api')
            return {
                'url': credentials.get('url', 'http://localhost:8002'),
                'api_key': credentials.get('api_key')
            }
        except Exception as e:
            logger.warning(f"Failed to get Brain API credentials from Vault: {e}")
            return {
                'url': os.getenv('BRAIN_API_URL', 'http://localhost:8002'),
                'api_key': os.getenv('BRAIN_API_KEY', '')
            }


# Singleton instance
@lru_cache(maxsize=1)
def get_vault_client() -> VaultClient:
    """Get or create Vault client singleton"""
    return VaultClient()


# Convenience functions
def get_deribit_credentials() -> Dict[str, str]:
    """Get Deribit API credentials"""
    return get_vault_client().get_exchange_credentials('deribit')


def get_binance_credentials() -> Dict[str, str]:
    """Get Binance API credentials"""
    return get_vault_client().get_exchange_credentials('binance')


def get_db_credentials() -> Dict[str, str]:
    """Get database credentials"""
    return get_vault_client().get_database_credentials()


def get_brain_credentials() -> Dict[str, str]:
    """Get Brain API credentials"""
    return get_vault_client().get_brain_api_credentials()
