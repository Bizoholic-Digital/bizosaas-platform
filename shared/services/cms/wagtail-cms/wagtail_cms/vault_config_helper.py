
import os
import hvac
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def get_vault_client() -> Optional[hvac.Client]:
    """Initialize Vault client."""
    vault_addr = os.getenv('VAULT_ADDR')
    vault_token = os.getenv('VAULT_TOKEN')
    
    if not vault_addr or not vault_token:
        logger.warning("VAULT_ADDR or VAULT_TOKEN not set. Using environment variables fallback.")
        return None
        
    try:
        client = hvac.Client(url=vault_addr, token=vault_token)
        if not client.is_authenticated():
            logger.error("Vault authentication failed.")
            return None
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Vault: {e}")
        return None

def get_secret(path: str, key: str = None, default: Any = None) -> Any:
    """Retrieve a secret from Vault with fallback to environment variables."""
    client = get_vault_client()
    
    if client:
        try:
            response = client.secrets.kv.v2.read_secret_version(path=path, mount_point='bizosaas')
            data = response['data']['data']
            if key:
                return data.get(key, default)
            return data
        except Exception as e:
            logger.warning(f"Failed to read secret {path} from Vault: {e}")
    
    # Fallback to environment variable if key is provided and matches env var pattern
    if key:
        env_var_name = key.upper()
        return os.getenv(env_var_name, default)
        
    return default

def get_database_config() -> Dict[str, str]:
    """Get database configuration from Vault or env vars."""
    db_config = get_secret('platform/database')
    
    if db_config:
        return {
            'HOST': db_config.get('host', 'localhost'),
            'PORT': db_config.get('port', '5432'),
            'NAME': db_config.get('database', 'wagtail'),
            'USER': db_config.get('username', 'wagtail'),
            'PASSWORD': db_config.get('password', ''),
        }
        
    return {
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'NAME': os.getenv('DB_NAME', 'wagtail'),
        'USER': os.getenv('DB_USER', 'wagtail'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
    }

def get_redis_config() -> str:
    """Get Redis URL from Vault or env vars."""
    redis_config = get_secret('platform/redis-connection')
    
    if redis_config:
        return redis_config.get('connection_string', 'redis://redis:6379/2')
        
    return os.getenv('REDIS_URL', 'redis://redis:6379/2')
