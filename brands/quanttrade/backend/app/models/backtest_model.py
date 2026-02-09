"""
Backtesting Models for QuantTrade Platform
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base
import enum


class BacktestStatus(str, enum.Enum):
    """Backtest status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Backtest(Base):
    """Backtest configuration and results"""
    __tablename__ = "backtests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)

    # Backtest configuration
    name = Column(String(100), nullable=False)
    description = Column(Text)

    # Time period
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    duration_days = Column(Integer)

    # Initial conditions
    initial_capital = Column(Float, nullable=False, default=100000.0)
    commission_rate = Column(Float, default=0.001)  # 0.1%
    slippage = Column(Float, default=0.0005)  # 0.05%

    # Execution status
    status = Column(Enum(BacktestStatus), default=BacktestStatus.PENDING)
    progress_percent = Column(Float, default=0.0)

    # Results summary
    final_portfolio_value = Column(Float)
    total_return = Column(Float)
    total_return_percent = Column(Float)
    annualized_return = Column(Float)
    volatility = Column(Float)

    # Risk metrics
    sharpe_ratio = Column(Float)
    sortino_ratio = Column(Float)
    calmar_ratio = Column(Float)
    max_drawdown = Column(Float)
    max_drawdown_percent = Column(Float)
    var_95 = Column(Float)  # Value at Risk 95%

    # Trading statistics
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    losing_trades = Column(Integer, default=0)
    win_rate = Column(Float)
    avg_trade_return = Column(Float)
    avg_win = Column(Float)
    avg_loss = Column(Float)
    profit_factor = Column(Float)  # Gross profit / Gross loss

    # Exposure metrics
    avg_time_in_market = Column(Float)  # Percentage of time invested
    avg_position_size = Column(Float)
    max_position_size = Column(Float)

    # Benchmark comparison
    benchmark_symbol = Column(String(20), default="SPY")
    benchmark_return = Column(Float)
    alpha = Column(Float)
    beta = Column(Float)
    correlation = Column(Float)

    # Execution details
    execution_time_seconds = Column(Float)
    data_points_processed = Column(Integer)

    # Configuration snapshot (JSON)
    strategy_parameters = Column(Text)  # Strategy config at time of backtest
    backtest_parameters = Column(Text)  # Backtest-specific parameters

    # Error handling
    error_message = Column(Text)
    warnings = Column(Text)  # JSON array of warnings

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    # Relationships
    user = relationship("User", back_populates="backtests")
    strategy = relationship("Strategy", back_populates="backtests")
    trades = relationship("BacktestTrade", back_populates="backtest", cascade="all, delete-orphan")
    daily_stats = relationship("BacktestDailyStats", back_populates="backtest", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Backtest(id={self.id}, name='{self.name}', status={self.status})>"


class BacktestTrade(Base):
    """Individual trades from backtest"""
    __tablename__ = "backtest_trades"

    id = Column(Integer, primary_key=True, index=True)
    backtest_id = Column(Integer, ForeignKey("backtests.id"), nullable=False)

    # Trade details
    symbol = Column(String(20), nullable=False)
    side = Column(String(10), nullable=False)  # buy, sell
    quantity = Column(Integer, nullable=False)
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float)

    # Timing
    entry_date = Column(DateTime(timezone=True), nullable=False)
    exit_date = Column(DateTime(timezone=True))
    holding_period_days = Column(Integer)

    # Performance
    pnl = Column(Float)
    return_percent = Column(Float)
    commission_paid = Column(Float, default=0.0)
    slippage_cost = Column(Float, default=0.0)

    # Signal information
    entry_signal = Column(String(100))
    exit_signal = Column(String(100))
    signal_strength = Column(Float)

    # Risk metrics
    position_size_percent = Column(Float)
    risk_amount = Column(Float)
    risk_reward_ratio = Column(Float)

    # Market context
    market_price_at_entry = Column(Float)  # Benchmark price
    market_price_at_exit = Column(Float)
    relative_performance = Column(Float)  # vs benchmark

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    backtest = relationship("Backtest", back_populates="trades")

    def __repr__(self):
        return f"<BacktestTrade(id={self.id}, symbol='{self.symbol}', pnl={self.pnl})>"


class BacktestDailyStats(Base):
    """Daily statistics from backtest"""
    __tablename__ = "backtest_daily_stats"

    id = Column(Integer, primary_key=True, index=True)
    backtest_id = Column(Integer, ForeignKey("backtests.id"), nullable=False)

    # Date
    date = Column(DateTime(timezone=True), nullable=False, index=True)

    # Portfolio values
    portfolio_value = Column(Float, nullable=False)
    cash_balance = Column(Float, nullable=False)
    invested_amount = Column(Float, nullable=False)

    # Daily performance
    daily_pnl = Column(Float, default=0.0)
    daily_return_percent = Column(Float, default=0.0)
    cumulative_return_percent = Column(Float, default=0.0)

    # Drawdown tracking
    peak_value = Column(Float, nullable=False)
    drawdown = Column(Float, default=0.0)
    drawdown_percent = Column(Float, default=0.0)

    # Position metrics
    num_positions = Column(Integer, default=0)
    long_positions = Column(Integer, default=0)
    short_positions = Column(Integer, default=0)
    total_exposure = Column(Float, default=0.0)

    # Trading activity
    trades_opened = Column(Integer, default=0)
    trades_closed = Column(Integer, default=0)
    signals_generated = Column(Integer, default=0)

    # Risk metrics
    daily_volatility = Column(Float, default=0.0)
    var_95 = Column(Float, default=0.0)

    # Benchmark comparison
    benchmark_return = Column(Float, default=0.0)
    relative_performance = Column(Float, default=0.0)

    # Sector/asset allocation (JSON)
    sector_allocation = Column(Text)
    position_breakdown = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    backtest = relationship("Backtest", back_populates="daily_stats")

    def __repr__(self):
        return f"<BacktestDailyStats(backtest_id={self.backtest_id}, date={self.date}, value={self.portfolio_value})>"


class BacktestComparison(Base):
    """Compare multiple backtests"""
    __tablename__ = "backtest_comparisons"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String(100), nullable=False)
    description = Column(Text)

    # Backtest IDs to compare (JSON array)
    backtest_ids = Column(Text, nullable=False)

    # Comparison metrics (JSON)
    comparison_results = Column(Text)

    # Settings
    normalize_returns = Column(Boolean, default=True)
    include_benchmark = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    user = relationship("User")

    def __repr__(self):
        return f"<BacktestComparison(id={self.id}, name='{self.name}')>"