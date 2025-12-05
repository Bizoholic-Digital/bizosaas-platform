"""
Trading AI Agents - Repurposed from BizOSaaS Platform
Leverages existing 88-agent ecosystem for trading intelligence
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd
import numpy as np
from dataclasses import dataclass
import logging
import httpx

from config import settings

logger = logging.getLogger(__name__)


@dataclass
class AgentResponse:
    """Standard agent response format"""
    agent_name: str
    success: bool
    data: Dict[str, Any]
    confidence: float
    timestamp: datetime
    metadata: Optional[Dict] = None


class BaseTradingAgent:
    """
    Base class for trading AI agents
    Integrates with BizOSaaS Brain API Gateway
    """
    
    def __init__(self, agent_name: str):
        """
        Initialize trading agent
        
        Args:
            agent_name: Unique agent identifier
        """
        self.agent_name = agent_name
        self.brain_api_url = settings.BRAIN_API_URL
        self.brain_api_key = settings.BRAIN_API_KEY
        
    async def call_brain_api(self, endpoint: str, data: Dict) -> Dict:
        """
        Call Brain API Gateway
        
        Args:
            endpoint: API endpoint
            data: Request data
            
        Returns:
            API response
        """
        url = f"{self.brain_api_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.brain_api_key}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=data, headers=headers)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Brain API call failed: {e}")
                return {"error": str(e)}
    
    async def register_with_brain(self):
        """Register agent with Brain API Gateway"""
        registration_data = {
            "agent_name": self.agent_name,
            "agent_type": "trading",
            "capabilities": self.get_capabilities(),
            "status": "active"
        }
        
        result = await self.call_brain_api("agents/register", registration_data)
        logger.info(f"Agent {self.agent_name} registered with Brain API")
        return result
    
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities"""
        return []


class PositionSizingAgent(BaseTradingAgent):
    """
    Position Sizing Agent
    Repurposed from Budget Optimization Agent
    Calculates optimal position sizes using multiple methods
    """
    
    def __init__(self):
        super().__init__("position_sizing_agent")
        
    def get_capabilities(self) -> List[str]:
        return [
            "kelly_criterion",
            "fixed_risk",
            "optimal_f",
            "risk_parity",
            "volatility_targeting"
        ]
    
    async def calculate_position_size(
        self,
        method: str,
        account_balance: float,
        strategy_stats: Dict,
        risk_params: Dict
    ) -> AgentResponse:
        """
        Calculate optimal position size
        
        Args:
            method: Sizing method (kelly, fixed_risk, optimal_f)
            account_balance: Current account balance
            strategy_stats: Strategy performance statistics
            risk_params: Risk parameters
            
        Returns:
            Agent response with position size recommendation
        """
        try:
            if method == "kelly":
                size = self._kelly_criterion(account_balance, strategy_stats)
            elif method == "fixed_risk":
                size = self._fixed_risk(account_balance, risk_params)
            elif method == "optimal_f":
                size = self._optimal_f(account_balance, strategy_stats)
            else:
                size = account_balance * 0.02  # Default 2%
            
            # Call Brain API for cross-validation with business agents
            brain_validation = await self.call_brain_api(
                "agents/validate_allocation",
                {
                    "agent": self.agent_name,
                    "allocation": size,
                    "context": "trading_position"
                }
            )
            
            confidence = brain_validation.get("confidence", 0.8)
            
            return AgentResponse(
                agent_name=self.agent_name,
                success=True,
                data={
                    "position_size": size,
                    "method": method,
                    "account_balance": account_balance,
                    "allocation_percent": (size / account_balance) * 100
                },
                confidence=confidence,
                timestamp=datetime.now(),
                metadata={"brain_validation": brain_validation}
            )
            
        except Exception as e:
            logger.error(f"Position sizing failed: {e}")
            return AgentResponse(
                agent_name=self.agent_name,
                success=False,
                data={"error": str(e)},
                confidence=0.0,
                timestamp=datetime.now()
            )
    
    def _kelly_criterion(self, balance: float, stats: Dict) -> float:
        """Kelly Criterion calculation"""
        win_rate = stats.get('win_rate', 0.5)
        avg_win = stats.get('avg_win', 0)
        avg_loss = stats.get('avg_loss', 0)
        
        if avg_loss == 0:
            return 0.0
        
        win_loss_ratio = avg_win / avg_loss
        kelly_fraction = (win_rate * win_loss_ratio - (1 - win_rate)) / win_loss_ratio
        kelly_fraction = max(0, min(kelly_fraction * 0.25, 0.1))  # Cap at 10%
        
        return balance * kelly_fraction
    
    def _fixed_risk(self, balance: float, params: Dict) -> float:
        """Fixed risk calculation"""
        risk_per_trade = params.get('risk_per_trade', 0.02)
        entry_price = params.get('entry_price', 0)
        stop_loss = params.get('stop_loss', 0)
        
        if entry_price == 0 or stop_loss == 0:
            return 0.0
        
        risk_amount = balance * risk_per_trade
        price_risk = abs(entry_price - stop_loss)
        
        return risk_amount / price_risk if price_risk > 0 else 0.0
    
    def _optimal_f(self, balance: float, stats: Dict) -> float:
        """Optimal F calculation"""
        trades = stats.get('trade_history', [])
        if not trades:
            return balance * 0.02
        
        largest_loss = abs(min(trades))
        if largest_loss == 0:
            return 0.0
        
        # Simplified optimal F
        best_f = 0.0
        best_twr = 0.0
        
        for f in np.arange(0.01, 0.5, 0.01):
            twr = 1.0
            for trade in trades:
                hpr = 1 + (f * trade / largest_loss)
                twr *= hpr
            
            if twr > best_twr:
                best_twr = twr
                best_f = f
        
        return balance * best_f * 0.5  # Apply safety factor


class MarketPatternAgent(BaseTradingAgent):
    """
    Market Pattern Recognition Agent
    Repurposed from Content Analysis Agent
    Identifies and analyzes market patterns using vector similarity
    """
    
    def __init__(self):
        super().__init__("market_pattern_agent")
        
    def get_capabilities(self) -> List[str]:
        return [
            "pattern_detection",
            "similarity_search",
            "trend_analysis",
            "anomaly_detection"
        ]
    
    async def detect_patterns(
        self,
        market_data: pd.DataFrame,
        pattern_types: List[str]
    ) -> AgentResponse:
        """
        Detect market patterns in data
        
        Args:
            market_data: OHLCV data
            pattern_types: Types of patterns to detect
            
        Returns:
            Agent response with detected patterns
        """
        try:
            detected_patterns = []
            
            for pattern_type in pattern_types:
                if pattern_type == "breakout":
                    patterns = self._detect_breakout(market_data)
                elif pattern_type == "reversal":
                    patterns = self._detect_reversal(market_data)
                elif pattern_type == "continuation":
                    patterns = self._detect_continuation(market_data)
                else:
                    continue
                
                detected_patterns.extend(patterns)
            
            # Send patterns to Brain API for cross-platform analysis
            brain_analysis = await self.call_brain_api(
                "agents/analyze_patterns",
                {
                    "agent": self.agent_name,
                    "patterns": detected_patterns,
                    "context": "market_trading"
                }
            )
            
            return AgentResponse(
                agent_name=self.agent_name,
                success=True,
                data={
                    "patterns": detected_patterns,
                    "count": len(detected_patterns),
                    "brain_insights": brain_analysis.get("insights", [])
                },
                confidence=0.85,
                timestamp=datetime.now(),
                metadata={"pattern_types": pattern_types}
            )
            
        except Exception as e:
            logger.error(f"Pattern detection failed: {e}")
            return AgentResponse(
                agent_name=self.agent_name,
                success=False,
                data={"error": str(e)},
                confidence=0.0,
                timestamp=datetime.now()
            )
    
    def _detect_breakout(self, data: pd.DataFrame) -> List[Dict]:
        """Detect breakout patterns"""
        patterns = []
        
        # Calculate 20-period high/low
        data['high_20'] = data['high'].rolling(window=20).max()
        data['low_20'] = data['low'].rolling(window=20).min()
        
        # Detect breakouts
        for i in range(len(data) - 1):
            if data.iloc[i]['close'] > data.iloc[i]['high_20']:
                patterns.append({
                    'type': 'breakout_up',
                    'timestamp': data.iloc[i]['timestamp'],
                    'price': data.iloc[i]['close'],
                    'strength': (data.iloc[i]['close'] - data.iloc[i]['high_20']) / data.iloc[i]['high_20']
                })
            elif data.iloc[i]['close'] < data.iloc[i]['low_20']:
                patterns.append({
                    'type': 'breakout_down',
                    'timestamp': data.iloc[i]['timestamp'],
                    'price': data.iloc[i]['close'],
                    'strength': (data.iloc[i]['low_20'] - data.iloc[i]['close']) / data.iloc[i]['low_20']
                })
        
        return patterns
    
    def _detect_reversal(self, data: pd.DataFrame) -> List[Dict]:
        """Detect reversal patterns"""
        patterns = []
        
        # Simple RSI-based reversal detection
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['rsi'] = 100 - (100 / (1 + rs))
        
        for i in range(len(data) - 1):
            if data.iloc[i]['rsi'] < 30:
                patterns.append({
                    'type': 'reversal_bullish',
                    'timestamp': data.iloc[i]['timestamp'],
                    'price': data.iloc[i]['close'],
                    'rsi': data.iloc[i]['rsi']
                })
            elif data.iloc[i]['rsi'] > 70:
                patterns.append({
                    'type': 'reversal_bearish',
                    'timestamp': data.iloc[i]['timestamp'],
                    'price': data.iloc[i]['close'],
                    'rsi': data.iloc[i]['rsi']
                })
        
        return patterns
    
    def _detect_continuation(self, data: pd.DataFrame) -> List[Dict]:
        """Detect continuation patterns"""
        patterns = []
        
        # Moving average trend continuation
        data['sma_20'] = data['close'].rolling(window=20).mean()
        data['sma_50'] = data['close'].rolling(window=50).mean()
        
        for i in range(len(data) - 1):
            if (data.iloc[i]['sma_20'] > data.iloc[i]['sma_50'] and
                data.iloc[i]['close'] > data.iloc[i]['sma_20']):
                patterns.append({
                    'type': 'continuation_bullish',
                    'timestamp': data.iloc[i]['timestamp'],
                    'price': data.iloc[i]['close'],
                    'trend_strength': (data.iloc[i]['sma_20'] - data.iloc[i]['sma_50']) / data.iloc[i]['sma_50']
                })
        
        return patterns


class StrategyPerformanceAgent(BaseTradingAgent):
    """
    Strategy Performance Analysis Agent
    Repurposed from Campaign Analytics Agent
    Monitors and analyzes strategy performance in real-time
    """
    
    def __init__(self):
        super().__init__("strategy_performance_agent")
        
    def get_capabilities(self) -> List[str]:
        return [
            "performance_monitoring",
            "strategy_comparison",
            "optimization_suggestions",
            "anomaly_detection"
        ]
    
    async def analyze_performance(
        self,
        strategy_id: str,
        trades: List[Dict],
        equity_curve: pd.DataFrame
    ) -> AgentResponse:
        """
        Analyze strategy performance
        
        Args:
            strategy_id: Strategy identifier
            trades: List of trades
            equity_curve: Equity curve data
            
        Returns:
            Agent response with performance analysis
        """
        try:
            # Calculate metrics
            metrics = self._calculate_metrics(trades, equity_curve)
            
            # Detect performance anomalies
            anomalies = self._detect_anomalies(equity_curve)
            
            # Get optimization suggestions
            suggestions = self._get_optimization_suggestions(metrics)
            
            # Send to Brain API for cross-platform insights
            brain_insights = await self.call_brain_api(
                "agents/analyze_performance",
                {
                    "agent": self.agent_name,
                    "strategy_id": strategy_id,
                    "metrics": metrics,
                    "context": "trading_strategy"
                }
            )
            
            return AgentResponse(
                agent_name=self.agent_name,
                success=True,
                data={
                    "strategy_id": strategy_id,
                    "metrics": metrics,
                    "anomalies": anomalies,
                    "suggestions": suggestions,
                    "brain_insights": brain_insights.get("insights", [])
                },
                confidence=0.9,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Performance analysis failed: {e}")
            return AgentResponse(
                agent_name=self.agent_name,
                success=False,
                data={"error": str(e)},
                confidence=0.0,
                timestamp=datetime.now()
            )
    
    def _calculate_metrics(self, trades: List[Dict], equity: pd.DataFrame) -> Dict:
        """Calculate performance metrics"""
        total_trades = len(trades)
        winning_trades = sum(1 for t in trades if t.get('pnl', 0) > 0)
        
        returns = equity['portfolio_value'].pct_change().dropna()
        
        return {
            "total_trades": total_trades,
            "win_rate": (winning_trades / total_trades * 100) if total_trades > 0 else 0,
            "sharpe_ratio": (returns.mean() / returns.std() * np.sqrt(252)) if returns.std() > 0 else 0,
            "max_drawdown": self._calculate_max_drawdown(equity),
            "total_return": ((equity['portfolio_value'].iloc[-1] / equity['portfolio_value'].iloc[0]) - 1) * 100
        }
    
    def _calculate_max_drawdown(self, equity: pd.DataFrame) -> float:
        """Calculate maximum drawdown"""
        cumulative = equity['portfolio_value']
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return drawdown.min() * 100
    
    def _detect_anomalies(self, equity: pd.DataFrame) -> List[Dict]:
        """Detect performance anomalies"""
        anomalies = []
        returns = equity['portfolio_value'].pct_change()
        
        # Detect large drawdowns
        threshold = returns.std() * 3
        for i, ret in enumerate(returns):
            if ret < -threshold:
                anomalies.append({
                    'type': 'large_loss',
                    'timestamp': equity.index[i],
                    'return': ret * 100
                })
        
        return anomalies
    
    def _get_optimization_suggestions(self, metrics: Dict) -> List[str]:
        """Generate optimization suggestions"""
        suggestions = []
        
        if metrics['win_rate'] < 50:
            suggestions.append("Consider adjusting entry criteria to improve win rate")
        
        if metrics['sharpe_ratio'] < 1.0:
            suggestions.append("Risk-adjusted returns are low - review position sizing")
        
        if abs(metrics['max_drawdown']) > 20:
            suggestions.append("Maximum drawdown is high - implement stricter risk controls")
        
        return suggestions


class RiskAssessmentAgent(BaseTradingAgent):
    """
    Risk Assessment Agent
    Repurposed from Business Risk Agent
    Monitors portfolio risk and generates alerts
    """
    
    def __init__(self):
        super().__init__("risk_assessment_agent")
        
    def get_capabilities(self) -> List[str]:
        return [
            "var_calculation",
            "stress_testing",
            "correlation_analysis",
            "risk_alerts"
        ]
    
    async def assess_risk(
        self,
        portfolio_value: float,
        positions: List[Dict],
        returns_history: pd.Series,
        risk_limits: Dict
    ) -> AgentResponse:
        """
        Assess portfolio risk
        
        Args:
            portfolio_value: Current portfolio value
            positions: Current positions
            returns_history: Historical returns
            risk_limits: Risk limit configuration
            
        Returns:
            Agent response with risk assessment
        """
        try:
            # Calculate risk metrics
            var_95 = self._calculate_var(returns_history, portfolio_value)
            cvar_95 = self._calculate_cvar(returns_history, portfolio_value)
            
            # Check risk limits
            violations = self._check_limits(
                portfolio_value,
                positions,
                var_95,
                risk_limits
            )
            
            # Generate alerts
            alerts = self._generate_alerts(violations)
            
            # Send to Brain API for enterprise-wide risk monitoring
            brain_risk = await self.call_brain_api(
                "agents/assess_risk",
                {
                    "agent": self.agent_name,
                    "portfolio_value": portfolio_value,
                    "var_95": var_95,
                    "violations": violations,
                    "context": "trading_portfolio"
                }
            )
            
            return AgentResponse(
                agent_name=self.agent_name,
                success=True,
                data={
                    "var_95": var_95,
                    "cvar_95": cvar_95,
                    "violations": violations,
                    "alerts": alerts,
                    "risk_score": brain_risk.get("risk_score", 0)
                },
                confidence=0.95,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Risk assessment failed: {e}")
            return AgentResponse(
                agent_name=self.agent_name,
                success=False,
                data={"error": str(e)},
                confidence=0.0,
                timestamp=datetime.now()
            )
    
    def _calculate_var(self, returns: pd.Series, portfolio_value: float) -> float:
        """Calculate Value at Risk"""
        if len(returns) == 0:
            return 0.0
        var_return = np.percentile(returns, 5)
        return abs(var_return * portfolio_value)
    
    def _calculate_cvar(self, returns: pd.Series, portfolio_value: float) -> float:
        """Calculate Conditional VaR"""
        if len(returns) == 0:
            return 0.0
        var_threshold = np.percentile(returns, 5)
        tail_returns = returns[returns <= var_threshold]
        cvar_return = tail_returns.mean() if len(tail_returns) > 0 else 0
        return abs(cvar_return * portfolio_value)
    
    def _check_limits(
        self,
        portfolio_value: float,
        positions: List[Dict],
        var: float,
        limits: Dict
    ) -> List[Dict]:
        """Check risk limit violations"""
        violations = []
        
        # Check VaR limit
        var_limit = portfolio_value * limits.get('max_var_pct', 0.05)
        if var > var_limit:
            violations.append({
                'type': 'var_exceeded',
                'current': var,
                'limit': var_limit
            })
        
        # Check position concentration
        for pos in positions:
            pos_value = pos.get('quantity', 0) * pos.get('current_price', 0)
            pos_pct = pos_value / portfolio_value
            if pos_pct > limits.get('max_position_size', 0.1):
                violations.append({
                    'type': 'position_size_exceeded',
                    'symbol': pos.get('symbol'),
                    'current': pos_pct,
                    'limit': limits.get('max_position_size')
                })
        
        return violations
    
    def _generate_alerts(self, violations: List[Dict]) -> List[Dict]:
        """Generate risk alerts"""
        alerts = []
        
        for violation in violations:
            severity = "high" if violation['type'] == 'var_exceeded' else "medium"
            alerts.append({
                'severity': severity,
                'message': f"{violation['type']}: {violation.get('current')} exceeds limit {violation.get('limit')}",
                'timestamp': datetime.now()
            })
        
        return alerts


# Agent Registry
TRADING_AGENTS = {
    "position_sizing": PositionSizingAgent,
    "market_pattern": MarketPatternAgent,
    "strategy_performance": StrategyPerformanceAgent,
    "risk_assessment": RiskAssessmentAgent
}


async def initialize_agents() -> Dict[str, BaseTradingAgent]:
    """
    Initialize all trading agents and register with Brain API
    
    Returns:
        Dictionary of initialized agents
    """
    agents = {}
    
    for agent_id, agent_class in TRADING_AGENTS.items():
        agent = agent_class()
        await agent.register_with_brain()
        agents[agent_id] = agent
        logger.info(f"Initialized and registered {agent_id}")
    
    return agents
