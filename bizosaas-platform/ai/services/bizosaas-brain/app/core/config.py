"""
Configuration settings for BizOSaaS Brain API
"""

import os
from typing import Optional

class Settings:
    """Configuration settings for the Brain API"""
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/bizosaas")
    
    # Superset configuration
    SUPERSET_URL: str = os.getenv("SUPERSET_URL", "http://localhost:8088")
    SUPERSET_USERNAME: str = os.getenv("SUPERSET_ADMIN_USERNAME", "admin")
    SUPERSET_PASSWORD: str = os.getenv("SUPERSET_ADMIN_PASSWORD", "admin_secure_password_2024")
    
    # Redis configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # ClickHouse configuration
    CLICKHOUSE_URL: str = os.getenv("CLICKHOUSE_URL", "http://localhost:8123")
    CLICKHOUSE_PASSWORD: str = os.getenv("CLICKHOUSE_PASSWORD", "clickhouse_secure_password_2024")
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-jwt-secret-change-in-production")
    
    # External API settings
    BRAIN_API_TOKEN: str = os.getenv("BRAIN_API_TOKEN", "brain_api_secure_token_2024")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

settings = Settings()