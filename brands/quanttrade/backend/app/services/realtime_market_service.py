"""
Real-time Market Data Service - WebSocket feeds for live trading data
"""

import asyncio
import json
import websockets
import yfinance as yf
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
import pandas as pd
import structlog
from dataclasses import dataclass, asdict
import aiohttp
from decimal import Decimal

from core.config import get_settings
from core.cache import get_redis_client

logger = structlog.get_logger(__name__)
settings = get_settings()


@dataclass
class MarketQuote:
    """Real-time market quote data structure"""
    symbol: str
    price: float
    bid: float
    ask: float
    bid_size: int
    ask_size: int
    volume: int
    timestamp: datetime
    change: float
    change_percent: float
    high: float
    low: float
    open: float
    previous_close: float


@dataclass
class MarketTick:
    """Individual market tick data"""
    symbol: str
    price: float
    size: int
    timestamp: datetime
    side: str  # 'buy' or 'sell'


@dataclass
class OrderBookLevel:
    """Order book level data"""
    price: float
    size: int
    num_orders: int


@dataclass
class OrderBook:
    """Order book data structure"""
    symbol: str
    bids: List[OrderBookLevel]
    asks: List[OrderBookLevel]
    timestamp: datetime


class RealTimeMarketDataService:
    """Real-time market data service with multiple data sources"""

    def __init__(self):
        self.redis_client = get_redis_client()
        self.active_connections: Dict[str, List[websockets.WebSocketServerProtocol]] = {}
        self.subscribed_symbols: Dict[str, int] = {}  # symbol -> subscriber count
        self.data_feeds: Dict[str, asyncio.Task] = {}  # symbol -> feed task
        self.quote_cache: Dict[str, MarketQuote] = {}
        self.tick_buffer: Dict[str, List[MarketTick]] = {}
        logger.info("Real-time market data service initialized")

    async def subscribe_to_symbol(self, symbol: str, websocket, callback: Optional[Callable] = None):
        """Subscribe a WebSocket connection to real-time data for a symbol"""
        try:
            symbol = symbol.upper()

            # Add to active connections
            if symbol not in self.active_connections:
                self.active_connections[symbol] = []
            self.active_connections[symbol].append(websocket)

            # Track subscriber count
            self.subscribed_symbols[symbol] = self.subscribed_symbols.get(symbol, 0) + 1

            # Start data feed if this is the first subscriber
            if self.subscribed_symbols[symbol] == 1:
                await self._start_data_feed(symbol)

            logger.info("WebSocket subscribed to symbol",
                       symbol=symbol,
                       subscribers=self.subscribed_symbols[symbol])

            # Send current quote if available
            if symbol in self.quote_cache:
                await self._send_to_websocket(websocket, {
                    "type": "quote",
                    "data": asdict(self.quote_cache[symbol])
                })

        except Exception as e:
            logger.error("Error subscribing to symbol", symbol=symbol, error=str(e))

    async def unsubscribe_from_symbol(self, symbol: str, websocket):
        """Unsubscribe a WebSocket connection from a symbol"""
        try:
            symbol = symbol.upper()

            # Remove from active connections
            if symbol in self.active_connections:
                if websocket in self.active_connections[symbol]:
                    self.active_connections[symbol].remove(websocket)

            # Update subscriber count
            if symbol in self.subscribed_symbols:
                self.subscribed_symbols[symbol] = max(0, self.subscribed_symbols[symbol] - 1)

                # Stop data feed if no more subscribers
                if self.subscribed_symbols[symbol] == 0:
                    await self._stop_data_feed(symbol)
                    del self.subscribed_symbols[symbol]

            logger.info("WebSocket unsubscribed from symbol",
                       symbol=symbol,
                       remaining_subscribers=self.subscribed_symbols.get(symbol, 0))

        except Exception as e:
            logger.error("Error unsubscribing from symbol", symbol=symbol, error=str(e))

    async def get_real_time_quote(self, symbol: str) -> Optional[MarketQuote]:
        """Get the latest real-time quote for a symbol"""
        try:
            symbol = symbol.upper()

            # Try cache first
            if symbol in self.quote_cache:
                return self.quote_cache[symbol]

            # Fetch from Yahoo Finance if not in cache
            quote_data = await self._fetch_yahoo_quote(symbol)
            if quote_data:
                quote = self._parse_yahoo_quote(symbol, quote_data)
                self.quote_cache[symbol] = quote
                return quote

            return None

        except Exception as e:
            logger.error("Error getting real-time quote", symbol=symbol, error=str(e))
            return None

    async def get_intraday_data(self, symbol: str, interval: str = "1m", period: str = "1d") -> Optional[pd.DataFrame]:
        """Get intraday data for a symbol"""
        try:
            symbol = symbol.upper()

            # Check Redis cache first
            cache_key = f"intraday:{symbol}:{interval}:{period}"
            cached_data = await self.redis_client.get(cache_key)

            if cached_data:
                # Deserialize from cache
                data_dict = json.loads(cached_data)
                df = pd.DataFrame(data_dict)
                df.index = pd.to_datetime(df.index)
                return df

            # Fetch from Yahoo Finance
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)

            if not data.empty:
                # Cache for 1 minute
                data_dict = data.to_dict('index')
                # Convert timestamps to strings for JSON serialization
                serializable_dict = {
                    str(k): v for k, v in data_dict.items()
                }
                await self.redis_client.setex(
                    cache_key,
                    60,  # 1 minute cache
                    json.dumps(serializable_dict, default=str)
                )

                return data

            return None

        except Exception as e:
            logger.error("Error getting intraday data", symbol=symbol, error=str(e))
            return None

    async def get_order_book(self, symbol: str) -> Optional[OrderBook]:
        """Get order book data for a symbol (mock implementation)"""
        try:
            # This is a mock implementation
            # In production, integrate with a broker API that provides Level 2 data
            quote = await self.get_real_time_quote(symbol)
            if not quote:
                return None

            # Generate mock order book based on current quote
            spread = abs(quote.ask - quote.bid)
            tick_size = 0.01

            bids = []
            asks = []

            # Generate 10 levels on each side
            for i in range(10):
                bid_price = quote.bid - (i * tick_size)
                ask_price = quote.ask + (i * tick_size)

                # Mock size decreasing with distance from best price
                size = max(100, 1000 - (i * 50))
                num_orders = max(1, 10 - i)

                bids.append(OrderBookLevel(bid_price, size, num_orders))
                asks.append(OrderBookLevel(ask_price, size, num_orders))

            return OrderBook(
                symbol=symbol,
                bids=bids,
                asks=asks,
                timestamp=datetime.now()
            )

        except Exception as e:
            logger.error("Error getting order book", symbol=symbol, error=str(e))
            return None

    async def get_market_hours(self, symbol: str) -> Dict[str, Any]:
        """Get market hours information for a symbol"""
        try:
            # Mock market hours - in production, get from market data provider
            current_time = datetime.now()
            market_hours = {
                "symbol": symbol,
                "timezone": "America/New_York",
                "is_open": True,  # Mock as always open for demo
                "next_open": "2024-01-16 09:30:00",
                "next_close": "2024-01-16 16:00:00",
                "session_type": "regular",
                "pre_market": {
                    "is_active": False,
                    "start": "04:00:00",
                    "end": "09:30:00"
                },
                "after_hours": {
                    "is_active": True,
                    "start": "16:00:00",
                    "end": "20:00:00"
                }
            }

            return market_hours

        except Exception as e:
            logger.error("Error getting market hours", symbol=symbol, error=str(e))
            return {}

    async def _start_data_feed(self, symbol: str):
        """Start real-time data feed for a symbol"""
        try:
            logger.info("Starting data feed", symbol=symbol)

            # Create background task for data feed
            self.data_feeds[symbol] = asyncio.create_task(
                self._run_data_feed(symbol)
            )

        except Exception as e:
            logger.error("Error starting data feed", symbol=symbol, error=str(e))

    async def _stop_data_feed(self, symbol: str):
        """Stop real-time data feed for a symbol"""
        try:
            if symbol in self.data_feeds:
                self.data_feeds[symbol].cancel()
                del self.data_feeds[symbol]

                logger.info("Stopped data feed", symbol=symbol)

        except Exception as e:
            logger.error("Error stopping data feed", symbol=symbol, error=str(e))

    async def _run_data_feed(self, symbol: str):
        """Run continuous data feed for a symbol"""
        try:
            while symbol in self.subscribed_symbols and self.subscribed_symbols[symbol] > 0:
                # Fetch latest quote
                quote_data = await self._fetch_yahoo_quote(symbol)
                if quote_data:
                    quote = self._parse_yahoo_quote(symbol, quote_data)
                    self.quote_cache[symbol] = quote

                    # Broadcast to all subscribers
                    await self._broadcast_quote(symbol, quote)

                    # Generate mock ticks
                    await self._generate_mock_ticks(symbol, quote)

                # Wait before next update (simulate real-time feed)
                await asyncio.sleep(1)  # 1-second updates

        except asyncio.CancelledError:
            logger.info("Data feed cancelled", symbol=symbol)
        except Exception as e:
            logger.error("Error in data feed", symbol=symbol, error=str(e))

    async def _fetch_yahoo_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch quote data from Yahoo Finance"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info

            if info:
                return {
                    "price": info.last_price,
                    "open": info.open,
                    "high": info.day_high,
                    "low": info.day_low,
                    "volume": info.ten_day_avg_volume,  # Approximation
                    "previous_close": info.previous_close,
                    "bid": info.last_price * 0.999,  # Mock bid slightly below last price
                    "ask": info.last_price * 1.001,  # Mock ask slightly above last price
                }

            return None

        except Exception as e:
            logger.error("Error fetching Yahoo quote", symbol=symbol, error=str(e))
            return None

    def _parse_yahoo_quote(self, symbol: str, data: Dict[str, Any]) -> MarketQuote:
        """Parse Yahoo Finance data into MarketQuote"""
        price = float(data.get("price", 0))
        previous_close = float(data.get("previous_close", price))

        change = price - previous_close
        change_percent = (change / previous_close * 100) if previous_close > 0 else 0

        return MarketQuote(
            symbol=symbol,
            price=price,
            bid=float(data.get("bid", price * 0.999)),
            ask=float(data.get("ask", price * 1.001)),
            bid_size=100,  # Mock size
            ask_size=100,  # Mock size
            volume=int(data.get("volume", 1000000)),
            timestamp=datetime.now(),
            change=change,
            change_percent=change_percent,
            high=float(data.get("high", price)),
            low=float(data.get("low", price)),
            open=float(data.get("open", price)),
            previous_close=previous_close
        )

    async def _broadcast_quote(self, symbol: str, quote: MarketQuote):
        """Broadcast quote to all subscribers"""
        try:
            if symbol not in self.active_connections:
                return

            message = {
                "type": "quote",
                "data": asdict(quote)
            }

            # Send to all active WebSocket connections
            disconnected = []
            for websocket in self.active_connections[symbol]:
                try:
                    await self._send_to_websocket(websocket, message)
                except Exception:
                    disconnected.append(websocket)

            # Remove disconnected WebSockets
            for websocket in disconnected:
                await self.unsubscribe_from_symbol(symbol, websocket)

        except Exception as e:
            logger.error("Error broadcasting quote", symbol=symbol, error=str(e))

    async def _generate_mock_ticks(self, symbol: str, quote: MarketQuote):
        """Generate mock tick data for demonstration"""
        try:
            # Generate 1-3 random ticks
            import random
            num_ticks = random.randint(1, 3)

            for _ in range(num_ticks):
                # Random price within bid-ask spread
                tick_price = random.uniform(quote.bid, quote.ask)
                tick_size = random.randint(100, 1000)
                tick_side = random.choice(['buy', 'sell'])

                tick = MarketTick(
                    symbol=symbol,
                    price=tick_price,
                    size=tick_size,
                    timestamp=datetime.now(),
                    side=tick_side
                )

                # Add to tick buffer
                if symbol not in self.tick_buffer:
                    self.tick_buffer[symbol] = []
                self.tick_buffer[symbol].append(tick)

                # Keep only last 100 ticks
                if len(self.tick_buffer[symbol]) > 100:
                    self.tick_buffer[symbol] = self.tick_buffer[symbol][-100:]

                # Broadcast tick
                await self._broadcast_tick(symbol, tick)

        except Exception as e:
            logger.error("Error generating mock ticks", symbol=symbol, error=str(e))

    async def _broadcast_tick(self, symbol: str, tick: MarketTick):
        """Broadcast tick data to subscribers"""
        try:
            if symbol not in self.active_connections:
                return

            message = {
                "type": "tick",
                "data": asdict(tick)
            }

            # Send to all active WebSocket connections
            for websocket in self.active_connections[symbol]:
                try:
                    await self._send_to_websocket(websocket, message)
                except Exception:
                    pass  # Will be cleaned up in next quote broadcast

        except Exception as e:
            logger.error("Error broadcasting tick", symbol=symbol, error=str(e))

    async def _send_to_websocket(self, websocket, message: Dict[str, Any]):
        """Send message to WebSocket connection"""
        try:
            if websocket.open:
                # Convert datetime objects to ISO format for JSON serialization
                serialized_message = self._serialize_message(message)
                await websocket.send(json.dumps(serialized_message))
        except Exception as e:
            logger.error("Error sending WebSocket message", error=str(e))
            raise

    def _serialize_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Serialize message for JSON transmission"""
        def serialize_value(value):
            if isinstance(value, datetime):
                return value.isoformat()
            elif isinstance(value, dict):
                return {k: serialize_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [serialize_value(item) for item in value]
            else:
                return value

        return serialize_value(message)

    async def get_symbol_stats(self, symbols: List[str]) -> Dict[str, Dict[str, Any]]:
        """Get comprehensive statistics for multiple symbols"""
        try:
            stats = {}

            for symbol in symbols:
                quote = await self.get_real_time_quote(symbol)
                if quote:
                    # Calculate additional stats
                    intraday_data = await self.get_intraday_data(symbol, "5m", "1d")

                    volatility = 0
                    avg_volume = quote.volume

                    if intraday_data is not None and not intraday_data.empty:
                        returns = intraday_data['Close'].pct_change().dropna()
                        volatility = returns.std() * (252 ** 0.5)  # Annualized
                        avg_volume = intraday_data['Volume'].mean()

                    stats[symbol] = {
                        "quote": asdict(quote),
                        "volatility": volatility,
                        "avg_volume": avg_volume,
                        "tick_count": len(self.tick_buffer.get(symbol, [])),
                        "last_update": quote.timestamp.isoformat()
                    }

            return stats

        except Exception as e:
            logger.error("Error getting symbol stats", error=str(e))
            return {}

    def get_subscription_info(self) -> Dict[str, Any]:
        """Get information about current subscriptions"""
        return {
            "active_symbols": list(self.subscribed_symbols.keys()),
            "total_subscribers": sum(self.subscribed_symbols.values()),
            "active_feeds": len(self.data_feeds),
            "cached_quotes": len(self.quote_cache),
            "subscription_details": dict(self.subscribed_symbols)
        }