"""
Configuration module with HashiCorp Vault integration
Provides centralized configuration management with secure secrets retrieval
"""

import os
import logging
from typing import Dict, Any, Optional
from pydantic_settings import BaseSettings
from pydantic import Field

# Import Vault helper
try:
    from vault_config_helper import (
        get_vault_secret,
        get_database_config,
        get_redis_config,
        VaultConfig
    )
    VAULT_ENABLED = True
except ImportError:
    VAULT_ENABLED = False
    print("⚠️  Vault configuration helper not available, using environment variables")

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings with Vault integration"""

    # Application
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8001, env="PORT")
    app_name: str = Field(default="CoreLDove Order Processing", env="APP_NAME")

    # Database configuration from Vault or environment
    database_url: Optional[str] = None

    # Redis configuration from Vault or environment
    redis_url: Optional[str] = None

    # Security configuration from Vault or environment
    jwt_secret_key: Optional[str] = None
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expiration_hours: int = Field(default=24, env="JWT_EXPIRATION_HOURS")

    # CORS
    cors_origins: list = Field(default=["*"], env="CORS_ORIGINS")

    # External Services
    saleor_api_url: str = Field(default="http://localhost:8000/api/brain/saleor", env="SALEOR_API_URL")
    brain_api_url: str = Field(default="http://localhost:8000/api/brain", env="BRAIN_API_URL")
    ai_crew_api_url: str = Field(default="http://localhost:8002/api/crew", env="AI_CREW_API_URL")

    # Vault configuration
    vault_addr: str = Field(default="http://bizosaas-vault:8200", env="VAULT_ADDR")
    vault_token: str = Field(default="bizosaas-dev-root-token", env="VAULT_TOKEN")
    vault_mount_path: str = Field(default="bizosaas", env="VAULT_MOUNT_PATH")

    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize Vault and retrieve secrets
        if VAULT_ENABLED:
            self._load_from_vault()
        else:
            self._load_from_env()

    def _load_from_vault(self):
        """Load configuration from Vault"""
        try:
            logger.info("Loading configuration from Vault...")

            # Get database configuration
            db_config = get_database_config()
            if db_config:
                self.database_url = f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config.get('database', 'bizosaas')}"
                logger.info("✅ Database configuration loaded from Vault")

            # Get Redis configuration
            redis_config = get_redis_config()
            if redis_config:
                self.redis_url = f"redis://{redis_config['host']}:{redis_config['port']}/0"
                logger.info("✅ Redis configuration loaded from Vault")

            # Get JWT secret (store if not exists)
            jwt_secret = get_vault_secret('platform/temporal-jwt-secret', 'secret_key')
            if jwt_secret:
                self.jwt_secret_key = jwt_secret
                logger.info("✅ JWT secret loaded from Vault")
            else:
                # If JWT secret doesn't exist, use environment or generate one
                self.jwt_secret_key = os.getenv('JWT_SECRET_KEY', 'insecure-jwt-key-change-in-production')
                logger.warning("⚠️  JWT secret not found in Vault, using environment variable")

        except Exception as e:
            logger.error(f"Failed to load configuration from Vault: {e}")
            logger.info("Falling back to environment variables")
            self._load_from_env()

    def _load_from_env(self):
        """Load configuration from environment variables"""
        logger.info("Loading configuration from environment variables...")

        self.database_url = os.getenv(
            'DATABASE_URL',
            'postgresql://postgres:password@localhost:5432/bizosaas_orders'
        )

        self.redis_url = os.getenv(
            'REDIS_URL',
            'redis://localhost:6379/0'
        )

        self.jwt_secret_key = os.getenv(
            'JWT_SECRET_KEY',
            'insecure-jwt-key-change-in-production'
        )

        logger.info("✅ Configuration loaded from environment variables")


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings