"""
Strategy Optimizer Agent - Advanced strategy development and optimization using genetic algorithms
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from crewai import Agent
from langchain.tools import Tool
import structlog
import numpy as np

from agents.base_agent import BaseTradingAgent
from core.config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()


class StrategyOptimizerAgent(BaseTradingAgent):
    """AI agent specialized in strategy development and optimization"""

    def __init__(self):
        super().__init__(
            agent_id="strategy_optimizer",
            name="Strategy Optimizer",
            description="Advanced algorithmic strategy development, backtesting optimization, and parameter tuning using genetic algorithms"
        )

    def _create_agent(self) -> Agent:
        """Create the Strategy Optimizer CrewAI agent"""
        return Agent(
            role="Quantitative Strategy Developer",
            goal="Develop and optimize algorithmic trading strategies using advanced mathematical models, genetic algorithms, and machine learning techniques to maximize risk-adjusted returns",
            backstory="""You are a world-class quantitative analyst and algorithmic trading specialist with 20+ years
            of experience at top hedge funds and proprietary trading firms. You excel at developing sophisticated
            trading strategies using mathematical models, statistical analysis, and machine learning. Your expertise
            includes genetic algorithms for parameter optimization, Monte Carlo simulations, and advanced backtesting
            methodologies. You have successfully deployed strategies that generated billions in profits while
            maintaining excellent risk-adjusted returns.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            max_iter=5,
            memory=True
        )

    def _create_tools(self) -> List[Tool]:
        """Create specialized tools for strategy optimization"""
        base_tools = self._create_base_tools()

        specialized_tools = [
            Tool(
                name="optimize_strategy_parameters",
                description="Optimize strategy parameters using genetic algorithms",
                func=self._optimize_strategy_parameters
            ),
            Tool(
                name="backtest_strategy",
                description="Perform comprehensive strategy backtesting with performance metrics",
                func=self._backtest_strategy
            ),
            Tool(
                name="monte_carlo_simulation",
                description="Run Monte Carlo simulation for strategy robustness testing",
                func=self._monte_carlo_simulation
            ),
            Tool(
                name="walk_forward_analysis",
                description="Perform walk-forward analysis to test strategy adaptability",
                func=self._walk_forward_analysis
            ),
            Tool(
                name="multi_asset_correlation_analysis",
                description="Analyze correlations and diversification benefits across assets",
                func=self._multi_asset_correlation_analysis
            ),
            Tool(
                name="risk_parity_optimization",
                description="Optimize portfolio using risk parity principles",
                func=self._risk_parity_optimization
            ),
            Tool(
                name="factor_exposure_analysis",
                description="Analyze strategy exposure to market factors",
                func=self._factor_exposure_analysis
            ),
            Tool(
                name="regime_adaptive_parameters",
                description="Adapt strategy parameters based on market regime detection",
                func=self._regime_adaptive_parameters
            )
        ]

        return base_tools + specialized_tools

    async def optimize(self, strategy_config: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Perform comprehensive strategy optimization"""
        try:
            logger.info("Starting strategy optimization", strategy_type=strategy_config.get("type"))

            symbols = strategy_config.get("symbols", ["SPY"])
            strategy_type = strategy_config.get("type", "momentum")
            optimization_period = strategy_config.get("optimization_period", "2y")

            # Get historical data for all symbols
            historical_data = {}
            for symbol in symbols:
                historical_data[symbol] = await self._get_historical_data(symbol, optimization_period)

            # Perform optimization steps
            optimized_params = self._optimize_strategy_parameters(strategy_config)
            backtest_results = self._backtest_strategy(strategy_config, optimized_params)
            monte_carlo_results = self._monte_carlo_simulation(strategy_config, optimized_params)
            walkforward_results = self._walk_forward_analysis(strategy_config, optimized_params)
            correlation_analysis = self._multi_asset_correlation_analysis(symbols)
            factor_exposure = self._factor_exposure_analysis(strategy_config, optimized_params)
            regime_params = self._regime_adaptive_parameters(strategy_config)

            # Generate final recommendation
            recommendation = self._generate_strategy_recommendation(
                backtest_results, monte_carlo_results, walkforward_results,
                correlation_analysis, factor_exposure
            )

            optimization_result = {
                "agent_id": self.agent_id,
                "strategy_type": strategy_type,
                "symbols": symbols,
                "timestamp": datetime.now().isoformat(),
                "optimized_parameters": optimized_params,
                "performance_metrics": backtest_results.get("metrics", {}),
                "recommendation": recommendation["status"],
                "confidence": recommendation["confidence"],
                "expected_annual_return": recommendation.get("expected_return"),
                "expected_volatility": recommendation.get("expected_volatility"),
                "expected_sharpe": recommendation.get("expected_sharpe"),
                "max_drawdown_estimate": recommendation.get("max_drawdown"),
                "analysis": {
                    "backtest_results": backtest_results,
                    "monte_carlo_simulation": monte_carlo_results,
                    "walk_forward_analysis": walkforward_results,
                    "correlation_analysis": correlation_analysis,
                    "factor_exposure": factor_exposure,
                    "regime_adaptive_params": regime_params
                },
                "implementation_notes": recommendation.get("implementation_notes", []),
                "risk_warnings": recommendation.get("risk_warnings", []),
                "capital_allocation": recommendation.get("capital_allocation", {}),
                "rebalancing_frequency": recommendation.get("rebalancing_frequency", "weekly")
            }

            logger.info("Strategy optimization completed",
                       strategy_type=strategy_type,
                       recommendation=recommendation["status"])
            return optimization_result

        except Exception as e:
            logger.error("Error in strategy optimization",
                        strategy_type=strategy_config.get("type"),
                        error=str(e))
            return {"error": f"Strategy optimization failed: {str(e)}"}

    def _optimize_strategy_parameters(self, strategy_config: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize strategy parameters using genetic algorithms"""
        strategy_type = strategy_config.get("type", "momentum")

        # Mock genetic algorithm optimization - in production, use actual GA
        if strategy_type == "momentum":
            optimized_params = {
                "lookback_period": 21,  # Optimized from range 10-50
                "momentum_threshold": 0.02,  # Optimized from 0.01-0.05
                "position_size": 0.25,  # Optimized from 0.1-0.5
                "stop_loss": 0.08,  # Optimized from 0.05-0.15
                "take_profit": 0.15,  # Optimized from 0.10-0.25
                "rebalance_frequency": "weekly",
                "optimization_generations": 100,
                "population_size": 50,
                "fitness_function": "sharpe_ratio",
                "optimization_score": 1.85
            }
        elif strategy_type == "mean_reversion":
            optimized_params = {
                "lookback_period": 14,
                "z_score_entry": 2.0,
                "z_score_exit": 0.5,
                "position_size": 0.20,
                "max_holding_period": 10,
                "volatility_filter": True,
                "optimization_score": 1.62
            }
        else:  # Default momentum
            optimized_params = {
                "lookback_period": 20,
                "signal_threshold": 0.015,
                "position_size": 0.30,
                "optimization_score": 1.45
            }

        return {
            "strategy_type": strategy_type,
            "parameters": optimized_params,
            "optimization_method": "genetic_algorithm",
            "optimization_period": "2_years",
            "validation_method": "walk_forward",
            "parameter_stability": "high",
            "overfitting_risk": "low"
        }

    def _backtest_strategy(self, strategy_config: Dict[str, Any], optimized_params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive strategy backtesting"""
        # Mock backtesting results - in production, integrate with VectorBT
        backtest_results = {
            "period": "2022-01-01 to 2024-01-01",
            "total_trades": 145,
            "winning_trades": 89,
            "losing_trades": 56,
            "win_rate": 0.614,
            "metrics": {
                "total_return": 0.342,  # 34.2% total return
                "annual_return": 0.168,  # 16.8% annual return
                "volatility": 0.142,    # 14.2% annual volatility
                "sharpe_ratio": 1.183,
                "sortino_ratio": 1.654,
                "calmar_ratio": 1.089,
                "max_drawdown": 0.154,  # 15.4% max drawdown
                "avg_drawdown": 0.043,
                "recovery_time": 23,    # days
                "profit_factor": 1.67,
                "expectancy": 0.024,    # 2.4% per trade
                "kelly_criterion": 0.18  # Optimal position size
            },
            "monthly_returns": [
                {"month": "2022-01", "return": 0.023},
                {"month": "2022-02", "return": -0.015},
                {"month": "2022-03", "return": 0.041},
                {"month": "2022-04", "return": 0.018},
                {"month": "2022-05", "return": -0.032}
                # ... more monthly data
            ],
            "drawdown_periods": [
                {"start": "2022-06-15", "end": "2022-08-12", "depth": -0.154, "duration": 58},
                {"start": "2023-03-08", "end": "2023-04-22", "depth": -0.087, "duration": 45}
            ],
            "trade_analysis": {
                "avg_win": 0.045,
                "avg_loss": -0.027,
                "largest_win": 0.126,
                "largest_loss": -0.089,
                "avg_trade_duration": 6.3,  # days
                "max_consecutive_wins": 7,
                "max_consecutive_losses": 4
            }
        }

        return backtest_results

    def _monte_carlo_simulation(self, strategy_config: Dict[str, Any], optimized_params: Dict[str, Any]) -> Dict[str, Any]:
        """Run Monte Carlo simulation for strategy robustness testing"""
        # Mock Monte Carlo results
        simulation_results = {
            "simulations_count": 10000,
            "time_horizon": "1_year",
            "confidence_intervals": {
                "95_percent": {"lower": -0.089, "upper": 0.412},
                "90_percent": {"lower": -0.067, "upper": 0.387},
                "80_percent": {"lower": -0.043, "upper": 0.354}
            },
            "return_distribution": {
                "mean": 0.168,
                "median": 0.172,
                "std_dev": 0.142,
                "skewness": -0.234,
                "kurtosis": 2.987,
                "var_95": -0.089,  # 95% Value at Risk
                "cvar_95": -0.124  # Conditional VaR
            },
            "scenario_analysis": {
                "bull_market_probability": 0.342,
                "bear_market_probability": 0.189,
                "sideways_market_probability": 0.469,
                "tail_risk_events": 0.073,
                "black_swan_probability": 0.012
            },
            "robustness_metrics": {
                "parameter_sensitivity": "low",
                "market_regime_adaptability": "high",
                "stress_test_survival": 0.934,
                "robustness_score": 0.847
            }
        }

        return simulation_results

    def _walk_forward_analysis(self, strategy_config: Dict[str, Any], optimized_params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform walk-forward analysis"""
        # Mock walk-forward analysis results
        walkforward_results = {
            "analysis_windows": 12,
            "optimization_window": "6_months",
            "validation_window": "1_month",
            "results": [
                {"window": 1, "optimization_sharpe": 1.23, "validation_sharpe": 1.18, "degradation": 0.041},
                {"window": 2, "optimization_sharpe": 1.45, "validation_sharpe": 1.31, "degradation": 0.097},
                {"window": 3, "optimization_sharpe": 1.67, "validation_sharpe": 1.52, "degradation": 0.090},
                {"window": 4, "optimization_sharpe": 1.34, "validation_sharpe": 1.29, "degradation": 0.037}
            ],
            "aggregate_metrics": {
                "avg_optimization_sharpe": 1.42,
                "avg_validation_sharpe": 1.33,
                "avg_degradation": 0.066,
                "consistency_score": 0.847,
                "overfitting_likelihood": "low",
                "strategy_robustness": "high"
            },
            "parameter_stability": {
                "lookback_period": {"mean": 20.3, "std": 2.1, "stability": "high"},
                "momentum_threshold": {"mean": 0.021, "std": 0.003, "stability": "high"},
                "position_size": {"mean": 0.248, "std": 0.028, "stability": "moderate"}
            }
        }

        return walkforward_results

    def _multi_asset_correlation_analysis(self, symbols: List[str]) -> Dict[str, Any]:
        """Analyze correlations and diversification benefits"""
        # Mock correlation analysis
        correlation_analysis = {
            "correlation_matrix": {
                "SPY": {"SPY": 1.00, "QQQ": 0.89, "GLD": -0.12, "VIX": -0.73},
                "QQQ": {"SPY": 0.89, "QQQ": 1.00, "GLD": -0.08, "VIX": -0.67},
                "GLD": {"SPY": -0.12, "QQQ": -0.08, "GLD": 1.00, "VIX": 0.23},
                "VIX": {"SPY": -0.73, "QQQ": -0.67, "GLD": 0.23, "VIX": 1.00}
            },
            "diversification_metrics": {
                "portfolio_correlation": 0.634,
                "diversification_ratio": 1.47,
                "effective_assets": 2.8,
                "concentration_risk": "moderate",
                "diversification_benefit": "significant"
            },
            "risk_contribution": {
                "SPY": 0.45,
                "QQQ": 0.38,
                "GLD": 0.12,
                "VIX": 0.05
            },
            "regime_correlations": {
                "bull_market": {"avg_correlation": 0.68, "max_correlation": 0.91},
                "bear_market": {"avg_correlation": 0.84, "max_correlation": 0.97},
                "volatile_market": {"avg_correlation": 0.76, "max_correlation": 0.93}
            }
        }

        return correlation_analysis

    def _risk_parity_optimization(self, symbols: List[str]) -> Dict[str, Any]:
        """Optimize portfolio using risk parity principles"""
        # Mock risk parity optimization
        risk_parity_result = {
            "optimal_weights": {
                "SPY": 0.35,
                "QQQ": 0.25,
                "GLD": 0.25,
                "VIX": 0.15
            },
            "risk_contributions": {
                "SPY": 0.25,
                "QQQ": 0.25,
                "GLD": 0.25,
                "VIX": 0.25
            },
            "expected_metrics": {
                "annual_return": 0.142,
                "annual_volatility": 0.118,
                "sharpe_ratio": 1.203,
                "max_drawdown": 0.089
            },
            "optimization_quality": "excellent",
            "rebalancing_threshold": 0.05
        }

        return risk_parity_result

    def _factor_exposure_analysis(self, strategy_config: Dict[str, Any], optimized_params: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze strategy exposure to market factors"""
        # Mock factor analysis
        factor_exposure = {
            "factor_loadings": {
                "market_beta": 0.87,
                "size_factor": 0.23,
                "value_factor": -0.12,
                "momentum_factor": 0.45,
                "quality_factor": 0.18,
                "low_volatility_factor": -0.34,
                "profitability_factor": 0.29
            },
            "factor_significance": {
                "market_beta": {"t_stat": 8.92, "p_value": 0.000, "significant": True},
                "momentum_factor": {"t_stat": 4.56, "p_value": 0.001, "significant": True},
                "size_factor": {"t_stat": 2.34, "p_value": 0.019, "significant": True}
            },
            "factor_attribution": {
                "market_return": 0.089,
                "factor_return": 0.067,
                "alpha": 0.012,  # Strategy generates 1.2% alpha
                "r_squared": 0.743,
                "tracking_error": 0.045
            },
            "factor_timing": {
                "market_timing_ability": 0.023,
                "factor_timing_ability": 0.015,
                "selectivity_skill": 0.008
            }
        }

        return factor_exposure

    def _regime_adaptive_parameters(self, strategy_config: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt strategy parameters based on market regime"""
        # Mock regime-adaptive parameters
        regime_params = {
            "current_regime": "trending_up_moderate_vol",
            "regime_confidence": 0.78,
            "adaptive_parameters": {
                "bull_market": {
                    "position_size": 0.35,
                    "momentum_threshold": 0.015,
                    "stop_loss": 0.10,
                    "take_profit": 0.20
                },
                "bear_market": {
                    "position_size": 0.15,
                    "momentum_threshold": 0.025,
                    "stop_loss": 0.06,
                    "take_profit": 0.12
                },
                "sideways_market": {
                    "position_size": 0.20,
                    "momentum_threshold": 0.030,
                    "stop_loss": 0.08,
                    "take_profit": 0.10
                },
                "high_volatility": {
                    "position_size": 0.10,
                    "momentum_threshold": 0.040,
                    "stop_loss": 0.05,
                    "take_profit": 0.08
                }
            },
            "regime_detection_accuracy": 0.834,
            "parameter_adaptation_frequency": "daily",
            "regime_transition_smoothing": True
        }

        return regime_params

    def _generate_strategy_recommendation(
        self,
        backtest_results: Dict[str, Any],
        monte_carlo_results: Dict[str, Any],
        walkforward_results: Dict[str, Any],
        correlation_analysis: Dict[str, Any],
        factor_exposure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive strategy recommendation"""

        # Extract key metrics
        sharpe_ratio = backtest_results.get("metrics", {}).get("sharpe_ratio", 0)
        max_drawdown = backtest_results.get("metrics", {}).get("max_drawdown", 1)
        win_rate = backtest_results.get("win_rate", 0.5)
        robustness_score = monte_carlo_results.get("robustness_metrics", {}).get("robustness_score", 0.5)
        consistency_score = walkforward_results.get("aggregate_metrics", {}).get("consistency_score", 0.5)
        alpha = factor_exposure.get("factor_attribution", {}).get("alpha", 0)

        # Scoring system
        score = 0
        max_score = 100

        # Performance scoring (40 points)
        if sharpe_ratio > 1.5:
            score += 20
        elif sharpe_ratio > 1.0:
            score += 15
        elif sharpe_ratio > 0.5:
            score += 10

        if max_drawdown < 0.10:
            score += 20
        elif max_drawdown < 0.15:
            score += 15
        elif max_drawdown < 0.20:
            score += 10

        # Robustness scoring (30 points)
        if robustness_score > 0.8:
            score += 15
        elif robustness_score > 0.6:
            score += 10
        elif robustness_score > 0.4:
            score += 5

        if consistency_score > 0.8:
            score += 15
        elif consistency_score > 0.6:
            score += 10
        elif consistency_score > 0.4:
            score += 5

        # Alpha generation (20 points)
        if alpha > 0.015:
            score += 20
        elif alpha > 0.010:
            score += 15
        elif alpha > 0.005:
            score += 10

        # Win rate (10 points)
        if win_rate > 0.65:
            score += 10
        elif win_rate > 0.55:
            score += 7
        elif win_rate > 0.50:
            score += 5

        confidence = min(score / max_score, 0.95)

        # Generate recommendation
        if score >= 80:
            status = "DEPLOY"
            implementation_notes = [
                "Strategy shows excellent risk-adjusted returns",
                "High robustness across market conditions",
                "Strong alpha generation capability",
                "Recommended for immediate deployment"
            ]
            risk_warnings = [
                "Monitor regime changes closely",
                "Consider position sizing based on volatility",
                "Regular parameter validation recommended"
            ]
        elif score >= 60:
            status = "OPTIMIZE_FURTHER"
            implementation_notes = [
                "Strategy shows promise but needs refinement",
                "Consider parameter optimization",
                "Test with smaller position sizes initially"
            ]
            risk_warnings = [
                "Moderate performance consistency",
                "Higher drawdown risk",
                "Consider additional risk controls"
            ]
        else:
            status = "REJECT"
            implementation_notes = [
                "Strategy does not meet minimum performance criteria",
                "Significant improvements needed",
                "Consider alternative approaches"
            ]
            risk_warnings = [
                "High risk of significant losses",
                "Poor risk-adjusted returns",
                "Not suitable for deployment"
            ]

        return {
            "status": status,
            "confidence": confidence,
            "score": score,
            "max_score": max_score,
            "expected_return": backtest_results.get("metrics", {}).get("annual_return", 0),
            "expected_volatility": backtest_results.get("metrics", {}).get("volatility", 0),
            "expected_sharpe": sharpe_ratio,
            "max_drawdown": max_drawdown,
            "implementation_notes": implementation_notes,
            "risk_warnings": risk_warnings,
            "capital_allocation": {
                "recommended_allocation": "25%" if status == "DEPLOY" else "10%" if status == "OPTIMIZE_FURTHER" else "0%",
                "max_allocation": "50%" if status == "DEPLOY" else "20%",
                "start_allocation": "10%" if status in ["DEPLOY", "OPTIMIZE_FURTHER"] else "0%"
            },
            "rebalancing_frequency": "weekly" if status == "DEPLOY" else "monthly",
            "monitoring_requirements": [
                "Daily P&L monitoring",
                "Weekly risk metrics review",
                "Monthly parameter validation",
                "Quarterly strategy review"
            ]
        }