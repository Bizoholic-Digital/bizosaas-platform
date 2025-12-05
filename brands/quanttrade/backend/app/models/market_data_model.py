"""
Market Data Models for QuantTrade Trading Platform
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, Index
from sqlalchemy.sql import func
from core.database import Base


class MarketData(Base):
    """Real-time and historical market data"""
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)

    # Symbol information
    symbol = Column(String(20), nullable=False, index=True)
    exchange = Column(String(20))
    asset_type = Column(String(20), default="stock")  # stock, etf, crypto, forex

    # Price data
    open_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    volume = Column(Integer, default=0)

    # Adjusted data
    adj_close = Column(Float)
    dividend_amount = Column(Float, default=0.0)
    split_coefficient = Column(Float, default=1.0)

    # Calculated indicators
    sma_20 = Column(Float)  # 20-day Simple Moving Average
    sma_50 = Column(Float)  # 50-day Simple Moving Average
    ema_12 = Column(Float)  # 12-day Exponential Moving Average
    ema_26 = Column(Float)  # 26-day Exponential Moving Average
    rsi_14 = Column(Float)  # 14-day RSI
    macd = Column(Float)    # MACD line
    macd_signal = Column(Float)  # MACD signal line
    bb_upper = Column(Float)  # Bollinger Band upper
    bb_lower = Column(Float)  # Bollinger Band lower
    atr_14 = Column(Float)   # Average True Range

    # Time information
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    timeframe = Column(String(10), default="1d")  # 1m, 5m, 15m, 1h, 4h, 1d, 1w

    # Data source and quality
    source = Column(String(50), default="yfinance")
    quality_score = Column(Float, default=1.0)  # Data quality indicator

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Indexes for performance
    __table_args__ = (
        Index('idx_symbol_date', 'symbol', 'date'),
        Index('idx_symbol_timeframe', 'symbol', 'timeframe'),
        Index('idx_date_timeframe', 'date', 'timeframe'),
    )

    def __repr__(self):
        return f"<MarketData(symbol='{self.symbol}', date={self.date}, close={self.close_price})>"


class CompanyInfo(Base):
    """Company fundamental information"""
    __tablename__ = "company_info"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), unique=True, nullable=False, index=True)

    # Basic company info
    company_name = Column(String(200), nullable=False)
    sector = Column(String(100))
    industry = Column(String(100))
    country = Column(String(50))
    website = Column(String(200))
    description = Column(Text)

    # Market data
    market_cap = Column(Float)
    enterprise_value = Column(Float)
    shares_outstanding = Column(Integer)
    float_shares = Column(Integer)

    # Financial ratios
    pe_ratio = Column(Float)
    peg_ratio = Column(Float)
    price_to_book = Column(Float)
    price_to_sales = Column(Float)
    ev_to_revenue = Column(Float)
    ev_to_ebitda = Column(Float)

    # Profitability
    profit_margin = Column(Float)
    operating_margin = Column(Float)
    gross_margin = Column(Float)
    return_on_equity = Column(Float)
    return_on_assets = Column(Float)

    # Financial health
    debt_to_equity = Column(Float)
    current_ratio = Column(Float)
    quick_ratio = Column(Float)
    cash_per_share = Column(Float)

    # Dividend info
    dividend_yield = Column(Float)
    payout_ratio = Column(Float)
    dividend_date = Column(DateTime(timezone=True))
    ex_dividend_date = Column(DateTime(timezone=True))

    # Growth metrics
    revenue_growth = Column(Float)
    earnings_growth = Column(Float)
    eps_growth = Column(Float)

    # Analyst data
    analyst_rating = Column(String(20))  # Strong Buy, Buy, Hold, Sell, Strong Sell
    price_target = Column(Float)
    num_analysts = Column(Integer)

    # 52-week data
    week_52_high = Column(Float)
    week_52_low = Column(Float)
    week_52_change = Column(Float)

    # Beta and volatility
    beta = Column(Float)
    volatility = Column(Float)  # 30-day historical volatility

    # Last update
    last_updated = Column(DateTime(timezone=True), nullable=False)
    data_source = Column(String(50), default="yfinance")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<CompanyInfo(symbol='{self.symbol}', name='{self.company_name}')>"


class EconomicIndicator(Base):
    """Economic indicators and macro data"""
    __tablename__ = "economic_indicators"

    id = Column(Integer, primary_key=True, index=True)

    # Indicator information
    indicator_name = Column(String(100), nullable=False, index=True)
    indicator_code = Column(String(50), unique=True, nullable=False)
    category = Column(String(50))  # interest_rates, inflation, employment, gdp, etc.

    # Data
    value = Column(Float, nullable=False)
    previous_value = Column(Float)
    change = Column(Float)
    change_percent = Column(Float)

    # Time information
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    frequency = Column(String(20))  # daily, weekly, monthly, quarterly, annually
    release_date = Column(DateTime(timezone=True))

    # Data source
    source = Column(String(50), default="fred")
    unit = Column(String(50))
    seasonally_adjusted = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Indexes
    __table_args__ = (
        Index('idx_indicator_date', 'indicator_code', 'date'),
    )

    def __repr__(self):
        return f"<EconomicIndicator(name='{self.indicator_name}', date={self.date}, value={self.value})>"


class NewsSentiment(Base):
    """News sentiment analysis for stocks"""
    __tablename__ = "news_sentiment"

    id = Column(Integer, primary_key=True, index=True)

    # Symbol and time
    symbol = Column(String(20), nullable=False, index=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)

    # News data
    headline = Column(Text, nullable=False)
    summary = Column(Text)
    url = Column(String(500))
    source = Column(String(100))

    # Sentiment analysis
    sentiment_score = Column(Float)  # -1.0 to 1.0
    sentiment_label = Column(String(20))  # positive, negative, neutral
    confidence = Column(Float)  # 0.0 to 1.0

    # Impact metrics
    relevance_score = Column(Float)  # How relevant to the symbol
    impact_score = Column(Float)  # Potential market impact
    keywords = Column(Text)  # JSON array of important keywords

    # Social media metrics
    social_mentions = Column(Integer, default=0)
    social_sentiment = Column(Float)

    # Timestamps
    published_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Indexes
    __table_args__ = (
        Index('idx_symbol_date', 'symbol', 'date'),
        Index('idx_sentiment_impact', 'sentiment_score', 'impact_score'),
    )

    def __repr__(self):
        return f"<NewsSentiment(symbol='{self.symbol}', sentiment={self.sentiment_score})>"