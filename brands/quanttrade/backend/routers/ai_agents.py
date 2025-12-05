"""
AI Agents API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from agents.trading_agents import TradingAgents
from config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize AI agents
try:
    ai_agents = TradingAgents(api_key=settings.OPENAI_API_KEY)
except Exception as e:
    logger.warning(f"AI Agents initialization failed: {e}. AI features will be limited.")
    ai_agents = None

class MarketAnalysisRequest(BaseModel):
    symbols: List[str]
    timeframe: str = "1d"

class StrategyDevelopmentRequest(BaseModel):
    strategy_type: str
    symbols: List[str]
    risk_level: str = "medium"

class RiskAssessmentRequest(BaseModel):
    positions: List[Dict[str, Any]]
    portfolio_value: float

@router.post("/analyze-market")
async def analyze_market(request: MarketAnalysisRequest):
    """Run AI market analysis"""
    if not ai_agents:
        raise HTTPException(
            status_code=503,
            detail="AI Agents not available. Please configure OPENAI_API_KEY."
        )

    try:
        result = await ai_agents.analyze_market(
            symbols=request.symbols,
            timeframe=request.timeframe
        )
        return result
    except Exception as e:
        logger.error(f"Market analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/develop-strategy")
async def develop_strategy(request: StrategyDevelopmentRequest):
    """Develop trading strategy with AI"""
    if not ai_agents:
        raise HTTPException(
            status_code=503,
            detail="AI Agents not available. Please configure OPENAI_API_KEY."
        )

    try:
        result = await ai_agents.develop_strategy(
            strategy_type=request.strategy_type,
            symbols=request.symbols,
            risk_level=request.risk_level
        )
        return result
    except Exception as e:
        logger.error(f"Strategy development failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/assess-risk")
async def assess_risk(request: RiskAssessmentRequest):
    """Assess portfolio risk with AI"""
    if not ai_agents:
        raise HTTPException(
            status_code=503,
            detail="AI Agents not available. Please configure OPENAI_API_KEY."
        )

    try:
        result = await ai_agents.assess_portfolio_risk(
            positions=request.positions,
            portfolio_value=request.portfolio_value
        )
        return result
    except Exception as e:
        logger.error(f"Risk assessment failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents")
async def list_agents():
    """List available AI agents"""
    return {
        "agents": [
            {
                "id": "market_analyst",
                "name": "Market Analyst",
                "description": "Technical and fundamental market analysis",
                "available": ai_agents is not None
            },
            {
                "id": "strategy_developer",
                "name": "Strategy Developer",
                "description": "Automated trading strategy creation",
                "available": ai_agents is not None
            },
            {
                "id": "risk_manager",
                "name": "Risk Manager",
                "description": "Portfolio risk assessment and management",
                "available": ai_agents is not None
            },
            {
                "id": "backtester",
                "name": "Backtester",
                "description": "Historical strategy validation",
                "available": ai_agents is not None
            },
            {
                "id": "signal_generator",
                "name": "Signal Generator",
                "description": "Trading signal generation",
                "available": ai_agents is not None
            }
        ]
    }
