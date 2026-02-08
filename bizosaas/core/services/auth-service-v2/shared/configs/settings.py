"""
Shared configuration settings for BizoSaaS platform
"""
import os
from typing import List, Optional
from pydantic import BaseSettings, PostgresDsn, RedisDsn, Field, validator


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    APP_NAME: str = "BizoSaaS"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field("development", env="ENVIRONMENT")
    DEBUG: bool = Field(False, env="DEBUG")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    
    # API Configuration  
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://app.bizosaas.local"],
        env="CORS_ORIGINS"
    )
    
    # Database
    POSTGRES_HOST: str = Field(..., env="POSTGRES_HOST")
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER") 
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")
    POSTGRES_PORT: int = Field(5432, env="POSTGRES_PORT")
    DATABASE_URL: Optional[PostgresDsn] = None
    
    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v, values):
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=str(values.get("POSTGRES_PORT")),
            path=f"/{values.get('POSTGRES_DB') or ''}"
        )
    
    # Redis
    REDIS_HOST: str = Field(..., env="REDIS_HOST")
    REDIS_PORT: int = Field(6379, env="REDIS_PORT")
    REDIS_PASSWORD: Optional[str] = Field(None, env="REDIS_PASSWORD")
    REDIS_DB: int = Field(0, env="REDIS_DB")
    REDIS_URL: Optional[RedisDsn] = None
    
    @validator("REDIS_URL", pre=True)
    def assemble_redis_connection(cls, v, values):
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme="redis",
            password=values.get("REDIS_PASSWORD"),
            host=values.get("REDIS_HOST"),
            port=str(values.get("REDIS_PORT")),
            path=f"/{values.get('REDIS_DB') or 0}"
        )
    
    # JWT Authentication
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # AI Services
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    OPENAI_BASE_URL: str = Field("https://openrouter.ai/api/v1", env="OPENAI_BASE_URL")
    OPENROUTER_API_KEY: Optional[str] = Field(None, env="OPENROUTER_API_KEY")
    
    # External APIs
    GOOGLE_ADS_DEVELOPER_TOKEN: Optional[str] = Field(None, env="GOOGLE_ADS_DEVELOPER_TOKEN")
    META_ADS_ACCESS_TOKEN: Optional[str] = Field(None, env="META_ADS_ACCESS_TOKEN") 
    LINKEDIN_ADS_ACCESS_TOKEN: Optional[str] = Field(None, env="LINKEDIN_ADS_ACCESS_TOKEN")
    
    # Stripe
    STRIPE_SECRET_KEY: Optional[str] = Field(None, env="STRIPE_SECRET_KEY")
    STRIPE_PUBLISHABLE_KEY: Optional[str] = Field(None, env="STRIPE_PUBLISHABLE_KEY")
    STRIPE_WEBHOOK_SECRET: Optional[str] = Field(None, env="STRIPE_WEBHOOK_SECRET")
    
    # Email
    SMTP_HOST: Optional[str] = Field(None, env="SMTP_HOST")
    SMTP_PORT: int = Field(587, env="SMTP_PORT")
    SMTP_USER: Optional[str] = Field(None, env="SMTP_USER")
    SMTP_PASSWORD: Optional[str] = Field(None, env="SMTP_PASSWORD")
    FROM_EMAIL: str = Field("noreply@bizosaas.com", env="FROM_EMAIL")
    
    # Security
    BCRYPT_ROUNDS: int = 12
    MAX_LOGIN_ATTEMPTS: int = 5
    LOGIN_LOCKOUT_MINUTES: int = 15
    
    # Feature Flags
    ENABLE_REGISTRATION: bool = Field(True, env="ENABLE_REGISTRATION")
    ENABLE_EMAIL_VERIFICATION: bool = Field(True, env="ENABLE_EMAIL_VERIFICATION")
    ENABLE_TWO_FACTOR: bool = Field(False, env="ENABLE_TWO_FACTOR")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(100, env="RATE_LIMIT_PER_MINUTE")
    RATE_LIMIT_BURST: int = Field(200, env="RATE_LIMIT_BURST")
    
    # File Storage
    STORAGE_TYPE: str = Field("local", env="STORAGE_TYPE")  # local, s3, minio
    STORAGE_BUCKET: Optional[str] = Field(None, env="STORAGE_BUCKET")
    MAX_FILE_SIZE_MB: int = Field(10, env="MAX_FILE_SIZE_MB")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


class DatabaseSettings(BaseSettings):
    """Database-specific settings"""
    
    POOL_SIZE: int = Field(10, env="DB_POOL_SIZE")
    MAX_OVERFLOW: int = Field(20, env="DB_MAX_OVERFLOW")
    POOL_TIMEOUT: int = Field(30, env="DB_POOL_TIMEOUT")
    POOL_RECYCLE: int = Field(3600, env="DB_POOL_RECYCLE")
    ECHO_SQL: bool = Field(False, env="DB_ECHO_SQL")
    
    class Config:
        env_file = ".env"


class RedisSettings(BaseSettings):
    """Redis-specific settings"""
    
    CONNECTION_POOL_SIZE: int = Field(10, env="REDIS_POOL_SIZE")
    SOCKET_TIMEOUT: int = Field(5, env="REDIS_SOCKET_TIMEOUT")
    SOCKET_CONNECT_TIMEOUT: int = Field(5, env="REDIS_CONNECT_TIMEOUT")
    RETRY_ON_TIMEOUT: bool = Field(True, env="REDIS_RETRY_ON_TIMEOUT")
    
    # Cache TTL settings (in seconds)
    DEFAULT_TTL: int = Field(3600, env="CACHE_DEFAULT_TTL")  # 1 hour
    USER_CACHE_TTL: int = Field(1800, env="CACHE_USER_TTL")  # 30 minutes
    SESSION_TTL: int = Field(86400, env="CACHE_SESSION_TTL")  # 24 hours
    
    class Config:
        env_file = ".env"


# Specialized settings instances
db_settings = DatabaseSettings()
redis_settings = RedisSettings()