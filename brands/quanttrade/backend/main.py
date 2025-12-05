"""
QuantTrade AI Trading Platform - Main FastAPI Application
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import List, Dict, Any, Optional
import asyncio
import logging
from datetime import datetime
import time

from routers import (
    portfolio_router,
    strategies_router,
    backtesting_router,
    market_data_router,
    ai_agents_router,
    trading_router,
    risk_router
)
from services.websocket_manager import WebSocketManager
from services.market_data_service import MarketDataService
from services.metrics import get_metrics, record_api_request
from config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global services
ws_manager = WebSocketManager()
market_service = MarketDataService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("Starting QuantTrade Trading Platform...")

    # Start market data streaming
    asyncio.create_task(market_service.stream_market_data(ws_manager))

    yield

    logger.info("Shutting down QuantTrade Trading Platform...")
    await ws_manager.disconnect_all()

# Initialize FastAPI app
app = FastAPI(
    title="QuantTrade AI Trading Platform",
    description="AI-Powered Quantitative Trading Engine",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(portfolio_router, prefix="/api/portfolio", tags=["Portfolio"])
app.include_router(strategies_router, prefix="/api/strategies", tags=["Strategies"])
app.include_router(backtesting_router, prefix="/api/backtest", tags=["Backtesting"])
app.include_router(market_data_router, prefix="/api/market", tags=["Market Data"])
app.include_router(ai_agents_router, prefix="/api/ai-agents", tags=["AI Agents"])
app.include_router(trading_router, prefix="/api/trading", tags=["Trading"])
app.include_router(risk_router, prefix="/api/risk", tags=["Risk Management"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "QuantTrade AI Trading Platform",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "api": "operational",
            "websocket": "operational",
            "market_data": "operational",
            "ai_agents": "operational"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return get_metrics()

@app.middleware("http")
async def track_requests(request, call_next):
    """Middleware to track API requests in Prometheus"""
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    record_api_request(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code,
        duration=duration
    )
    
    return response

@app.websocket("/ws/market-data")
async def websocket_market_data(websocket: WebSocket):
    """WebSocket endpoint for real-time market data"""
    await ws_manager.connect(websocket, "market_data")
    try:
        while True:
            data = await websocket.receive_text()
            # Handle client messages if needed
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, "market_data")

@app.websocket("/ws/trading")
async def websocket_trading(websocket: WebSocket):
    """WebSocket endpoint for real-time trading updates"""
    await ws_manager.connect(websocket, "trading")
    try:
        while True:
            data = await websocket.receive_text()
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, "trading")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8012,
        reload=True,
        log_level="info"
    )
