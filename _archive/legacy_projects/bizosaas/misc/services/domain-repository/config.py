"""
Configuration for Domain Repository Service

This module provides configuration management using Pydantic Settings.
"""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "BizOSaaS Domain Repository"
    version: str = "1.0.0"
    debug: bool = False
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8011
    reload: bool = True
    
    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://admin:securepassword@localhost:5432/bizosaas",
        env="DATABASE_URL"
    )
    database_echo: bool = False
    database_pool_size: int = 10
    database_max_overflow: int = 20
    
    # Event Bus
    event_bus_url: str = Field(
        default="http://localhost:8009",
        env="EVENT_BUS_URL"
    )
    enable_event_publishing: bool = Field(
        default=True,
        env="ENABLE_EVENT_PUBLISHING"
    )
    
    # Security
    secret_key: str = Field(
        default="your-super-secret-key-here-make-it-long-and-random-for-development",
        env="SECRET_KEY"
    )
    
    # CORS
    cors_origins: list = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    # Redis (for caching)
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL"
    )
    cache_ttl: int = 3600  # 1 hour default TTL
    
    # Multi-tenancy
    default_tenant_id: str = "00000000-0000-4000-8000-000000000001"
    
    # Performance
    max_page_size: int = 100
    default_page_size: int = 50
    request_timeout: int = 30
    
    # Monitoring
    enable_metrics: bool = True
    metrics_port: int = 9090
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get application settings (singleton)"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """Reload settings (useful for testing)"""
    global _settings
    _settings = Settings()
    return _settings