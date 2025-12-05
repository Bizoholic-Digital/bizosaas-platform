"""
Binance Exchange API Client for Crypto Spot and Futures Trading
Supports market data, order execution, and account management
"""
import asyncio
import hashlib
import hmac
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
import aiohttp
from urllib.parse import urlencode
from config import settings
import logging

logger = logging.getLogger(__name__)


class BinanceClient:
    """
    Binance API client for crypto spot and futures trading
    Supports both testnet and production environments
    """
    
    BASE_URL_PROD = "https://api.binance.com"
    BASE_URL_TEST = "https://testnet.binance.vision"
    WS_URL_PROD = "wss://stream.binance.com:9443/ws"
    WS_URL_TEST = "wss://testnet.binance.vision/ws"
    
    def __init__(self, api_key: str = None, api_secret: str = None, testnet: bool = True):
        """
        Initialize Binance client
        
        Args:
            api_key: API key from Binance
            api_secret: API secret from Binance
            testnet: Use testnet if True, production if False
        """
        self.api_key = api_key or settings.BINANCE_API_KEY
        self.api_secret = api_secret or settings.BINANCE_API_SECRET
        self.testnet = testnet
        self.base_url = self.BASE_URL_TEST if testnet else self.BASE_URL_PROD
        self.ws_url = self.WS_URL_TEST if testnet else self.WS_URL_PROD
        self.session: Optional[aiohttp.ClientSession] = None
        self.ws: Optional[aiohttp.ClientWebSocketResponse] = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
        
    async def connect(self):
        """Initialize HTTP session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
    async def close(self):
        """Close HTTP session and WebSocket connection"""
        if self.ws:
            await self.ws.close()
        if self.session:
            await self.session.close()
            
    def _generate_signature(self, params: Dict) -> str:
        """
        Generate HMAC SHA256 signature for authenticated requests
        
        Args:
            params: Request parameters
            
        Returns:
            Signature string
        """
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
        
    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        signed: bool = False
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Binance API
        
        Args:
            method: HTTP method (GET, POST, DELETE)
            endpoint: API endpoint
            params: Request parameters
            signed: Whether request requires signature
            
        Returns:
            API response as dictionary
        """
        if not self.session:
            await self.connect()
            
        url = f"{self.base_url}{endpoint}"
        headers = {"X-MBX-APIKEY": self.api_key} if self.api_key else {}
        
        if params is None:
            params = {}
            
        if signed:
            params["timestamp"] = int(time.time() * 1000)
            params["signature"] = self._generate_signature(params)
            
        try:
            async with self.session.request(method, url, params=params, headers=headers) as response:
                data = await response.json()
                
                if response.status != 200:
                    logger.error(f"Binance API error: {data}")
                    raise Exception(f"Binance API error: {data}")
                    
                return data
                
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise
            
    # Market Data Methods
    
    async def get_exchange_info(self) -> Dict[str, Any]:
        """
        Get exchange information including trading rules and symbols
        
        Returns:
            Exchange information
        """
        return await self._request("GET", "/api/v3/exchangeInfo")
        
    async def get_ticker(self, symbol: str) -> Dict[str, Any]:
        """
        Get 24hr ticker price change statistics
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            
        Returns:
            Ticker data
        """
        params = {"symbol": symbol}
        return await self._request("GET", "/api/v3/ticker/24hr", params)
        
    async def get_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get latest price for a symbol
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Price data
        """
        params = {"symbol": symbol}
        return await self._request("GET", "/api/v3/ticker/price", params)
        
    async def get_order_book(self, symbol: str, limit: int = 100) -> Dict[str, Any]:
        """
        Get order book for a symbol
        
        Args:
            symbol: Trading pair symbol
            limit: Order book depth (5, 10, 20, 50, 100, 500, 1000, 5000)
            
        Returns:
            Order book data
        """
        params = {
            "symbol": symbol,
            "limit": limit
        }
        return await self._request("GET", "/api/v3/depth", params)
        
    async def get_klines(
        self,
        symbol: str,
        interval: str = "1h",
        limit: int = 500,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None
    ) -> List[List]:
        """
        Get candlestick data
        
        Args:
            symbol: Trading pair symbol
            interval: Kline interval (1m, 5m, 15m, 1h, 4h, 1d, etc.)
            limit: Number of klines to return (max 1000)
            start_time: Start timestamp (ms)
            end_time: End timestamp (ms)
            
        Returns:
            List of klines
        """
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
            
        return await self._request("GET", "/api/v3/klines", params)
        
    # Trading Methods
    
    async def create_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        time_in_force: str = "GTC"
    ) -> Dict[str, Any]:
        """
        Create a new order
        
        Args:
            symbol: Trading pair symbol
            side: Order side (BUY, SELL)
            order_type: Order type (LIMIT, MARKET, STOP_LOSS, etc.)
            quantity: Order quantity
            price: Order price (required for LIMIT orders)
            time_in_force: Time in force (GTC, IOC, FOK)
            
        Returns:
            Order response
        """
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity
        }
        
        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = time_in_force
            
        return await self._request("POST", "/api/v3/order", params, signed=True)
        
    async def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Cancel an active order
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID to cancel
            
        Returns:
            Cancellation response
        """
        params = {
            "symbol": symbol,
            "orderId": order_id
        }
        return await self._request("DELETE", "/api/v3/order", params, signed=True)
        
    async def cancel_all_orders(self, symbol: str) -> List[Dict]:
        """
        Cancel all open orders for a symbol
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            List of cancelled orders
        """
        params = {"symbol": symbol}
        return await self._request("DELETE", "/api/v3/openOrders", params, signed=True)
        
    async def get_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Get order details
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID
            
        Returns:
            Order details
        """
        params = {
            "symbol": symbol,
            "orderId": order_id
        }
        return await self._request("GET", "/api/v3/order", params, signed=True)
        
    async def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict]:
        """
        Get all open orders
        
        Args:
            symbol: Trading pair symbol (None for all symbols)
            
        Returns:
            List of open orders
        """
        params = {}
        if symbol:
            params["symbol"] = symbol
            
        return await self._request("GET", "/api/v3/openOrders", params, signed=True)
        
    # Account Methods
    
    async def get_account(self) -> Dict[str, Any]:
        """
        Get account information
        
        Returns:
            Account information including balances
        """
        return await self._request("GET", "/api/v3/account", signed=True)
        
    async def get_balance(self, asset: str) -> Dict[str, Any]:
        """
        Get balance for a specific asset
        
        Args:
            asset: Asset symbol (e.g., 'BTC', 'USDT')
            
        Returns:
            Asset balance
        """
        account = await self.get_account()
        balances = account.get("balances", [])
        
        for balance in balances:
            if balance["asset"] == asset:
                return balance
                
        return {"asset": asset, "free": "0", "locked": "0"}
        
    async def get_trades(self, symbol: str, limit: int = 500) -> List[Dict]:
        """
        Get trade history
        
        Args:
            symbol: Trading pair symbol
            limit: Number of trades to return (max 1000)
            
        Returns:
            List of trades
        """
        params = {
            "symbol": symbol,
            "limit": limit
        }
        return await self._request("GET", "/api/v3/myTrades", params, signed=True)
        
    # WebSocket Methods
    
    async def subscribe_ticker(self, symbol: str, callback):
        """
        Subscribe to ticker updates via WebSocket
        
        Args:
            symbol: Trading pair symbol (lowercase)
            callback: Callback function for ticker updates
        """
        if not self.ws:
            stream = f"{symbol.lower()}@ticker"
            ws_url = f"{self.ws_url}/{stream}"
            self.ws = await self.session.ws_connect(ws_url)
            
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                import json
                data = json.loads(msg.data)
                await callback(data)
                
    async def subscribe_kline(self, symbol: str, interval: str, callback):
        """
        Subscribe to kline/candlestick updates via WebSocket
        
        Args:
            symbol: Trading pair symbol (lowercase)
            interval: Kline interval (1m, 5m, 15m, 1h, etc.)
            callback: Callback function for kline updates
        """
        if not self.ws:
            stream = f"{symbol.lower()}@kline_{interval}"
            ws_url = f"{self.ws_url}/{stream}"
            self.ws = await self.session.ws_connect(ws_url)
            
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                import json
                data = json.loads(msg.data)
                await callback(data)
                
    async def subscribe_depth(self, symbol: str, callback):
        """
        Subscribe to order book depth updates via WebSocket
        
        Args:
            symbol: Trading pair symbol (lowercase)
            callback: Callback function for depth updates
        """
        if not self.ws:
            stream = f"{symbol.lower()}@depth"
            ws_url = f"{self.ws_url}/{stream}"
            self.ws = await self.session.ws_connect(ws_url)
            
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                import json
                data = json.loads(msg.data)
                await callback(data)
