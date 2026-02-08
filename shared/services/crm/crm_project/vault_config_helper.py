"""
Vault Configuration Helper for BizOSaaS Services
Provides simple utilities for services to retrieve secrets from HashiCorp Vault

This module can be copied into each service or imported as a shared library.
All services can use this to migrate from environment variables to Vault.

Usage Examples:

1. Django/Wagtail Settings:
    from vault_config_helper import get_vault_secret, get_database_config

    SECRET_KEY = get_vault_secret('platform/django-secret-key', 'secret_key', fallback=os.getenv('SECRET_KEY'))
    db_config = get_database_config()
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db_config['database'],
            'USER': db_config['username'],
            'PASSWORD': db_config['password'],
            'HOST': db_config['host'],
            'PORT': db_config['port'],
        }
    }

2. Saleor Settings:
    from vault_config_helper import get_vault_secret

    SECRET_KEY = get_vault_secret('platform/saleor-secret-key', 'secret_key', fallback=os.environ.get('SECRET_KEY'))

3. FastAPI/Temporal Services:
    from vault_config_helper import VaultConfig

    vault = VaultConfig()
    redis_config = vault.get_secret('platform/redis-connection')
    REDIS_URL = redis_config.get('connection_string')
"""

import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class VaultConfig:
    """
    Lightweight Vault client for service configuration
    Provides fallback to environment variables if Vault is unavailable
    """

    def __init__(
        self,
        vault_addr: Optional[str] = None,
        vault_token: Optional[str] = None,
        mount_path: str = "bizosaas"
    ):
        """
        Initialize Vault configuration helper

        Args:
            vault_addr: Vault server address (default: from VAULT_ADDR env or http://bizosaas-vault:8200)
            vault_token: Vault authentication token (default: from VAULT_TOKEN env)
            mount_path: KV v2 mount path (default: bizosaas)
        """
        self.vault_addr = vault_addr or os.getenv('VAULT_ADDR', 'http://bizosaas-vault:8200')
        self.vault_token = vault_token or os.getenv('VAULT_TOKEN', 'bizosaas-dev-root-token')
        self.mount_path = mount_path
        self.client = None
        self._vault_available = False

        try:
            import hvac
            self.client = hvac.Client(url=self.vault_addr, token=self.vault_token)

            # Test connection
            if self.client.is_authenticated():
                self._vault_available = True
                logger.info(f"✅ Vault connected: {self.vault_addr}")
            else:
                logger.warning(f"⚠️  Vault authentication failed, using fallback values")
        except ImportError:
            logger.warning("⚠️  hvac library not installed. Install with: pip install hvac==2.1.0")
        except Exception as e:
            logger.warning(f"⚠️  Vault connection failed: {e}. Using fallback values.")

    def get_secret(self, path: str, key: Optional[str] = None, fallback: Any = None) -> Any:
        """
        Retrieve secret from Vault with automatic fallback

        Args:
            path: Secret path in Vault (e.g., 'platform/database' or 'platform/django-secret-key')
            key: Specific key within the secret (optional, returns entire secret if None)
            fallback: Fallback value if Vault is unavailable or secret not found

        Returns:
            Secret value(s) or fallback

        Examples:
            # Get entire secret object
            db_config = vault.get_secret('platform/database')

            # Get specific key from secret
            db_password = vault.get_secret('platform/database', 'password', fallback='default_pass')
        """
        if not self._vault_available:
            logger.debug(f"Vault unavailable, using fallback for {path}")
            return fallback

        try:
            response = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                mount_point=self.mount_path
            )

            if response and 'data' in response and 'data' in response['data']:
                secret_data = response['data']['data']

                if key:
                    return secret_data.get(key, fallback)
                else:
                    return secret_data
            else:
                logger.warning(f"No data at Vault path: {path}, using fallback")
                return fallback

        except Exception as e:
            logger.warning(f"Failed to retrieve {path} from Vault: {e}. Using fallback.")
            return fallback

    def is_available(self) -> bool:
        """Check if Vault is available and authenticated"""
        return self._vault_available


# Global singleton instance
_vault_instance: Optional[VaultConfig] = None

def get_vault_config() -> VaultConfig:
    """Get or create global VaultConfig instance"""
    global _vault_instance
    if _vault_instance is None:
        _vault_instance = VaultConfig()
    return _vault_instance


# Convenience functions for common configurations

def get_vault_secret(path: str, key: Optional[str] = None, fallback: Any = None) -> Any:
    """
    Simple function to get secret from Vault with fallback

    Usage:
        SECRET_KEY = get_vault_secret('platform/django-secret-key', 'secret_key',
                                       fallback=os.getenv('SECRET_KEY'))
    """
    vault = get_vault_config()
    return vault.get_secret(path, key, fallback)


def get_database_config() -> Dict[str, str]:
    """
    Get PostgreSQL database configuration from Vault

    Returns dict with keys: host, port, database, username, password
    Falls back to environment variables if Vault unavailable
    """
    vault = get_vault_config()

    # Try Vault first
    db_config = vault.get_secret('platform/database')

    if db_config:
        return {
            'host': db_config.get('host', 'bizosaas-postgres-unified'),
            'port': db_config.get('port', '5432'),
            'database': db_config.get('database', 'bizosaas'),
            'username': db_config.get('username', 'postgres'),
            'password': db_config.get('password', ''),
        }

    # Fallback to environment variables
    return {
        'host': os.getenv('POSTGRES_HOST', 'bizosaas-postgres-unified'),
        'port': os.getenv('POSTGRES_PORT', '5432'),
        'database': os.getenv('POSTGRES_DB', 'bizosaas'),
        'username': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', ''),
    }


def get_redis_config() -> Dict[str, str]:
    """
    Get Redis configuration from Vault

    Returns dict with keys: host, port, connection_string
    Falls back to environment variables if Vault unavailable
    """
    vault = get_vault_config()

    # Try Vault first
    redis_config = vault.get_secret('platform/redis-connection')

    if redis_config:
        return {
            'host': redis_config.get('host', 'bizosaas-redis'),
            'port': redis_config.get('port', '6379'),
            'connection_string': redis_config.get('connection_string', 'redis://bizosaas-redis:6379/0'),
        }

    # Fallback to environment variables
    return {
        'host': os.getenv('REDIS_HOST', 'bizosaas-redis'),
        'port': os.getenv('REDIS_PORT', '6379'),
        'connection_string': os.getenv('REDIS_URL', 'redis://bizosaas-redis:6379/0'),
    }


def get_temporal_config() -> Dict[str, str]:
    """
    Get Temporal workflow engine configuration from Vault

    Returns dict with keys: host, port, namespace, connection_string
    Falls back to environment variables if Vault unavailable
    """
    vault = get_vault_config()

    # Try Vault first
    temporal_config = vault.get_secret('platform/temporal-connection')

    if temporal_config:
        return {
            'host': temporal_config.get('host', 'temporal'),
            'port': temporal_config.get('port', '7233'),
            'namespace': temporal_config.get('namespace', 'bizosaas'),
            'connection_string': temporal_config.get('connection_string', 'temporal:7233'),
        }

    # Fallback to environment variables
    return {
        'host': os.getenv('TEMPORAL_HOST', 'temporal'),
        'port': os.getenv('TEMPORAL_PORT', '7233'),
        'namespace': os.getenv('TEMPORAL_NAMESPACE', 'bizosaas'),
        'connection_string': os.getenv('TEMPORAL_URL', 'temporal:7233'),
    }


def get_django_secret_key(service_name: str = 'django-crm') -> str:
    """
    Get Django SECRET_KEY from Vault for a specific service

    Args:
        service_name: Service identifier (django-crm, wagtail, saleor)

    Returns:
        SECRET_KEY string
    """
    vault = get_vault_config()

    # Try service-specific secret key
    secret_key = vault.get_secret(f'platform/{service_name}-secret-key', 'secret_key')

    if secret_key:
        return secret_key

    # Fallback to environment variable
    return os.getenv('SECRET_KEY', 'insecure-change-this-in-production')


def get_openrouter_config() -> Dict[str, str]:
    """
    Get OpenRouter API configuration from Vault

    Returns dict with api_key and base_url
    """
    vault = get_vault_config()

    config = vault.get_secret('platform/openrouter-api-key')

    if config:
        return {
            'api_key': config.get('api_key', ''),
            'base_url': 'https://openrouter.ai/api/v1',
        }

    # Fallback
    return {
        'api_key': os.getenv('OPENROUTER_API_KEY', os.getenv('OPENAI_API_KEY', '')),
        'base_url': 'https://openrouter.ai/api/v1',
    }


# Health check function
def vault_health_check() -> Dict[str, Any]:
    """
    Check Vault connectivity and return status

    Returns:
        Dict with 'available', 'addr', and 'authenticated' keys
    """
    vault = get_vault_config()

    return {
        'available': vault.is_available(),
        'addr': vault.vault_addr,
        'authenticated': vault._vault_available,
        'mount_path': vault.mount_path,
    }


if __name__ == '__main__':
    # Test the vault configuration
    import sys

    logging.basicConfig(level=logging.INFO)

    print("\n🔐 Testing Vault Configuration Helper\n")
    print("=" * 60)

    # Health check
    health = vault_health_check()
    print(f"\n✅ Vault Health Check:")
    print(f"   Available: {health['available']}")
    print(f"   Address: {health['addr']}")
    print(f"   Authenticated: {health['authenticated']}")

    if not health['available']:
        print("\n⚠️  Vault not available - testing fallback mode")

    # Test database config
    print(f"\n📊 Database Configuration:")
    db_config = get_database_config()
    print(f"   Host: {db_config['host']}")
    print(f"   Port: {db_config['port']}")
    print(f"   Database: {db_config['database']}")
    print(f"   Username: {db_config['username']}")
    print(f"   Password: {'*' * len(db_config['password']) if db_config['password'] else 'NOT SET'}")

    # Test Redis config
    print(f"\n🔴 Redis Configuration:")
    redis_config = get_redis_config()
    print(f"   Host: {redis_config['host']}")
    print(f"   Port: {redis_config['port']}")
    print(f"   Connection: {redis_config['connection_string']}")

    # Test Temporal config
    print(f"\n⏱️  Temporal Configuration:")
    temporal_config = get_temporal_config()
    print(f"   Host: {temporal_config['host']}")
    print(f"   Port: {temporal_config['port']}")
    print(f"   Namespace: {temporal_config['namespace']}")

    # Test Django secret key
    print(f"\n🔑 Django Secret Key:")
    secret_key = get_django_secret_key('django-crm')
    print(f"   Length: {len(secret_key)} characters")
    print(f"   Preview: {secret_key[:10]}..." if len(secret_key) > 10 else f"   Value: {secret_key}")

    # Test OpenRouter config
    print(f"\n🤖 OpenRouter Configuration:")
    openrouter_config = get_openrouter_config()
    api_key = openrouter_config['api_key']
    print(f"   API Key: {api_key[:15]}..." if api_key else "   API Key: NOT SET")
    print(f"   Base URL: {openrouter_config['base_url']}")

    print("\n" + "=" * 60)
    print("✅ Vault configuration helper test complete!\n")