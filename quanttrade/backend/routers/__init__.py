"""
API Routers
"""
from .portfolio import router as portfolio_router
from .strategies import router as strategies_router
from .backtesting import router as backtesting_router
from .market_data import router as market_data_router
from .ai_agents import router as ai_agents_router
from .trading import router as trading_router
from .risk import router as risk_router

__all__ = [
    "portfolio_router",
    "strategies_router",
    "backtesting_router",
    "market_data_router",
    "ai_agents_router",
    "trading_router",
    "risk_router"
]
