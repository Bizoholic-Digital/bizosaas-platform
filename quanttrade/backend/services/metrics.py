"""
QuantTrade Backend - Prometheus Metrics Integration
Exposes trading metrics for Prometheus scraping
"""

from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    Summary,
    Info,
    generate_latest,
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
)
from fastapi import Response
from typing import Dict, Any
import time

# Create custom registry for QuantTrade metrics
registry = CollectorRegistry()

# ==========================================
# TRADING METRICS
# ==========================================

# Trade Execution Metrics
trades_total = Counter(
    'quanttrade_trades_total',
    'Total number of trades executed',
    ['strategy', 'side', 'symbol', 'status'],
    registry=registry
)

trade_pnl = Gauge(
    'quanttrade_trade_pnl',
    'Profit/Loss per trade',
    ['strategy', 'symbol', 'trade_id'],
    registry=registry
)

trade_execution_latency = Histogram(
    'quanttrade_trade_execution_latency_seconds',
    'Trade execution latency in seconds',
    ['exchange', 'order_type'],
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0),
    registry=registry
)

# Portfolio Metrics
portfolio_value = Gauge(
    'quanttrade_portfolio_value_usd',
    'Current portfolio value in USD',
    ['account_id'],
    registry=registry
)

portfolio_pnl_total = Gauge(
    'quanttrade_portfolio_pnl_total_usd',
    'Total portfolio P&L in USD',
    ['account_id'],
    registry=registry
)

portfolio_pnl_daily = Gauge(
    'quanttrade_portfolio_pnl_daily_usd',
    'Daily portfolio P&L in USD',
    ['account_id'],
    registry=registry
)

# Position Metrics
position_size = Gauge(
    'quanttrade_position_size',
    'Current position size',
    ['symbol', 'side'],
    registry=registry
)

position_count = Gauge(
    'quanttrade_position_count',
    'Number of open positions',
    ['account_id'],
    registry=registry
)

position_exposure = Gauge(
    'quanttrade_position_exposure_usd',
    'Total position exposure in USD',
    ['account_id', 'symbol'],
    registry=registry
)

# Strategy Metrics
strategy_performance = Gauge(
    'quanttrade_strategy_performance_pct',
    'Strategy performance percentage',
    ['strategy_name', 'timeframe'],
    registry=registry
)

strategy_win_rate = Gauge(
    'quanttrade_strategy_win_rate_pct',
    'Strategy win rate percentage',
    ['strategy_name'],
    registry=registry
)

strategy_sharpe_ratio = Gauge(
    'quanttrade_strategy_sharpe_ratio',
    'Strategy Sharpe ratio',
    ['strategy_name'],
    registry=registry
)

strategy_max_drawdown = Gauge(
    'quanttrade_strategy_max_drawdown_pct',
    'Strategy maximum drawdown percentage',
    ['strategy_name'],
    registry=registry
)

# ==========================================
# RISK METRICS
# ==========================================

risk_var = Gauge(
    'quanttrade_risk_var_usd',
    'Value at Risk in USD',
    ['account_id', 'confidence_level'],
    registry=registry
)

risk_cvar = Gauge(
    'quanttrade_risk_cvar_usd',
    'Conditional Value at Risk in USD',
    ['account_id', 'confidence_level'],
    registry=registry
)

risk_limit_usage = Gauge(
    'quanttrade_risk_limit_usage_pct',
    'Risk limit usage percentage',
    ['account_id', 'limit_type'],
    registry=registry
)

# Greeks
portfolio_delta = Gauge(
    'quanttrade_portfolio_delta',
    'Portfolio delta (options)',
    ['account_id'],
    registry=registry
)

portfolio_gamma = Gauge(
    'quanttrade_portfolio_gamma',
    'Portfolio gamma (options)',
    ['account_id'],
    registry=registry
)

portfolio_theta = Gauge(
    'quanttrade_portfolio_theta',
    'Portfolio theta (options)',
    ['account_id'],
    registry=registry
)

portfolio_vega = Gauge(
    'quanttrade_portfolio_vega',
    'Portfolio vega (options)',
    ['account_id'],
    registry=registry
)

# ==========================================
# MARKET DATA METRICS
# ==========================================

market_data_updates = Counter(
    'quanttrade_market_data_updates_total',
    'Total market data updates received',
    ['symbol', 'data_type'],
    registry=registry
)

market_data_latency = Histogram(
    'quanttrade_market_data_latency_seconds',
    'Market data update latency',
    ['exchange', 'symbol'],
    buckets=(0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0),
    registry=registry
)

websocket_connections = Gauge(
    'quanttrade_websocket_connections',
    'Number of active WebSocket connections',
    ['exchange', 'connection_type'],
    registry=registry
)

# ==========================================
# SYSTEM METRICS
# ==========================================

api_requests_total = Counter(
    'quanttrade_api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status'],
    registry=registry
)

api_request_duration = Histogram(
    'quanttrade_api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint'],
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0),
    registry=registry
)

active_strategies = Gauge(
    'quanttrade_active_strategies',
    'Number of active trading strategies',
    ['account_id'],
    registry=registry
)

ai_agent_calls = Counter(
    'quanttrade_ai_agent_calls_total',
    'Total AI agent calls',
    ['agent_name', 'status'],
    registry=registry
)

temporal_workflow_executions = Counter(
    'quanttrade_temporal_workflow_executions_total',
    'Total Temporal workflow executions',
    ['workflow_type', 'status'],
    registry=registry
)

# ==========================================
# APPLICATION INFO
# ==========================================

app_info = Info(
    'quanttrade_app',
    'QuantTrade application information',
    registry=registry
)

# Set application info
app_info.info({
    'version': '1.0.0',
    'environment': 'production',
    'platform': 'bizosaas',
})

# ==========================================
# METRICS ENDPOINT
# ==========================================

def get_metrics() -> Response:
    """
    Prometheus metrics endpoint
    Returns metrics in Prometheus format
    """
    return Response(
        content=generate_latest(registry),
        media_type=CONTENT_TYPE_LATEST
    )


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def record_trade(
    strategy: str,
    side: str,
    symbol: str,
    status: str,
    pnl: float = 0.0,
    trade_id: str = None
):
    """Record a trade execution"""
    trades_total.labels(
        strategy=strategy,
        side=side,
        symbol=symbol,
        status=status
    ).inc()
    
    if trade_id and pnl != 0.0:
        trade_pnl.labels(
            strategy=strategy,
            symbol=symbol,
            trade_id=trade_id
        ).set(pnl)


def record_trade_latency(exchange: str, order_type: str, latency: float):
    """Record trade execution latency"""
    trade_execution_latency.labels(
        exchange=exchange,
        order_type=order_type
    ).observe(latency)


def update_portfolio_metrics(
    account_id: str,
    value: float,
    total_pnl: float,
    daily_pnl: float,
    position_count_val: int
):
    """Update portfolio metrics"""
    portfolio_value.labels(account_id=account_id).set(value)
    portfolio_pnl_total.labels(account_id=account_id).set(total_pnl)
    portfolio_pnl_daily.labels(account_id=account_id).set(daily_pnl)
    position_count.labels(account_id=account_id).set(position_count_val)


def update_strategy_metrics(
    strategy_name: str,
    performance: float,
    win_rate: float,
    sharpe: float,
    max_dd: float
):
    """Update strategy performance metrics"""
    strategy_performance.labels(
        strategy_name=strategy_name,
        timeframe='all'
    ).set(performance)
    
    strategy_win_rate.labels(strategy_name=strategy_name).set(win_rate)
    strategy_sharpe_ratio.labels(strategy_name=strategy_name).set(sharpe)
    strategy_max_drawdown.labels(strategy_name=strategy_name).set(max_dd)


def update_risk_metrics(
    account_id: str,
    var_95: float,
    cvar_95: float,
    greeks: Dict[str, float] = None
):
    """Update risk metrics"""
    risk_var.labels(
        account_id=account_id,
        confidence_level='95'
    ).set(var_95)
    
    risk_cvar.labels(
        account_id=account_id,
        confidence_level='95'
    ).set(cvar_95)
    
    if greeks:
        portfolio_delta.labels(account_id=account_id).set(greeks.get('delta', 0))
        portfolio_gamma.labels(account_id=account_id).set(greeks.get('gamma', 0))
        portfolio_theta.labels(account_id=account_id).set(greeks.get('theta', 0))
        portfolio_vega.labels(account_id=account_id).set(greeks.get('vega', 0))


def record_market_data_update(symbol: str, data_type: str, latency: float = None):
    """Record market data update"""
    market_data_updates.labels(
        symbol=symbol,
        data_type=data_type
    ).inc()
    
    if latency is not None:
        market_data_latency.labels(
            exchange='deribit',  # or determine dynamically
            symbol=symbol
        ).observe(latency)


def record_api_request(method: str, endpoint: str, status: int, duration: float):
    """Record API request metrics"""
    api_requests_total.labels(
        method=method,
        endpoint=endpoint,
        status=str(status)
    ).inc()
    
    api_request_duration.labels(
        method=method,
        endpoint=endpoint
    ).observe(duration)
