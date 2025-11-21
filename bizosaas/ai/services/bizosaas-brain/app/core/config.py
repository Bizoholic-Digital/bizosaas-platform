"""
Configuration settings for BizOSaaS Brain API
Uses HashiCorp Vault for secure secret management
"""

import os
from typing import Optional
import sys

# Add vault_client to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

try:
    from vault_client import get_vault_client
    VAULT_AVAILABLE = True
except ImportError:
    VAULT_AVAILABLE = False
    print("WARNING: VaultClient not available, falling back to environment variables")

class Settings:
    """Configuration settings for the Brain API"""
    
    def __init__(self):
        """Initialize settings from Vault or environment variables"""
        self._vault = None
        if VAULT_AVAILABLE:
            try:
                self._vault = get_vault_client()
                health = self._vault.health_check()
                if not health.get('vault_connected'):
                    print(f"WARNING: Vault not connected: {health.get('error')}, using environment variables")
                    self._vault = None
            except Exception as e:
                print(f"WARNING: Failed to initialize Vault client: {e}, using environment variables")
                self._vault = None
        
        self._load_config()
    
    def _load_config(self):
        """Load configuration from Vault or environment variables"""
        if self._vault:
            try:
                # Load from Vault
                db_config = self._vault.get_database_config()
                redis_config = self._vault.get_redis_config()
                django_config = self._vault.get_django_config()
                
                # Database settings
                self.DATABASE_URL = db_config.get('url', os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/bizosaas"))
                
                # Redis configuration
                self.REDIS_URL = redis_config.get('url', os.getenv("REDIS_URL", "redis://localhost:6379"))
                
                # Security settings from Django config
                self.SECRET_KEY = django_config.get('secret_key', os.getenv("SECRET_KEY", "your-secret-key-change-in-production"))
                self.JWT_SECRET = django_config.get('jwt_secret', os.getenv("JWT_SECRET", "your-jwt-secret-change-in-production"))
                
                # Try to get service-specific config
                try:
                    superset_config = self._vault.get_service_config('superset')
                    self.SUPERSET_URL = superset_config.get('url', os.getenv("SUPERSET_URL", "http://localhost:8088"))
                    self.SUPERSET_USERNAME = superset_config.get('username', os.getenv("SUPERSET_ADMIN_USERNAME", "admin"))
                    self.SUPERSET_PASSWORD = superset_config.get('password', os.getenv("SUPERSET_ADMIN_PASSWORD", "admin_secure_password_2024"))
                except:
                    # Fallback to environment variables if service config not in Vault
                    self.SUPERSET_URL = os.getenv("SUPERSET_URL", "http://localhost:8088")
                    self.SUPERSET_USERNAME = os.getenv("SUPERSET_ADMIN_USERNAME", "admin")
                    self.SUPERSET_PASSWORD = os.getenv("SUPERSET_ADMIN_PASSWORD", "admin_secure_password_2024")
                
                try:
                    clickhouse_config = self._vault.get_service_config('clickhouse')
                    self.CLICKHOUSE_URL = clickhouse_config.get('url', os.getenv("CLICKHOUSE_URL", "http://localhost:8123"))
                    self.CLICKHOUSE_PASSWORD = clickhouse_config.get('password', os.getenv("CLICKHOUSE_PASSWORD", "clickhouse_secure_password_2024"))
                except:
                    self.CLICKHOUSE_URL = os.getenv("CLICKHOUSE_URL", "http://localhost:8123")
                    self.CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "clickhouse_secure_password_2024")
                
                # External API settings
                self.BRAIN_API_TOKEN = os.getenv("BRAIN_API_TOKEN", "brain_api_secure_token_2024")
                
                print("INFO: Configuration loaded from Vault successfully")
                
            except Exception as e:
                print(f"WARNING: Failed to load config from Vault: {e}, using environment variables")
                self._load_from_env()
        else:
            self._load_from_env()
        
        # Environment settings (always from env)
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
        self.DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    
    def _load_from_env(self):
        """Fallback: Load all settings from environment variables"""
        self.DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/bizosaas")
        self.SUPERSET_URL = os.getenv("SUPERSET_URL", "http://localhost:8088")
        self.SUPERSET_USERNAME = os.getenv("SUPERSET_ADMIN_USERNAME", "admin")
        self.SUPERSET_PASSWORD = os.getenv("SUPERSET_ADMIN_PASSWORD", "admin_secure_password_2024")
        self.REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.CLICKHOUSE_URL = os.getenv("CLICKHOUSE_URL", "http://localhost:8123")
        self.CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "clickhouse_secure_password_2024")
        self.SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
        self.JWT_SECRET = os.getenv("JWT_SECRET", "your-jwt-secret-change-in-production")
        self.BRAIN_API_TOKEN = os.getenv("BRAIN_API_TOKEN", "brain_api_secure_token_2024")

settings = Settings()