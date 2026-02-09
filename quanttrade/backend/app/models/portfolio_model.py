"""
Portfolio Model for QuantTrade Trading Platform
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base


class Portfolio(Base):
    """Portfolio model for tracking user's trading portfolio"""
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False, default="Main Portfolio")

    # Portfolio values
    initial_value = Column(Float, nullable=False, default=100000.0)
    current_value = Column(Float, nullable=False, default=100000.0)
    cash_balance = Column(Float, nullable=False, default=100000.0)
    invested_amount = Column(Float, default=0.0)

    # Performance metrics
    total_return = Column(Float, default=0.0)
    total_return_percent = Column(Float, default=0.0)
    daily_pnl = Column(Float, default=0.0)
    daily_pnl_percent = Column(Float, default=0.0)
    max_drawdown = Column(Float, default=0.0)
    max_drawdown_percent = Column(Float, default=0.0)

    # Risk metrics
    sharpe_ratio = Column(Float, default=0.0)
    sortino_ratio = Column(Float, default=0.0)
    calmar_ratio = Column(Float, default=0.0)
    beta = Column(Float, default=1.0)

    # Trading statistics
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    losing_trades = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)
    avg_win = Column(Float, default=0.0)
    avg_loss = Column(Float, default=0.0)
    profit_factor = Column(Float, default=0.0)

    # Settings
    is_active = Column(Boolean, default=True)
    is_paper_trading = Column(Boolean, default=True)
    auto_rebalance = Column(Boolean, default=False)

    # Portfolio type and strategy
    portfolio_type = Column(String(50), default="diversified")  # aggressive, conservative, diversified
    strategy_allocation = Column(Text)  # JSON string of strategy allocations

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_rebalanced = Column(DateTime(timezone=True))

    # Relationships
    user = relationship("User", back_populates="portfolios")
    positions = relationship("Position", back_populates="portfolio", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Portfolio(id={self.id}, name='{self.name}', value={self.current_value})>"


class PortfolioHistory(Base):
    """Historical portfolio performance tracking"""
    __tablename__ = "portfolio_history"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)

    # Daily snapshot values
    date = Column(DateTime(timezone=True), nullable=False)
    total_value = Column(Float, nullable=False)
    cash_balance = Column(Float, nullable=False)
    invested_amount = Column(Float, nullable=False)

    # Daily performance
    daily_return = Column(Float, default=0.0)
    daily_return_percent = Column(Float, default=0.0)
    cumulative_return = Column(Float, default=0.0)
    cumulative_return_percent = Column(Float, default=0.0)

    # Benchmark comparison
    benchmark_return = Column(Float, default=0.0)  # SPY or other benchmark
    alpha = Column(Float, default=0.0)  # Excess return over benchmark

    # Risk metrics for the day
    volatility = Column(Float, default=0.0)
    value_at_risk = Column(Float, default=0.0)  # VaR 95%

    # Position counts
    long_positions = Column(Integer, default=0)
    short_positions = Column(Integer, default=0)

    # Sector/asset allocation (JSON)
    sector_allocation = Column(Text)
    asset_allocation = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    portfolio = relationship("Portfolio")

    def __repr__(self):
        return f"<PortfolioHistory(id={self.id}, date={self.date}, value={self.total_value})>"