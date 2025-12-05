"""
Deribit Exchange API Client for Crypto Options Trading
Supports market data, order execution, and account management
"""
import asyncio
import hashlib
import hmac
import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
import aiohttp
from config import settings
import logging

logger = logging.getLogger(__name__)


class DeribitClient:
    """
    Deribit API client for crypto options trading
    Supports both testnet and production environments
    """
    
    BASE_URL_PROD = "https://www.deribit.com/api/v2"
    BASE_URL_TEST = "https://test.deribit.com/api/v2"
    WS_URL_PROD = "wss://www.deribit.com/ws/api/v2"
    WS_URL_TEST = "wss://test.deribit.com/ws/api/v2"
    
    def __init__(self, api_key: str = None, api_secret: str = None, testnet: bool = True):
        """
        Initialize Deribit client
        
        Args:
            api_key: API key from Deribit
            api_secret: API secret from Deribit
            testnet: Use testnet if True, production if False
        """
        self.api_key = api_key or settings.DERIBIT_API_KEY
        self.api_secret = api_secret or settings.DERIBIT_API_SECRET
        self.testnet = testnet
        self.base_url = self.BASE_URL_TEST if testnet else self.BASE_URL_PROD
        self.ws_url = self.WS_URL_TEST if testnet else self.WS_URL_PROD
        self.session: Optional[aiohttp.ClientSession] = None
        self.ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
        
    async def connect(self):
        """Initialize HTTP session and authenticate"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        if self.api_key and self.api_secret:
            await self.authenticate()
            
    async def close(self):
        """Close HTTP session and WebSocket connection"""
        if self.ws:
            await self.ws.close()
        if self.session:
            await self.session.close()
            
    async def authenticate(self) -> Dict[str, Any]:
        """
        Authenticate with Deribit API using client credentials
        
        Returns:
            Authentication response with access and refresh tokens
        """
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }
        
        response = await self._request("public/auth", params)
        
        if "result" in response:
            self.access_token = response["result"]["access_token"]
            self.refresh_token = response["result"]["refresh_token"]
            logger.info("Successfully authenticated with Deribit")
        
        return response
        
    async def _request(self, method: str, params: Dict = None) -> Dict[str, Any]:
        """
        Make HTTP request to Deribit API
        
        Args:
            method: API method (e.g., 'public/get_instruments')
            params: Request parameters
            
        Returns:
            API response as dictionary
        """
        if not self.session:
            await self.connect()
            
        url = f"{self.base_url}/{method}"
        headers = {}
        
        if self.access_token and not method.startswith("public/"):
            headers["Authorization"] = f"Bearer {self.access_token}"
            
        try:
            async with self.session.get(url, params=params, headers=headers) as response:
                data = await response.json()
                
                if "error" in data:
                    logger.error(f"Deribit API error: {data['error']}")
                    raise Exception(f"Deribit API error: {data['error']}")
                    
                return data
                
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise
            
    # Market Data Methods
    
    async def get_instruments(self, currency: str = "BTC", kind: str = "option") -> List[Dict]:
        """
        Get available instruments
        
        Args:
            currency: Currency (BTC, ETH, SOL, etc.)
            kind: Instrument kind (option, future, spot)
            
        Returns:
            List of instruments
        """
        params = {
            "currency": currency,
            "kind": kind
        }
        
        response = await self._request("public/get_instruments", params)
        return response.get("result", [])
        
    async def get_order_book(self, instrument_name: str, depth: int = 10) -> Dict[str, Any]:
        """
        Get order book for an instrument
        
        Args:
            instrument_name: Instrument name (e.g., 'BTC-25DEC24-100000-C')
            depth: Order book depth
            
        Returns:
            Order book data
        """
        params = {
            "instrument_name": instrument_name,
            "depth": depth
        }
        
        response = await self._request("public/get_order_book", params)
        return response.get("result", {})
        
    async def get_ticker(self, instrument_name: str) -> Dict[str, Any]:
        """
        Get ticker data for an instrument
        
        Args:
            instrument_name: Instrument name
            
        Returns:
            Ticker data including mark price, Greeks, etc.
        """
        params = {"instrument_name": instrument_name}
        response = await self._request("public/ticker", params)
        return response.get("result", {})
        
    async def get_index_price(self, index_name: str) -> Dict[str, Any]:
        """
        Get current index price
        
        Args:
            index_name: Index name (e.g., 'btc_usd')
            
        Returns:
            Index price data
        """
        params = {"index_name": index_name}
        response = await self._request("public/get_index_price", params)
        return response.get("result", {})
        
    # Trading Methods
    
    async def buy(
        self,
        instrument_name: str,
        amount: float,
        price: Optional[float] = None,
        order_type: str = "limit",
        post_only: bool = False
    ) -> Dict[str, Any]:
        """
        Place a buy order
        
        Args:
            instrument_name: Instrument to buy
            amount: Order amount (in contracts)
            price: Limit price (None for market orders)
            order_type: Order type (limit, market)
            post_only: Post-only flag
            
        Returns:
            Order response
        """
        params = {
            "instrument_name": instrument_name,
            "amount": amount,
            "type": order_type
        }
        
        if price:
            params["price"] = price
        if post_only:
            params["post_only"] = True
            
        response = await self._request("private/buy", params)
        return response.get("result", {})
        
    async def sell(
        self,
        instrument_name: str,
        amount: float,
        price: Optional[float] = None,
        order_type: str = "limit",
        post_only: bool = False
    ) -> Dict[str, Any]:
        """
        Place a sell order
        
        Args:
            instrument_name: Instrument to sell
            amount: Order amount (in contracts)
            price: Limit price (None for market orders)
            order_type: Order type (limit, market)
            post_only: Post-only flag
            
        Returns:
            Order response
        """
        params = {
            "instrument_name": instrument_name,
            "amount": amount,
            "type": order_type
        }
        
        if price:
            params["price"] = price
        if post_only:
            params["post_only"] = True
            
        response = await self._request("private/sell", params)
        return response.get("result", {})
        
    async def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """
        Cancel an order
        
        Args:
            order_id: Order ID to cancel
            
        Returns:
            Cancellation response
        """
        params = {"order_id": order_id}
        response = await self._request("private/cancel", params)
        return response.get("result", {})
        
    async def cancel_all_orders(self, currency: Optional[str] = None) -> Dict[str, Any]:
        """
        Cancel all open orders
        
        Args:
            currency: Currency to cancel orders for (None for all)
            
        Returns:
            Cancellation response
        """
        params = {}
        if currency:
            params["currency"] = currency
            
        response = await self._request("private/cancel_all", params)
        return response.get("result", {})
        
    # Account Methods
    
    async def get_account_summary(self, currency: str = "BTC") -> Dict[str, Any]:
        """
        Get account summary
        
        Args:
            currency: Currency for account summary
            
        Returns:
            Account summary with balance, equity, margin, etc.
        """
        params = {"currency": currency}
        response = await self._request("private/get_account_summary", params)
        return response.get("result", {})
        
    async def get_positions(self, currency: str = "BTC", kind: str = "option") -> List[Dict]:
        """
        Get current positions
        
        Args:
            currency: Currency
            kind: Position kind (option, future)
            
        Returns:
            List of positions
        """
        params = {
            "currency": currency,
            "kind": kind
        }
        
        response = await self._request("private/get_positions", params)
        return response.get("result", [])
        
    async def get_open_orders(self, currency: Optional[str] = None, kind: Optional[str] = None) -> List[Dict]:
        """
        Get open orders
        
        Args:
            currency: Currency filter
            kind: Instrument kind filter
            
        Returns:
            List of open orders
        """
        params = {}
        if currency:
            params["currency"] = currency
        if kind:
            params["kind"] = kind
            
        response = await self._request("private/get_open_orders", params)
        return response.get("result", [])
        
    async def get_transaction_log(
        self,
        currency: str = "BTC",
        start_timestamp: Optional[int] = None,
        end_timestamp: Optional[int] = None
    ) -> List[Dict]:
        """
        Get transaction log
        
        Args:
            currency: Currency
            start_timestamp: Start timestamp (ms)
            end_timestamp: End timestamp (ms)
            
        Returns:
            List of transactions
        """
        params = {"currency": currency}
        if start_timestamp:
            params["start_timestamp"] = start_timestamp
        if end_timestamp:
            params["end_timestamp"] = end_timestamp
            
        response = await self._request("private/get_transaction_log", params)
        return response.get("result", {}).get("logs", [])
        
    # WebSocket Methods
    
    async def subscribe_ticker(self, instrument_name: str, callback):
        """
        Subscribe to ticker updates via WebSocket
        
        Args:
            instrument_name: Instrument to subscribe to
            callback: Callback function for ticker updates
        """
        if not self.ws:
            self.ws = await self.session.ws_connect(self.ws_url)
            
        subscribe_msg = {
            "jsonrpc": "2.0",
            "method": "public/subscribe",
            "params": {
                "channels": [f"ticker.{instrument_name}.raw"]
            },
            "id": 1
        }
        
        await self.ws.send_json(subscribe_msg)
        
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                if "params" in data:
                    await callback(data["params"]["data"])
