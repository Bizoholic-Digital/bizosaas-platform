"""
Market data service for real-time and historical data
"""
import yfinance as yf
import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio
import logging
from alpha_vantage.timeseries import TimeSeries

logger = logging.getLogger(__name__)

class MarketDataService:
    """Service for fetching market data"""

    def __init__(self, alpha_vantage_key: str = "demo"):
        self.av_key = alpha_vantage_key
        self.ts = TimeSeries(key=alpha_vantage_key, output_format='pandas')
        self.cache = {}

    async def get_current_price(self, symbol: str) -> Dict[str, Any]:
        """Get current price for a symbol"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            return {
                "symbol": symbol,
                "price": info.get('currentPrice', info.get('regularMarketPrice', 0)),
                "change": info.get('regularMarketChange', 0),
                "change_percent": info.get('regularMarketChangePercent', 0),
                "volume": info.get('volume', 0),
                "market_cap": info.get('marketCap', 0),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": str(e)
            }

    async def get_historical_data(self,
                                  symbol: str,
                                  period: str = "1mo",
                                  interval: str = "1d") -> Dict[str, Any]:
        """Get historical OHLCV data"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period, interval=interval)

            data = []
            for idx, row in hist.iterrows():
                data.append({
                    "timestamp": idx.isoformat(),
                    "open": float(row['Open']),
                    "high": float(row['High']),
                    "low": float(row['Low']),
                    "close": float(row['Close']),
                    "volume": int(row['Volume'])
                })

            return {
                "symbol": symbol,
                "period": period,
                "interval": interval,
                "data": data
            }
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": str(e)
            }

    async def get_quote(self, symbol: str) -> Dict[str, Any]:
        """Get detailed quote for a symbol"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            return {
                "symbol": symbol,
                "name": info.get('longName', symbol),
                "price": info.get('currentPrice', info.get('regularMarketPrice', 0)),
                "open": info.get('regularMarketOpen', 0),
                "high": info.get('dayHigh', 0),
                "low": info.get('dayLow', 0),
                "volume": info.get('volume', 0),
                "avg_volume": info.get('averageVolume', 0),
                "market_cap": info.get('marketCap', 0),
                "pe_ratio": info.get('trailingPE', 0),
                "dividend_yield": info.get('dividendYield', 0),
                "52w_high": info.get('fiftyTwoWeekHigh', 0),
                "52w_low": info.get('fiftyTwoWeekLow', 0),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching quote for {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": str(e)
            }

    async def get_technical_indicators(self, symbol: str, period: str = "3mo") -> Dict[str, Any]:
        """Calculate technical indicators"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)

            # Calculate indicators
            close = hist['Close']

            # Simple Moving Averages
            sma_20 = close.rolling(window=20).mean().iloc[-1]
            sma_50 = close.rolling(window=50).mean().iloc[-1]
            sma_200 = close.rolling(window=200).mean().iloc[-1] if len(close) >= 200 else None

            # RSI
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))

            # MACD
            exp1 = close.ewm(span=12, adjust=False).mean()
            exp2 = close.ewm(span=26, adjust=False).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=9, adjust=False).mean()

            return {
                "symbol": symbol,
                "indicators": {
                    "sma_20": float(sma_20) if not pd.isna(sma_20) else None,
                    "sma_50": float(sma_50) if not pd.isna(sma_50) else None,
                    "sma_200": float(sma_200) if sma_200 and not pd.isna(sma_200) else None,
                    "rsi": float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else None,
                    "macd": float(macd.iloc[-1]) if not pd.isna(macd.iloc[-1]) else None,
                    "macd_signal": float(signal.iloc[-1]) if not pd.isna(signal.iloc[-1]) else None,
                    "current_price": float(close.iloc[-1])
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error calculating indicators for {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": str(e)
            }

    async def search_symbols(self, query: str) -> List[Dict[str, Any]]:
        """Search for stock symbols"""
        try:
            # This is a simple implementation
            # In production, use a proper API or database
            ticker = yf.Ticker(query.upper())
            info = ticker.info

            if info:
                return [{
                    "symbol": query.upper(),
                    "name": info.get('longName', query),
                    "type": info.get('quoteType', 'EQUITY'),
                    "exchange": info.get('exchange', 'Unknown')
                }]
            return []
        except Exception as e:
            logger.error(f"Error searching symbols: {e}")
            return []

    async def stream_market_data(self, ws_manager, symbols: List[str] = None):
        """Stream real-time market data via WebSocket"""
        if not symbols:
            symbols = ["SPY", "QQQ", "AAPL", "MSFT", "GOOGL"]

        while True:
            try:
                for symbol in symbols:
                    data = await self.get_current_price(symbol)
                    await ws_manager.broadcast(data, "market_data")

                await asyncio.sleep(5)  # Update every 5 seconds
            except Exception as e:
                logger.error(f"Error streaming market data: {e}")
                await asyncio.sleep(10)
