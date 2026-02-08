"""
Portfolio Service for QuantTrade Platform
Portfolio management and performance tracking
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np
import structlog
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.cache import get_cache, CacheKeys
from core.config import get_settings
from models.portfolio_model import Portfolio, PortfolioHistory
from models.position_model import Position, PositionStatus
from services.market_data_service import MarketDataService

logger = structlog.get_logger(__name__)
settings = get_settings()


class PortfolioService:
    """Service for portfolio management"""

    def __init__(self):
        self.cache = get_cache()
        self.market_service = MarketDataService()

    async def get_portfolio(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user's portfolio with current positions"""
        # Check cache first
        cache_key = CacheKeys.portfolio(str(user_id))
        cached_portfolio = await self.cache.get(cache_key)

        if cached_portfolio:
            logger.debug("Cache hit for portfolio", user_id=user_id)
            return cached_portfolio

        try:
            async with get_db() as db:
                # Get user's main portfolio
                stmt = select(Portfolio).where(Portfolio.user_id == user_id, Portfolio.is_active == True)
                result = await db.execute(stmt)
                portfolio = result.scalar_one_or_none()

                if not portfolio:
                    # Create default portfolio for new user
                    portfolio = await self._create_default_portfolio(db, user_id)

                # Get active positions
                positions_stmt = select(Position).where(
                    Position.portfolio_id == portfolio.id,
                    Position.status == PositionStatus.OPEN
                )
                positions_result = await db.execute(positions_stmt)
                positions = positions_result.scalars().all()

                # Update positions with current market data
                portfolio_data = await self._calculate_portfolio_value(portfolio, positions)

                # Cache for 60 seconds
                await self.cache.set(cache_key, portfolio_data, ttl=60)

                logger.info("Portfolio retrieved", user_id=user_id, value=portfolio_data['total_value'])
                return portfolio_data

        except Exception as e:
            logger.error("Failed to get portfolio", user_id=user_id, error=str(e))
            return None

    async def _create_default_portfolio(self, db: AsyncSession, user_id: int) -> Portfolio:
        """Create default portfolio for new user"""
        portfolio = Portfolio(
            user_id=user_id,
            name="Main Portfolio",
            initial_value=settings.DEFAULT_PORTFOLIO_VALUE,
            current_value=settings.DEFAULT_PORTFOLIO_VALUE,
            cash_balance=settings.DEFAULT_PORTFOLIO_VALUE
        )

        db.add(portfolio)
        await db.commit()
        await db.refresh(portfolio)

        logger.info("Default portfolio created", user_id=user_id, portfolio_id=portfolio.id)
        return portfolio

    async def _calculate_portfolio_value(
        self,
        portfolio: Portfolio,
        positions: List[Position]
    ) -> Dict[str, Any]:
        """Calculate current portfolio value and metrics"""
        total_invested = 0.0
        total_market_value = 0.0
        total_unrealized_pnl = 0.0
        day_pnl = 0.0

        position_data = []

        # Get current quotes for all symbols
        symbols = [pos.symbol for pos in positions if pos.status == PositionStatus.OPEN]
        if symbols:
            quotes = await self.market_service.get_multiple_quotes(symbols)
        else:
            quotes = {}

        for position in positions:
            if position.status != PositionStatus.OPEN:
                continue

            symbol = position.symbol
            current_price = position.current_price

            # Update with latest market data if available
            if symbol in quotes:
                quote = quotes[symbol]
                current_price = quote['price']

                # Update position in database
                position.current_price = current_price
                position.market_value = current_price * position.quantity
                position.unrealized_pnl = (current_price - position.avg_entry_price) * position.quantity
                position.unrealized_pnl_percent = (position.unrealized_pnl / (position.avg_entry_price * position.quantity)) * 100

                # Calculate day P&L (simplified - using change from quote)
                day_change = quote.get('change', 0)
                position.day_pnl = day_change * position.quantity
                position.day_pnl_percent = quote.get('change_percent', 0)

            market_value = current_price * position.quantity
            invested_value = position.avg_entry_price * position.quantity
            unrealized_pnl = market_value - invested_value

            total_invested += invested_value
            total_market_value += market_value
            total_unrealized_pnl += unrealized_pnl
            day_pnl += position.day_pnl

            position_data.append({
                'id': position.id,
                'symbol': position.symbol,
                'side': position.side,
                'quantity': position.quantity,
                'avg_price': position.avg_entry_price,
                'current_price': current_price,
                'market_value': market_value,
                'unrealized_pnl': unrealized_pnl,
                'unrealized_pnl_percent': (unrealized_pnl / invested_value) * 100 if invested_value > 0 else 0,
                'day_change': position.day_pnl,
                'day_change_percent': position.day_pnl_percent,
                'sector': position.sector,
                'stop_loss': position.stop_loss,
                'take_profit': position.take_profit,
                'entry_date': position.entry_date.isoformat() if position.entry_date else None
            })

        # Calculate portfolio totals
        total_value = portfolio.cash_balance + total_market_value
        total_return = total_value - portfolio.initial_value
        total_return_percent = (total_return / portfolio.initial_value) * 100 if portfolio.initial_value > 0 else 0

        # Calculate buying power (simplified)
        buying_power = portfolio.cash_balance * 2  # 2:1 margin ratio

        # Update portfolio in database
        portfolio.current_value = total_value
        portfolio.invested_amount = total_invested
        portfolio.total_return = total_return
        portfolio.total_return_percent = total_return_percent
        portfolio.daily_pnl = day_pnl
        portfolio.daily_pnl_percent = (day_pnl / total_value) * 100 if total_value > 0 else 0

        return {
            'id': portfolio.id,
            'name': portfolio.name,
            'total_value': total_value,
            'cash_balance': portfolio.cash_balance,
            'invested_amount': total_invested,
            'market_value': total_market_value,
            'buying_power': buying_power,
            'total_return': total_return,
            'total_return_percent': total_return_percent,
            'daily_pnl': day_pnl,
            'daily_pnl_percent': portfolio.daily_pnl_percent,
            'unrealized_pnl': total_unrealized_pnl,
            'active_positions': len([p for p in positions if p.status == PositionStatus.OPEN]),
            'positions': position_data,
            'performance_metrics': {
                'sharpe_ratio': portfolio.sharpe_ratio,
                'max_drawdown': portfolio.max_drawdown,
                'win_rate': portfolio.win_rate,
                'total_trades': portfolio.total_trades,
                'winning_trades': portfolio.winning_trades
            },
            'updated_at': datetime.now().isoformat()
        }

    async def get_positions(self, user_id: int, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get user's positions with optional status filter"""
        try:
            async with get_db() as db:
                # Get user's portfolio
                portfolio_stmt = select(Portfolio).where(
                    Portfolio.user_id == user_id,
                    Portfolio.is_active == True
                )
                portfolio_result = await db.execute(portfolio_stmt)
                portfolio = portfolio_result.scalar_one_or_none()

                if not portfolio:
                    return []

                # Build positions query
                positions_query = select(Position).where(Position.portfolio_id == portfolio.id)

                if status:
                    positions_query = positions_query.where(Position.status == status)

                positions_query = positions_query.order_by(desc(Position.created_at))

                positions_result = await db.execute(positions_query)
                positions = positions_result.scalars().all()

                # Get current quotes for open positions
                open_symbols = [pos.symbol for pos in positions if pos.status == PositionStatus.OPEN]
                quotes = {}
                if open_symbols:
                    quotes = await self.market_service.get_multiple_quotes(open_symbols)

                position_data = []
                for position in positions:
                    current_price = position.current_price

                    # Update with latest data if position is open
                    if position.status == PositionStatus.OPEN and position.symbol in quotes:
                        quote = quotes[position.symbol]
                        current_price = quote['price']

                    market_value = current_price * position.quantity
                    invested_value = position.avg_entry_price * position.quantity
                    unrealized_pnl = market_value - invested_value

                    position_data.append({
                        'id': position.id,
                        'symbol': position.symbol,
                        'side': position.side.value,
                        'status': position.status.value,
                        'quantity': position.quantity,
                        'avg_entry_price': position.avg_entry_price,
                        'current_price': current_price,
                        'market_value': market_value,
                        'unrealized_pnl': unrealized_pnl,
                        'unrealized_pnl_percent': (unrealized_pnl / invested_value) * 100 if invested_value > 0 else 0,
                        'realized_pnl': position.realized_pnl,
                        'day_pnl': position.day_pnl,
                        'day_pnl_percent': position.day_pnl_percent,
                        'stop_loss': position.stop_loss,
                        'take_profit': position.take_profit,
                        'sector': position.sector,
                        'entry_date': position.entry_date.isoformat() if position.entry_date else None,
                        'exit_date': position.exit_date.isoformat() if position.exit_date else None,
                        'holding_period_days': position.holding_period_days,
                        'created_at': position.created_at.isoformat(),
                        'updated_at': position.updated_at.isoformat() if position.updated_at else None
                    })

                logger.info("Positions retrieved", user_id=user_id, count=len(position_data))
                return position_data

        except Exception as e:
            logger.error("Failed to get positions", user_id=user_id, error=str(e))
            return []

    async def get_portfolio_history(
        self,
        user_id: int,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """Get portfolio performance history"""
        try:
            async with get_db() as db:
                # Get user's portfolio
                portfolio_stmt = select(Portfolio).where(
                    Portfolio.user_id == user_id,
                    Portfolio.is_active == True
                )
                portfolio_result = await db.execute(portfolio_stmt)
                portfolio = portfolio_result.scalar_one_or_none()

                if not portfolio:
                    return []

                # Get history
                start_date = datetime.now() - timedelta(days=days)
                history_stmt = select(PortfolioHistory).where(
                    PortfolioHistory.portfolio_id == portfolio.id,
                    PortfolioHistory.date >= start_date
                ).order_by(PortfolioHistory.date)

                history_result = await db.execute(history_stmt)
                history_records = history_result.scalars().all()

                history_data = []
                for record in history_records:
                    history_data.append({
                        'date': record.date.isoformat(),
                        'total_value': record.total_value,
                        'cash_balance': record.cash_balance,
                        'invested_amount': record.invested_amount,
                        'daily_return': record.daily_return,
                        'daily_return_percent': record.daily_return_percent,
                        'cumulative_return': record.cumulative_return,
                        'cumulative_return_percent': record.cumulative_return_percent,
                        'benchmark_return': record.benchmark_return,
                        'alpha': record.alpha
                    })

                return history_data

        except Exception as e:
            logger.error("Failed to get portfolio history", user_id=user_id, error=str(e))
            return []

    async def update_portfolio_metrics(self, portfolio_id: int) -> bool:
        """Update portfolio risk and performance metrics"""
        try:
            async with get_db() as db:
                # Get portfolio
                portfolio_stmt = select(Portfolio).where(Portfolio.id == portfolio_id)
                portfolio_result = await db.execute(portfolio_stmt)
                portfolio = portfolio_result.scalar_one_or_none()

                if not portfolio:
                    return False

                # Get historical performance data
                history_stmt = select(PortfolioHistory).where(
                    PortfolioHistory.portfolio_id == portfolio_id
                ).order_by(PortfolioHistory.date).limit(252)  # Last year

                history_result = await db.execute(history_stmt)
                history_records = history_result.scalars().all()

                if len(history_records) < 30:  # Need at least 30 days
                    return False

                # Calculate metrics
                daily_returns = [record.daily_return_percent / 100 for record in history_records]
                returns_series = pd.Series(daily_returns)

                # Sharpe Ratio (annualized)
                excess_returns = returns_series - (settings.RISK_FREE_RATE / 252)
                sharpe_ratio = np.sqrt(252) * excess_returns.mean() / returns_series.std()

                # Sortino Ratio
                negative_returns = returns_series[returns_series < 0]
                if len(negative_returns) > 0:
                    sortino_ratio = np.sqrt(252) * excess_returns.mean() / negative_returns.std()
                else:
                    sortino_ratio = sharpe_ratio

                # Maximum Drawdown
                cumulative_returns = (1 + returns_series).cumprod()
                rolling_max = cumulative_returns.expanding().max()
                drawdown = (cumulative_returns - rolling_max) / rolling_max
                max_drawdown = drawdown.min()

                # Calmar Ratio
                annual_return = returns_series.mean() * 252
                calmar_ratio = annual_return / abs(max_drawdown) if max_drawdown != 0 else 0

                # Update portfolio
                portfolio.sharpe_ratio = float(sharpe_ratio)
                portfolio.sortino_ratio = float(sortino_ratio)
                portfolio.max_drawdown = float(max_drawdown)
                portfolio.calmar_ratio = float(calmar_ratio)

                await db.commit()

                logger.info("Portfolio metrics updated", portfolio_id=portfolio_id)
                return True

        except Exception as e:
            logger.error("Failed to update portfolio metrics", portfolio_id=portfolio_id, error=str(e))
            return False

    async def create_portfolio_snapshot(self, user_id: int) -> bool:
        """Create daily portfolio snapshot for history tracking"""
        try:
            portfolio_data = await self.get_portfolio(user_id)
            if not portfolio_data:
                return False

            async with get_db() as db:
                # Check if snapshot already exists for today
                today = datetime.now().date()
                existing_stmt = select(PortfolioHistory).where(
                    PortfolioHistory.portfolio_id == portfolio_data['id'],
                    func.date(PortfolioHistory.date) == today
                )
                existing_result = await db.execute(existing_stmt)
                existing_snapshot = existing_result.scalar_one_or_none()

                if existing_snapshot:
                    # Update existing snapshot
                    existing_snapshot.total_value = portfolio_data['total_value']
                    existing_snapshot.cash_balance = portfolio_data['cash_balance']
                    existing_snapshot.invested_amount = portfolio_data['invested_amount']
                    existing_snapshot.daily_return = portfolio_data['daily_pnl']
                    existing_snapshot.daily_return_percent = portfolio_data['daily_pnl_percent']
                    existing_snapshot.cumulative_return = portfolio_data['total_return']
                    existing_snapshot.cumulative_return_percent = portfolio_data['total_return_percent']
                else:
                    # Create new snapshot
                    snapshot = PortfolioHistory(
                        portfolio_id=portfolio_data['id'],
                        date=datetime.now(),
                        total_value=portfolio_data['total_value'],
                        cash_balance=portfolio_data['cash_balance'],
                        invested_amount=portfolio_data['invested_amount'],
                        daily_return=portfolio_data['daily_pnl'],
                        daily_return_percent=portfolio_data['daily_pnl_percent'],
                        cumulative_return=portfolio_data['total_return'],
                        cumulative_return_percent=portfolio_data['total_return_percent']
                    )
                    db.add(snapshot)

                await db.commit()
                logger.info("Portfolio snapshot created", user_id=user_id)
                return True

        except Exception as e:
            logger.error("Failed to create portfolio snapshot", user_id=user_id, error=str(e))
            return False