"""
Market Analyst Agent - Advanced market analysis using multiple data sources
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from crewai import Agent
from langchain.tools import Tool
import structlog

from agents.base_agent import BaseTradingAgent
from core.config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()


class MarketAnalystAgent(BaseTradingAgent):
    """AI agent specialized in comprehensive market analysis"""

    def __init__(self):
        super().__init__(
            agent_id="market_analyst",
            name="Market Analyst",
            description="Advanced market analysis using technical indicators, sentiment analysis, and pattern recognition"
        )

    def _create_agent(self) -> Agent:
        """Create the Market Analyst CrewAI agent"""
        return Agent(
            role="Senior Market Analyst",
            goal="Provide comprehensive market analysis and trading recommendations based on technical indicators, market sentiment, and price patterns",
            backstory="""You are a seasoned market analyst with 15+ years of experience in quantitative
            trading and technical analysis. You excel at identifying market trends, support/resistance levels,
            and generating actionable trading signals. Your analysis combines multiple timeframes and
            incorporates market sentiment to provide well-rounded investment recommendations.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            max_iter=3,
            memory=True
        )

    def _create_tools(self) -> List[Tool]:
        """Create specialized tools for market analysis"""
        base_tools = self._create_base_tools()

        specialized_tools = [
            Tool(
                name="detect_chart_patterns",
                description="Identify chart patterns like triangles, head and shoulders, double tops/bottoms",
                func=self._detect_chart_patterns
            ),
            Tool(
                name="analyze_support_resistance",
                description="Identify key support and resistance levels",
                func=self._analyze_support_resistance
            ),
            Tool(
                name="calculate_momentum_indicators",
                description="Calculate momentum indicators like RSI, MACD, Stochastic",
                func=self._calculate_momentum_indicators
            ),
            Tool(
                name="analyze_volume_profile",
                description="Analyze volume patterns and volume-price relationships",
                func=self._analyze_volume_profile
            ),
            Tool(
                name="detect_market_regime",
                description="Identify current market regime (trending, ranging, volatile)",
                func=self._detect_market_regime
            )
        ]

        return base_tools + specialized_tools

    async def analyze(self, symbol: str, timeframe: str = "1d", **kwargs) -> Dict[str, Any]:
        """Perform comprehensive market analysis"""
        try:
            logger.info("Starting market analysis", symbol=symbol, timeframe=timeframe)

            # Get market data
            quote = await self._get_market_quote(symbol)
            historical = await self._get_historical_data(symbol, "3mo")
            technical_indicators = self._calculate_technical_indicators(symbol)

            # Perform specialized analysis
            patterns = self._detect_chart_patterns(symbol)
            support_resistance = self._analyze_support_resistance(symbol)
            momentum = self._calculate_momentum_indicators(symbol)
            volume_analysis = self._analyze_volume_profile(symbol)
            market_regime = self._detect_market_regime(symbol)

            # Generate recommendation
            recommendation = self._generate_recommendation(
                quote, technical_indicators, patterns, support_resistance, momentum
            )

            analysis_result = {
                "agent_id": self.agent_id,
                "symbol": symbol,
                "timeframe": timeframe,
                "timestamp": datetime.now().isoformat(),
                "current_price": quote.get("price", 0),
                "recommendation": recommendation["action"],
                "confidence": recommendation["confidence"],
                "target_price": recommendation.get("target_price"),
                "stop_loss": recommendation.get("stop_loss"),
                "time_horizon": recommendation.get("time_horizon", "5-10 days"),
                "analysis": {
                    "technical_indicators": technical_indicators.get("indicators", {}),
                    "chart_patterns": patterns,
                    "support_resistance": support_resistance,
                    "momentum_analysis": momentum,
                    "volume_profile": volume_analysis,
                    "market_regime": market_regime
                },
                "reasoning": recommendation["reasoning"],
                "risk_factors": recommendation.get("risk_factors", []),
                "key_levels": {
                    "resistance": support_resistance.get("resistance", []),
                    "support": support_resistance.get("support", [])
                }
            }

            logger.info("Market analysis completed", symbol=symbol, recommendation=recommendation["action"])
            return analysis_result

        except Exception as e:
            logger.error("Error in market analysis", symbol=symbol, error=str(e))
            return {"error": f"Market analysis failed: {str(e)}"}

    def _detect_chart_patterns(self, symbol: str) -> Dict[str, Any]:
        """Detect chart patterns"""
        # Mock pattern detection - in production, use actual pattern recognition algorithms
        patterns = {
            "detected_patterns": [
                {
                    "pattern": "ascending_triangle",
                    "confidence": 0.78,
                    "timeframe": "daily",
                    "status": "forming",
                    "breakout_target": 195.50,
                    "pattern_height": 12.30
                },
                {
                    "pattern": "bullish_flag",
                    "confidence": 0.65,
                    "timeframe": "4h",
                    "status": "completed",
                    "target_achieved": True
                }
            ],
            "pattern_strength": "moderate",
            "overall_bias": "bullish"
        }

        return patterns

    def _analyze_support_resistance(self, symbol: str) -> Dict[str, Any]:
        """Analyze support and resistance levels"""
        # Mock support/resistance analysis
        levels = {
            "support": [
                {"level": 175.00, "strength": "strong", "touches": 4, "last_test": "2024-01-12"},
                {"level": 170.50, "strength": "moderate", "touches": 2, "last_test": "2024-01-08"}
            ],
            "resistance": [
                {"level": 185.00, "strength": "strong", "touches": 3, "last_test": "2024-01-15"},
                {"level": 190.00, "strength": "moderate", "touches": 2, "last_test": "2024-01-10"}
            ],
            "current_zone": "between_levels",
            "nearest_support": 175.00,
            "nearest_resistance": 185.00
        }

        return levels

    def _calculate_momentum_indicators(self, symbol: str) -> Dict[str, Any]:
        """Calculate momentum indicators"""
        # Mock momentum analysis
        momentum = {
            "rsi_analysis": {
                "current_rsi": 68.5,
                "interpretation": "approaching_overbought",
                "divergence": None,
                "trend": "rising"
            },
            "macd_analysis": {
                "macd_line": 2.45,
                "signal_line": 1.89,
                "histogram": 0.56,
                "signal": "bullish_crossover",
                "strength": "moderate"
            },
            "stochastic": {
                "k_percent": 75.2,
                "d_percent": 72.8,
                "signal": "overbought_warning",
                "crossover": None
            },
            "overall_momentum": "bullish_but_extended"
        }

        return momentum

    def _analyze_volume_profile(self, symbol: str) -> Dict[str, Any]:
        """Analyze volume patterns"""
        # Mock volume analysis
        volume_analysis = {
            "volume_trend": "increasing",
            "volume_ratio": 1.35,  # vs 20-day average
            "volume_price_trend": "confirming_uptrend",
            "accumulation_distribution": "positive",
            "volume_breakouts": [
                {"date": "2024-01-15", "volume_spike": 2.1, "price_reaction": "positive"}
            ],
            "interpretation": "institutional_accumulation"
        }

        return volume_analysis

    def _detect_market_regime(self, symbol: str) -> Dict[str, Any]:
        """Detect current market regime"""
        # Mock market regime detection
        regime = {
            "regime_type": "trending_up",
            "volatility_level": "moderate",
            "trend_strength": 0.72,
            "regime_duration": "14_days",
            "regime_confidence": 0.81,
            "expected_continuation": "high",
            "regime_characteristics": [
                "consistent_higher_highs",
                "volume_confirmation",
                "sector_rotation_positive"
            ]
        }

        return regime

    def _generate_recommendation(
        self,
        quote: Dict[str, Any],
        technical: Dict[str, Any],
        patterns: Dict[str, Any],
        support_resistance: Dict[str, Any],
        momentum: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate trading recommendation based on analysis"""

        current_price = quote.get("price", 0)
        if not current_price:
            return {"action": "HOLD", "confidence": 0.0, "reasoning": ["Insufficient data"]}

        # Scoring system
        bullish_signals = 0
        bearish_signals = 0
        total_weight = 0

        # Technical indicators scoring
        rsi = technical.get("indicators", {}).get("rsi_14", 50)
        if 30 <= rsi <= 70:
            bullish_signals += 1
        elif rsi > 80:
            bearish_signals += 1
        total_weight += 1

        # MACD analysis
        macd_signal = momentum.get("macd_analysis", {}).get("signal")
        if macd_signal == "bullish_crossover":
            bullish_signals += 2
        elif macd_signal == "bearish_crossover":
            bearish_signals += 2
        total_weight += 2

        # Pattern analysis
        pattern_bias = patterns.get("overall_bias", "neutral")
        if pattern_bias == "bullish":
            bullish_signals += 1
        elif pattern_bias == "bearish":
            bearish_signals += 1
        total_weight += 1

        # Calculate confidence
        net_score = bullish_signals - bearish_signals
        confidence = abs(net_score) / max(total_weight, 1)

        # Generate recommendation
        if net_score > 1:
            action = "BUY"
            target_price = current_price * 1.08  # 8% upside target
            stop_loss = support_resistance.get("nearest_support", current_price * 0.95)
        elif net_score < -1:
            action = "SELL"
            target_price = current_price * 0.92  # 8% downside target
            stop_loss = support_resistance.get("nearest_resistance", current_price * 1.05)
        else:
            action = "HOLD"
            target_price = current_price
            stop_loss = None

        reasoning = [
            f"Technical momentum is {momentum.get('overall_momentum', 'neutral')}",
            f"Chart patterns show {pattern_bias} bias",
            f"RSI at {rsi:.1f} indicates {'overbought' if rsi > 70 else 'oversold' if rsi < 30 else 'neutral'} conditions",
            f"Volume analysis suggests {momentum.get('volume_price_trend', 'neutral')} trend"
        ]

        risk_factors = [
            "Market volatility could impact position",
            "Sector rotation risk" if action == "BUY" else "Momentum could continue" if action == "SELL" else "Range-bound trading risk"
        ]

        return {
            "action": action,
            "confidence": min(confidence, 0.95),  # Cap confidence at 95%
            "target_price": target_price,
            "stop_loss": stop_loss,
            "time_horizon": "5-10 days",
            "reasoning": reasoning,
            "risk_factors": risk_factors,
            "score_breakdown": {
                "bullish_signals": bullish_signals,
                "bearish_signals": bearish_signals,
                "net_score": net_score,
                "total_weight": total_weight
            }
        }