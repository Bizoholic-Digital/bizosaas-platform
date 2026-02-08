"""
Refined Finance & Trading Agents (QuantTrade Focus)
Category 6 of the 20 Core Agent Architecture
"""

import asyncio
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from enum import Enum

from crewai import Agent, Task, Crew, Process
from .base_agent import BaseAgent, AgentRole, AgentTaskRequest

class TradingStrategyAgent(BaseAgent):
    """
    6.1 Trading Strategy Agent
    Purpose: Backtesting, Signal generation, Risk management
    """
    
    def __init__(self):
        super().__init__(
            agent_name="trading_strategy_agent",
            agent_role=AgentRole.OPERATIONS,
            description="Agent for algorithmic trading strategy development and backtesting",
            version="2.0.0"
        )
        
        self.crew_agent = Agent(
            role='Quantitative Trading Strategist',
            goal='Develop and validate high-Sharpe ratio trading strategies across multiple asset classes',
            backstory="""You are an expert quant with deep knowledge of market microstructure, 
            statistical arbitrage, and risk management. You excel at identifying alpha, 
            performing rigorous backtests, and maintaining strict risk controls.""",
            verbose=True,
            allow_delegation=False
        )

    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute trading strategy tasks"""
        input_data = task_request.input_data
        mode = input_data.get('mode', 'strategy_backtest')
        
        trading_task = Task(
            description=f"""
            Perform {mode.replace('_', ' ')} for:
            {json.dumps(input_data.get('market_context', {}))}
            
            Asset Class: {input_data.get('asset_class', 'Equities/Forex')}
            Risk Parameters: {json.dumps(input_data.get('risk_params', {'max_drawdown': '5%', 'leverage': '1x'}))}
            
            Deliverables:
            1. Strategy Logic & Signal Generation Rules
            2. Full Backtest Metrics (Sharpe, CAGR, Max DD, Win Rate)
            3. Risk Scenarios Analysis
            4. Position Sizing Recommendations
            5. Execution Protocol
            """,
            agent=self.crew_agent,
            expected_output=f"A detailed quantitative trading {mode} report."
        )
        
        crew = Crew(
            agents=[self.crew_agent],
            tasks=[trading_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "agent": self.agent_name,
            "strategy_task_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "results": str(result)
        }

class FinancialAnalyticsAgent(BaseAgent):
    """
    6.2 Financial Analytics Agent
    Purpose: Revenue forecasting, ROI analysis, Budget optimization
    """
    
    def __init__(self):
        super().__init__(
            agent_name="financial_analytics_agent",
            agent_role=AgentRole.ANALYTICS,
            description="Agent for comprehensive financial analysis and revenue forecasting",
            version="2.0.0"
        )
        
        self.crew_agent = Agent(
            role='Chief Financial Analyst',
            goal='Provide accurate financial insights and optimize capital allocation for growth',
            backstory="""You are a senior financial analyst with expertise in SaaS metrics, 
            venture capital modeling, and algorithmic wealth management. You excel at 
            interpreting balance sheets and identifying revenue growth levers.""",
            verbose=True,
            allow_delegation=True
        )

    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute financial analytics tasks"""
        input_data = task_request.input_data
        mode = input_data.get('mode', 'revenue_forecasting')
        
        finance_task = Task(
            description=f"""
            Execute {mode.replace('_', ' ')} for:
            {json.dumps(input_data.get('financial_data', {}))}
            
            Metric Focus: {json.dumps(input_data.get('target_metrics', ['MRR', 'Churn', 'CAC', 'LTV']))}
            Time Period: {input_data.get('forecast_period', '12 Months')}
            
            Requirements:
            1. Forecasted Revenue with confidence bands
            2. Customer Acquisition Cost (CAC) Efficiency Analysis
            3. Budget Allocation Optimization (where to spend next $10k)
            4. Sensitivity Analysis (Worst/Best case scenarios)
            5. ROI breakdown by channel/agent
            """,
            agent=self.crew_agent,
            expected_output=f"A high-level financial {mode} report."
        )
        
        crew = Crew(
            agents=[self.crew_agent],
            tasks=[finance_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "agent": self.agent_name,
            "finance_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "results": str(result)
        }
