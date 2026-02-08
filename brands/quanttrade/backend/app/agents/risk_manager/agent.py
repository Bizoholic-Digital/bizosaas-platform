"""
Risk Manager Agent - Portfolio risk assessment and optimization
"""

from typing import Dict, Any, List
from datetime import datetime
from crewai import Agent
from langchain.tools import Tool
import structlog
import numpy as np

from agents.base_agent import BaseTradingAgent
from core.config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()


class RiskManagerAgent(BaseTradingAgent):
    """AI agent specialized in portfolio risk management and position sizing"""

    def __init__(self):
        super().__init__(
            agent_id="risk_manager",
            name="Risk Management Agent",
            description="Portfolio risk assessment, position sizing optimization, and drawdown management"
        )

    def _create_agent(self) -> Agent:
        """Create the Risk Manager CrewAI agent"""
        return Agent(
            role="Senior Risk Manager",
            goal="Assess portfolio risk, optimize position sizing, and provide risk management recommendations to minimize drawdowns while maximizing risk-adjusted returns",
            backstory="""You are an expert risk manager with deep expertise in quantitative risk models,
            portfolio theory, and derivatives. You have managed institutional portfolios worth billions
            and have a proven track record of protecting capital during market downturns. Your approach
            combines traditional risk metrics with modern machine learning techniques to provide
            comprehensive risk assessments.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            max_iter=3,
            memory=True
        )

    def _create_tools(self) -> List[Tool]:
        """Create specialized tools for risk management"""
        base_tools = self._create_base_tools()

        specialized_tools = [
            Tool(
                name="calculate_portfolio_var",
                description="Calculate Value at Risk (VaR) for portfolio positions",
                func=self._calculate_portfolio_var
            ),
            Tool(
                name="analyze_correlation_matrix",
                description="Analyze correlations between portfolio positions",
                func=self._analyze_correlation_matrix
            ),
            Tool(
                name="calculate_optimal_position_size",
                description="Calculate optimal position size using Kelly Criterion and other methods",
                func=self._calculate_optimal_position_size
            ),
            Tool(
                name="assess_concentration_risk",
                description="Assess portfolio concentration risk by sector, market cap, geography",
                func=self._assess_concentration_risk
            ),
            Tool(
                name="calculate_sharpe_sortino_ratios",
                description="Calculate risk-adjusted performance metrics",
                func=self._calculate_sharpe_sortino_ratios
            ),
            Tool(
                name="stress_test_portfolio",
                description="Perform stress testing under various market scenarios",
                func=self._stress_test_portfolio
            )
        ]

        return base_tools + specialized_tools

    async def analyze(self, portfolio_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Perform comprehensive risk analysis"""
        try:
            logger.info("Starting risk analysis for portfolio")

            # Get portfolio positions
            positions = portfolio_data.get("positions", [])
            total_value = portfolio_data.get("total_value", 100000)

            # Perform risk calculations
            var_analysis = self._calculate_portfolio_var(positions, total_value)
            correlation_analysis = self._analyze_correlation_matrix(positions)
            concentration_risk = self._assess_concentration_risk(positions, total_value)
            stress_test_results = self._stress_test_portfolio(positions, total_value)
            performance_metrics = self._calculate_sharpe_sortino_ratios(portfolio_data)

            # Generate position sizing recommendations
            position_sizing_recs = self._generate_position_sizing_recommendations(
                positions, total_value, var_analysis
            )

            # Generate overall risk assessment
            risk_assessment = self._generate_risk_assessment(
                var_analysis, correlation_analysis, concentration_risk, stress_test_results
            )

            analysis_result = {
                "agent_id": self.agent_id,
                "portfolio_analysis": True,
                "timestamp": datetime.now().isoformat(),
                "total_portfolio_value": total_value,
                "confidence": 0.92,
                "risk_assessment": risk_assessment,
                "var_analysis": var_analysis,
                "correlation_analysis": correlation_analysis,
                "concentration_risk": concentration_risk,
                "stress_test_results": stress_test_results,
                "performance_metrics": performance_metrics,
                "position_sizing": position_sizing_recs,
                "recommendations": self._generate_risk_recommendations(
                    risk_assessment, concentration_risk, var_analysis
                ),
                "alerts": self._generate_risk_alerts(
                    var_analysis, concentration_risk, correlation_analysis
                )
            }

            logger.info("Risk analysis completed", risk_level=risk_assessment.get("overall_risk_level"))
            return analysis_result

        except Exception as e:
            logger.error("Error in risk analysis", error=str(e))
            return {"error": f"Risk analysis failed: {str(e)}"}

    def _calculate_portfolio_var(self, positions: List[Dict], total_value: float) -> Dict[str, Any]:
        """Calculate Value at Risk for the portfolio"""
        # Mock VaR calculation - in production, use historical simulation or Monte Carlo

        if not positions:
            return {
                "var_95_daily": 0.0,
                "var_99_daily": 0.0,
                "expected_shortfall_95": 0.0,
                "var_95_percent": 0.0
            }

        # Simple VaR estimation based on position sizes and volatilities
        portfolio_volatility = 0.18  # 18% annual volatility assumption
        daily_volatility = portfolio_volatility / np.sqrt(252)

        var_95_daily = total_value * daily_volatility * 1.645  # 95th percentile
        var_99_daily = total_value * daily_volatility * 2.33   # 99th percentile
        expected_shortfall_95 = var_95_daily * 1.3  # Expected loss beyond VaR

        return {
            "var_95_daily": var_95_daily,
            "var_99_daily": var_99_daily,
            "expected_shortfall_95": expected_shortfall_95,
            "var_95_percent": (var_95_daily / total_value) * 100,
            "portfolio_volatility_annual": portfolio_volatility,
            "methodology": "parametric_var"
        }

    def _analyze_correlation_matrix(self, positions: List[Dict]) -> Dict[str, Any]:
        """Analyze correlations between portfolio positions"""
        # Mock correlation analysis
        if len(positions) < 2:
            return {"correlation_risk": "low", "diversification_score": 1.0}

        # Simulate correlation matrix
        symbols = [pos.get("symbol", "UNKNOWN") for pos in positions[:10]]  # Limit to 10 for simplicity

        # Mock correlation data
        avg_correlation = 0.65  # Assume moderate correlation between positions
        max_correlation = 0.85
        min_correlation = 0.15

        correlation_analysis = {
            "avg_correlation": avg_correlation,
            "max_correlation": max_correlation,
            "min_correlation": min_correlation,
            "correlation_risk": "moderate" if avg_correlation > 0.6 else "low" if avg_correlation < 0.3 else "high",
            "diversification_score": max(0, 1 - avg_correlation),
            "highly_correlated_pairs": [
                {"pair": ["AAPL", "MSFT"], "correlation": 0.78},
                {"pair": ["GOOGL", "META"], "correlation": 0.82}
            ],
            "recommendations": [
                "Consider reducing correlation by adding different sectors",
                "Monitor tech sector concentration" if avg_correlation > 0.7 else "Diversification looks adequate"
            ]
        }

        return correlation_analysis

    def _calculate_optimal_position_size(self, symbol: str, portfolio_value: float) -> Dict[str, Any]:
        """Calculate optimal position size using multiple methods"""
        # Mock position sizing calculation

        # Kelly Criterion estimation
        win_rate = 0.65  # 65% win rate assumption
        avg_win = 0.08   # 8% average win
        avg_loss = 0.04  # 4% average loss

        kelly_fraction = ((win_rate * avg_win) - ((1 - win_rate) * avg_loss)) / avg_win
        kelly_fraction = max(0, min(kelly_fraction, 0.25))  # Cap at 25%

        # Risk parity approach
        risk_parity_size = 0.05  # 5% for equal risk contribution

        # Fixed percentage
        fixed_percentage = 0.1  # 10% fixed allocation

        # Volatility-adjusted sizing
        volatility_adjustment = min(0.15, 0.20 / 0.25)  # Inverse volatility weighting

        return {
            "kelly_criterion": kelly_fraction,
            "risk_parity": risk_parity_size,
            "fixed_percentage": fixed_percentage,
            "volatility_adjusted": volatility_adjustment,
            "recommended_size": min(kelly_fraction * 0.5, 0.08),  # Conservative Kelly
            "max_position_size": 0.12,
            "risk_per_trade": 0.02,  # 2% maximum risk per trade
            "methodology_used": "conservative_kelly_with_caps"
        }

    def _assess_concentration_risk(self, positions: List[Dict], total_value: float) -> Dict[str, Any]:
        """Assess portfolio concentration risk"""
        if not positions:
            return {"concentration_risk": "none", "herfindahl_index": 0}

        # Calculate sector concentration
        sector_allocation = {}
        for pos in positions:
            sector = pos.get("sector", "Unknown")
            market_value = pos.get("market_value", 0)
            if sector not in sector_allocation:
                sector_allocation[sector] = 0
            sector_allocation[sector] += market_value

        # Convert to percentages
        sector_percentages = {
            sector: (value / total_value) * 100 if total_value > 0 else 0
            for sector, value in sector_allocation.items()
        }

        # Calculate Herfindahl-Hirschman Index
        hhi = sum((pct / 100) ** 2 for pct in sector_percentages.values())

        # Identify concentration risk
        max_sector_allocation = max(sector_percentages.values()) if sector_percentages else 0
        concentration_level = (
            "high" if max_sector_allocation > 40 else
            "moderate" if max_sector_allocation > 25 else
            "low"
        )

        # Individual position concentration
        position_sizes = [
            (pos.get("market_value", 0) / total_value) * 100 if total_value > 0 else 0
            for pos in positions
        ]
        max_position_size = max(position_sizes) if position_sizes else 0

        return {
            "concentration_risk": concentration_level,
            "herfindahl_index": hhi,
            "sector_allocation": sector_percentages,
            "max_sector_allocation": max_sector_allocation,
            "max_position_size": max_position_size,
            "position_count": len(positions),
            "diversification_ratio": min(1.0, len(positions) / 20),  # Optimal around 20 positions
            "concentration_warnings": [
                f"High concentration in {sector}"
                for sector, pct in sector_percentages.items()
                if pct > 35
            ]
        }

    def _stress_test_portfolio(self, positions: List[Dict], total_value: float) -> Dict[str, Any]:
        """Perform stress testing scenarios"""
        # Mock stress test results
        scenarios = {
            "market_crash_2008": {
                "scenario_name": "2008 Financial Crisis",
                "market_decline": -37.0,
                "portfolio_impact": -32.5,
                "estimated_loss": total_value * 0.325,
                "recovery_time_months": 18
            },
            "covid_crash_2020": {
                "scenario_name": "COVID-19 Market Crash",
                "market_decline": -34.0,
                "portfolio_impact": -28.8,
                "estimated_loss": total_value * 0.288,
                "recovery_time_months": 5
            },
            "tech_bubble_2000": {
                "scenario_name": "Dot-com Bubble Burst",
                "market_decline": -49.0,
                "portfolio_impact": -45.2,
                "estimated_loss": total_value * 0.452,
                "recovery_time_months": 31
            },
            "interest_rate_shock": {
                "scenario_name": "Interest Rate Shock (+3%)",
                "market_decline": -15.0,
                "portfolio_impact": -12.3,
                "estimated_loss": total_value * 0.123,
                "recovery_time_months": 8
            }
        }

        # Calculate worst-case scenario
        worst_case = max(scenarios.values(), key=lambda x: abs(x["portfolio_impact"]))

        return {
            "scenarios": scenarios,
            "worst_case_scenario": worst_case,
            "stress_test_summary": {
                "max_drawdown_estimate": worst_case["portfolio_impact"],
                "max_loss_estimate": worst_case["estimated_loss"],
                "avg_recovery_time": sum(s["recovery_time_months"] for s in scenarios.values()) / len(scenarios)
            },
            "portfolio_resilience": "moderate" if abs(worst_case["portfolio_impact"]) < 40 else "low"
        }

    def _calculate_sharpe_sortino_ratios(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate risk-adjusted performance metrics"""
        # Mock performance metrics calculation
        total_return_percent = portfolio_data.get("total_return_percent", 0)
        risk_free_rate = settings.RISK_FREE_RATE * 100  # Convert to percentage

        # Assume portfolio volatility
        portfolio_volatility = 18.0  # 18% annual volatility

        # Calculate Sharpe ratio
        sharpe_ratio = (total_return_percent - risk_free_rate) / portfolio_volatility if portfolio_volatility > 0 else 0

        # Calculate Sortino ratio (assuming downside deviation is 70% of total volatility)
        downside_deviation = portfolio_volatility * 0.7
        sortino_ratio = (total_return_percent - risk_free_rate) / downside_deviation if downside_deviation > 0 else 0

        return {
            "sharpe_ratio": sharpe_ratio,
            "sortino_ratio": sortino_ratio,
            "calmar_ratio": total_return_percent / 8.2 if total_return_percent > 0 else 0,  # Assuming 8.2% max drawdown
            "information_ratio": sharpe_ratio * 0.8,  # Approximation
            "portfolio_volatility": portfolio_volatility,
            "risk_adjusted_return": total_return_percent / portfolio_volatility if portfolio_volatility > 0 else 0
        }

    def _generate_position_sizing_recommendations(
        self, positions: List[Dict], total_value: float, var_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate position sizing recommendations"""

        current_position_sizes = [
            (pos.get("market_value", 0) / total_value) * 100 if total_value > 0 else 0
            for pos in positions
        ]

        avg_position_size = sum(current_position_sizes) / len(current_position_sizes) if current_position_sizes else 0

        return {
            "current_avg_position_size": avg_position_size,
            "recommended_max_position": 8.0,  # 8% maximum per position
            "recommended_avg_position": 5.0,  # 5% average position size
            "total_risk_budget": 2.0,  # 2% total portfolio risk
            "risk_per_trade": 1.0,  # 1% risk per individual trade
            "position_sizing_method": "kelly_criterion_conservative",
            "rebalancing_frequency": "monthly",
            "size_adjustments_needed": [
                {
                    "symbol": pos.get("symbol"),
                    "current_size": (pos.get("market_value", 0) / total_value) * 100,
                    "recommended_size": min(8.0, (pos.get("market_value", 0) / total_value) * 100),
                    "action": "reduce" if (pos.get("market_value", 0) / total_value) * 100 > 8.0 else "maintain"
                }
                for pos in positions[:5]  # Show top 5 positions
            ]
        }

    def _generate_risk_assessment(
        self, var_analysis: Dict, correlation_analysis: Dict,
        concentration_risk: Dict, stress_test: Dict
    ) -> Dict[str, Any]:
        """Generate overall risk assessment"""

        # Risk scoring (0-100, higher is riskier)
        var_score = min(100, (var_analysis.get("var_95_percent", 0) / 5.0) * 100)  # 5% daily VaR = 100 risk score
        correlation_score = correlation_analysis.get("avg_correlation", 0) * 100
        concentration_score = min(100, concentration_risk.get("max_sector_allocation", 0) * 2)  # 50% concentration = 100 risk score

        overall_risk_score = (var_score + correlation_score + concentration_score) / 3

        risk_level = (
            "low" if overall_risk_score < 30 else
            "moderate" if overall_risk_score < 60 else
            "high"
        )

        return {
            "overall_risk_level": risk_level,
            "risk_score": overall_risk_score,
            "risk_components": {
                "var_risk": var_score,
                "correlation_risk": correlation_score,
                "concentration_risk": concentration_score
            },
            "portfolio_beta": 1.15,  # Mock beta
            "correlation_to_market": 0.78,
            "diversification_effectiveness": correlation_analysis.get("diversification_score", 0.5)
        }

    def _generate_risk_recommendations(
        self, risk_assessment: Dict, concentration_risk: Dict, var_analysis: Dict
    ) -> List[str]:
        """Generate risk management recommendations"""
        recommendations = []

        if risk_assessment.get("risk_score", 0) > 60:
            recommendations.append("Consider reducing overall portfolio risk exposure")

        if concentration_risk.get("max_sector_allocation", 0) > 35:
            recommendations.append("Reduce sector concentration, particularly in largest sector")

        if var_analysis.get("var_95_percent", 0) > 3:
            recommendations.append("Daily VaR is elevated - consider position size reduction")

        if concentration_risk.get("max_position_size", 0) > 10:
            recommendations.append("Reduce individual position sizes to below 8% of portfolio")

        recommendations.extend([
            "Implement stop-loss orders on high-risk positions",
            "Consider portfolio hedging during volatile periods",
            "Regular rebalancing to maintain target allocations",
            "Monitor correlation changes during market stress"
        ])

        return recommendations

    def _generate_risk_alerts(
        self, var_analysis: Dict, concentration_risk: Dict, correlation_analysis: Dict
    ) -> List[Dict[str, str]]:
        """Generate risk alerts"""
        alerts = []

        if var_analysis.get("var_95_percent", 0) > 4:
            alerts.append({
                "level": "high",
                "message": "Daily VaR exceeds 4% of portfolio value"
            })

        if concentration_risk.get("max_sector_allocation", 0) > 40:
            alerts.append({
                "level": "warning",
                "message": "High sector concentration detected"
            })

        if correlation_analysis.get("avg_correlation", 0) > 0.8:
            alerts.append({
                "level": "warning",
                "message": "High correlation between positions reduces diversification benefits"
            })

        return alerts