"""
Backtesting API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from services.backtesting_service import BacktestingService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize service
backtest_service = BacktestingService()

class BacktestSMARequest(BaseModel):
    symbol: str
    fast_window: int = 50
    slow_window: int = 200
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class BacktestRSIRequest(BaseModel):
    symbol: str
    rsi_window: int = 14
    rsi_lower: int = 30
    rsi_upper: int = 70
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class OptimizeRequest(BaseModel):
    symbol: str
    strategy_type: str
    param_ranges: Dict[str, List]
    start_date: str
    end_date: str

@router.post("/sma-crossover")
async def backtest_sma_crossover(request: BacktestSMARequest):
    """Backtest SMA Crossover strategy"""
    try:
        result = await backtest_service.backtest_sma_crossover(
            symbol=request.symbol,
            fast_window=request.fast_window,
            slow_window=request.slow_window,
            start_date=request.start_date,
            end_date=request.end_date
        )
        return result
    except Exception as e:
        logger.error(f"SMA backtest failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/rsi-strategy")
async def backtest_rsi_strategy(request: BacktestRSIRequest):
    """Backtest RSI Mean Reversion strategy"""
    try:
        result = await backtest_service.backtest_rsi_strategy(
            symbol=request.symbol,
            rsi_window=request.rsi_window,
            rsi_lower=request.rsi_lower,
            rsi_upper=request.rsi_upper,
            start_date=request.start_date,
            end_date=request.end_date
        )
        return result
    except Exception as e:
        logger.error(f"RSI backtest failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/optimize")
async def optimize_strategy(request: OptimizeRequest):
    """Optimize strategy parameters"""
    try:
        result = await backtest_service.optimize_strategy(
            symbol=request.symbol,
            strategy_type=request.strategy_type,
            param_ranges=request.param_ranges,
            start_date=request.start_date,
            end_date=request.end_date
        )
        return result
    except Exception as e:
        logger.error(f"Optimization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/strategies")
async def list_strategies():
    """List available strategies for backtesting"""
    return {
        "strategies": [
            {
                "id": "sma_crossover",
                "name": "SMA Crossover",
                "description": "Simple Moving Average crossover strategy",
                "parameters": ["fast_window", "slow_window"]
            },
            {
                "id": "rsi_strategy",
                "name": "RSI Mean Reversion",
                "description": "RSI-based mean reversion strategy",
                "parameters": ["rsi_window", "rsi_lower", "rsi_upper"]
            }
        ]
    }
