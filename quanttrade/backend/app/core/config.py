"""
QuantTrade Backend Configuration
Settings for the AI-Powered Trading Platform
"""

import os
from typing import List, Optional
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Application
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    SECRET_KEY: str = Field(default="quanttrade-secret-key", env="SECRET_KEY")
    ALLOWED_HOSTS: List[str] = Field(default=["*"], env="ALLOWED_HOSTS")

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://quanttrade:quanttrade@localhost:5432/quanttrade",
        env="DATABASE_URL"
    )
    DATABASE_POOL_SIZE: int = Field(default=10, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(default=20, env="DATABASE_MAX_OVERFLOW")

    # Redis Cache
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    REDIS_CACHE_TTL: int = Field(default=300, env="REDIS_CACHE_TTL")  # 5 minutes

    # Market Data APIs
    ALPHA_VANTAGE_API_KEY: Optional[str] = Field(default=None, env="ALPHA_VANTAGE_API_KEY")
    YAHOO_FINANCE_ENABLED: bool = Field(default=True, env="YAHOO_FINANCE_ENABLED")
    POLYGON_API_KEY: Optional[str] = Field(default=None, env="POLYGON_API_KEY")
    FINNHUB_API_KEY: Optional[str] = Field(default=None, env="FINNHUB_API_KEY")

    # AI Services
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    LANGCHAIN_TRACING_V2: bool = Field(default=False, env="LANGCHAIN_TRACING_V2")
    LANGCHAIN_API_KEY: Optional[str] = Field(default=None, env="LANGCHAIN_API_KEY")

    # CrewAI Configuration
    CREWAI_MODEL: str = Field(default="gpt-4", env="CREWAI_MODEL")
    CREWAI_TEMPERATURE: float = Field(default=0.1, env="CREWAI_TEMPERATURE")
    CREWAI_MAX_TOKENS: int = Field(default=2000, env="CREWAI_MAX_TOKENS")

    # Trading Configuration
    DEFAULT_PORTFOLIO_VALUE: float = Field(default=100000.0, env="DEFAULT_PORTFOLIO_VALUE")
    MAX_POSITION_SIZE: float = Field(default=0.1, env="MAX_POSITION_SIZE")  # 10% of portfolio
    RISK_FREE_RATE: float = Field(default=0.02, env="RISK_FREE_RATE")  # 2% risk-free rate
    COMMISSION_RATE: float = Field(default=0.001, env="COMMISSION_RATE")  # 0.1% commission

    # Backtesting
    DEFAULT_BACKTEST_START: str = Field(default="2020-01-01", env="DEFAULT_BACKTEST_START")
    DEFAULT_BACKTEST_END: str = Field(default="2024-01-01", env="DEFAULT_BACKTEST_END")
    BACKTEST_CACHE_TTL: int = Field(default=3600, env="BACKTEST_CACHE_TTL")  # 1 hour

    # Real-time Data
    MARKET_DATA_UPDATE_INTERVAL: int = Field(default=5, env="MARKET_DATA_UPDATE_INTERVAL")  # 5 seconds
    WEBSOCKET_HEARTBEAT_INTERVAL: int = Field(default=30, env="WEBSOCKET_HEARTBEAT_INTERVAL")  # 30 seconds

    # Security
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ENABLE_CORS: bool = Field(default=True, env="ENABLE_CORS")

    # Monitoring
    PROMETHEUS_ENABLED: bool = Field(default=True, env="PROMETHEUS_ENABLED")
    PROMETHEUS_PORT: int = Field(default=9090, env="PROMETHEUS_PORT")

    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(default="json", env="LOG_FORMAT")
    LOG_FILE: Optional[str] = Field(default=None, env="LOG_FILE")

    # Feature Flags
    ENABLE_AI_AGENTS: bool = Field(default=True, env="ENABLE_AI_AGENTS")
    ENABLE_BACKTESTING: bool = Field(default=True, env="ENABLE_BACKTESTING")
    ENABLE_REAL_TRADING: bool = Field(default=False, env="ENABLE_REAL_TRADING")
    ENABLE_PAPER_TRADING: bool = Field(default=True, env="ENABLE_PAPER_TRADING")

    # VectorBT Configuration
    VECTORBT_CACHE_DIR: str = Field(default="./data/vectorbt_cache", env="VECTORBT_CACHE_DIR")
    VECTORBT_PARALLEL: bool = Field(default=True, env="VECTORBT_PARALLEL")
    VECTORBT_NUM_WORKERS: int = Field(default=4, env="VECTORBT_NUM_WORKERS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.ENVIRONMENT == "development"

    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.ENVIRONMENT == "production"

    def get_database_url(self) -> str:
        """Get database URL with connection pooling parameters"""
        if "?" in self.DATABASE_URL:
            return f"{self.DATABASE_URL}&pool_size={self.DATABASE_POOL_SIZE}&max_overflow={self.DATABASE_MAX_OVERFLOW}"
        return f"{self.DATABASE_URL}?pool_size={self.DATABASE_POOL_SIZE}&max_overflow={self.DATABASE_MAX_OVERFLOW}"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()