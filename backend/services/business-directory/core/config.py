"""
Business Directory Service Configuration
Centralized configuration management for the FastAPI Business Directory service
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseSettings, validator, Field
import os


class Settings(BaseSettings):
    """
    Application settings with environment variable support
    """
    
    # Application Info
    APP_NAME: str = "BizOSaaS Business Directory Service"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "AI-powered Business Directory with Multi-tenant Architecture"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8003
    DEBUG: bool = Field(default=False, env="DEBUG")
    RELOAD: bool = Field(default=False, env="RELOAD")
    
    # Environment
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://bizosaas:bizosaas123@localhost:5432/bizosaas",
        env="DATABASE_URL"
    )
    DATABASE_POOL_SIZE: int = Field(default=20, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(default=30, env="DATABASE_MAX_OVERFLOW")
    DATABASE_ECHO: bool = Field(default=False, env="DATABASE_ECHO")
    
    # Redis Configuration
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL"
    )
    REDIS_CACHE_TTL: int = Field(default=3600, env="REDIS_CACHE_TTL")  # 1 hour
    
    # Authentication & Security
    SECRET_KEY: str = Field(
        default="your-super-secret-key-change-this-in-production",
        env="SECRET_KEY"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    ALGORITHM: str = "HS256"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:3001", 
            "http://localhost:3002",
            "http://localhost:3003",
            "http://localhost:3004",
            "http://localhost:3005",
            "http://localhost:3006",
            "http://localhost:3007",
            "http://localhost:3008",
            "https://bizosaas.com",
            "https://admin.bizosaas.com",
            "https://client.bizosaas.com"
        ],
        env="CORS_ORIGINS"
    )
    
    # AI & Vector Search Configuration
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    EMBEDDING_MODEL: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        env="EMBEDDING_MODEL"
    )
    VECTOR_SEARCH_LIMIT: int = Field(default=20, env="VECTOR_SEARCH_LIMIT")
    SIMILARITY_THRESHOLD: float = Field(default=0.7, env="SIMILARITY_THRESHOLD")
    
    # File Storage Configuration
    UPLOAD_DIR: str = Field(default="uploads/business-directory", env="UPLOAD_DIR")
    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = Field(
        default=["image/jpeg", "image/png", "image/webp", "image/gif"],
        env="ALLOWED_IMAGE_TYPES"
    )
    
    # Business Directory Specific
    DEFAULT_SEARCH_RADIUS: float = Field(default=25.0, env="DEFAULT_SEARCH_RADIUS")  # kilometers
    MAX_SEARCH_RADIUS: float = Field(default=100.0, env="MAX_SEARCH_RADIUS")  # kilometers
    BUSINESS_APPROVAL_REQUIRED: bool = Field(default=True, env="BUSINESS_APPROVAL_REQUIRED")
    REVIEW_MODERATION_REQUIRED: bool = Field(default=True, env="REVIEW_MODERATION_REQUIRED")
    
    # Pagination Configuration
    DEFAULT_PAGE_SIZE: int = Field(default=20, env="DEFAULT_PAGE_SIZE")
    MAX_PAGE_SIZE: int = Field(default=100, env="MAX_PAGE_SIZE")
    
    # Email Configuration (for notifications)
    SMTP_HOST: Optional[str] = Field(default=None, env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USERNAME: Optional[str] = Field(default=None, env="SMTP_USERNAME")
    SMTP_PASSWORD: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    SMTP_TLS: bool = Field(default=True, env="SMTP_TLS")
    
    # External Services
    GOOGLE_MAPS_API_KEY: Optional[str] = Field(default=None, env="GOOGLE_MAPS_API_KEY")
    GEOCODING_SERVICE: str = Field(default="nominatim", env="GEOCODING_SERVICE")
    
    # Monitoring & Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    ENABLE_METRICS: bool = Field(default=True, env="ENABLE_METRICS")
    METRICS_PORT: int = Field(default=8004, env="METRICS_PORT")
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_REQUESTS_PER_MINUTE")
    RATE_LIMIT_SEARCH_PER_MINUTE: int = Field(default=30, env="RATE_LIMIT_SEARCH_PER_MINUTE")
    
    # Celery Configuration (Background Tasks)
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/1",
        env="CELERY_BROKER_URL"
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/1",
        env="CELERY_RESULT_BACKEND"
    )
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("ALLOWED_IMAGE_TYPES", pre=True)
    def parse_allowed_image_types(cls, v):
        """Parse allowed image types from string or list"""
        if isinstance(v, str):
            return [mime_type.strip() for mime_type in v.split(",")]
        return v
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.ENVIRONMENT.lower() == "development"
    
    @property
    def database_config(self) -> Dict[str, Any]:
        """Get database configuration for SQLAlchemy"""
        return {
            "pool_size": self.DATABASE_POOL_SIZE,
            "max_overflow": self.DATABASE_MAX_OVERFLOW,
            "echo": self.DATABASE_ECHO and self.is_development,
            "pool_pre_ping": True,
            "pool_recycle": 3600,  # 1 hour
        }
    
    @property
    def redis_config(self) -> Dict[str, Any]:
        """Get Redis configuration"""
        return {
            "url": self.REDIS_URL,
            "encoding": "utf-8",
            "decode_responses": True,
            "health_check_interval": 30,
            "retry_on_timeout": True,
        }
    
    def get_api_prefix(self) -> str:
        """Get API prefix for FastAPI routing"""
        return "/api/brain/business-directory"
    
    def get_docs_config(self) -> Dict[str, Any]:
        """Get documentation configuration"""
        return {
            "title": self.APP_NAME,
            "description": self.APP_DESCRIPTION,
            "version": self.APP_VERSION,
            "docs_url": "/docs" if not self.is_production else None,
            "redoc_url": "/redoc" if not self.is_production else None,
            "openapi_url": "/openapi.json" if not self.is_production else None,
        }
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


# Service Registry Configuration
SERVICE_REGISTRY = {
    "business_directory": {
        "name": "Business Directory Service",
        "version": settings.APP_VERSION,
        "port": settings.PORT,
        "health_endpoint": "/health",
        "metrics_endpoint": "/metrics",
        "api_prefix": settings.get_api_prefix(),
        "dependencies": [
            "postgresql",
            "redis",
            "openai" if settings.OPENAI_API_KEY else None
        ]
    }
}

# Database Table Configurations
TABLE_CONFIG = {
    "tenant_isolation": True,
    "soft_delete": True,
    "audit_fields": True,
    "vector_search": True,
    "full_text_search": True,
}

# AI Configuration
AI_CONFIG = {
    "embedding_dimensions": 384,  # all-MiniLM-L6-v2 dimensions
    "batch_size": 32,
    "max_tokens": 512,
    "similarity_functions": ["cosine", "euclidean", "dot_product"],
    "search_types": ["semantic", "keyword", "hybrid"],
}

# Cache Configuration
CACHE_CONFIG = {
    "business_details": {"ttl": 3600, "prefix": "biz:"},
    "search_results": {"ttl": 1800, "prefix": "search:"},
    "categories": {"ttl": 7200, "prefix": "cat:"},
    "location_cache": {"ttl": 86400, "prefix": "loc:"},
}