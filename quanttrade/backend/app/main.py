"""
QuantTrade Backend - AI-Powered Trading Platform
FastAPI + VectorBT + CrewAI Trading Agents
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from datetime import datetime
import structlog

from core.config import get_settings
from core.database import init_db, close_db
from core.cache import init_cache, close_cache
from api.routes import portfolio, positions, market, strategies, backtesting, ai_agents
from routes import agents, websocket
from services.market_data_service import MarketDataService
from services.portfolio_service import PortfolioService

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="ISO"),
        structlog.dev.ConsoleRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(20),
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Global services
market_data_service: MarketDataService = None
portfolio_service: PortfolioService = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting QuantTrade Backend...")

    # Initialize database
    await init_db()
    logger.info("Database initialized")

    # Initialize cache
    await init_cache()
    logger.info("Cache initialized")

    # Initialize services
    global market_data_service, portfolio_service
    market_data_service = MarketDataService()
    portfolio_service = PortfolioService()

    logger.info("Services initialized")
    logger.info("QuantTrade Backend started successfully on port 8012")

    yield

    # Cleanup
    logger.info("Shutting down QuantTrade Backend...")
    await close_cache()
    await close_db()
    logger.info("QuantTrade Backend shutdown complete")

# Create FastAPI application
app = FastAPI(
    title="QuantTrade API",
    description="AI-Powered Trading Platform with VectorBT Backtesting and CrewAI Agents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Get settings
settings = get_settings()

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Health check endpoint
@app.get("/", tags=["Health"])
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "quanttrade-backend",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.ENVIRONMENT,
        "components": {
            "database": "connected",
            "cache": "connected",
            "market_data": "active",
            "ai_agents": "ready"
        }
    }

# API Routes
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["Portfolio"])
app.include_router(positions.router, prefix="/api/positions", tags=["Positions"])
app.include_router(market.router, prefix="/api/market", tags=["Market Data"])
app.include_router(strategies.router, prefix="/api/strategies", tags=["Trading Strategies"])
app.include_router(backtesting.router, prefix="/api/backtesting", tags=["Backtesting"])
app.include_router(ai_agents.router, prefix="/api/ai-agents", tags=["AI Agents"])
app.include_router(agents.router, prefix="/api/agents", tags=["CrewAI Trading Agents"])
app.include_router(websocket.router, tags=["WebSocket Real-time Data"])

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error("HTTP exception", status_code=exc.status_code, detail=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "timestamp": datetime.utcnow().isoformat()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error("Unhandled exception", exception=str(exc))
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# WebSocket endpoint for real-time data
@app.websocket("/ws")
async def websocket_endpoint(websocket):
    """WebSocket endpoint for real-time trading data"""
    await websocket.accept()
    logger.info("WebSocket connection established")

    try:
        while True:
            # Send real-time market data
            data = await market_data_service.get_real_time_data()
            await websocket.send_json(data)

            # Wait for client message or timeout
            await websocket.receive_text()

    except Exception as e:
        logger.error("WebSocket error", error=str(e))
    finally:
        await websocket.close()
        logger.info("WebSocket connection closed")

if __name__ == "__main__":
    # Development server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8012,
        reload=True if settings.ENVIRONMENT == "development" else False,
        log_level="info"
    )