"""
Market Data API Routes for QuantTrade Platform
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import structlog

from services.market_data_service import MarketDataService

logger = structlog.get_logger(__name__)
router = APIRouter()


def get_market_service() -> MarketDataService:
    """Get market data service instance"""
    return MarketDataService()


@router.get("/quote/{symbol}")
async def get_quote(
    symbol: str,
    market_service: MarketDataService = Depends(get_market_service)
):
    """Get real-time quote for a symbol"""
    try:
        quote = await market_service.get_real_time_quote(symbol.upper())

        if not quote:
            raise HTTPException(status_code=404, detail=f"Quote not found for symbol: {symbol}")

        logger.info("Quote retrieved via API", symbol=symbol)
        return quote

    except HTTPException:
        raise
    except Exception as e:
        logger.error("API: Failed to get quote", symbol=symbol, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve quote")


@router.get("/quotes")
async def get_multiple_quotes(
    symbols: str = Query(..., description="Comma-separated list of symbols"),
    market_service: MarketDataService = Depends(get_market_service)
):
    """Get real-time quotes for multiple symbols"""
    try:
        symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]

        if not symbol_list:
            raise HTTPException(status_code=400, detail="No symbols provided")

        if len(symbol_list) > 50:  # Limit to prevent abuse
            raise HTTPException(status_code=400, detail="Too many symbols requested (max 50)")

        quotes = await market_service.get_multiple_quotes(symbol_list)

        logger.info("Multiple quotes retrieved via API", symbols=symbol_list, count=len(quotes))
        return {
            "quotes": quotes,
            "requested_symbols": symbol_list,
            "found_symbols": list(quotes.keys()),
            "missing_symbols": [s for s in symbol_list if s not in quotes]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("API: Failed to get multiple quotes", symbols=symbols, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve quotes")


@router.get("/historical/{symbol}")
async def get_historical_data(
    symbol: str,
    period: str = Query(default="1y", description="Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)"),
    interval: str = Query(default="1d", description="Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)"),
    market_service: MarketDataService = Depends(get_market_service)
):
    """Get historical data for a symbol"""
    try:
        # Convert period to start/end dates
        end_date = datetime.now()

        period_mapping = {
            "1d": timedelta(days=1),
            "5d": timedelta(days=5),
            "1mo": timedelta(days=30),
            "3mo": timedelta(days=90),
            "6mo": timedelta(days=180),
            "1y": timedelta(days=365),
            "2y": timedelta(days=730),
            "5y": timedelta(days=1825),
            "10y": timedelta(days=3650),
        }

        if period not in period_mapping:
            raise HTTPException(status_code=400, detail=f"Invalid period: {period}")

        start_date = end_date - period_mapping[period]

        historical_data = await market_service.get_historical_data(
            symbol.upper(), start_date, end_date, interval
        )

        if historical_data is None or historical_data.empty:
            raise HTTPException(status_code=404, detail=f"Historical data not found for symbol: {symbol}")

        # Convert DataFrame to JSON-friendly format
        data_records = []
        for index, row in historical_data.iterrows():
            record = {
                "date": index.isoformat(),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"]),
            }

            # Add technical indicators if available
            if "SMA_20" in row and pd.notna(row["SMA_20"]):
                record["sma_20"] = float(row["SMA_20"])
            if "SMA_50" in row and pd.notna(row["SMA_50"]):
                record["sma_50"] = float(row["SMA_50"])
            if "RSI" in row and pd.notna(row["RSI"]):
                record["rsi"] = float(row["RSI"])
            if "MACD" in row and pd.notna(row["MACD"]):
                record["macd"] = float(row["MACD"])

            data_records.append(record)

        logger.info(
            "Historical data retrieved via API",
            symbol=symbol,
            period=period,
            interval=interval,
            records=len(data_records)
        )

        return {
            "symbol": symbol.upper(),
            "period": period,
            "interval": interval,
            "data": data_records,
            "count": len(data_records)
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("API: Failed to get historical data", symbol=symbol, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve historical data")


@router.get("/movers")
async def get_market_movers(
    limit: int = Query(default=20, ge=1, le=100),
    market_service: MarketDataService = Depends(get_market_service)
):
    """Get market movers (gainers, losers, most active)"""
    try:
        movers = await market_service.get_market_movers(limit)

        logger.info("Market movers retrieved via API", limit=limit)
        return movers

    except Exception as e:
        logger.error("API: Failed to get market movers", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve market movers")


@router.get("/sectors")
async def get_sector_performance(
    market_service: MarketDataService = Depends(get_market_service)
):
    """Get sector performance data"""
    try:
        sectors = await market_service.get_sector_performance()

        logger.info("Sector performance retrieved via API", sectors_count=len(sectors))
        return {
            "sectors": sectors,
            "updated_at": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error("API: Failed to get sector performance", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve sector performance")


@router.get("/indices")
async def get_market_indices(
    market_service: MarketDataService = Depends(get_market_service)
):
    """Get major market indices"""
    try:
        indices = await market_service.get_market_indices()

        logger.info("Market indices retrieved via API", indices_count=len(indices))
        return {
            "indices": indices,
            "updated_at": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error("API: Failed to get market indices", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve market indices")


@router.get("/overview")
async def get_market_overview(
    market_service: MarketDataService = Depends(get_market_service)
):
    """Get comprehensive market overview"""
    try:
        # Get all market data
        indices = await market_service.get_market_indices()
        movers = await market_service.get_market_movers(10)
        sectors = await market_service.get_sector_performance()

        # Market status
        market_status = market_service._get_market_status()

        overview = {
            "market_status": market_status,
            "indices": indices,
            "movers": movers,
            "sectors": sectors,
            "updated_at": datetime.now().isoformat()
        }

        logger.info("Market overview retrieved via API")
        return overview

    except Exception as e:
        logger.error("API: Failed to get market overview", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve market overview")


@router.get("/search")
async def search_symbols(
    query: str = Query(..., min_length=1, description="Search query for symbols"),
    limit: int = Query(default=10, ge=1, le=50)
):
    """Search for symbols (mock implementation)"""
    try:
        # Mock symbol search - in production, use actual symbol search API
        mock_symbols = [
            {"symbol": "AAPL", "name": "Apple Inc.", "type": "stock", "exchange": "NASDAQ"},
            {"symbol": "MSFT", "name": "Microsoft Corporation", "type": "stock", "exchange": "NASDAQ"},
            {"symbol": "GOOGL", "name": "Alphabet Inc.", "type": "stock", "exchange": "NASDAQ"},
            {"symbol": "AMZN", "name": "Amazon.com Inc.", "type": "stock", "exchange": "NASDAQ"},
            {"symbol": "TSLA", "name": "Tesla Inc.", "type": "stock", "exchange": "NASDAQ"},
            {"symbol": "META", "name": "Meta Platforms Inc.", "type": "stock", "exchange": "NASDAQ"},
            {"symbol": "NVDA", "name": "NVIDIA Corporation", "type": "stock", "exchange": "NASDAQ"},
            {"symbol": "SPY", "name": "SPDR S&P 500 ETF Trust", "type": "etf", "exchange": "NYSE"},
            {"symbol": "QQQ", "name": "Invesco QQQ Trust", "type": "etf", "exchange": "NASDAQ"},
        ]

        # Simple filter based on query
        query_upper = query.upper()
        filtered_symbols = [
            symbol for symbol in mock_symbols
            if query_upper in symbol["symbol"] or query_upper in symbol["name"].upper()
        ][:limit]

        logger.info("Symbol search performed", query=query, results=len(filtered_symbols))
        return {
            "query": query,
            "results": filtered_symbols,
            "total": len(filtered_symbols)
        }

    except Exception as e:
        logger.error("API: Failed to search symbols", query=query, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to search symbols")


@router.get("/status")
async def get_market_status():
    """Get current market status"""
    try:
        market_service = MarketDataService()
        status = market_service._get_market_status()

        return {
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "timezone": "UTC"
        }

    except Exception as e:
        logger.error("API: Failed to get market status", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve market status")