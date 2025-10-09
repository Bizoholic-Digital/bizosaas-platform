"""
Configuration settings for QuantTrade platform
"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""

    # App Configuration
    APP_NAME: str = "QuantTrade AI Trading Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8012

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3012",
        "http://127.0.0.1:3012",
        "http://localhost:3000",
    ]

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/quanttrade"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Market Data APIs
    ALPHA_VANTAGE_API_KEY: str = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
    YAHOO_FINANCE_ENABLED: bool = True

    # AI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # Trading Configuration
    DEFAULT_PAPER_TRADING: bool = True
    MAX_POSITION_SIZE: float = 0.1  # 10% max position size
    DEFAULT_STOP_LOSS: float = 0.02  # 2% stop loss
    DEFAULT_TAKE_PROFIT: float = 0.05  # 5% take profit

    # Backtesting Configuration
    BACKTEST_START_CAPITAL: float = 100000.0
    BACKTEST_COMMISSION: float = 0.001  # 0.1% commission

    # Risk Management
    MAX_DAILY_LOSS: float = 0.02  # 2% max daily loss
    MAX_PORTFOLIO_RISK: float = 0.05  # 5% max portfolio risk
    POSITION_SIZE_METHOD: str = "kelly"  # kelly, fixed, risk_parity

    # WebSocket
    WS_HEARTBEAT_INTERVAL: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
