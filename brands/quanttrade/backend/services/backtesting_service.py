"""
Backtesting Framework for Trading Strategies
Comprehensive backtesting engine with performance metrics
"""
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
import logging

from services.strategy_engine import BaseStrategy, TradingSignal

logger = logging.getLogger(__name__)


@dataclass
class BacktestConfig:
    """Backtesting configuration"""
    initial_capital: float = 100000.0
    commission: float = 0.001  # 0.1%
    slippage: float = 0.0005  # 0.05%
    start_date: datetime = None
    end_date: datetime = None
    
    def __post_init__(self):
        if self.start_date is None:
            self.start_date = datetime.now() - timedelta(days=365)
        if self.end_date is None:
            self.end_date = datetime.now()


@dataclass
class Trade:
    """Individual trade record"""
    entry_time: datetime
    exit_time: Optional[datetime] = None
    symbol: str = ""
    side: str = ""  # 'buy' or 'sell'
    entry_price: float = 0.0
    exit_price: Optional[float] = None
    quantity: float = 0.0
    commission: float = 0.0
    slippage: float = 0.0
    pnl: float = 0.0
    pnl_percent: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BacktestResult:
    """Comprehensive backtest results"""
    # Configuration
    initial_capital: float
    final_capital: float
    start_date: datetime
    end_date: datetime
    
    # Returns
    total_return: float
    total_return_percent: float
    annualized_return: float
    
    # Trade statistics
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    
    # Risk metrics
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown: float
    max_drawdown_percent: float
    volatility: float
    
    # Trade metrics
    avg_win: float
    avg_loss: float
    profit_factor: float
    avg_trade_duration: timedelta
    
    # Time series data
    equity_curve: pd.DataFrame
    trade_history: List[Trade]
    
    # Additional metrics
    calmar_ratio: float = 0.0
    recovery_factor: float = 0.0


class BacktestingEngine:
    """
    Backtesting engine for trading strategies
    Simulates historical trading with realistic execution
    """
    
    def __init__(self, config: BacktestConfig):
        """
        Initialize backtesting engine
        
        Args:
            config: Backtesting configuration
        """
        self.config = config
        self.portfolio_value = config.initial_capital
        self.cash = config.initial_capital
        self.positions: Dict[str, Dict] = {}
        self.trades: List[Trade] = []
        self.equity_curve: List[Dict] = []
        
    async def run_backtest(
        self,
        strategy: BaseStrategy,
        market_data: pd.DataFrame
    ) -> BacktestResult:
        """
        Run backtest for a strategy
        
        Args:
            strategy: Trading strategy to backtest
            market_data: Historical market data
            
        Returns:
            Backtest results
        """
        logger.info(f"Starting backtest for {strategy.name}")
        
        # Filter data by date range
        data = market_data[
            (market_data['timestamp'] >= self.config.start_date) &
            (market_data['timestamp'] <= self.config.end_date)
        ].copy()
        
        # Reset state
        self.portfolio_value = self.config.initial_capital
        self.cash = self.config.initial_capital
        self.positions = {}
        self.trades = []
        self.equity_curve = []
        
        # Iterate through historical data
        for i in range(len(data)):
            current_data = data.iloc[:i+1]
            current_row = data.iloc[i]
            
            # Update portfolio value
            self._update_portfolio_value(current_row)
            
            # Record equity
            self.equity_curve.append({
                'timestamp': current_row['timestamp'],
                'portfolio_value': self.portfolio_value,
                'cash': self.cash,
                'positions_value': self.portfolio_value - self.cash
            })
            
            # Generate signals
            if len(current_data) >= 50:  # Minimum data for indicators
                signals = await strategy.generate_signals(current_data)
                
                # Execute signals
                for signal in signals:
                    if strategy.validate_signal(signal):
                        self._execute_signal(signal, current_row, strategy)
            
            # Check for exit conditions
            self._check_exit_conditions(current_row)
        
        # Close all remaining positions
        final_row = data.iloc[-1]
        self._close_all_positions(final_row)
        
        # Calculate performance metrics
        result = self._calculate_performance()
        
        logger.info(f"Backtest complete. Final capital: ${result.final_capital:,.2f}")
        
        return result
    
    def _execute_signal(
        self,
        signal: TradingSignal,
        current_data: pd.Series,
        strategy: BaseStrategy
    ):
        """
        Execute a trading signal
        
        Args:
            signal: Trading signal
            current_data: Current market data
            strategy: Strategy instance
        """
        # Calculate position size
        stop_loss_price = signal.price * (1 - self.config.commission - 0.02)  # 2% stop loss
        position_size = strategy.calculate_position_size(
            self.cash,
            signal.price,
            stop_loss_price
        )
        
        # Apply slippage
        execution_price = signal.price * (1 + self.config.slippage if signal.side == 'buy' else 1 - self.config.slippage)
        
        # Calculate costs
        position_value = position_size * execution_price
        commission = position_value * self.config.commission
        total_cost = position_value + commission
        
        # Check if we have enough cash
        if total_cost > self.cash:
            logger.warning(f"Insufficient cash for {signal.symbol}: ${total_cost:,.2f} > ${self.cash:,.2f}")
            return
        
        # Execute trade
        if signal.side == 'buy':
            self.cash -= total_cost
            
            # Create position
            self.positions[signal.symbol] = {
                'quantity': position_size,
                'entry_price': execution_price,
                'entry_time': current_data['timestamp'],
                'stop_loss': stop_loss_price,
                'take_profit': signal.price * (1 + 0.05),  # 5% take profit
                'commission': commission,
                'signal_metadata': signal.metadata
            }
            
            logger.info(f"BUY {signal.symbol}: {position_size:.4f} @ ${execution_price:.2f}")
    
    def _check_exit_conditions(self, current_data: pd.Series):
        """
        Check exit conditions for open positions
        
        Args:
            current_data: Current market data
        """
        symbols_to_close = []
        
        for symbol, position in self.positions.items():
            if symbol == current_data.get('symbol'):
                current_price = current_data['close']
                
                # Check stop loss
                if current_price <= position['stop_loss']:
                    symbols_to_close.append((symbol, current_price, 'stop_loss'))
                
                # Check take profit
                elif current_price >= position['take_profit']:
                    symbols_to_close.append((symbol, current_price, 'take_profit'))
        
        # Close positions
        for symbol, exit_price, reason in symbols_to_close:
            self._close_position(symbol, exit_price, current_data['timestamp'], reason)
    
    def _close_position(
        self,
        symbol: str,
        exit_price: float,
        exit_time: datetime,
        reason: str = 'manual'
    ):
        """
        Close a position
        
        Args:
            symbol: Symbol to close
            exit_price: Exit price
            exit_time: Exit timestamp
            reason: Reason for closing
        """
        if symbol not in self.positions:
            return
        
        position = self.positions[symbol]
        
        # Apply slippage
        execution_price = exit_price * (1 - self.config.slippage)
        
        # Calculate P&L
        position_value = position['quantity'] * execution_price
        commission = position_value * self.config.commission
        proceeds = position_value - commission
        
        entry_cost = position['quantity'] * position['entry_price'] + position['commission']
        pnl = proceeds - entry_cost
        pnl_percent = (pnl / entry_cost) * 100
        
        # Update cash
        self.cash += proceeds
        
        # Record trade
        trade = Trade(
            entry_time=position['entry_time'],
            exit_time=exit_time,
            symbol=symbol,
            side='buy',  # We only track long positions for now
            entry_price=position['entry_price'],
            exit_price=execution_price,
            quantity=position['quantity'],
            commission=position['commission'] + commission,
            slippage=self.config.slippage * position['quantity'] * (position['entry_price'] + execution_price),
            pnl=pnl,
            pnl_percent=pnl_percent,
            metadata={'exit_reason': reason, **position['signal_metadata']}
        )
        
        self.trades.append(trade)
        
        # Remove position
        del self.positions[symbol]
        
        logger.info(f"SELL {symbol}: {position['quantity']:.4f} @ ${execution_price:.2f} | P&L: ${pnl:.2f} ({pnl_percent:.2f}%) | Reason: {reason}")
    
    def _close_all_positions(self, final_data: pd.Series):
        """
        Close all remaining positions at the end of backtest
        
        Args:
            final_data: Final market data row
        """
        symbols = list(self.positions.keys())
        for symbol in symbols:
            if symbol == final_data.get('symbol'):
                self._close_position(
                    symbol,
                    final_data['close'],
                    final_data['timestamp'],
                    'backtest_end'
                )
    
    def _update_portfolio_value(self, current_data: pd.Series):
        """
        Update portfolio value based on current prices
        
        Args:
            current_data: Current market data
        """
        positions_value = 0
        
        for symbol, position in self.positions.items():
            if symbol == current_data.get('symbol'):
                positions_value += position['quantity'] * current_data['close']
        
        self.portfolio_value = self.cash + positions_value
    
    def _calculate_performance(self) -> BacktestResult:
        """
        Calculate comprehensive performance metrics
        
        Returns:
            Backtest results
        """
        # Convert equity curve to DataFrame
        equity_df = pd.DataFrame(self.equity_curve)
        equity_df.set_index('timestamp', inplace=True)
        
        # Calculate returns
        equity_df['returns'] = equity_df['portfolio_value'].pct_change()
        
        # Basic metrics
        final_capital = self.portfolio_value
        total_return = final_capital - self.config.initial_capital
        total_return_percent = (total_return / self.config.initial_capital) * 100
        
        # Annualized return
        days = (self.config.end_date - self.config.start_date).days
        years = days / 365.25
        annualized_return = ((final_capital / self.config.initial_capital) ** (1 / years) - 1) * 100 if years > 0 else 0
        
        # Trade statistics
        total_trades = len(self.trades)
        winning_trades = sum(1 for t in self.trades if t.pnl > 0)
        losing_trades = total_trades - winning_trades
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # Win/Loss metrics
        wins = [t.pnl for t in self.trades if t.pnl > 0]
        losses = [abs(t.pnl) for t in self.trades if t.pnl < 0]
        
        avg_win = np.mean(wins) if wins else 0
        avg_loss = np.mean(losses) if losses else 0
        profit_factor = sum(wins) / sum(losses) if losses and sum(losses) > 0 else 0
        
        # Risk metrics
        returns = equity_df['returns'].dropna()
        volatility = returns.std() * np.sqrt(252) * 100  # Annualized
        
        # Sharpe Ratio (assuming 0% risk-free rate)
        sharpe_ratio = (returns.mean() / returns.std() * np.sqrt(252)) if returns.std() > 0 else 0
        
        # Sortino Ratio
        downside_returns = returns[returns < 0]
        downside_std = downside_returns.std() * np.sqrt(252)
        sortino_ratio = (returns.mean() / downside_std * np.sqrt(252)) if downside_std > 0 else 0
        
        # Maximum Drawdown
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min() * 100
        max_drawdown_value = (equity_df['portfolio_value'].max() - equity_df['portfolio_value'].min())
        
        # Average trade duration
        trade_durations = [
            (t.exit_time - t.entry_time) for t in self.trades if t.exit_time
        ]
        avg_trade_duration = np.mean([d.total_seconds() for d in trade_durations]) if trade_durations else 0
        avg_trade_duration = timedelta(seconds=avg_trade_duration)
        
        # Calmar Ratio
        calmar_ratio = (annualized_return / abs(max_drawdown)) if max_drawdown != 0 else 0
        
        # Recovery Factor
        recovery_factor = (total_return / abs(max_drawdown_value)) if max_drawdown_value != 0 else 0
        
        return BacktestResult(
            initial_capital=self.config.initial_capital,
            final_capital=final_capital,
            start_date=self.config.start_date,
            end_date=self.config.end_date,
            total_return=total_return,
            total_return_percent=total_return_percent,
            annualized_return=annualized_return,
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate=win_rate,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            max_drawdown=max_drawdown_value,
            max_drawdown_percent=max_drawdown,
            volatility=volatility,
            avg_win=avg_win,
            avg_loss=avg_loss,
            profit_factor=profit_factor,
            avg_trade_duration=avg_trade_duration,
            equity_curve=equity_df,
            trade_history=self.trades,
            calmar_ratio=calmar_ratio,
            recovery_factor=recovery_factor
        )


class PerformanceAnalyzer:
    """
    Advanced performance analysis and reporting
    """
    
    @staticmethod
    def generate_report(result: BacktestResult) -> str:
        """
        Generate human-readable performance report
        
        Args:
            result: Backtest results
            
        Returns:
            Formatted report string
        """
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║              BACKTEST PERFORMANCE REPORT                      ║
╚══════════════════════════════════════════════════════════════╝

📊 OVERVIEW
────────────────────────────────────────────────────────────────
Period: {result.start_date.strftime('%Y-%m-%d')} to {result.end_date.strftime('%Y-%m-%d')}
Initial Capital: ${result.initial_capital:,.2f}
Final Capital: ${result.final_capital:,.2f}

💰 RETURNS
────────────────────────────────────────────────────────────────
Total Return: ${result.total_return:,.2f} ({result.total_return_percent:.2f}%)
Annualized Return: {result.annualized_return:.2f}%

📈 TRADE STATISTICS
────────────────────────────────────────────────────────────────
Total Trades: {result.total_trades}
Winning Trades: {result.winning_trades}
Losing Trades: {result.losing_trades}
Win Rate: {result.win_rate:.2f}%
Average Win: ${result.avg_win:.2f}
Average Loss: ${result.avg_loss:.2f}
Profit Factor: {result.profit_factor:.2f}
Avg Trade Duration: {result.avg_trade_duration}

⚠️  RISK METRICS
────────────────────────────────────────────────────────────────
Sharpe Ratio: {result.sharpe_ratio:.2f}
Sortino Ratio: {result.sortino_ratio:.2f}
Max Drawdown: ${result.max_drawdown:,.2f} ({result.max_drawdown_percent:.2f}%)
Volatility: {result.volatility:.2f}%
Calmar Ratio: {result.calmar_ratio:.2f}
Recovery Factor: {result.recovery_factor:.2f}

════════════════════════════════════════════════════════════════
"""
        return report
    
    @staticmethod
    def calculate_monthly_returns(equity_curve: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate monthly returns
        
        Args:
            equity_curve: Equity curve DataFrame
            
        Returns:
            Monthly returns DataFrame
        """
        monthly = equity_curve['portfolio_value'].resample('M').last()
        monthly_returns = monthly.pct_change() * 100
        return monthly_returns.to_frame('return')
