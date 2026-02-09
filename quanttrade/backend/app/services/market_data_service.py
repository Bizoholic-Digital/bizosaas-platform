"""
Market Data Service for QuantTrade Platform
Real-time and historical market data management
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import yfinance as yf
import pandas as pd
import numpy as np
import structlog
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.cache import get_cache, CacheKeys
from core.config import get_settings
from models.market_data_model import MarketData, CompanyInfo

logger = structlog.get_logger(__name__)
settings = get_settings()


class MarketDataService:
    """Service for managing market data"""

    def __init__(self):
        self.cache = get_cache()
        self.update_interval = settings.MARKET_DATA_UPDATE_INTERVAL

    async def get_real_time_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get real-time quote for a symbol"""
        # Check cache first
        cache_key = CacheKeys.market_data(symbol)
        cached_data = await self.cache.get(cache_key)

        if cached_data:
            logger.debug("Cache hit for market data", symbol=symbol)
            return cached_data

        try:
            # Fetch from Yahoo Finance
            ticker = yf.Ticker(symbol)
            info = ticker.info

            # Get current price data
            hist = ticker.history(period="1d", interval="1m")

            if hist.empty:
                logger.warning("No data available", symbol=symbol)
                return None

            latest = hist.iloc[-1]

            quote_data = {
                "symbol": symbol,
                "price": float(latest['Close']),
                "open": float(latest['Open']),
                "high": float(latest['High']),
                "low": float(latest['Low']),
                "volume": int(latest['Volume']),
                "change": float(latest['Close'] - latest['Open']),
                "change_percent": float((latest['Close'] - latest['Open']) / latest['Open'] * 100),
                "timestamp": datetime.now().isoformat(),
                "market_cap": info.get('marketCap'),
                "pe_ratio": info.get('trailingPE'),
                "dividend_yield": info.get('dividendYield'),
                "52_week_high": info.get('fiftyTwoWeekHigh'),
                "52_week_low": info.get('fiftyTwoWeekLow'),
                "avg_volume": info.get('averageVolume'),
                "sector": info.get('sector'),
                "industry": info.get('industry')
            }

            # Cache for 30 seconds
            await self.cache.set(cache_key, quote_data, ttl=30)

            logger.info("Real-time quote fetched", symbol=symbol, price=quote_data['price'])
            return quote_data

        except Exception as e:
            logger.error("Failed to fetch real-time quote", symbol=symbol, error=str(e))
            return None

    async def get_historical_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """Get historical data for a symbol"""
        try:
            # Check if data exists in database first
            # For now, fetch from Yahoo Finance directly
            ticker = yf.Ticker(symbol)
            hist = ticker.history(
                start=start_date,
                end=end_date,
                interval=interval,
                auto_adjust=True,
                prepost=False
            )

            if hist.empty:
                logger.warning("No historical data available", symbol=symbol)
                return None

            # Add technical indicators
            hist = self._add_technical_indicators(hist)

            logger.info(
                "Historical data fetched",
                symbol=symbol,
                start=start_date.date(),
                end=end_date.date(),
                rows=len(hist)
            )

            return hist

        except Exception as e:
            logger.error("Failed to fetch historical data", symbol=symbol, error=str(e))
            return None

    def _add_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add technical indicators to price data"""
        try:
            # Simple Moving Averages
            df['SMA_20'] = df['Close'].rolling(window=20).mean()
            df['SMA_50'] = df['Close'].rolling(window=50).mean()

            # Exponential Moving Averages
            df['EMA_12'] = df['Close'].ewm(span=12).mean()
            df['EMA_26'] = df['Close'].ewm(span=26).mean()

            # MACD
            df['MACD'] = df['EMA_12'] - df['EMA_26']
            df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()

            # RSI
            df['RSI'] = self._calculate_rsi(df['Close'])

            # Bollinger Bands
            bb_period = 20
            bb_std = 2
            df['BB_Middle'] = df['Close'].rolling(window=bb_period).mean()
            bb_std_dev = df['Close'].rolling(window=bb_period).std()
            df['BB_Upper'] = df['BB_Middle'] + (bb_std_dev * bb_std)
            df['BB_Lower'] = df['BB_Middle'] - (bb_std_dev * bb_std)

            # Average True Range (ATR)
            df['ATR'] = self._calculate_atr(df)

            return df

        except Exception as e:
            logger.error("Failed to calculate technical indicators", error=str(e))
            return df

    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def _calculate_atr(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())

        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        return true_range.rolling(window=period).mean()

    async def get_multiple_quotes(self, symbols: List[str]) -> Dict[str, Dict[str, Any]]:
        """Get real-time quotes for multiple symbols"""
        tasks = [self.get_real_time_quote(symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        quotes = {}
        for symbol, result in zip(symbols, results):
            if isinstance(result, Exception):
                logger.error("Failed to get quote", symbol=symbol, error=str(result))
                continue
            if result:
                quotes[symbol] = result

        return quotes

    async def get_market_movers(self, limit: int = 20) -> Dict[str, List[Dict[str, Any]]]:
        """Get market movers (gainers, losers, most active)"""
        try:
            # Popular symbols for demo (in production, use screener APIs)
            symbols = [
                'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX',
                'SPY', 'QQQ', 'IWM', 'DIA', 'AMD', 'INTC', 'CRM', 'ORCL'
            ]

            quotes = await self.get_multiple_quotes(symbols)

            # Sort by different criteria
            sorted_quotes = sorted(
                [q for q in quotes.values() if q],
                key=lambda x: x.get('change_percent', 0),
                reverse=True
            )

            gainers = sorted_quotes[:limit]
            losers = sorted_quotes[-limit:][::-1]  # Reverse for ascending order

            # Most active (by volume)
            most_active = sorted(
                [q for q in quotes.values() if q and q.get('volume')],
                key=lambda x: x.get('volume', 0),
                reverse=True
            )[:limit]

            return {
                "gainers": gainers,
                "losers": losers,
                "most_active": most_active
            }

        except Exception as e:
            logger.error("Failed to get market movers", error=str(e))
            return {"gainers": [], "losers": [], "most_active": []}

    async def get_sector_performance(self) -> List[Dict[str, Any]]:
        """Get sector performance data"""
        try:
            # Sector ETFs
            sector_etfs = {
                'Technology': 'XLK',
                'Healthcare': 'XLV',
                'Financial': 'XLF',
                'Consumer Discretionary': 'XLY',
                'Communication': 'XLC',
                'Industrials': 'XLI',
                'Consumer Staples': 'XLP',
                'Energy': 'XLE',
                'Utilities': 'XLU',
                'Real Estate': 'XLRE',
                'Materials': 'XLB'
            }

            quotes = await self.get_multiple_quotes(list(sector_etfs.values()))

            sector_performance = []
            for sector_name, etf_symbol in sector_etfs.items():
                if etf_symbol in quotes:
                    quote = quotes[etf_symbol]
                    sector_performance.append({
                        'sector': sector_name,
                        'symbol': etf_symbol,
                        'price': quote['price'],
                        'change': quote['change'],
                        'change_percent': quote['change_percent']
                    })

            # Sort by performance
            sector_performance.sort(key=lambda x: x['change_percent'], reverse=True)

            return sector_performance

        except Exception as e:
            logger.error("Failed to get sector performance", error=str(e))
            return []

    async def get_market_indices(self) -> Dict[str, Dict[str, Any]]:
        """Get major market indices"""
        indices = {
            'SPY': 'S&P 500',
            'QQQ': 'NASDAQ 100',
            'IWM': 'Russell 2000',
            'DIA': 'Dow Jones',
            'VIX': 'Volatility Index'
        }

        quotes = await self.get_multiple_quotes(list(indices.keys()))

        market_data = {}
        for symbol, name in indices.items():
            if symbol in quotes:
                quote_data = quotes[symbol]
                quote_data['name'] = name
                market_data[symbol] = quote_data

        return market_data

    async def get_real_time_data(self) -> Dict[str, Any]:
        """Get comprehensive real-time market data for WebSocket"""
        try:
            # Get various market data
            indices = await self.get_market_indices()
            movers = await self.get_market_movers(10)
            sectors = await self.get_sector_performance()

            return {
                "timestamp": datetime.now().isoformat(),
                "indices": indices,
                "movers": movers,
                "sectors": sectors,
                "market_status": self._get_market_status()
            }

        except Exception as e:
            logger.error("Failed to get real-time data", error=str(e))
            return {
                "timestamp": datetime.now().isoformat(),
                "error": "Failed to fetch market data"
            }

    def _get_market_status(self) -> str:
        """Determine current market status"""
        now = datetime.now()
        hour = now.hour
        weekday = now.weekday()

        # Weekend
        if weekday >= 5:  # Saturday = 5, Sunday = 6
            return "closed"

        # Market hours (9:30 AM - 4:00 PM EST, simplified)
        if 9 <= hour < 16:
            return "open"
        elif 4 <= hour < 9:
            return "pre_market"
        elif 16 <= hour < 20:
            return "after_hours"
        else:
            return "closed"

    async def store_market_data(self, symbol: str, data: pd.DataFrame) -> bool:
        """Store market data to database"""
        try:
            async with get_db() as db:
                for index, row in data.iterrows():
                    market_data = MarketData(
                        symbol=symbol,
                        date=index,
                        open_price=row['Open'],
                        high_price=row['High'],
                        low_price=row['Low'],
                        close_price=row['Close'],
                        volume=row['Volume'],
                        adj_close=row.get('Adj Close', row['Close']),
                        sma_20=row.get('SMA_20'),
                        sma_50=row.get('SMA_50'),
                        ema_12=row.get('EMA_12'),
                        ema_26=row.get('EMA_26'),
                        rsi_14=row.get('RSI'),
                        macd=row.get('MACD'),
                        macd_signal=row.get('MACD_Signal'),
                        bb_upper=row.get('BB_Upper'),
                        bb_lower=row.get('BB_Lower'),
                        atr_14=row.get('ATR')
                    )
                    db.add(market_data)

                await db.commit()
                logger.info("Market data stored", symbol=symbol, rows=len(data))
                return True

        except Exception as e:
            logger.error("Failed to store market data", symbol=symbol, error=str(e))
            return False