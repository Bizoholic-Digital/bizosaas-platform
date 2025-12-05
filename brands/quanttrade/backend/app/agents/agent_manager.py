"""
Agent Manager - Orchestrates all CrewAI trading agents for comprehensive market analysis
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
from crewai import Crew, Task
import structlog

from agents.market_analyst.agent import MarketAnalystAgent
from agents.risk_manager.agent import RiskManagerAgent
from agents.news_sentiment.agent import NewsSentimentAgent
from agents.strategy_optimizer.agent import StrategyOptimizerAgent

logger = structlog.get_logger(__name__)


class TradingAgentManager:
    """Manages and coordinates all QuantTrade AI agents"""

    def __init__(self):
        self.agents = {
            "market_analyst": MarketAnalystAgent(),
            "risk_manager": RiskManagerAgent(),
            "news_sentiment": NewsSentimentAgent(),
            "strategy_optimizer": StrategyOptimizerAgent()
        }
        logger.info("Trading Agent Manager initialized with agents",
                   agent_count=len(self.agents))

    async def comprehensive_analysis(
        self,
        symbol: str,
        analysis_type: str = "full",
        **kwargs
    ) -> Dict[str, Any]:
        """Perform comprehensive analysis using all relevant agents"""
        try:
            logger.info("Starting comprehensive analysis",
                       symbol=symbol,
                       analysis_type=analysis_type)

            results = {
                "symbol": symbol,
                "analysis_type": analysis_type,
                "timestamp": datetime.now().isoformat(),
                "agent_results": {},
                "consolidated_recommendation": {},
                "execution_summary": {}
            }

            # Run analyses based on type
            if analysis_type in ["full", "market"]:
                logger.info("Running market analysis", symbol=symbol)
                market_result = await self.agents["market_analyst"].analyze(symbol, **kwargs)
                results["agent_results"]["market_analyst"] = market_result

            if analysis_type in ["full", "risk"]:
                logger.info("Running risk analysis", symbol=symbol)
                risk_result = await self.agents["risk_manager"].assess_risk(symbol, **kwargs)
                results["agent_results"]["risk_manager"] = risk_result

            if analysis_type in ["full", "sentiment"]:
                logger.info("Running sentiment analysis", symbol=symbol)
                sentiment_result = await self.agents["news_sentiment"].analyze_sentiment(symbol, **kwargs)
                results["agent_results"]["news_sentiment"] = sentiment_result

            # Generate consolidated recommendation
            results["consolidated_recommendation"] = self._consolidate_recommendations(
                results["agent_results"]
            )

            # Generate execution summary
            results["execution_summary"] = self._generate_execution_summary(
                results["agent_results"], results["consolidated_recommendation"]
            )

            logger.info("Comprehensive analysis completed",
                       symbol=symbol,
                       recommendation=results["consolidated_recommendation"].get("action"))

            return results

        except Exception as e:
            logger.error("Error in comprehensive analysis",
                        symbol=symbol,
                        error=str(e))
            return {"error": f"Comprehensive analysis failed: {str(e)}"}

    async def strategy_development(
        self,
        strategy_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Develop and optimize trading strategy"""
        try:
            logger.info("Starting strategy development",
                       strategy_type=strategy_config.get("type"))

            # First, get market analysis for all symbols
            symbols = strategy_config.get("symbols", ["SPY"])
            market_analyses = {}

            for symbol in symbols:
                market_analyses[symbol] = await self.agents["market_analyst"].analyze(symbol)

            # Perform strategy optimization
            optimization_result = await self.agents["strategy_optimizer"].optimize(
                strategy_config,
                market_data=market_analyses
            )

            # Risk assessment of the strategy
            risk_assessment = await self.agents["risk_manager"].assess_strategy_risk(
                strategy_config,
                optimization_result
            )

            # Consolidate strategy recommendation
            strategy_recommendation = self._consolidate_strategy_recommendation(
                optimization_result,
                risk_assessment,
                market_analyses
            )

            result = {
                "strategy_config": strategy_config,
                "timestamp": datetime.now().isoformat(),
                "optimization_result": optimization_result,
                "risk_assessment": risk_assessment,
                "market_analyses": market_analyses,
                "final_recommendation": strategy_recommendation,
                "implementation_plan": self._generate_implementation_plan(strategy_recommendation)
            }

            logger.info("Strategy development completed",
                       strategy_type=strategy_config.get("type"),
                       recommendation=strategy_recommendation.get("action"))

            return result

        except Exception as e:
            logger.error("Error in strategy development",
                        strategy_type=strategy_config.get("type"),
                        error=str(e))
            return {"error": f"Strategy development failed: {str(e)}"}

    async def portfolio_rebalancing_analysis(
        self,
        portfolio_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze portfolio and provide rebalancing recommendations"""
        try:
            logger.info("Starting portfolio rebalancing analysis",
                       portfolio_value=portfolio_data.get("total_value"))

            positions = portfolio_data.get("positions", [])
            symbols = [pos["symbol"] for pos in positions]

            # Parallel analysis of all positions
            analysis_tasks = []
            for symbol in symbols:
                analysis_tasks.append(self.comprehensive_analysis(symbol, "market"))

            position_analyses = await asyncio.gather(*analysis_tasks)

            # Risk analysis of current portfolio
            portfolio_risk = await self.agents["risk_manager"].analyze_portfolio_risk(portfolio_data)

            # Generate rebalancing recommendations
            rebalancing_recommendation = self._generate_rebalancing_recommendation(
                portfolio_data,
                position_analyses,
                portfolio_risk
            )

            result = {
                "portfolio_data": portfolio_data,
                "timestamp": datetime.now().isoformat(),
                "position_analyses": dict(zip(symbols, position_analyses)),
                "portfolio_risk": portfolio_risk,
                "rebalancing_recommendation": rebalancing_recommendation,
                "execution_plan": self._generate_rebalancing_execution_plan(rebalancing_recommendation)
            }

            logger.info("Portfolio rebalancing analysis completed",
                       recommendation_count=len(rebalancing_recommendation.get("recommendations", [])))

            return result

        except Exception as e:
            logger.error("Error in portfolio rebalancing analysis", error=str(e))
            return {"error": f"Portfolio rebalancing analysis failed: {str(e)}"}

    def _consolidate_recommendations(self, agent_results: Dict[str, Any]) -> Dict[str, Any]:
        """Consolidate recommendations from multiple agents"""

        # Initialize scoring
        buy_score = 0
        sell_score = 0
        hold_score = 0
        total_weight = 0

        consolidated_reasoning = []
        risk_factors = []
        confidence_scores = []

        # Market Analyst weight: 40%
        if "market_analyst" in agent_results:
            market_result = agent_results["market_analyst"]
            weight = 0.4

            if not market_result.get("error"):
                action = market_result.get("recommendation", "HOLD")
                confidence = market_result.get("confidence", 0.5)

                if action == "BUY":
                    buy_score += weight * confidence
                elif action == "SELL":
                    sell_score += weight * confidence
                else:
                    hold_score += weight * confidence

                total_weight += weight
                confidence_scores.append(confidence * weight)
                consolidated_reasoning.extend(market_result.get("reasoning", []))
                risk_factors.extend(market_result.get("risk_factors", []))

        # Risk Manager weight: 30%
        if "risk_manager" in agent_results:
            risk_result = agent_results["risk_manager"]
            weight = 0.3

            if not risk_result.get("error"):
                risk_level = risk_result.get("risk_level", "MODERATE")
                confidence = risk_result.get("confidence", 0.5)

                # Risk manager influences position sizing more than direction
                if risk_level == "LOW":
                    # Low risk supports current recommendation
                    pass
                elif risk_level == "HIGH":
                    # High risk reduces confidence in BUY/increases HOLD
                    buy_score *= 0.7
                    hold_score += weight * 0.3

                confidence_scores.append(confidence * weight)
                risk_factors.extend(risk_result.get("risk_factors", []))

        # News Sentiment weight: 30%
        if "news_sentiment" in agent_results:
            sentiment_result = agent_results["news_sentiment"]
            weight = 0.3

            if not sentiment_result.get("error"):
                sentiment = sentiment_result.get("overall_sentiment", "NEUTRAL")
                confidence = sentiment_result.get("confidence", 0.5)

                if sentiment == "BULLISH":
                    buy_score += weight * confidence
                elif sentiment == "BEARISH":
                    sell_score += weight * confidence
                else:
                    hold_score += weight * confidence

                total_weight += weight
                confidence_scores.append(confidence * weight)
                consolidated_reasoning.extend(sentiment_result.get("key_insights", []))

        # Determine final recommendation
        if total_weight == 0:
            return {
                "action": "HOLD",
                "confidence": 0.0,
                "reasoning": ["Insufficient data for recommendation"],
                "risk_factors": ["No agent data available"]
            }

        # Normalize scores
        buy_score /= total_weight
        sell_score /= total_weight
        hold_score /= total_weight

        # Determine action
        max_score = max(buy_score, sell_score, hold_score)
        if max_score == buy_score and buy_score > 0.4:
            action = "BUY"
            final_confidence = buy_score
        elif max_score == sell_score and sell_score > 0.4:
            action = "SELL"
            final_confidence = sell_score
        else:
            action = "HOLD"
            final_confidence = hold_score

        # Calculate weighted confidence
        weighted_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.5

        return {
            "action": action,
            "confidence": min(weighted_confidence, 0.95),
            "score_breakdown": {
                "buy_score": buy_score,
                "sell_score": sell_score,
                "hold_score": hold_score
            },
            "reasoning": consolidated_reasoning[:5],  # Top 5 reasons
            "risk_factors": list(set(risk_factors))[:3],  # Top 3 unique risk factors
            "agent_consensus": {
                "total_agents": len(agent_results),
                "successful_analyses": len([r for r in agent_results.values() if not r.get("error")]),
                "consensus_strength": max_score
            }
        }

    def _consolidate_strategy_recommendation(
        self,
        optimization_result: Dict[str, Any],
        risk_assessment: Dict[str, Any],
        market_analyses: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Consolidate strategy optimization with risk assessment"""

        opt_recommendation = optimization_result.get("recommendation", "REJECT")
        opt_confidence = optimization_result.get("confidence", 0.0)

        risk_level = risk_assessment.get("risk_level", "HIGH")
        risk_confidence = risk_assessment.get("confidence", 0.5)

        # Adjust recommendation based on risk
        if opt_recommendation == "DEPLOY":
            if risk_level == "LOW":
                action = "DEPLOY"
                confidence = (opt_confidence + risk_confidence) / 2
            elif risk_level == "MODERATE":
                action = "DEPLOY_LIMITED"
                confidence = opt_confidence * 0.8
            else:
                action = "OPTIMIZE_FURTHER"
                confidence = opt_confidence * 0.6
        elif opt_recommendation == "OPTIMIZE_FURTHER":
            if risk_level == "LOW":
                action = "OPTIMIZE_FURTHER"
                confidence = opt_confidence
            else:
                action = "REJECT"
                confidence = opt_confidence * 0.7
        else:
            action = "REJECT"
            confidence = min(opt_confidence, risk_confidence)

        return {
            "action": action,
            "confidence": confidence,
            "optimization_status": opt_recommendation,
            "risk_level": risk_level,
            "expected_performance": optimization_result.get("performance_metrics", {}),
            "risk_metrics": risk_assessment.get("risk_metrics", {}),
            "implementation_notes": optimization_result.get("implementation_notes", []),
            "risk_warnings": risk_assessment.get("risk_warnings", [])
        }

    def _generate_execution_summary(
        self,
        agent_results: Dict[str, Any],
        consolidated_recommendation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate execution summary for the analysis"""

        successful_agents = [name for name, result in agent_results.items() if not result.get("error")]
        failed_agents = [name for name, result in agent_results.items() if result.get("error")]

        return {
            "analysis_quality": {
                "successful_agents": len(successful_agents),
                "total_agents": len(agent_results),
                "success_rate": len(successful_agents) / len(agent_results) if agent_results else 0,
                "failed_agents": failed_agents
            },
            "recommendation_strength": {
                "consensus_level": consolidated_recommendation.get("agent_consensus", {}).get("consensus_strength", 0),
                "confidence": consolidated_recommendation.get("confidence", 0),
                "action": consolidated_recommendation.get("action", "HOLD")
            },
            "execution_timestamp": datetime.now().isoformat(),
            "next_analysis_recommended": datetime.now().strftime("%Y-%m-%d %H:%M")  # Could be more sophisticated
        }

    def _generate_rebalancing_recommendation(
        self,
        portfolio_data: Dict[str, Any],
        position_analyses: List[Dict[str, Any]],
        portfolio_risk: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate portfolio rebalancing recommendations"""

        recommendations = []
        current_positions = portfolio_data.get("positions", [])

        for i, position in enumerate(current_positions):
            if i < len(position_analyses):
                analysis = position_analyses[i]
                symbol = position["symbol"]
                current_weight = position.get("weight", 0)

                if not analysis.get("error"):
                    recommendation = analysis.get("consolidated_recommendation", {})
                    action = recommendation.get("action", "HOLD")
                    confidence = recommendation.get("confidence", 0.5)

                    if action == "BUY" and confidence > 0.7:
                        target_weight = min(current_weight * 1.2, 0.3)  # Increase by 20%, max 30%
                        recommendations.append({
                            "symbol": symbol,
                            "action": "INCREASE",
                            "current_weight": current_weight,
                            "target_weight": target_weight,
                            "confidence": confidence,
                            "reason": f"Strong buy signal with {confidence:.1%} confidence"
                        })
                    elif action == "SELL" and confidence > 0.7:
                        target_weight = max(current_weight * 0.5, 0.02)  # Decrease by 50%, min 2%
                        recommendations.append({
                            "symbol": symbol,
                            "action": "DECREASE",
                            "current_weight": current_weight,
                            "target_weight": target_weight,
                            "confidence": confidence,
                            "reason": f"Strong sell signal with {confidence:.1%} confidence"
                        })

        return {
            "recommendations": recommendations,
            "portfolio_risk_level": portfolio_risk.get("risk_level", "MODERATE"),
            "rebalancing_urgency": "HIGH" if len(recommendations) > 3 else "MODERATE" if len(recommendations) > 0 else "LOW",
            "estimated_impact": {
                "risk_reduction": 0.15 if len(recommendations) > 2 else 0.05,
                "expected_return_change": 0.02 if len(recommendations) > 2 else 0.0
            }
        }

    def _generate_implementation_plan(self, strategy_recommendation: Dict[str, Any]) -> Dict[str, Any]:
        """Generate implementation plan for strategy"""

        action = strategy_recommendation.get("action", "REJECT")

        if action == "DEPLOY":
            return {
                "phase": "immediate_deployment",
                "timeline": "1-2_weeks",
                "steps": [
                    "Finalize strategy parameters",
                    "Set up production environment",
                    "Implement risk controls",
                    "Begin with 10% allocation",
                    "Scale to full allocation over 30 days"
                ],
                "monitoring_requirements": [
                    "Daily P&L review",
                    "Weekly risk metrics",
                    "Monthly performance review"
                ]
            }
        elif action == "DEPLOY_LIMITED":
            return {
                "phase": "limited_deployment",
                "timeline": "2-4_weeks",
                "steps": [
                    "Additional testing with smaller size",
                    "Enhanced risk monitoring setup",
                    "Gradual parameter optimization",
                    "Maximum 5% allocation initially"
                ]
            }
        elif action == "OPTIMIZE_FURTHER":
            return {
                "phase": "continued_optimization",
                "timeline": "4-8_weeks",
                "steps": [
                    "Parameter sensitivity analysis",
                    "Alternative objective functions",
                    "Extended backtesting period",
                    "Monte Carlo stress testing"
                ]
            }
        else:
            return {
                "phase": "strategy_rejection",
                "timeline": "immediate",
                "steps": [
                    "Document lessons learned",
                    "Archive strategy research",
                    "Consider alternative approaches"
                ]
            }

    def _generate_rebalancing_execution_plan(self, rebalancing_recommendation: Dict[str, Any]) -> Dict[str, Any]:
        """Generate execution plan for portfolio rebalancing"""

        recommendations = rebalancing_recommendation.get("recommendations", [])
        urgency = rebalancing_recommendation.get("rebalancing_urgency", "LOW")

        if urgency == "HIGH":
            timeline = "1-2_days"
            approach = "immediate_rebalancing"
        elif urgency == "MODERATE":
            timeline = "1_week"
            approach = "gradual_rebalancing"
        else:
            timeline = "2-4_weeks"
            approach = "opportunistic_rebalancing"

        return {
            "approach": approach,
            "timeline": timeline,
            "execution_steps": [
                "Review current market conditions",
                "Calculate optimal trade sizes",
                "Execute trades in priority order",
                "Monitor execution impact",
                "Document rebalancing results"
            ],
            "trade_priority": sorted(recommendations, key=lambda x: x.get("confidence", 0), reverse=True),
            "cost_estimation": {
                "estimated_commission": len(recommendations) * 1.00,  # $1 per trade
                "estimated_spread_cost": len(recommendations) * 0.05,  # 5 cents per share
                "total_cost_estimate": len(recommendations) * 1.05
            }
        }

    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        status = {
            "manager_status": "active",
            "total_agents": len(self.agents),
            "agent_details": {},
            "last_updated": datetime.now().isoformat()
        }

        for name, agent in self.agents.items():
            status["agent_details"][name] = agent.get_status()

        return status