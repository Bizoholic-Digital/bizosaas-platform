import hvac
import os
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class VaultService:
    _instance = None
    _client: Optional[hvac.Client] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VaultService, cls).__new__(cls)
        return cls._instance

    def __init__(self, vault_url: Optional[str] = None):
        if self._client is None:
            self.vault_url = vault_url or os.getenv("VAULT_ADDR") or os.getenv("VAULT_URL", "https://vault.bizoholic.net")
            self.token = os.getenv("VAULT_TOKEN") 
            self.mount_point = os.getenv("VAULT_MOUNT_POINT", "secret")
            self.secret_path = os.getenv("VAULT_SECRET_PATH", "bizosaas/gateway/config")
            
            if self.token:
                try:
                    self._client = hvac.Client(url=self.vault_url, token=self.token)
                    if not self._client.is_authenticated():
                        logger.error("Vault authentication failed")
                        self._client = None
                    else:
                        logger.info(f"Connected to Vault at {self.vault_url} for {self.secret_path}")
                except Exception as e:
                    logger.error(f"Failed to connect to Vault: {str(e)}")
            else:
                logger.warning("VAULT_TOKEN not provided. Vault integration disabled.")

    def get_secret(self, key: str, default: Any = None) -> Any:
        # 1. Try Vault
        if self._client:
            try:
                read_response = self._client.secrets.kv.v2.read_secret_version(
                    path=self.secret_path,
                    mount_point=self.mount_point
                )
                secrets = read_response['data']['data']
                if key in secrets:
                    return secrets[key]
            except Exception as e:
                # Silently log debug if key is not in Vault
                pass

        # 2. Fallback to Environ (and .env already loaded by other things)
        return os.getenv(key, default)

# Singleton access
vault_service = VaultService()

def get_config_val(key: str, default: Any = None) -> Any:
    return vault_service.get_secret(key, default)
