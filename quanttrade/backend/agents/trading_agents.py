"""
AI Trading Agents powered by CrewAI
"""
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class TradingAgents:
    """Collection of AI trading agents"""

    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.7,
            api_key=api_key
        )

    def create_market_analyst(self) -> Agent:
        """Create Market Analyst Agent"""
        return Agent(
            role="Market Analyst",
            goal="Analyze market conditions, technical indicators, and fundamental data to identify trading opportunities",
            backstory="""You are an expert quantitative analyst with 15 years of experience in
            financial markets. You specialize in technical analysis, pattern recognition, and
            market sentiment analysis. You use advanced statistical methods and machine learning
            to predict market movements.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=True
        )

    def create_strategy_developer(self) -> Agent:
        """Create Strategy Developer Agent"""
        return Agent(
            role="Strategy Developer",
            goal="Design and optimize trading strategies based on market analysis and backtesting results",
            backstory="""You are a quantitative strategy developer with expertise in algorithmic
            trading systems. You excel at creating robust trading strategies that balance risk and
            return. You understand position sizing, risk management, and portfolio optimization.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=True
        )

    def create_risk_manager(self) -> Agent:
        """Create Risk Manager Agent"""
        return Agent(
            role="Risk Manager",
            goal="Assess and manage portfolio risk, ensuring positions stay within risk parameters",
            backstory="""You are a professional risk manager with deep expertise in portfolio
            risk assessment, Value at Risk (VaR), and stress testing. You ensure all trading
            activities comply with risk management policies and protect capital.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def create_backtester(self) -> Agent:
        """Create Backtester Agent"""
        return Agent(
            role="Strategy Backtester",
            goal="Validate trading strategies through rigorous historical backtesting and performance analysis",
            backstory="""You are a quantitative researcher specializing in strategy validation.
            You use advanced backtesting frameworks to test strategies across different market
            conditions, identifying potential weaknesses and optimization opportunities.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def create_signal_generator(self) -> Agent:
        """Create Signal Generator Agent"""
        return Agent(
            role="Signal Generator",
            goal="Generate actionable trading signals based on strategy rules and market conditions",
            backstory="""You are a trading signal expert who translates complex market analysis
            into clear buy/sell signals. You consider multiple timeframes, indicators, and market
            conditions to generate high-probability trading signals.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=True
        )

    async def analyze_market(self, symbols: List[str], timeframe: str = "1d") -> Dict[str, Any]:
        """Run market analysis crew"""
        analyst = self.create_market_analyst()
        signal_gen = self.create_signal_generator()

        # Create analysis task
        analysis_task = Task(
            description=f"""Analyze the following symbols: {', '.join(symbols)} on {timeframe} timeframe.
            Provide technical analysis including:
            1. Trend direction and strength
            2. Key support and resistance levels
            3. Momentum indicators (RSI, MACD, Stochastic)
            4. Volume analysis
            5. Chart patterns
            6. Market sentiment

            Format your analysis in a structured way for each symbol.""",
            agent=analyst,
            expected_output="Comprehensive market analysis with technical indicators and sentiment"
        )

        # Create signal generation task
        signal_task = Task(
            description="""Based on the market analysis, generate trading signals for each symbol.
            For each signal provide:
            1. Action (BUY/SELL/HOLD)
            2. Entry price range
            3. Stop loss level
            4. Take profit targets
            5. Position size recommendation
            6. Confidence level (1-10)
            7. Reasoning

            Only generate signals with confidence >= 7.""",
            agent=signal_gen,
            expected_output="Actionable trading signals with entry/exit levels"
        )

        # Create crew
        crew = Crew(
            agents=[analyst, signal_gen],
            tasks=[analysis_task, signal_task],
            process=Process.sequential,
            verbose=True
        )

        try:
            result = crew.kickoff()
            return {
                "success": True,
                "analysis": str(result),
                "timestamp": "now"
            }
        except Exception as e:
            logger.error(f"Market analysis failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def develop_strategy(self,
                              strategy_type: str,
                              symbols: List[str],
                              risk_level: str = "medium") -> Dict[str, Any]:
        """Develop trading strategy"""
        developer = self.create_strategy_developer()
        risk_mgr = self.create_risk_manager()
        backtester = self.create_backtester()

        # Strategy development task
        dev_task = Task(
            description=f"""Develop a {strategy_type} trading strategy for {', '.join(symbols)}.
            Risk level: {risk_level}

            The strategy should include:
            1. Entry rules (clear conditions for opening positions)
            2. Exit rules (stop loss and take profit conditions)
            3. Position sizing rules
            4. Timeframe selection
            5. Risk management parameters
            6. Expected win rate and risk/reward ratio

            Make the strategy rules precise and executable.""",
            agent=developer,
            expected_output="Complete trading strategy with precise entry/exit rules"
        )

        # Risk assessment task
        risk_task = Task(
            description="""Review the trading strategy and assess its risk profile.
            Provide:
            1. Maximum drawdown estimate
            2. Position size limits
            3. Portfolio heat (total risk exposure)
            4. Risk per trade
            5. Correlation risk
            6. Risk mitigation recommendations

            Ensure the strategy aligns with the specified risk level.""",
            agent=risk_mgr,
            expected_output="Risk assessment report with recommendations"
        )

        # Backtesting recommendations task
        backtest_task = Task(
            description="""Outline a comprehensive backtesting plan for this strategy.
            Include:
            1. Historical data requirements (timeframe, symbols)
            2. Key performance metrics to track
            3. Market conditions to test (bull, bear, sideways)
            4. Walk-forward analysis approach
            5. Overfitting prevention measures

            Provide specific recommendations for validating this strategy.""",
            agent=backtester,
            expected_output="Backtesting plan with validation methodology"
        )

        # Create crew
        crew = Crew(
            agents=[developer, risk_mgr, backtester],
            tasks=[dev_task, risk_task, backtest_task],
            process=Process.sequential,
            verbose=True
        )

        try:
            result = crew.kickoff()
            return {
                "success": True,
                "strategy": str(result),
                "timestamp": "now"
            }
        except Exception as e:
            logger.error(f"Strategy development failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def assess_portfolio_risk(self,
                                   positions: List[Dict[str, Any]],
                                   portfolio_value: float) -> Dict[str, Any]:
        """Assess portfolio risk"""
        risk_mgr = self.create_risk_manager()

        risk_task = Task(
            description=f"""Analyze the current portfolio and assess risk levels.

            Portfolio value: ${portfolio_value:,.2f}
            Current positions: {len(positions)}

            Analyze:
            1. Total portfolio exposure and leverage
            2. Position concentration risk
            3. Sector/asset correlation
            4. Value at Risk (VaR) estimates
            5. Maximum potential loss scenarios
            6. Recommended position adjustments

            Provide specific recommendations for risk reduction if needed.""",
            agent=risk_mgr,
            expected_output="Portfolio risk assessment with actionable recommendations"
        )

        crew = Crew(
            agents=[risk_mgr],
            tasks=[risk_task],
            process=Process.sequential,
            verbose=True
        )

        try:
            result = crew.kickoff()
            return {
                "success": True,
                "risk_assessment": str(result),
                "timestamp": "now"
            }
        except Exception as e:
            logger.error(f"Risk assessment failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
