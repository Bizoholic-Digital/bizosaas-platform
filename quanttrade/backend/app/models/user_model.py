"""
User Model for QuantTrade Trading Platform
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base


class User(Base):
    """User model for traders"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Profile information
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(20))

    # Trading preferences
    risk_tolerance = Column(String(20), default="moderate")  # conservative, moderate, aggressive
    investment_experience = Column(String(20), default="beginner")  # beginner, intermediate, advanced
    preferred_strategies = Column(Text)  # JSON string of preferred strategy types

    # Account settings
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)

    # Financial information
    initial_capital = Column(Float, default=100000.0)  # Starting portfolio value
    max_risk_per_trade = Column(Float, default=0.02)  # 2% max risk per trade

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))

    # Relationships
    portfolios = relationship("Portfolio", back_populates="user", cascade="all, delete-orphan")
    strategies = relationship("Strategy", back_populates="user", cascade="all, delete-orphan")
    backtests = relationship("Backtest", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"