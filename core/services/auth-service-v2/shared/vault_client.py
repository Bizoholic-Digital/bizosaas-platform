"""
HashiCorp Vault Client for BizOSaaS
Secure credential management across all services
"""

import os
import json
import logging
import requests
from typing import Dict, Any, Optional
from dataclasses import dataclass
from functools import lru_cache

logger = logging.getLogger(__name__)

@dataclass
class VaultConfig:
    """Vault configuration"""
    url: str = "http://localhost:8200"
    token: str = "bizosaas-root-token"
    mount_point: str = "bizosaas"
    timeout: int = 30

class VaultClient:
    """
    Secure HashiCorp Vault client for BizOSaas credential management
    
    Usage:
        vault = VaultClient()
        db_creds = vault.get_database_credentials("coreldove")
        api_key = vault.get_api_key("openrouter")
    """
    
    def __init__(self, config: Optional[VaultConfig] = None):
        self.config = config or VaultConfig()
        self.session = requests.Session()
        self.session.headers.update({
            "X-Vault-Token": self.config.token,
            "Content-Type": "application/json"
        })
        
    def _make_request(self, method: str, path: str, data: Dict = None) -> Dict[str, Any]:
        """Make authenticated request to Vault"""
        url = f"{self.config.url}/v1/{path}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json() if response.content else {}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Vault request failed: {e}")
            raise VaultConnectionError(f"Failed to connect to Vault: {e}")
    
    def get_secret(self, path: str) -> Dict[str, Any]:
        """Get secret from Vault KV store"""
        full_path = f"{self.config.mount_point}/data/{path}"
        response = self._make_request("GET", full_path)
        
        if "data" in response and "data" in response["data"]:
            return response["data"]["data"]
        else:
            raise VaultSecretNotFound(f"Secret not found at path: {path}")
    
    @lru_cache(maxsize=100)
    def get_database_credentials(self, project: str) -> Dict[str, str]:
        """Get database credentials for a specific project"""
        try:
            # Try project-specific credentials first
            if project in ["coreldove", "bizoholic", "thrillring", "analytics", "readonly", "n8n"]:
                project_creds = self.get_secret(f"postgresql/{project}")
                
                # If only password is stored, combine with main DB config
                if "password" in project_creds and len(project_creds) == 1:
                    main_creds = self.get_secret("postgresql/main")
                    return {
                        **main_creds,
                        "password": project_creds["password"],
                        "database": project if project != "main" else main_creds.get("database", "postgres")
                    }
                else:
                    return project_creds
            else:
                # Fallback to main database
                return self.get_secret("postgresql/main")
                
        except VaultSecretNotFound:
            logger.warning(f"Database credentials not found for {project}, using main")
            return self.get_secret("postgresql/main")
    
    @lru_cache(maxsize=50)
    def get_api_key(self, service: str) -> str:
        """Get API key for external service"""
        secret = self.get_secret(f"api-keys/{service}")
        
        # Handle different key formats
        if "api_key" in secret:
            return secret["api_key"]
        elif "token" in secret:
            return secret["token"]
        else:
            # Return the first value if key name is unclear
            return next(iter(secret.values()))
    
    def get_service_credentials(self, service: str) -> Dict[str, str]:
        """Get complete credentials for a service"""
        return self.get_secret(service)
    
    def get_telegram_bot_token(self, bot_name: str) -> str:
        """Get Telegram bot token"""
        secret = self.get_secret(f"telegram-bots/{bot_name}")
        return secret["token"]
    
    def get_infrastructure_credentials(self, provider: str) -> Dict[str, str]:
        """Get infrastructure provider credentials"""
        return self.get_secret(f"infrastructure/{provider}")
    
    def health_check(self) -> bool:
        """Check if Vault is healthy and accessible"""
        try:
            response = self._make_request("GET", "sys/health")
            return response.get("sealed", True) is False
        except Exception as e:
            logger.error(f"Vault health check failed: {e}")
            return False

# Custom Exceptions
class VaultConnectionError(Exception):
    """Raised when unable to connect to Vault"""
    pass

class VaultSecretNotFound(Exception):
    """Raised when secret is not found in Vault"""
    pass

# Convenience functions for common use cases
def get_database_url(project: str) -> str:
    """Get database URL for a project"""
    vault = VaultClient()
    creds = vault.get_database_credentials(project)
    
    return f"postgresql://{creds['user']}:{creds['password']}@{creds['host']}:{creds['port']}/{creds.get('database', project)}"

def get_redis_url() -> str:
    """Get Redis/Dragonfly URL"""
    vault = VaultClient()
    creds = vault.get_service_credentials("dragonfly")
    
    if creds.get("password"):
        return f"redis://:{creds['password']}@{creds['host']}:{creds['port']}"
    else:
        return f"redis://{creds['host']}:{creds['port']}"

def get_openrouter_key() -> str:
    """Get OpenRouter API key for CrewAI"""
    vault = VaultClient()
    return vault.get_api_key("openrouter")

def get_n8n_credentials() -> Dict[str, str]:
    """Get n8n credentials"""
    vault = VaultClient()
    return vault.get_service_credentials("n8n")

def get_amazon_credentials() -> Dict[str, str]:
    """Get Amazon credentials"""
    vault = VaultClient()
    return vault.get_service_credentials("api-keys/amazon")

def get_wordpress_credentials() -> Dict[str, str]:
    """Get WordPress admin credentials"""
    vault = VaultClient()
    return vault.get_service_credentials("wordpress")

# Environment variable integration
def init_environment_from_vault():
    """
    Initialize environment variables from Vault
    Useful for applications that still rely on environment variables
    """
    vault = VaultClient()
    
    try:
        # Set database URLs
        for project in ["coreldove", "bizoholic", "thrillring"]:
            os.environ[f"{project.upper()}_DATABASE_URL"] = get_database_url(project)
        
        # Set Redis URL
        os.environ["REDIS_URL"] = get_redis_url()
        
        # Set API keys
        os.environ["OPENROUTER_API_KEY"] = get_openrouter_key()
        
        # Set other common environment variables
        n8n_creds = get_n8n_credentials()
        os.environ["N8N_HOST"] = n8n_creds["host"]
        os.environ["N8N_WEBHOOK_URL"] = n8n_creds["webhook_url"]
        
        logger.info("Environment variables initialized from Vault")
        
    except Exception as e:
        logger.error(f"Failed to initialize environment from Vault: {e}")
        raise

if __name__ == "__main__":
    # Test the Vault client
    vault = VaultClient()
    
    print("🔐 Testing Vault Client...")
    
    if vault.health_check():
        print("✅ Vault is healthy")
        
        # Test retrieving some credentials
        try:
            db_creds = vault.get_database_credentials("coreldove")
            print(f"✅ CoreLDove DB: {db_creds['host']}:{db_creds['port']}")
            
            api_key = vault.get_api_key("openrouter")
            print(f"✅ OpenRouter API: {api_key[:10]}...")
            
            print("🎉 Vault client working correctly!")
            
        except Exception as e:
            print(f"❌ Error retrieving secrets: {e}")
    else:
        print("❌ Vault health check failed")