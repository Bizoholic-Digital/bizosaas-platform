"""
Risk Management Service
Comprehensive risk controls and portfolio monitoring
"""
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from datetime import datetime
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class RiskLimits:
    """Risk limit configuration"""
    max_position_size: float = 0.1  # 10% of portfolio
    max_portfolio_risk: float = 0.05  # 5% total portfolio risk
    max_daily_loss: float = 0.02  # 2% max daily loss
    max_drawdown: float = 0.15  # 15% max drawdown
    max_leverage: float = 1.0  # No leverage by default
    var_confidence: float = 0.95  # 95% VaR confidence


@dataclass
class PortfolioRisk:
    """Portfolio risk metrics"""
    total_value: float
    total_exposure: float
    var_95: float
    cvar_95: float
    portfolio_delta: Optional[float] = None
    portfolio_gamma: Optional[float] = None
    portfolio_theta: Optional[float] = None
    portfolio_vega: Optional[float] = None
    margin_utilization: float = 0.0
    leverage: float = 1.0


class RiskManager:
    """
    Comprehensive risk management service
    Handles position sizing, risk limits, and portfolio monitoring
    """
    
    def __init__(self, limits: RiskLimits):
        """
        Initialize risk manager
        
        Args:
            limits: Risk limit configuration
        """
        self.limits = limits
        self.daily_pnl_history: List[float] = []
        self.portfolio_values: List[float] = []
        
    def calculate_position_size_kelly(
        self,
        account_balance: float,
        win_rate: float,
        avg_win: float,
        avg_loss: float,
        max_risk: Optional[float] = None
    ) -> float:
        """
        Calculate optimal position size using Kelly Criterion
        
        Args:
            account_balance: Current account balance
            win_rate: Historical win rate (0-1)
            avg_win: Average win amount
            avg_loss: Average loss amount
            max_risk: Maximum risk override
            
        Returns:
            Optimal position size as fraction of account
        """
        if avg_loss == 0 or win_rate == 0:
            return 0.0
            
        # Kelly formula: f = (p * b - q) / b
        # where p = win rate, q = loss rate, b = win/loss ratio
        win_loss_ratio = avg_win / avg_loss
        kelly_fraction = (win_rate * win_loss_ratio - (1 - win_rate)) / win_loss_ratio
        
        # Apply Kelly fraction cap (typically 25-50% of full Kelly)
        kelly_fraction = max(0, min(kelly_fraction * 0.25, self.limits.max_position_size))
        
        # Apply maximum risk limit if provided
        if max_risk:
            kelly_fraction = min(kelly_fraction, max_risk)
            
        position_size = account_balance * kelly_fraction
        
        logger.info(f"Kelly position size: ${position_size:,.2f} ({kelly_fraction*100:.2f}% of account)")
        
        return position_size
    
    def calculate_position_size_fixed(
        self,
        account_balance: float,
        risk_per_trade: float,
        entry_price: float,
        stop_loss_price: float
    ) -> float:
        """
        Calculate position size using fixed risk method
        
        Args:
            account_balance: Current account balance
            risk_per_trade: Risk per trade as fraction (e.g., 0.02 for 2%)
            entry_price: Entry price
            stop_loss_price: Stop loss price
            
        Returns:
            Position size in units
        """
        # Calculate risk amount in dollars
        risk_amount = account_balance * risk_per_trade
        
        # Calculate price risk per unit
        price_risk = abs(entry_price - stop_loss_price)
        
        if price_risk == 0:
            return 0.0
            
        # Calculate position size
        position_size = risk_amount / price_risk
        
        # Apply maximum position size limit
        max_size = account_balance * self.limits.max_position_size / entry_price
        position_size = min(position_size, max_size)
        
        logger.info(f"Fixed risk position size: {position_size:.4f} units (${position_size * entry_price:,.2f})")
        
        return position_size
    
    def calculate_var(
        self,
        returns: pd.Series,
        confidence: float = 0.95,
        portfolio_value: float = 100000.0
    ) -> float:
        """
        Calculate Value at Risk (VaR)
        
        Args:
            returns: Historical returns series
            confidence: Confidence level (default 95%)
            portfolio_value: Current portfolio value
            
        Returns:
            VaR in dollars
        """
        if len(returns) == 0:
            return 0.0
            
        # Calculate VaR using historical simulation
        var_percentile = (1 - confidence) * 100
        var_return = np.percentile(returns, var_percentile)
        var_dollar = abs(var_return * portfolio_value)
        
        logger.info(f"VaR ({confidence*100}%): ${var_dollar:,.2f}")
        
        return var_dollar
    
    def calculate_cvar(
        self,
        returns: pd.Series,
        confidence: float = 0.95,
        portfolio_value: float = 100000.0
    ) -> float:
        """
        Calculate Conditional Value at Risk (CVaR / Expected Shortfall)
        
        Args:
            returns: Historical returns series
            confidence: Confidence level (default 95%)
            portfolio_value: Current portfolio value
            
        Returns:
            CVaR in dollars
        """
        if len(returns) == 0:
            return 0.0
            
        # Calculate VaR threshold
        var_percentile = (1 - confidence) * 100
        var_threshold = np.percentile(returns, var_percentile)
        
        # Calculate CVaR as average of returns below VaR
        tail_returns = returns[returns <= var_threshold]
        cvar_return = tail_returns.mean() if len(tail_returns) > 0 else 0
        cvar_dollar = abs(cvar_return * portfolio_value)
        
        logger.info(f"CVaR ({confidence*100}%): ${cvar_dollar:,.2f}")
        
        return cvar_dollar
    
    def calculate_portfolio_greeks(
        self,
        positions: List[Dict]
    ) -> Tuple[float, float, float, float]:
        """
        Calculate portfolio-level Greeks for options positions
        
        Args:
            positions: List of position dictionaries with Greeks
            
        Returns:
            Tuple of (delta, gamma, theta, vega)
        """
        total_delta = sum(p.get('delta', 0) * p.get('quantity', 0) for p in positions)
        total_gamma = sum(p.get('gamma', 0) * p.get('quantity', 0) for p in positions)
        total_theta = sum(p.get('theta', 0) * p.get('quantity', 0) for p in positions)
        total_vega = sum(p.get('vega', 0) * p.get('quantity', 0) for p in positions)
        
        return total_delta, total_gamma, total_theta, total_vega
    
    def assess_portfolio_risk(
        self,
        portfolio_value: float,
        positions: List[Dict],
        returns_history: pd.Series
    ) -> PortfolioRisk:
        """
        Comprehensive portfolio risk assessment
        
        Args:
            portfolio_value: Current portfolio value
            positions: List of current positions
            returns_history: Historical returns
            
        Returns:
            Portfolio risk metrics
        """
        # Calculate total exposure
        total_exposure = sum(
            p.get('quantity', 0) * p.get('current_price', 0) 
            for p in positions
        )
        
        # Calculate VaR and CVaR
        var_95 = self.calculate_var(returns_history, 0.95, portfolio_value)
        cvar_95 = self.calculate_cvar(returns_history, 0.95, portfolio_value)
        
        # Calculate Greeks for options positions
        delta, gamma, theta, vega = self.calculate_portfolio_greeks(positions)
        
        # Calculate leverage
        leverage = total_exposure / portfolio_value if portfolio_value > 0 else 0
        
        # Calculate margin utilization (simplified)
        margin_utilization = min(total_exposure / (portfolio_value * 2), 1.0)
        
        risk_metrics = PortfolioRisk(
            total_value=portfolio_value,
            total_exposure=total_exposure,
            var_95=var_95,
            cvar_95=cvar_95,
            portfolio_delta=delta,
            portfolio_gamma=gamma,
            portfolio_theta=theta,
            portfolio_vega=vega,
            margin_utilization=margin_utilization,
            leverage=leverage
        )
        
        logger.info(f"Portfolio Risk - Value: ${portfolio_value:,.2f}, VaR: ${var_95:,.2f}, Leverage: {leverage:.2f}x")
        
        return risk_metrics
    
    def validate_trade(
        self,
        trade_value: float,
        portfolio_value: float,
        current_exposure: float,
        daily_pnl: float
    ) -> Tuple[bool, str]:
        """
        Validate if a trade meets risk limits
        
        Args:
            trade_value: Value of proposed trade
            portfolio_value: Current portfolio value
            current_exposure: Current total exposure
            daily_pnl: Today's P&L
            
        Returns:
            Tuple of (is_valid, reason)
        """
        # Check position size limit
        position_pct = trade_value / portfolio_value
        if position_pct > self.limits.max_position_size:
            return False, f"Position size {position_pct*100:.1f}% exceeds limit {self.limits.max_position_size*100:.1f}%"
        
        # Check portfolio risk limit
        new_exposure = current_exposure + trade_value
        exposure_pct = new_exposure / portfolio_value
        if exposure_pct > self.limits.max_portfolio_risk:
            return False, f"Portfolio exposure {exposure_pct*100:.1f}% exceeds limit {self.limits.max_portfolio_risk*100:.1f}%"
        
        # Check daily loss limit
        daily_loss_pct = abs(daily_pnl) / portfolio_value
        if daily_pnl < 0 and daily_loss_pct > self.limits.max_daily_loss:
            return False, f"Daily loss {daily_loss_pct*100:.1f}% exceeds limit {self.limits.max_daily_loss*100:.1f}%"
        
        # Check leverage limit
        leverage = new_exposure / portfolio_value
        if leverage > self.limits.max_leverage:
            return False, f"Leverage {leverage:.2f}x exceeds limit {self.limits.max_leverage:.2f}x"
        
        return True, "Trade approved"
    
    def check_drawdown_limit(
        self,
        current_value: float,
        peak_value: float
    ) -> Tuple[bool, float]:
        """
        Check if current drawdown exceeds limit
        
        Args:
            current_value: Current portfolio value
            peak_value: Peak portfolio value
            
        Returns:
            Tuple of (within_limit, current_drawdown)
        """
        if peak_value == 0:
            return True, 0.0
            
        drawdown = (peak_value - current_value) / peak_value
        within_limit = drawdown <= self.limits.max_drawdown
        
        if not within_limit:
            logger.warning(f"Drawdown {drawdown*100:.1f}% exceeds limit {self.limits.max_drawdown*100:.1f}%")
        
        return within_limit, drawdown
    
    def update_daily_pnl(self, pnl: float):
        """
        Update daily P&L history
        
        Args:
            pnl: Daily P&L
        """
        self.daily_pnl_history.append(pnl)
        
        # Keep only last 30 days
        if len(self.daily_pnl_history) > 30:
            self.daily_pnl_history = self.daily_pnl_history[-30:]
    
    def update_portfolio_value(self, value: float):
        """
        Update portfolio value history
        
        Args:
            value: Portfolio value
        """
        self.portfolio_values.append(value)
        
        # Keep only last 252 days (1 trading year)
        if len(self.portfolio_values) > 252:
            self.portfolio_values = self.portfolio_values[-252:]
    
    def get_risk_summary(self, portfolio_risk: PortfolioRisk) -> str:
        """
        Generate human-readable risk summary
        
        Args:
            portfolio_risk: Portfolio risk metrics
            
        Returns:
            Formatted risk summary
        """
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║                    RISK SUMMARY                               ║
╚══════════════════════════════════════════════════════════════╝

💼 PORTFOLIO
────────────────────────────────────────────────────────────────
Total Value: ${portfolio_risk.total_value:,.2f}
Total Exposure: ${portfolio_risk.total_exposure:,.2f}
Leverage: {portfolio_risk.leverage:.2f}x
Margin Utilization: {portfolio_risk.margin_utilization*100:.1f}%

⚠️  RISK METRICS
────────────────────────────────────────────────────────────────
VaR (95%): ${portfolio_risk.var_95:,.2f}
CVaR (95%): ${portfolio_risk.cvar_95:,.2f}

📊 GREEKS (Options Portfolio)
────────────────────────────────────────────────────────────────
Delta: {portfolio_risk.portfolio_delta or 0:.4f}
Gamma: {portfolio_risk.portfolio_gamma or 0:.4f}
Theta: {portfolio_risk.portfolio_theta or 0:.4f}
Vega: {portfolio_risk.portfolio_vega or 0:.4f}

🛡️  RISK LIMITS
────────────────────────────────────────────────────────────────
Max Position Size: {self.limits.max_position_size*100:.1f}%
Max Portfolio Risk: {self.limits.max_portfolio_risk*100:.1f}%
Max Daily Loss: {self.limits.max_daily_loss*100:.1f}%
Max Drawdown: {self.limits.max_drawdown*100:.1f}%
Max Leverage: {self.limits.max_leverage:.1f}x

════════════════════════════════════════════════════════════════
"""
        return summary


class PositionSizer:
    """
    Advanced position sizing algorithms
    """
    
    @staticmethod
    def optimal_f(
        trades: List[float],
        initial_capital: float
    ) -> float:
        """
        Calculate Optimal F (Ralph Vince method)
        
        Args:
            trades: List of trade P&Ls
            initial_capital: Initial capital
            
        Returns:
            Optimal F fraction
        """
        if not trades:
            return 0.0
            
        # Find largest loss
        largest_loss = abs(min(trades))
        
        if largest_loss == 0:
            return 0.0
        
        # Calculate TWR for different f values
        best_f = 0.0
        best_twr = 0.0
        
        for f in np.arange(0.01, 1.0, 0.01):
            twr = 1.0
            for trade in trades:
                hpr = 1 + (f * trade / largest_loss)
                twr *= hpr
            
            if twr > best_twr:
                best_twr = twr
                best_f = f
        
        # Apply safety factor (typically 50% of optimal)
        return best_f * 0.5
    
    @staticmethod
    def risk_parity(
        assets: List[str],
        volatilities: Dict[str, float],
        total_capital: float
    ) -> Dict[str, float]:
        """
        Calculate risk parity allocation
        
        Args:
            assets: List of asset symbols
            volatilities: Dictionary of asset volatilities
            total_capital: Total capital to allocate
            
        Returns:
            Dictionary of asset allocations
        """
        # Calculate inverse volatility weights
        inv_vols = {asset: 1/volatilities[asset] for asset in assets if volatilities[asset] > 0}
        total_inv_vol = sum(inv_vols.values())
        
        # Normalize to get weights
        weights = {asset: inv_vol/total_inv_vol for asset, inv_vol in inv_vols.items()}
        
        # Calculate dollar allocations
        allocations = {asset: weight * total_capital for asset, weight in weights.items()}
        
        return allocations
