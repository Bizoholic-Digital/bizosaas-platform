"""
Database models for QuantTrade trading platform
SQLAlchemy models with multi-tenant support
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, JSON, Enum as SQLEnum, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
import enum

Base = declarative_base()


class AccountType(str, enum.Enum):
    """Trading account types"""
    PAPER = "paper"
    LIVE = "live"


class OrderSide(str, enum.Enum):
    """Order side"""
    BUY = "buy"
    SELL = "sell"


class OrderType(str, enum.Enum):
    """Order types"""
    MARKET = "market"
    LIMIT = "limit"
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"


class OrderStatus(str, enum.Enum):
    """Order status"""
    PENDING = "pending"
    OPEN = "open"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class StrategyStatus(str, enum.Enum):
    """Strategy status"""
    ACTIVE = "active"
    PAUSED = "paused"
    STOPPED = "stopped"
    BACKTESTING = "backtesting"


class TradingAccount(Base):
    """
    Trading account model with multi-tenant support
    Supports both paper and live trading accounts
    """
    __tablename__ = "trading_accounts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Account details
    name = Column(String(255), nullable=False)
    exchange = Column(String(50), nullable=False)  # deribit, binance
    account_type = Column(SQLEnum(AccountType), default=AccountType.PAPER)
    
    # Balance tracking
    initial_balance = Column(Float, default=0.0)
    current_balance = Column(Float, default=0.0)
    available_balance = Column(Float, default=0.0)
    margin_used = Column(Float, default=0.0)
    
    # Performance metrics
    total_pnl = Column(Float, default=0.0)
    realized_pnl = Column(Float, default=0.0)
    unrealized_pnl = Column(Float, default=0.0)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    positions = relationship("Position", back_populates="account", cascade="all, delete-orphan")
    trades = relationship("Trade", back_populates="account", cascade="all, delete-orphan")
    strategies = relationship("Strategy", back_populates="account", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_trading_accounts_tenant', 'tenant_id'),
        Index('idx_trading_accounts_user', 'user_id'),
    )


class Position(Base):
    """
    Current trading positions
    Tracks open positions with real-time P&L
    """
    __tablename__ = "positions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey('trading_accounts.id'), nullable=False)
    
    # Position details
    symbol = Column(String(50), nullable=False, index=True)
    side = Column(SQLEnum(OrderSide), nullable=False)
    quantity = Column(Float, nullable=False)
    entry_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=False)
    
    # P&L tracking
    unrealized_pnl = Column(Float, default=0.0)
    unrealized_pnl_percent = Column(Float, default=0.0)
    
    # Risk metrics (for options)
    delta = Column(Float, nullable=True)
    gamma = Column(Float, nullable=True)
    theta = Column(Float, nullable=True)
    vega = Column(Float, nullable=True)
    implied_volatility = Column(Float, nullable=True)
    
    # Metadata
    opened_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    account = relationship("TradingAccount", back_populates="positions")
    
    __table_args__ = (
        Index('idx_positions_account', 'account_id'),
        Index('idx_positions_symbol', 'symbol'),
    )


class Trade(Base):
    """
    Historical trade records
    Complete trade history with execution details
    """
    __tablename__ = "trades"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey('trading_accounts.id'), nullable=False)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('strategies.id'), nullable=True)
    
    # Trade details
    symbol = Column(String(50), nullable=False, index=True)
    side = Column(SQLEnum(OrderSide), nullable=False)
    order_type = Column(SQLEnum(OrderType), nullable=False)
    quantity = Column(Float, nullable=False)
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=True)
    
    # Execution details
    exchange_order_id = Column(String(255), nullable=True)
    commission = Column(Float, default=0.0)
    slippage = Column(Float, default=0.0)
    
    # P&L
    realized_pnl = Column(Float, default=0.0)
    realized_pnl_percent = Column(Float, default=0.0)
    
    # Timestamps
    entry_time = Column(DateTime, default=datetime.utcnow)
    exit_time = Column(DateTime, nullable=True)
    
    # Status
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING)
    
    # Additional data
    metadata = Column(JSONB, nullable=True)
    
    # Relationships
    account = relationship("TradingAccount", back_populates="trades")
    strategy = relationship("Strategy", back_populates="trades")
    
    __table_args__ = (
        Index('idx_trades_account', 'account_id'),
        Index('idx_trades_strategy', 'strategy_id'),
        Index('idx_trades_symbol', 'symbol'),
        Index('idx_trades_entry_time', 'entry_time'),
    )


class Strategy(Base):
    """
    Trading strategy configurations
    Stores strategy parameters and performance
    """
    __tablename__ = "strategies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey('trading_accounts.id'), nullable=False)
    
    # Strategy details
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    strategy_type = Column(String(100), nullable=False)  # rsi_momentum, mean_reversion, etc.
    
    # Configuration
    parameters = Column(JSONB, nullable=False)  # Strategy-specific parameters
    
    # Performance metrics
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    losing_trades = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)
    total_pnl = Column(Float, default=0.0)
    sharpe_ratio = Column(Float, nullable=True)
    max_drawdown = Column(Float, nullable=True)
    
    # Status
    status = Column(SQLEnum(StrategyStatus), default=StrategyStatus.PAUSED)
    is_active = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_run_at = Column(DateTime, nullable=True)
    
    # Relationships
    account = relationship("TradingAccount", back_populates="strategies")
    trades = relationship("Trade", back_populates="strategy")
    backtest_results = relationship("BacktestResult", back_populates="strategy", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_strategies_account', 'account_id'),
        Index('idx_strategies_status', 'status'),
    )


class BacktestResult(Base):
    """
    Backtesting results storage
    Comprehensive backtest metrics and trade history
    """
    __tablename__ = "backtest_results"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('strategies.id'), nullable=False)
    
    # Backtest parameters
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    initial_capital = Column(Float, nullable=False)
    
    # Performance metrics
    final_capital = Column(Float, nullable=False)
    total_return = Column(Float, nullable=False)
    total_return_percent = Column(Float, nullable=False)
    
    # Trade statistics
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    losing_trades = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)
    
    # Risk metrics
    sharpe_ratio = Column(Float, nullable=True)
    sortino_ratio = Column(Float, nullable=True)
    max_drawdown = Column(Float, nullable=True)
    max_drawdown_percent = Column(Float, nullable=True)
    volatility = Column(Float, nullable=True)
    
    # Additional metrics
    avg_win = Column(Float, nullable=True)
    avg_loss = Column(Float, nullable=True)
    profit_factor = Column(Float, nullable=True)
    
    # Detailed results
    equity_curve = Column(JSONB, nullable=True)  # Time series of portfolio value
    trade_history = Column(JSONB, nullable=True)  # List of all trades
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    strategy = relationship("Strategy", back_populates="backtest_results")
    
    __table_args__ = (
        Index('idx_backtest_results_strategy', 'strategy_id'),
        Index('idx_backtest_results_created', 'created_at'),
    )


class MarketPattern(Base):
    """
    Market pattern storage with vector embeddings
    Uses pgvector for similarity search
    """
    __tablename__ = "market_patterns"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Pattern details
    pattern_type = Column(String(100), nullable=False)  # breakout, reversal, continuation
    symbol = Column(String(50), nullable=False)
    timeframe = Column(String(20), nullable=False)  # 1m, 5m, 1h, 1d
    
    # Pattern data
    pattern_data = Column(JSONB, nullable=False)  # OHLCV and indicators
    # pattern_vector = Column(Vector(1536), nullable=True)  # Embedding for similarity search
    
    # Performance
    success_rate = Column(Float, nullable=True)
    avg_return = Column(Float, nullable=True)
    occurrences = Column(Integer, default=1)
    
    # Metadata
    detected_at = Column(DateTime, default=datetime.utcnow)
    last_seen_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_market_patterns_tenant', 'tenant_id'),
        Index('idx_market_patterns_type', 'pattern_type'),
        Index('idx_market_patterns_symbol', 'symbol'),
    )


class RiskMetric(Base):
    """
    Historical risk metrics tracking
    Portfolio-level risk monitoring
    """
    __tablename__ = "risk_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey('trading_accounts.id'), nullable=False)
    
    # Risk metrics
    portfolio_value = Column(Float, nullable=False)
    var_95 = Column(Float, nullable=True)  # Value at Risk (95%)
    cvar_95 = Column(Float, nullable=True)  # Conditional VaR (95%)
    
    # Position metrics
    total_positions = Column(Integer, default=0)
    total_exposure = Column(Float, default=0.0)
    margin_utilization = Column(Float, default=0.0)
    
    # Greeks (for options portfolios)
    portfolio_delta = Column(Float, nullable=True)
    portfolio_gamma = Column(Float, nullable=True)
    portfolio_theta = Column(Float, nullable=True)
    portfolio_vega = Column(Float, nullable=True)
    
    # Metadata
    calculated_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_risk_metrics_account', 'account_id'),
        Index('idx_risk_metrics_calculated', 'calculated_at'),
    )
