"""
Base Agent Class for QuantTrade CrewAI Trading Agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
import pandas as pd
from crewai import Agent, Task, Crew
from langchain.tools import Tool
import structlog

from core.config import get_settings
from services.market_data_service import MarketDataService

logger = structlog.get_logger(__name__)
settings = get_settings()


class BaseTradingAgent(ABC):
    """Base class for all QuantTrade AI trading agents"""

    def __init__(self, agent_id: str, name: str, description: str):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.market_service = MarketDataService()
        self.agent = self._create_agent()
        self.tools = self._create_tools()

    @abstractmethod
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent with specific configuration"""
        pass

    @abstractmethod
    def _create_tools(self) -> List[Tool]:
        """Create tools specific to this agent"""
        pass

    @abstractmethod
    async def analyze(self, symbol: str, **kwargs) -> Dict[str, Any]:
        """Main analysis method - must be implemented by each agent"""
        pass

    def _create_base_tools(self) -> List[Tool]:
        """Create common tools used by all trading agents"""
        return [
            Tool(
                name="get_market_quote",
                description="Get real-time market quote for a symbol",
                func=self._get_market_quote
            ),
            Tool(
                name="get_historical_data",
                description="Get historical price data for analysis",
                func=self._get_historical_data
            ),
            Tool(
                name="calculate_technical_indicators",
                description="Calculate technical indicators from price data",
                func=self._calculate_technical_indicators
            ),
            Tool(
                name="get_market_indices",
                description="Get major market indices performance",
                func=self._get_market_indices
            ),
            Tool(
                name="get_sector_performance",
                description="Get sector performance data",
                func=self._get_sector_performance
            )
        ]

    async def _get_market_quote(self, symbol: str) -> Dict[str, Any]:
        """Tool to get real-time market quote"""
        try:
            quote = await self.market_service.get_real_time_quote(symbol)
            return quote or {"error": f"No data found for {symbol}"}
        except Exception as e:
            logger.error("Error getting market quote", symbol=symbol, error=str(e))
            return {"error": str(e)}

    async def _get_historical_data(self, symbol: str, period: str = "1y") -> Dict[str, Any]:
        """Tool to get historical data"""
        try:
            from datetime import datetime, timedelta

            period_mapping = {
                "1d": timedelta(days=1),
                "5d": timedelta(days=5),
                "1mo": timedelta(days=30),
                "3mo": timedelta(days=90),
                "6mo": timedelta(days=180),
                "1y": timedelta(days=365),
                "2y": timedelta(days=730)
            }

            end_date = datetime.now()
            start_date = end_date - period_mapping.get(period, timedelta(days=365))

            data = await self.market_service.get_historical_data(symbol, start_date, end_date)

            if data is not None and not data.empty:
                # Convert to dict for JSON serialization
                return {
                    "symbol": symbol,
                    "period": period,
                    "data_points": len(data),
                    "latest_price": float(data['Close'].iloc[-1]),
                    "price_change_period": float(data['Close'].iloc[-1] - data['Close'].iloc[0]),
                    "high_period": float(data['High'].max()),
                    "low_period": float(data['Low'].min()),
                    "avg_volume": float(data['Volume'].mean())
                }
            else:
                return {"error": f"No historical data found for {symbol}"}

        except Exception as e:
            logger.error("Error getting historical data", symbol=symbol, error=str(e))
            return {"error": str(e)}

    def _calculate_technical_indicators(self, symbol: str) -> Dict[str, Any]:
        """Calculate technical indicators"""
        try:
            # This would integrate with the historical data
            # For now, return mock indicators
            indicators = {
                "rsi_14": 68.5,
                "sma_20": 175.30,
                "sma_50": 172.80,
                "ema_12": 176.20,
                "macd": 2.45,
                "macd_signal": 1.89,
                "bollinger_upper": 185.50,
                "bollinger_lower": 165.20,
                "atr_14": 4.25
            }

            return {
                "symbol": symbol,
                "indicators": indicators,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error("Error calculating technical indicators", symbol=symbol, error=str(e))
            return {"error": str(e)}

    async def _get_market_indices(self) -> Dict[str, Any]:
        """Tool to get market indices"""
        try:
            indices = await self.market_service.get_market_indices()
            return indices
        except Exception as e:
            logger.error("Error getting market indices", error=str(e))
            return {"error": str(e)}

    async def _get_sector_performance(self) -> Dict[str, Any]:
        """Tool to get sector performance"""
        try:
            sectors = await self.market_service.get_sector_performance()
            return {"sectors": sectors}
        except Exception as e:
            logger.error("Error getting sector performance", error=str(e))
            return {"error": str(e)}

    def create_task(self, description: str, context: Dict[str, Any]) -> Task:
        """Create a task for this agent"""
        return Task(
            description=description,
            agent=self.agent,
            context=context
        )

    def get_status(self) -> Dict[str, Any]:
        """Get agent status information"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "status": "active",
            "tools_count": len(self.tools),
            "last_updated": datetime.now().isoformat()
        }