"""
Portfolio Management API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory storage (replace with database in production)
portfolios = {}

class Position(BaseModel):
    symbol: str
    quantity: float
    entry_price: float
    entry_date: str
    current_price: Optional[float] = None

class Portfolio(BaseModel):
    id: str
    name: str
    initial_capital: float
    current_value: float
    positions: List[Position]
    cash: float

@router.get("/")
async def get_portfolio():
    """Get current portfolio"""
    # Demo portfolio
    demo_portfolio = {
        "id": "demo",
        "name": "Demo Portfolio",
        "initial_capital": 100000.0,
        "current_value": 105000.0,
        "cash": 50000.0,
        "positions": [
            {
                "symbol": "AAPL",
                "quantity": 100,
                "entry_price": 150.00,
                "current_price": 155.00,
                "entry_date": "2024-01-01",
                "pnl": 500.00,
                "pnl_percent": 3.33
            },
            {
                "symbol": "MSFT",
                "quantity": 75,
                "entry_price": 350.00,
                "current_price": 360.00,
                "entry_date": "2024-01-15",
                "pnl": 750.00,
                "pnl_percent": 2.86
            }
        ],
        "total_pnl": 5000.0,
        "total_pnl_percent": 5.0,
        "timestamp": datetime.now().isoformat()
    }
    return demo_portfolio

@router.get("/performance")
async def get_performance():
    """Get portfolio performance metrics"""
    return {
        "total_return": 5.0,
        "daily_return": 0.5,
        "sharpe_ratio": 1.8,
        "max_drawdown": -2.5,
        "win_rate": 65.0,
        "profit_factor": 2.1,
        "equity_curve": [
            {"date": "2024-01-01", "value": 100000},
            {"date": "2024-02-01", "value": 102000},
            {"date": "2024-03-01", "value": 105000}
        ],
        "timestamp": datetime.now().isoformat()
    }

@router.get("/positions")
async def get_positions():
    """Get current positions"""
    return {
        "positions": [
            {
                "symbol": "AAPL",
                "quantity": 100,
                "entry_price": 150.00,
                "current_price": 155.00,
                "pnl": 500.00,
                "pnl_percent": 3.33,
                "allocation": 14.76
            },
            {
                "symbol": "MSFT",
                "quantity": 75,
                "entry_price": 350.00,
                "current_price": 360.00,
                "pnl": 750.00,
                "pnl_percent": 2.86,
                "allocation": 25.71
            }
        ],
        "total_positions": 2,
        "total_value": 42000.0,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/history")
async def get_trade_history():
    """Get trade history"""
    return {
        "trades": [
            {
                "id": 1,
                "symbol": "TSLA",
                "type": "BUY",
                "quantity": 50,
                "price": 200.00,
                "date": "2024-01-10",
                "status": "completed"
            },
            {
                "id": 2,
                "symbol": "TSLA",
                "type": "SELL",
                "quantity": 50,
                "price": 210.00,
                "date": "2024-02-15",
                "status": "completed",
                "pnl": 500.00
            }
        ],
        "total_trades": 2,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/allocation")
async def get_allocation():
    """Get portfolio allocation"""
    return {
        "allocation": {
            "equities": 47.62,
            "cash": 47.62,
            "crypto": 4.76
        },
        "sector_allocation": {
            "technology": 40.47,
            "finance": 7.15,
            "cash": 47.62,
            "crypto": 4.76
        },
        "timestamp": datetime.now().isoformat()
    }
