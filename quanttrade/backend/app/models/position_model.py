"""
Position Model for QuantTrade Trading Platform
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base
import enum


class PositionSide(str, enum.Enum):
    """Position side enumeration"""
    LONG = "long"
    SHORT = "short"


class PositionStatus(str, enum.Enum):
    """Position status enumeration"""
    OPEN = "open"
    CLOSED = "closed"
    PARTIAL = "partial"


class OrderType(str, enum.Enum):
    """Order type enumeration"""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class Position(Base):
    """Position model for individual stock positions"""
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)

    # Position details
    symbol = Column(String(20), nullable=False, index=True)
    side = Column(Enum(PositionSide), nullable=False)
    status = Column(Enum(PositionStatus), default=PositionStatus.OPEN)

    # Quantity and pricing
    quantity = Column(Integer, nullable=False)
    avg_entry_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=False)
    market_value = Column(Float, nullable=False)

    # P&L calculations
    unrealized_pnl = Column(Float, default=0.0)
    unrealized_pnl_percent = Column(Float, default=0.0)
    realized_pnl = Column(Float, default=0.0)
    day_pnl = Column(Float, default=0.0)
    day_pnl_percent = Column(Float, default=0.0)

    # Risk management
    stop_loss = Column(Float)
    take_profit = Column(Float)
    trailing_stop = Column(Float)
    max_loss_percent = Column(Float, default=0.05)  # 5% max loss

    # Position metadata
    sector = Column(String(50))
    industry = Column(String(100))
    asset_class = Column(String(30), default="equity")  # equity, crypto, forex, commodity

    # Trading information
    entry_date = Column(DateTime(timezone=True), nullable=False)
    exit_date = Column(DateTime(timezone=True))
    holding_period_days = Column(Integer, default=0)

    # Strategy that opened this position
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    entry_signal = Column(String(100))  # The signal that triggered entry
    confidence_score = Column(Float)  # AI confidence in this trade

    # Commission and fees
    entry_commission = Column(Float, default=0.0)
    exit_commission = Column(Float, default=0.0)
    total_fees = Column(Float, default=0.0)

    # Risk metrics
    position_size_percent = Column(Float)  # Percentage of portfolio
    risk_amount = Column(Float)  # Amount at risk
    risk_reward_ratio = Column(Float)

    # Tags and notes
    tags = Column(Text)  # JSON array of tags
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    portfolio = relationship("Portfolio", back_populates="positions")
    strategy = relationship("Strategy", back_populates="positions")
    trades = relationship("Trade", back_populates="position", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Position(id={self.id}, symbol='{self.symbol}', side={self.side}, qty={self.quantity})>"


class Trade(Base):
    """Individual trade executions (buy/sell orders)"""
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=False)

    # Trade details
    symbol = Column(String(20), nullable=False)
    side = Column(String(10), nullable=False)  # buy, sell
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    order_type = Column(Enum(OrderType), default=OrderType.MARKET)

    # Execution details
    executed_at = Column(DateTime(timezone=True), nullable=False)
    execution_id = Column(String(100))  # Broker execution ID
    commission = Column(Float, default=0.0)
    fees = Column(Float, default=0.0)

    # Order metadata
    order_id = Column(String(100))
    fill_status = Column(String(20), default="filled")  # filled, partial, rejected
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    position = relationship("Position", back_populates="trades")

    def __repr__(self):
        return f"<Trade(id={self.id}, symbol='{self.symbol}', side={self.side}, qty={self.quantity})>"


class Watchlist(Base):
    """User watchlists for tracking symbols"""
    __tablename__ = "watchlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String(100), nullable=False)
    description = Column(Text)
    is_default = Column(Boolean, default=False)

    # Watchlist settings
    auto_alerts = Column(Boolean, default=False)
    price_alerts = Column(Boolean, default=True)
    news_alerts = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User")
    items = relationship("WatchlistItem", back_populates="watchlist", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Watchlist(id={self.id}, name='{self.name}', user_id={self.user_id})>"


class WatchlistItem(Base):
    """Individual items in a watchlist"""
    __tablename__ = "watchlist_items"

    id = Column(Integer, primary_key=True, index=True)
    watchlist_id = Column(Integer, ForeignKey("watchlists.id"), nullable=False)

    symbol = Column(String(20), nullable=False)
    added_price = Column(Float)  # Price when added to watchlist
    target_price = Column(Float)  # Target price for alerts
    stop_price = Column(Float)  # Stop price for alerts

    # Alert settings
    price_alerts_enabled = Column(Boolean, default=True)
    volume_alerts_enabled = Column(Boolean, default=False)
    news_alerts_enabled = Column(Boolean, default=True)

    # Notes and tags
    notes = Column(Text)
    tags = Column(Text)  # JSON array

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    watchlist = relationship("Watchlist", back_populates="items")

    def __repr__(self):
        return f"<WatchlistItem(id={self.id}, symbol='{self.symbol}')>"