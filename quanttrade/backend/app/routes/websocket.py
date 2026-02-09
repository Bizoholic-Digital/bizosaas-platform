"""
WebSocket Routes - Real-time market data streaming
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from typing import Dict, Any, List, Optional, Set
import json
import asyncio
import structlog

from services.realtime_market_service import RealTimeMarketDataService
from core.auth import get_current_user_ws

logger = structlog.get_logger(__name__)
router = APIRouter()

# Initialize real-time market data service
market_data_service = RealTimeMarketDataService()

# Track active WebSocket connections
active_connections: Dict[str, Set[WebSocket]] = {}


@router.websocket("/ws/market/{symbol}")
async def websocket_market_data(websocket: WebSocket, symbol: str):
    """
    WebSocket endpoint for real-time market data for a specific symbol
    """
    await websocket.accept()

    try:
        logger.info("WebSocket connection established", symbol=symbol)

        # Subscribe to symbol
        await market_data_service.subscribe_to_symbol(symbol, websocket)

        # Keep connection alive and handle client messages
        while True:
            try:
                # Wait for client message (with timeout to send heartbeat)
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)

                # Parse client message
                try:
                    message = json.loads(data)
                    await handle_client_message(websocket, symbol, message)
                except json.JSONDecodeError:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": "Invalid JSON format"
                    }))

            except asyncio.TimeoutError:
                # Send heartbeat
                await websocket.send_text(json.dumps({
                    "type": "heartbeat",
                    "timestamp": str(asyncio.get_event_loop().time())
                }))

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected", symbol=symbol)
        await market_data_service.unsubscribe_from_symbol(symbol, websocket)
    except Exception as e:
        logger.error("WebSocket error", symbol=symbol, error=str(e))
        await market_data_service.unsubscribe_from_symbol(symbol, websocket)


@router.websocket("/ws/market")
async def websocket_multi_symbol(websocket: WebSocket):
    """
    WebSocket endpoint for real-time market data for multiple symbols
    """
    await websocket.accept()
    subscribed_symbols: Set[str] = set()

    try:
        logger.info("Multi-symbol WebSocket connection established")

        # Send initial connection message
        await websocket.send_text(json.dumps({
            "type": "connection_established",
            "message": "Multi-symbol market data WebSocket connected",
            "supported_commands": [
                "subscribe",
                "unsubscribe",
                "get_quote",
                "get_order_book",
                "list_subscriptions"
            ]
        }))

        # Handle client messages
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)

                try:
                    message = json.loads(data)
                    await handle_multi_symbol_message(websocket, message, subscribed_symbols)
                except json.JSONDecodeError:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": "Invalid JSON format"
                    }))

            except asyncio.TimeoutError:
                # Send heartbeat
                await websocket.send_text(json.dumps({
                    "type": "heartbeat",
                    "timestamp": str(asyncio.get_event_loop().time()),
                    "subscribed_symbols": list(subscribed_symbols)
                }))

    except WebSocketDisconnect:
        logger.info("Multi-symbol WebSocket disconnected",
                   subscribed_count=len(subscribed_symbols))

        # Unsubscribe from all symbols
        for symbol in subscribed_symbols:
            await market_data_service.unsubscribe_from_symbol(symbol, websocket)

    except Exception as e:
        logger.error("Multi-symbol WebSocket error", error=str(e))

        # Cleanup subscriptions
        for symbol in subscribed_symbols:
            await market_data_service.unsubscribe_from_symbol(symbol, websocket)


@router.websocket("/ws/portfolio")
async def websocket_portfolio_updates(websocket: WebSocket):
    """
    WebSocket endpoint for real-time portfolio updates
    """
    await websocket.accept()

    try:
        logger.info("Portfolio WebSocket connection established")

        # Send initial connection message
        await websocket.send_text(json.dumps({
            "type": "connection_established",
            "message": "Portfolio updates WebSocket connected"
        }))

        # Handle client messages and send portfolio updates
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=60.0)

                try:
                    message = json.loads(data)
                    await handle_portfolio_message(websocket, message)
                except json.JSONDecodeError:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": "Invalid JSON format"
                    }))

            except asyncio.TimeoutError:
                # Send portfolio heartbeat with mock data
                await websocket.send_text(json.dumps({
                    "type": "portfolio_update",
                    "data": {
                        "total_value": 125750.0,
                        "day_change": 2350.0,
                        "day_change_percent": 1.91,
                        "unrealized_pnl": 8750.0,
                        "timestamp": str(asyncio.get_event_loop().time())
                    }
                }))

    except WebSocketDisconnect:
        logger.info("Portfolio WebSocket disconnected")
    except Exception as e:
        logger.error("Portfolio WebSocket error", error=str(e))


async def handle_client_message(websocket: WebSocket, symbol: str, message: Dict[str, Any]):
    """Handle client messages for single symbol WebSocket"""
    try:
        message_type = message.get("type", "")

        if message_type == "get_quote":
            quote = await market_data_service.get_real_time_quote(symbol)
            if quote:
                await websocket.send_text(json.dumps({
                    "type": "quote_response",
                    "symbol": symbol,
                    "data": quote.__dict__,
                    "timestamp": quote.timestamp.isoformat()
                }))
            else:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"Unable to get quote for {symbol}"
                }))

        elif message_type == "get_order_book":
            order_book = await market_data_service.get_order_book(symbol)
            if order_book:
                await websocket.send_text(json.dumps({
                    "type": "order_book_response",
                    "symbol": symbol,
                    "data": {
                        "bids": [{"price": level.price, "size": level.size, "orders": level.num_orders}
                                for level in order_book.bids],
                        "asks": [{"price": level.price, "size": level.size, "orders": level.num_orders}
                                for level in order_book.asks],
                        "timestamp": order_book.timestamp.isoformat()
                    }
                }))
            else:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"Unable to get order book for {symbol}"
                }))

        elif message_type == "get_intraday":
            interval = message.get("interval", "1m")
            period = message.get("period", "1d")

            data = await market_data_service.get_intraday_data(symbol, interval, period)
            if data is not None and not data.empty:
                # Convert to JSON-serializable format
                chart_data = []
                for timestamp, row in data.iterrows():
                    chart_data.append({
                        "timestamp": timestamp.isoformat(),
                        "open": row['Open'],
                        "high": row['High'],
                        "low": row['Low'],
                        "close": row['Close'],
                        "volume": row['Volume']
                    })

                await websocket.send_text(json.dumps({
                    "type": "intraday_response",
                    "symbol": symbol,
                    "interval": interval,
                    "period": period,
                    "data": chart_data[-100:]  # Send last 100 data points
                }))
            else:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"Unable to get intraday data for {symbol}"
                }))

        else:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": f"Unknown message type: {message_type}"
            }))

    except Exception as e:
        logger.error("Error handling client message", symbol=symbol, error=str(e))
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": f"Internal error: {str(e)}"
        }))


async def handle_multi_symbol_message(websocket: WebSocket, message: Dict[str, Any], subscribed_symbols: Set[str]):
    """Handle client messages for multi-symbol WebSocket"""
    try:
        message_type = message.get("type", "")

        if message_type == "subscribe":
            symbols = message.get("symbols", [])
            if isinstance(symbols, str):
                symbols = [symbols]

            for symbol in symbols:
                symbol = symbol.upper()
                if symbol not in subscribed_symbols:
                    await market_data_service.subscribe_to_symbol(symbol, websocket)
                    subscribed_symbols.add(symbol)

            await websocket.send_text(json.dumps({
                "type": "subscription_response",
                "action": "subscribe",
                "symbols": symbols,
                "total_subscribed": len(subscribed_symbols)
            }))

        elif message_type == "unsubscribe":
            symbols = message.get("symbols", [])
            if isinstance(symbols, str):
                symbols = [symbols]

            for symbol in symbols:
                symbol = symbol.upper()
                if symbol in subscribed_symbols:
                    await market_data_service.unsubscribe_from_symbol(symbol, websocket)
                    subscribed_symbols.remove(symbol)

            await websocket.send_text(json.dumps({
                "type": "subscription_response",
                "action": "unsubscribe",
                "symbols": symbols,
                "total_subscribed": len(subscribed_symbols)
            }))

        elif message_type == "get_quotes":
            symbols = message.get("symbols", list(subscribed_symbols))
            if isinstance(symbols, str):
                symbols = [symbols]

            quotes = {}
            for symbol in symbols:
                quote = await market_data_service.get_real_time_quote(symbol)
                if quote:
                    quotes[symbol] = {
                        "price": quote.price,
                        "change": quote.change,
                        "change_percent": quote.change_percent,
                        "volume": quote.volume,
                        "timestamp": quote.timestamp.isoformat()
                    }

            await websocket.send_text(json.dumps({
                "type": "quotes_response",
                "data": quotes
            }))

        elif message_type == "list_subscriptions":
            await websocket.send_text(json.dumps({
                "type": "subscriptions_list",
                "subscribed_symbols": list(subscribed_symbols),
                "count": len(subscribed_symbols)
            }))

        elif message_type == "get_stats":
            symbols = message.get("symbols", list(subscribed_symbols))
            stats = await market_data_service.get_symbol_stats(symbols)

            await websocket.send_text(json.dumps({
                "type": "stats_response",
                "data": stats
            }))

        else:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": f"Unknown message type: {message_type}"
            }))

    except Exception as e:
        logger.error("Error handling multi-symbol message", error=str(e))
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": f"Internal error: {str(e)}"
        }))


async def handle_portfolio_message(websocket: WebSocket, message: Dict[str, Any]):
    """Handle client messages for portfolio WebSocket"""
    try:
        message_type = message.get("type", "")

        if message_type == "get_portfolio":
            # Mock portfolio data
            portfolio_data = {
                "total_value": 125750.0,
                "cash": 15750.0,
                "positions_value": 110000.0,
                "day_change": 2350.0,
                "day_change_percent": 1.91,
                "total_return": 25750.0,
                "total_return_percent": 25.75,
                "positions": [
                    {
                        "symbol": "AAPL",
                        "quantity": 100,
                        "avg_cost": 150.0,
                        "current_price": 175.0,
                        "market_value": 17500.0,
                        "unrealized_pnl": 2500.0,
                        "unrealized_pnl_percent": 16.67
                    },
                    {
                        "symbol": "GOOGL",
                        "quantity": 50,
                        "avg_cost": 120.0,
                        "current_price": 135.0,
                        "market_value": 6750.0,
                        "unrealized_pnl": 750.0,
                        "unrealized_pnl_percent": 12.5
                    }
                ]
            }

            await websocket.send_text(json.dumps({
                "type": "portfolio_response",
                "data": portfolio_data
            }))

        elif message_type == "get_performance":
            # Mock performance data
            performance_data = {
                "daily_returns": [0.5, 1.2, -0.3, 0.8, 1.9],
                "monthly_return": 5.2,
                "ytd_return": 25.75,
                "sharpe_ratio": 1.85,
                "max_drawdown": -8.2,
                "win_rate": 68.5
            }

            await websocket.send_text(json.dumps({
                "type": "performance_response",
                "data": performance_data
            }))

        else:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": f"Unknown message type: {message_type}"
            }))

    except Exception as e:
        logger.error("Error handling portfolio message", error=str(e))
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": f"Internal error: {str(e)}"
        }))


@router.get("/ws/info")
async def get_websocket_info():
    """Get information about WebSocket endpoints"""
    return {
        "websocket_endpoints": {
            "/ws/market/{symbol}": {
                "description": "Real-time market data for a specific symbol",
                "supported_messages": [
                    "get_quote",
                    "get_order_book",
                    "get_intraday"
                ]
            },
            "/ws/market": {
                "description": "Real-time market data for multiple symbols",
                "supported_messages": [
                    "subscribe",
                    "unsubscribe",
                    "get_quotes",
                    "list_subscriptions",
                    "get_stats"
                ]
            },
            "/ws/portfolio": {
                "description": "Real-time portfolio updates and information",
                "supported_messages": [
                    "get_portfolio",
                    "get_performance"
                ]
            }
        },
        "subscription_info": market_data_service.get_subscription_info(),
        "message_format": {
            "client_to_server": {
                "type": "message_type",
                "symbol": "AAPL (optional)",
                "symbols": ["AAPL", "GOOGL"]
            },
            "server_to_client": {
                "type": "response_type",
                "data": "response_data",
                "timestamp": "ISO_timestamp"
            }
        }
    }