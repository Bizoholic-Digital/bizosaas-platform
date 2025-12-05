"""
QuantTrade Configuration Settings
"""
import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "QuantTrade AI Trading Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # API
    API_HOST: str = Field(default="0.0.0.0", env="API_HOST")
    API_PORT: int = Field(default=8012, env="API_PORT")
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3010", "http://localhost:3000"],
        env="CORS_ORIGINS"
    )
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/quanttrade",
        env="DATABASE_URL"
    )
    
    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL"
    )
    
    # Exchange API Keys - Deribit
    DERIBIT_API_KEY: str = Field(default="", env="DERIBIT_API_KEY")
    DERIBIT_API_SECRET: str = Field(default="", env="DERIBIT_API_SECRET")
    DERIBIT_TESTNET: bool = Field(default=True, env="DERIBIT_TESTNET")
    
    # Exchange API Keys - Binance
    BINANCE_API_KEY: str = Field(default="", env="BINANCE_API_KEY")
    BINANCE_API_SECRET: str = Field(default="", env="BINANCE_API_SECRET")
    BINANCE_TESTNET: bool = Field(default=True, env="BINANCE_TESTNET")
    
    # Brain API Integration
    BRAIN_API_URL: str = Field(
        default="http://localhost:8002",
        env="BRAIN_API_URL"
    )
    BRAIN_API_KEY: str = Field(default="", env="BRAIN_API_KEY")
    
    # Vault Integration
    VAULT_ADDR: str = Field(
        default="http://localhost:8200",
        env="VAULT_ADDR"
    )
    VAULT_TOKEN: str = Field(default="", env="VAULT_TOKEN")
    
    # Temporal Integration
    TEMPORAL_HOST: str = Field(
        default="localhost:7233",
        env="TEMPORAL_HOST"
    )
    TEMPORAL_NAMESPACE: str = Field(
        default="quanttrade",
        env="TEMPORAL_NAMESPACE"
    )
    
    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        env="SECRET_KEY"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Trading Settings
    DEFAULT_RISK_PER_TRADE: float = 0.02  # 2% risk per trade
    MAX_POSITION_SIZE: float = 0.1  # 10% max position size
    MAX_DAILY_LOSS: float = 0.02  # 2% max daily loss
    MAX_PORTFOLIO_RISK: float = 0.05  # 5% max portfolio risk
    POSITION_SIZE_METHOD: str = "kelly"  # kelly, fixed, risk_parity

    # WebSocket
    WS_HEARTBEAT_INTERVAL: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
