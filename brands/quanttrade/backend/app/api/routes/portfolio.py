"""
Portfolio API Routes for QuantTrade Platform
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict, Any, Optional
import structlog

from services.portfolio_service import PortfolioService

logger = structlog.get_logger(__name__)
router = APIRouter()


def get_portfolio_service() -> PortfolioService:
    """Get portfolio service instance"""
    return PortfolioService()


# Mock authentication for demo
async def get_current_user() -> Dict[str, Any]:
    """Mock user authentication - replace with real auth"""
    return {"id": 1, "username": "demo_user", "email": "demo@quanttrade.com"}


@router.get("/")
async def get_portfolio(
    user: dict = Depends(get_current_user),
    portfolio_service: PortfolioService = Depends(get_portfolio_service)
):
    """Get user's portfolio summary"""
    try:
        portfolio = await portfolio_service.get_portfolio(user["id"])

        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        logger.info("Portfolio retrieved via API", user_id=user["id"])
        return portfolio

    except Exception as e:
        logger.error("API: Failed to get portfolio", user_id=user["id"], error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve portfolio")


@router.get("/history")
async def get_portfolio_history(
    days: int = Query(default=30, ge=1, le=365),
    user: dict = Depends(get_current_user),
    portfolio_service: PortfolioService = Depends(get_portfolio_service)
):
    """Get portfolio performance history"""
    try:
        history = await portfolio_service.get_portfolio_history(user["id"], days)

        logger.info("Portfolio history retrieved", user_id=user["id"], days=days)
        return {
            "history": history,
            "period_days": days,
            "total_points": len(history)
        }

    except Exception as e:
        logger.error("API: Failed to get portfolio history", user_id=user["id"], error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve portfolio history")


@router.get("/performance")
async def get_portfolio_performance(
    user: dict = Depends(get_current_user),
    portfolio_service: PortfolioService = Depends(get_portfolio_service)
):
    """Get detailed portfolio performance metrics"""
    try:
        portfolio = await portfolio_service.get_portfolio(user["id"])

        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        performance_data = {
            "current_value": portfolio["total_value"],
            "total_return": portfolio["total_return"],
            "total_return_percent": portfolio["total_return_percent"],
            "daily_pnl": portfolio["daily_pnl"],
            "daily_pnl_percent": portfolio["daily_pnl_percent"],
            "unrealized_pnl": portfolio["unrealized_pnl"],
            "cash_balance": portfolio["cash_balance"],
            "invested_amount": portfolio["invested_amount"],
            "buying_power": portfolio["buying_power"],
            "active_positions": portfolio["active_positions"],
            "metrics": portfolio["performance_metrics"],
            "allocation": await _calculate_allocation(portfolio["positions"])
        }

        logger.info("Portfolio performance retrieved", user_id=user["id"])
        return performance_data

    except Exception as e:
        logger.error("API: Failed to get portfolio performance", user_id=user["id"], error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve portfolio performance")


@router.post("/snapshot")
async def create_portfolio_snapshot(
    user: dict = Depends(get_current_user),
    portfolio_service: PortfolioService = Depends(get_portfolio_service)
):
    """Create portfolio snapshot for history tracking"""
    try:
        success = await portfolio_service.create_portfolio_snapshot(user["id"])

        if not success:
            raise HTTPException(status_code=500, detail="Failed to create portfolio snapshot")

        logger.info("Portfolio snapshot created via API", user_id=user["id"])
        return {"success": True, "message": "Portfolio snapshot created successfully"}

    except Exception as e:
        logger.error("API: Failed to create portfolio snapshot", user_id=user["id"], error=str(e))
        raise HTTPException(status_code=500, detail="Failed to create portfolio snapshot")


async def _calculate_allocation(positions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate portfolio allocation by sector and asset"""
    sector_allocation = {}
    total_value = sum(pos["market_value"] for pos in positions)

    if total_value == 0:
        return {"sectors": {}, "top_holdings": []}

    # Calculate sector allocation
    for position in positions:
        sector = position.get("sector", "Unknown")
        market_value = position["market_value"]

        if sector not in sector_allocation:
            sector_allocation[sector] = 0
        sector_allocation[sector] += market_value

    # Convert to percentages
    sector_percentages = {
        sector: (value / total_value) * 100
        for sector, value in sector_allocation.items()
    }

    # Get top holdings
    top_holdings = sorted(
        [
            {
                "symbol": pos["symbol"],
                "market_value": pos["market_value"],
                "percentage": (pos["market_value"] / total_value) * 100
            }
            for pos in positions
        ],
        key=lambda x: x["market_value"],
        reverse=True
    )[:10]

    return {
        "sectors": sector_percentages,
        "top_holdings": top_holdings
    }