"""
Market Data API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from services.market_data_service import MarketDataService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize service
market_service = MarketDataService()

@router.get("/quote/{symbol}")
async def get_quote(symbol: str):
    """Get detailed quote for a symbol"""
    try:
        result = await market_service.get_quote(symbol.upper())
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Quote fetch failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/price/{symbol}")
async def get_current_price(symbol: str):
    """Get current price for a symbol"""
    try:
        result = await market_service.get_current_price(symbol.upper())
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Price fetch failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/historical/{symbol}")
async def get_historical_data(
    symbol: str,
    period: str = Query(default="1mo", regex="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|10y|ytd|max)$"),
    interval: str = Query(default="1d", regex="^(1m|2m|5m|15m|30m|60m|90m|1h|1d|5d|1wk|1mo|3mo)$")
):
    """Get historical OHLCV data"""
    try:
        result = await market_service.get_historical_data(
            symbol.upper(),
            period=period,
            interval=interval
        )
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Historical data fetch failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/indicators/{symbol}")
async def get_technical_indicators(symbol: str, period: str = "3mo"):
    """Get technical indicators for a symbol"""
    try:
        result = await market_service.get_technical_indicators(symbol.upper(), period)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Indicators calculation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
async def search_symbols(query: str = Query(..., min_length=1)):
    """Search for stock symbols"""
    try:
        results = await market_service.search_symbols(query)
        return {"results": results}
    except Exception as e:
        logger.error(f"Symbol search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/watchlist")
async def get_watchlist():
    """Get default watchlist symbols"""
    symbols = ["SPY", "QQQ", "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "BTC-USD"]
    results = []

    for symbol in symbols:
        try:
            price_data = await market_service.get_current_price(symbol)
            if "error" not in price_data:
                results.append(price_data)
        except Exception as e:
            logger.error(f"Error fetching {symbol}: {e}")
            continue

    return {"watchlist": results}
