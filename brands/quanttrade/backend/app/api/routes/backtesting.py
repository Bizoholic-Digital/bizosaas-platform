"""
Backtesting API Routes for QuantTrade Platform - Enhanced with VectorBT Integration
"""

from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import structlog

from services.backtesting_service import VectorBTBacktestingService, BacktestConfig
from core.auth import get_current_user

logger = structlog.get_logger(__name__)
router = APIRouter()

# Initialize VectorBT backtesting service
vectorbt_service = VectorBTBacktestingService()


class BacktestRequest(BaseModel):
    """Request model for creating backtest"""
    strategy_id: int
    name: str
    description: Optional[str] = None
    start_date: str
    end_date: str
    initial_capital: float = 100000.0
    commission_rate: float = 0.001
    slippage: float = 0.0005


class VectorBTBacktestRequest(BaseModel):
    """Enhanced request model for VectorBT backtesting"""
    strategy_config: Dict[str, Any] = Field(..., description="Strategy configuration")
    symbols: List[str] = Field(..., description="List of symbols to backtest")
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    initial_capital: float = Field(default=100000.0, description="Initial capital")
    commission: float = Field(default=0.001, description="Commission rate")
    slippage: float = Field(default=0.0005, description="Slippage rate")
    risk_free_rate: float = Field(default=0.02, description="Risk-free rate for Sharpe calculation")
    benchmark: str = Field(default="SPY", description="Benchmark symbol")
    position_size: float = Field(default=0.25, description="Position size per trade")
    max_leverage: float = Field(default=1.0, description="Maximum leverage")


class MonteCarloRequest(BaseModel):
    """Request model for Monte Carlo backtesting"""
    strategy_config: Dict[str, Any]
    symbols: List[str]
    num_simulations: int = Field(default=1000, ge=100, le=10000, description="Number of Monte Carlo simulations")
    start_date: str
    end_date: str
    initial_capital: float = Field(default=100000.0, description="Initial capital")


class WalkForwardRequest(BaseModel):
    """Request model for walk-forward analysis"""
    strategy_config: Dict[str, Any]
    symbols: List[str]
    train_period_months: int = Field(default=12, ge=3, le=36, description="Training period in months")
    test_period_months: int = Field(default=3, ge=1, le=12, description="Test period in months")
    start_date: str
    end_date: str


# Mock authentication for demo
async def get_current_user() -> Dict[str, Any]:
    """Mock user authentication - replace with real auth"""
    return {"id": 1, "username": "demo_user", "email": "demo@quanttrade.com"}


@router.get("/")
async def get_backtests(
    status: Optional[str] = Query(None, description="Filter by backtest status"),
    strategy_id: Optional[int] = Query(None, description="Filter by strategy ID"),
    user: dict = Depends(get_current_user)
):
    """Get user's backtests"""
    try:
        # Mock backtests data
        mock_backtests = [
            {
                "id": 1,
                "name": "Momentum Scanner - 2023 Full Year",
                "description": "Full year backtest of momentum scanner strategy",
                "strategy_id": 1,
                "strategy_name": "Momentum Scanner",
                "status": "completed",
                "start_date": "2023-01-01",
                "end_date": "2023-12-31",
                "duration_days": 365,
                "initial_capital": 100000.0,
                "final_portfolio_value": 118750.0,
                "total_return": 18750.0,
                "total_return_percent": 18.75,
                "annualized_return": 18.75,
                "sharpe_ratio": 1.85,
                "max_drawdown_percent": -8.2,
                "total_trades": 156,
                "win_rate": 68.5,
                "created_at": "2024-01-01T10:00:00Z",
                "completed_at": "2024-01-01T10:05:32Z",
                "execution_time_seconds": 332.5
            },
            {
                "id": 2,
                "name": "Mean Reversion - Q4 2023",
                "description": "Q4 2023 backtest of mean reversion strategy",
                "strategy_id": 2,
                "strategy_name": "Mean Reversion",
                "status": "completed",
                "start_date": "2023-10-01",
                "end_date": "2023-12-31",
                "duration_days": 92,
                "initial_capital": 100000.0,
                "final_portfolio_value": 106450.0,
                "total_return": 6450.0,
                "total_return_percent": 6.45,
                "annualized_return": 25.8,
                "sharpe_ratio": 1.42,
                "max_drawdown_percent": -4.1,
                "total_trades": 34,
                "win_rate": 73.5,
                "created_at": "2024-01-05T14:00:00Z",
                "completed_at": "2024-01-05T14:02:15Z",
                "execution_time_seconds": 135.2
            },
            {
                "id": 3,
                "name": "Combined Strategy Test",
                "description": "Testing momentum + mean reversion combined",
                "strategy_id": 1,
                "strategy_name": "Momentum Scanner",
                "status": "running",
                "start_date": "2023-06-01",
                "end_date": "2024-01-15",
                "duration_days": 228,
                "initial_capital": 150000.0,
                "progress_percent": 78.5,
                "created_at": "2024-01-15T09:00:00Z",
                "started_at": "2024-01-15T09:00:15Z"
            }
        ]

        # Apply filters
        filtered_backtests = mock_backtests

        if status:
            filtered_backtests = [b for b in filtered_backtests if b["status"] == status]

        if strategy_id:
            filtered_backtests = [b for b in filtered_backtests if b["strategy_id"] == strategy_id]

        logger.info("Backtests retrieved via API", user_id=user["id"], count=len(filtered_backtests))

        return {
            "backtests": filtered_backtests,
            "total": len(filtered_backtests),
            "completed_count": len([b for b in mock_backtests if b["status"] == "completed"]),
            "running_count": len([b for b in mock_backtests if b["status"] == "running"]),
            "failed_count": len([b for b in mock_backtests if b["status"] == "failed"])
        }

    except Exception as e:
        logger.error("API: Failed to get backtests", user_id=user["id"], error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve backtests")


@router.get("/{backtest_id}")
async def get_backtest(
    backtest_id: int,
    user: dict = Depends(get_current_user)
):
    """Get detailed backtest results"""
    try:
        # Mock detailed backtest results
        if backtest_id == 1:
            backtest = {
                "id": 1,
                "name": "Momentum Scanner - 2023 Full Year",
                "description": "Comprehensive backtest of momentum scanner strategy over full 2023",
                "strategy_id": 1,
                "strategy_name": "Momentum Scanner",
                "status": "completed",
                "configuration": {
                    "start_date": "2023-01-01",
                    "end_date": "2023-12-31",
                    "initial_capital": 100000.0,
                    "commission_rate": 0.001,
                    "slippage": 0.0005,
                    "benchmark": "SPY"
                },
                "results": {
                    "final_portfolio_value": 118750.0,
                    "total_return": 18750.0,
                    "total_return_percent": 18.75,
                    "annualized_return": 18.75,
                    "benchmark_return": 12.31,
                    "alpha": 6.44,
                    "beta": 1.15,
                    "volatility": 0.195,
                    "sharpe_ratio": 1.85,
                    "sortino_ratio": 2.34,
                    "calmar_ratio": 2.28,
                    "max_drawdown": -8200.0,
                    "max_drawdown_percent": -8.2,
                    "var_95": -2100.0
                },
                "trading_stats": {
                    "total_trades": 156,
                    "winning_trades": 107,
                    "losing_trades": 49,
                    "win_rate": 68.5,
                    "avg_trade_return": 0.032,
                    "avg_win": 0.067,
                    "avg_loss": -0.024,
                    "profit_factor": 2.79,
                    "avg_holding_period": 4.2,
                    "max_consecutive_wins": 12,
                    "max_consecutive_losses": 4
                },
                "monthly_returns": [
                    {"month": "2023-01", "return_percent": 2.8, "benchmark_return": 1.2, "trades": 14},
                    {"month": "2023-02", "return_percent": -1.2, "benchmark_return": -0.8, "trades": 11},
                    {"month": "2023-03", "return_percent": 3.4, "benchmark_return": 2.1, "trades": 16},
                    {"month": "2023-04", "return_percent": 1.9, "benchmark_return": 1.5, "trades": 12},
                    {"month": "2023-05", "return_percent": 2.1, "benchmark_return": 0.9, "trades": 13},
                    {"month": "2023-06", "return_percent": 1.5, "benchmark_return": 1.8, "trades": 10},
                    {"month": "2023-07", "return_percent": 3.2, "benchmark_return": 2.4, "trades": 15},
                    {"month": "2023-08", "return_percent": -2.1, "benchmark_return": -1.2, "trades": 9},
                    {"month": "2023-09", "return_percent": 0.8, "benchmark_return": 0.3, "trades": 11},
                    {"month": "2023-10", "return_percent": 2.9, "benchmark_return": 1.7, "trades": 14},
                    {"month": "2023-11", "return_percent": 4.1, "benchmark_return": 2.8, "trades": 17},
                    {"month": "2023-12", "return_percent": 1.3, "benchmark_return": 1.1, "trades": 14}
                ],
                "top_trades": [
                    {
                        "symbol": "NVDA",
                        "entry_date": "2023-05-15",
                        "exit_date": "2023-05-22",
                        "entry_price": 285.50,
                        "exit_price": 342.80,
                        "quantity": 350,
                        "pnl": 20055.0,
                        "return_percent": 20.08,
                        "holding_days": 7
                    },
                    {
                        "symbol": "AAPL",
                        "entry_date": "2023-07-08",
                        "exit_date": "2023-07-18",
                        "entry_price": 178.20,
                        "exit_price": 194.35,
                        "quantity": 560,
                        "pnl": 9044.0,
                        "return_percent": 9.06,
                        "holding_days": 10
                    }
                ],
                "worst_trades": [
                    {
                        "symbol": "META",
                        "entry_date": "2023-08-12",
                        "exit_date": "2023-08-15",
                        "entry_price": 298.40,
                        "exit_price": 275.20,
                        "quantity": 170,
                        "pnl": -3944.0,
                        "return_percent": -7.77,
                        "holding_days": 3
                    }
                ],
                "execution_details": {
                    "created_at": "2024-01-01T10:00:00Z",
                    "started_at": "2024-01-01T10:00:15Z",
                    "completed_at": "2024-01-01T10:05:32Z",
                    "execution_time_seconds": 332.5,
                    "data_points_processed": 124800
                }
            }
        else:
            raise HTTPException(status_code=404, detail="Backtest not found")

        logger.info("Backtest details retrieved via API", user_id=user["id"], backtest_id=backtest_id)
        return backtest

    except HTTPException:
        raise
    except Exception as e:
        logger.error("API: Failed to get backtest", user_id=user["id"], backtest_id=backtest_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve backtest")


@router.post("/")
async def create_backtest(
    backtest_data: BacktestRequest,
    user: dict = Depends(get_current_user)
):
    """Create and run new backtest"""
    try:
        # Mock backtest creation and execution
        new_backtest = {
            "id": 999,  # Mock ID
            "name": backtest_data.name,
            "description": backtest_data.description,
            "strategy_id": backtest_data.strategy_id,
            "status": "running",
            "start_date": backtest_data.start_date,
            "end_date": backtest_data.end_date,
            "initial_capital": backtest_data.initial_capital,
            "commission_rate": backtest_data.commission_rate,
            "slippage": backtest_data.slippage,
            "progress_percent": 0.0,
            "created_at": "2024-01-15T16:00:00Z",
            "started_at": "2024-01-15T16:00:05Z",
            "estimated_completion": "2024-01-15T16:03:00Z"
        }

        logger.info(
            "Mock backtest created and started via API",
            user_id=user["id"],
            strategy_id=backtest_data.strategy_id,
            backtest_name=backtest_data.name
        )

        return {
            "success": True,
            "message": "Backtest created and started successfully",
            "backtest": new_backtest
        }

    except Exception as e:
        logger.error("API: Failed to create backtest", user_id=user["id"], error=str(e))
        raise HTTPException(status_code=500, detail="Failed to create backtest")


@router.get("/{backtest_id}/progress")
async def get_backtest_progress(
    backtest_id: int,
    user: dict = Depends(get_current_user)
):
    """Get backtest execution progress"""
    try:
        # Mock progress data
        progress_data = {
            "backtest_id": backtest_id,
            "status": "running",
            "progress_percent": 65.8,
            "current_date": "2023-08-15",
            "trades_processed": 102,
            "data_points_processed": 82000,
            "estimated_completion": "2024-01-15T16:03:00Z",
            "elapsed_time_seconds": 185.3,
            "estimated_remaining_seconds": 95.2,
            "interim_results": {
                "current_portfolio_value": 112450.0,
                "unrealized_return_percent": 12.45,
                "trades_so_far": 102,
                "win_rate_so_far": 71.6,
                "max_drawdown_so_far": -5.8
            }
        }

        logger.info("Backtest progress retrieved via API", user_id=user["id"], backtest_id=backtest_id)
        return progress_data

    except Exception as e:
        logger.error("API: Failed to get backtest progress", user_id=user["id"], backtest_id=backtest_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve backtest progress")


@router.delete("/{backtest_id}")
async def delete_backtest(
    backtest_id: int,
    user: dict = Depends(get_current_user)
):
    """Delete a backtest"""
    try:
        logger.info("Mock backtest deleted via API", user_id=user["id"], backtest_id=backtest_id)

        return {
            "success": True,
            "message": "Backtest deleted successfully",
            "backtest_id": backtest_id
        }

    except Exception as e:
        logger.error("API: Failed to delete backtest", user_id=user["id"], backtest_id=backtest_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to delete backtest")


@router.post("/{backtest_id}/cancel")
async def cancel_backtest(
    backtest_id: int,
    user: dict = Depends(get_current_user)
):
    """Cancel a running backtest"""
    try:
        logger.info("Mock backtest cancelled via API", user_id=user["id"], backtest_id=backtest_id)

        return {
            "success": True,
            "message": "Backtest cancelled successfully",
            "backtest_id": backtest_id,
            "status": "cancelled",
            "cancelled_at": "2024-01-15T16:15:00Z"
        }

    except Exception as e:
        logger.error("API: Failed to cancel backtest", user_id=user["id"], backtest_id=backtest_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to cancel backtest")


@router.post("/compare")
async def compare_backtests(
    backtest_ids: List[int],
    user: dict = Depends(get_current_user)
):
    """Compare multiple backtests"""
    try:
        if len(backtest_ids) < 2:
            raise HTTPException(status_code=400, detail="At least 2 backtests required for comparison")

        if len(backtest_ids) > 5:
            raise HTTPException(status_code=400, detail="Maximum 5 backtests can be compared at once")

        # Mock comparison data
        comparison_data = {
            "backtest_ids": backtest_ids,
            "comparison_metrics": {
                "total_return_percent": [18.75, 12.45, 15.30],  # For each backtest
                "sharpe_ratio": [1.85, 1.42, 1.67],
                "max_drawdown_percent": [-8.2, -4.1, -6.8],
                "win_rate": [68.5, 73.5, 69.2],
                "total_trades": [156, 34, 89],
                "avg_trade_return": [0.032, 0.058, 0.041]
            },
            "rankings": {
                "best_return": {"backtest_id": 1, "value": 18.75},
                "best_sharpe": {"backtest_id": 1, "value": 1.85},
                "lowest_drawdown": {"backtest_id": 2, "value": -4.1},
                "highest_win_rate": {"backtest_id": 2, "value": 73.5}
            },
            "correlation_matrix": [
                [1.0, 0.65, 0.72],
                [0.65, 1.0, 0.58],
                [0.72, 0.58, 1.0]
            ],
            "generated_at": "2024-01-15T16:30:00Z"
        }

        logger.info("Backtest comparison performed via API", user_id=user["id"], backtest_ids=backtest_ids)
        return comparison_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error("API: Failed to compare backtests", user_id=user["id"], error=str(e))
        raise HTTPException(status_code=500, detail="Failed to compare backtests")


# Enhanced VectorBT Backtesting Endpoints

@router.post("/vectorbt/backtest")
async def run_vectorbt_backtest(
    request: VectorBTBacktestRequest,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user)
):
    """
    Run comprehensive backtesting using VectorBT engine
    """
    try:
        logger.info("Starting VectorBT backtesting",
                   user_id=user["id"],
                   strategy_type=request.strategy_config.get("type"),
                   symbols=request.symbols)

        # Create backtest configuration
        config = BacktestConfig(
            initial_capital=request.initial_capital,
            commission=request.commission,
            slippage=request.slippage,
            start_date=request.start_date,
            end_date=request.end_date,
            benchmark=request.benchmark,
            risk_free_rate=request.risk_free_rate,
            position_size=request.position_size,
            max_leverage=request.max_leverage
        )

        # Run backtesting
        result = await vectorbt_service.backtest_strategy(
            strategy_config={
                **request.strategy_config,
                "symbols": request.symbols
            },
            config=config
        )

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        # Store result in database (background task)
        background_tasks.add_task(
            store_backtest_result,
            user_id=user["id"],
            backtest_data=result
        )

        return {
            "status": "success",
            "backtest_id": result.get("timestamp", ""),
            "data": result,
            "message": "VectorBT backtesting completed successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in VectorBT backtesting",
                    user_id=user["id"],
                    error=str(e))
        raise HTTPException(status_code=500, detail=f"VectorBT backtesting failed: {str(e)}")


@router.post("/vectorbt/monte-carlo")
async def run_monte_carlo_backtest(
    request: MonteCarloRequest,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user)
):
    """
    Run Monte Carlo backtesting simulation
    """
    try:
        logger.info("Starting Monte Carlo backtesting",
                   user_id=user["id"],
                   simulations=request.num_simulations,
                   strategy_type=request.strategy_config.get("type"))

        # Create backtest configuration
        config = BacktestConfig(
            initial_capital=request.initial_capital,
            start_date=request.start_date,
            end_date=request.end_date
        )

        # Run Monte Carlo simulation
        result = await vectorbt_service.monte_carlo_backtest(
            strategy_config={
                **request.strategy_config,
                "symbols": request.symbols
            },
            num_simulations=request.num_simulations,
            config=config
        )

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        # Store result in database (background task)
        background_tasks.add_task(
            store_monte_carlo_result,
            user_id=user["id"],
            monte_carlo_data=result
        )

        return {
            "status": "success",
            "analysis_id": result.get("timestamp", ""),
            "data": result,
            "message": f"Monte Carlo simulation with {request.num_simulations} iterations completed"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in Monte Carlo backtesting",
                    user_id=user["id"],
                    error=str(e))
        raise HTTPException(status_code=500, detail=f"Monte Carlo backtesting failed: {str(e)}")


@router.post("/vectorbt/walk-forward")
async def run_walk_forward_analysis(
    request: WalkForwardRequest,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user)
):
    """
    Run walk-forward analysis for strategy validation
    """
    try:
        logger.info("Starting walk-forward analysis",
                   user_id=user["id"],
                   train_period=request.train_period_months,
                   test_period=request.test_period_months)

        # Create backtest configuration
        config = BacktestConfig(
            start_date=request.start_date,
            end_date=request.end_date
        )

        # Run walk-forward analysis
        result = await vectorbt_service.walk_forward_analysis(
            strategy_config={
                **request.strategy_config,
                "symbols": request.symbols
            },
            train_period_months=request.train_period_months,
            test_period_months=request.test_period_months,
            config=config
        )

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        # Store result in database (background task)
        background_tasks.add_task(
            store_walk_forward_result,
            user_id=user["id"],
            walk_forward_data=result
        )

        return {
            "status": "success",
            "analysis_id": result.get("timestamp", ""),
            "data": result,
            "message": "Walk-forward analysis completed successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in walk-forward analysis",
                    user_id=user["id"],
                    error=str(e))
        raise HTTPException(status_code=500, detail=f"Walk-forward analysis failed: {str(e)}")


@router.get("/vectorbt/strategies")
async def get_supported_strategies():
    """
    Get list of supported backtesting strategies
    """
    return {
        "supported_strategies": {
            "momentum": {
                "name": "Momentum Strategy",
                "description": "Buy assets with positive price momentum, sell with negative momentum",
                "parameters": {
                    "lookback_period": {"type": "int", "default": 20, "range": [5, 100]},
                    "momentum_threshold": {"type": "float", "default": 0.02, "range": [0.01, 0.10]},
                    "position_size": {"type": "float", "default": 0.25, "range": [0.1, 1.0]}
                }
            },
            "mean_reversion": {
                "name": "Mean Reversion Strategy",
                "description": "Buy oversold assets, sell overbought assets using Bollinger Bands",
                "parameters": {
                    "lookback_period": {"type": "int", "default": 20, "range": [10, 50]},
                    "std_dev": {"type": "float", "default": 2.0, "range": [1.5, 3.0]},
                    "position_size": {"type": "float", "default": 0.25, "range": [0.1, 1.0]}
                }
            },
            "pairs_trading": {
                "name": "Pairs Trading Strategy",
                "description": "Statistical arbitrage between correlated assets",
                "parameters": {
                    "entry_threshold": {"type": "float", "default": 2.0, "range": [1.5, 3.0]},
                    "exit_threshold": {"type": "float", "default": 0.5, "range": [0.1, 1.0]},
                    "lookback_period": {"type": "int", "default": 30, "range": [20, 60]}
                }
            }
        }
    }


@router.get("/vectorbt/performance-metrics")
async def get_performance_metrics_info():
    """
    Get information about available performance metrics
    """
    return {
        "performance_metrics": {
            "return_metrics": {
                "total_return": "Total percentage return over the backtest period",
                "annual_return": "Annualized return percentage",
                "monthly_returns": "Month-by-month return breakdown"
            },
            "risk_metrics": {
                "volatility": "Annualized volatility of returns",
                "sharpe_ratio": "Risk-adjusted return metric (return per unit of risk)",
                "sortino_ratio": "Downside risk-adjusted return metric",
                "calmar_ratio": "Return to max drawdown ratio",
                "max_drawdown": "Maximum peak-to-trough decline",
                "var_95": "Value at Risk at 95% confidence level",
                "cvar_95": "Conditional Value at Risk (expected tail loss)"
            },
            "trading_metrics": {
                "total_trades": "Number of completed trades",
                "win_rate": "Percentage of profitable trades",
                "profit_factor": "Ratio of gross profit to gross loss",
                "avg_trade_duration": "Average holding period per trade",
                "best_trade": "Highest single trade profit",
                "worst_trade": "Largest single trade loss"
            },
            "distribution_metrics": {
                "skewness": "Asymmetry of return distribution",
                "kurtosis": "Tail heaviness of return distribution",
                "tail_ratio": "Ratio of 95th to 5th percentile returns"
            }
        }
    }


# Background task functions for storing results
async def store_backtest_result(user_id: str, backtest_data: Dict[str, Any]):
    """Store backtest result in database"""
    try:
        logger.info("Storing VectorBT backtest result", user_id=user_id)
        # Implementation would store in backtest_results table
    except Exception as e:
        logger.error("Failed to store backtest result", error=str(e))


async def store_monte_carlo_result(user_id: str, monte_carlo_data: Dict[str, Any]):
    """Store Monte Carlo result in database"""
    try:
        logger.info("Storing Monte Carlo result", user_id=user_id)
        # Implementation would store in monte_carlo_results table
    except Exception as e:
        logger.error("Failed to store Monte Carlo result", error=str(e))


async def store_walk_forward_result(user_id: str, walk_forward_data: Dict[str, Any]):
    """Store walk-forward analysis result in database"""
    try:
        logger.info("Storing walk-forward result", user_id=user_id)
        # Implementation would store in walk_forward_results table
    except Exception as e:
        logger.error("Failed to store walk-forward result", error=str(e))