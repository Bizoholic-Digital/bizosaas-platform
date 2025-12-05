"""
Agent Routes - FastAPI endpoints for CrewAI trading agents
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import structlog

from agents.agent_manager import TradingAgentManager
from core.auth import get_current_user
from core.database import get_db
from sqlalchemy.orm import Session

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/agents", tags=["AI Agents"])

# Initialize agent manager
agent_manager = TradingAgentManager()


# Pydantic models for request/response
class AnalysisRequest(BaseModel):
    symbol: str = Field(..., description="Stock symbol to analyze")
    analysis_type: str = Field(default="full", description="Type of analysis: full, market, risk, sentiment")
    timeframe: str = Field(default="1d", description="Analysis timeframe")
    include_fundamentals: bool = Field(default=False, description="Include fundamental analysis")


class StrategyRequest(BaseModel):
    strategy_type: str = Field(..., description="Strategy type: momentum, mean_reversion, pairs_trading")
    symbols: List[str] = Field(..., description="List of symbols for the strategy")
    optimization_period: str = Field(default="2y", description="Period for optimization")
    risk_level: str = Field(default="moderate", description="Risk level: low, moderate, high")
    capital_allocation: float = Field(default=100000.0, description="Capital for strategy")


class PortfolioRequest(BaseModel):
    positions: List[Dict[str, Any]] = Field(..., description="Current portfolio positions")
    total_value: float = Field(..., description="Total portfolio value")
    benchmark: str = Field(default="SPY", description="Benchmark for comparison")


class AnalysisResponse(BaseModel):
    analysis_id: str
    status: str
    symbol: str
    timestamp: str
    recommendation: Dict[str, Any]
    confidence: float


@router.post("/analyze", response_model=Dict[str, Any])
async def comprehensive_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Perform comprehensive market analysis using multiple AI agents
    """
    try:
        logger.info("Starting comprehensive analysis",
                   user_id=current_user.get("user_id"),
                   symbol=request.symbol,
                   analysis_type=request.analysis_type)

        # Perform analysis
        result = await agent_manager.comprehensive_analysis(
            symbol=request.symbol,
            analysis_type=request.analysis_type,
            timeframe=request.timeframe,
            include_fundamentals=request.include_fundamentals
        )

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        # Store analysis result in database (background task)
        background_tasks.add_task(
            store_analysis_result,
            user_id=current_user.get("user_id"),
            analysis_data=result,
            db=db
        )

        return {
            "status": "success",
            "analysis_id": result.get("timestamp", ""),
            "data": result,
            "message": f"Analysis completed for {request.symbol}"
        }

    except Exception as e:
        logger.error("Error in comprehensive analysis",
                    symbol=request.symbol,
                    error=str(e))
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/strategy/develop")
async def develop_strategy(
    request: StrategyRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Develop and optimize trading strategy using AI agents
    """
    try:
        logger.info("Starting strategy development",
                   user_id=current_user.get("user_id"),
                   strategy_type=request.strategy_type,
                   symbols=request.symbols)

        strategy_config = {
            "type": request.strategy_type,
            "symbols": request.symbols,
            "optimization_period": request.optimization_period,
            "risk_level": request.risk_level,
            "capital_allocation": request.capital_allocation
        }

        # Develop strategy
        result = await agent_manager.strategy_development(strategy_config)

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        # Store strategy result in database (background task)
        background_tasks.add_task(
            store_strategy_result,
            user_id=current_user.get("user_id"),
            strategy_data=result,
            db=db
        )

        return {
            "status": "success",
            "strategy_id": result.get("timestamp", ""),
            "data": result,
            "message": f"Strategy development completed for {request.strategy_type}"
        }

    except Exception as e:
        logger.error("Error in strategy development",
                    strategy_type=request.strategy_type,
                    error=str(e))
        raise HTTPException(status_code=500, detail=f"Strategy development failed: {str(e)}")


@router.post("/portfolio/rebalance")
async def analyze_portfolio_rebalancing(
    request: PortfolioRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze portfolio and provide rebalancing recommendations
    """
    try:
        logger.info("Starting portfolio rebalancing analysis",
                   user_id=current_user.get("user_id"),
                   portfolio_value=request.total_value)

        portfolio_data = {
            "positions": request.positions,
            "total_value": request.total_value,
            "benchmark": request.benchmark
        }

        # Analyze portfolio
        result = await agent_manager.portfolio_rebalancing_analysis(portfolio_data)

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        # Store portfolio analysis result (background task)
        background_tasks.add_task(
            store_portfolio_analysis,
            user_id=current_user.get("user_id"),
            portfolio_data=result,
            db=db
        )

        return {
            "status": "success",
            "analysis_id": result.get("timestamp", ""),
            "data": result,
            "message": "Portfolio rebalancing analysis completed"
        }

    except Exception as e:
        logger.error("Error in portfolio rebalancing analysis", error=str(e))
        raise HTTPException(status_code=500, detail=f"Portfolio analysis failed: {str(e)}")


@router.get("/analyze/{symbol}")
async def quick_symbol_analysis(
    symbol: str,
    analysis_type: str = "market",
    current_user: dict = Depends(get_current_user)
):
    """
    Quick analysis for a single symbol
    """
    try:
        result = await agent_manager.comprehensive_analysis(
            symbol=symbol,
            analysis_type=analysis_type
        )

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        return {
            "status": "success",
            "symbol": symbol,
            "recommendation": result.get("consolidated_recommendation", {}),
            "confidence": result.get("consolidated_recommendation", {}).get("confidence", 0),
            "timestamp": result.get("timestamp")
        }

    except Exception as e:
        logger.error("Error in quick analysis", symbol=symbol, error=str(e))
        raise HTTPException(status_code=500, detail=f"Quick analysis failed: {str(e)}")


@router.get("/status")
async def get_agents_status():
    """
    Get status of all AI agents
    """
    try:
        status = agent_manager.get_agent_status()
        return {
            "status": "success",
            "data": status
        }

    except Exception as e:
        logger.error("Error getting agent status", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get agent status: {str(e)}")


@router.get("/agents/{agent_id}/status")
async def get_agent_status(agent_id: str):
    """
    Get status of specific agent
    """
    try:
        if agent_id not in agent_manager.agents:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")

        agent = agent_manager.agents[agent_id]
        status = agent.get_status()

        return {
            "status": "success",
            "agent_id": agent_id,
            "data": status
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting specific agent status",
                    agent_id=agent_id,
                    error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get agent status: {str(e)}")


@router.post("/market-analyst/analyze")
async def market_analyst_analysis(
    request: AnalysisRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Direct market analyst analysis
    """
    try:
        market_analyst = agent_manager.agents["market_analyst"]
        result = await market_analyst.analyze(
            symbol=request.symbol,
            timeframe=request.timeframe
        )

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        return {
            "status": "success",
            "agent": "market_analyst",
            "data": result
        }

    except Exception as e:
        logger.error("Error in market analyst analysis", error=str(e))
        raise HTTPException(status_code=500, detail=f"Market analyst analysis failed: {str(e)}")


@router.post("/risk-manager/assess")
async def risk_manager_assessment(
    request: AnalysisRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Direct risk manager assessment
    """
    try:
        risk_manager = agent_manager.agents["risk_manager"]
        result = await risk_manager.assess_risk(
            symbol=request.symbol,
            timeframe=request.timeframe
        )

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        return {
            "status": "success",
            "agent": "risk_manager",
            "data": result
        }

    except Exception as e:
        logger.error("Error in risk manager assessment", error=str(e))
        raise HTTPException(status_code=500, detail=f"Risk manager assessment failed: {str(e)}")


@router.post("/sentiment-analyzer/analyze")
async def sentiment_analysis(
    request: AnalysisRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Direct sentiment analysis
    """
    try:
        sentiment_analyzer = agent_manager.agents["news_sentiment"]
        result = await sentiment_analyzer.analyze_sentiment(
            symbol=request.symbol,
            timeframe=request.timeframe
        )

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        return {
            "status": "success",
            "agent": "news_sentiment",
            "data": result
        }

    except Exception as e:
        logger.error("Error in sentiment analysis", error=str(e))
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {str(e)}")


@router.post("/strategy-optimizer/optimize")
async def strategy_optimization(
    request: StrategyRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Direct strategy optimization
    """
    try:
        strategy_optimizer = agent_manager.agents["strategy_optimizer"]

        strategy_config = {
            "type": request.strategy_type,
            "symbols": request.symbols,
            "optimization_period": request.optimization_period,
            "risk_level": request.risk_level,
            "capital_allocation": request.capital_allocation
        }

        result = await strategy_optimizer.optimize(strategy_config)

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        return {
            "status": "success",
            "agent": "strategy_optimizer",
            "data": result
        }

    except Exception as e:
        logger.error("Error in strategy optimization", error=str(e))
        raise HTTPException(status_code=500, detail=f"Strategy optimization failed: {str(e)}")


# Background tasks for storing results
async def store_analysis_result(user_id: str, analysis_data: Dict[str, Any], db: Session):
    """Store analysis result in database"""
    try:
        # Implementation would store in analysis_results table
        logger.info("Storing analysis result", user_id=user_id)
    except Exception as e:
        logger.error("Failed to store analysis result", error=str(e))


async def store_strategy_result(user_id: str, strategy_data: Dict[str, Any], db: Session):
    """Store strategy result in database"""
    try:
        # Implementation would store in strategy_results table
        logger.info("Storing strategy result", user_id=user_id)
    except Exception as e:
        logger.error("Failed to store strategy result", error=str(e))


async def store_portfolio_analysis(user_id: str, portfolio_data: Dict[str, Any], db: Session):
    """Store portfolio analysis in database"""
    try:
        # Implementation would store in portfolio_analysis table
        logger.info("Storing portfolio analysis", user_id=user_id)
    except Exception as e:
        logger.error("Failed to store portfolio analysis", error=str(e))