"""
Backtesting service using VectorBT
"""
import vectorbt as vbt
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class BacktestingService:
    """Service for strategy backtesting using VectorBT"""

    def __init__(self, initial_capital: float = 100000.0, commission: float = 0.001):
        self.initial_capital = initial_capital
        self.commission = commission

    async def fetch_historical_data(self,
                                    symbol: str,
                                    start_date: str,
                                    end_date: str,
                                    interval: str = "1d") -> pd.DataFrame:
        """Fetch historical price data"""
        try:
            # Download data using VectorBT's built-in data fetcher
            data = vbt.YFData.download(
                symbol,
                start=start_date,
                end=end_date,
                interval=interval
            )
            return data.get()
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            raise

    async def backtest_sma_crossover(self,
                                     symbol: str,
                                     fast_window: int = 50,
                                     slow_window: int = 200,
                                     start_date: str = None,
                                     end_date: str = None) -> Dict[str, Any]:
        """Backtest Simple Moving Average Crossover Strategy"""

        if not start_date:
            start_date = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        try:
            # Fetch data
            data = await self.fetch_historical_data(symbol, start_date, end_date)
            close = data.get('Close')

            # Calculate SMAs
            fast_sma = vbt.MA.run(close, fast_window, short_name='fast')
            slow_sma = vbt.MA.run(close, slow_window, short_name='slow')

            # Generate signals
            entries = fast_sma.ma_crossed_above(slow_sma)
            exits = fast_sma.ma_crossed_below(slow_sma)

            # Run backtest
            portfolio = vbt.Portfolio.from_signals(
                close,
                entries,
                exits,
                init_cash=self.initial_capital,
                fees=self.commission,
                freq='1D'
            )

            # Calculate metrics
            metrics = self._calculate_metrics(portfolio)

            return {
                "success": True,
                "strategy": "SMA Crossover",
                "parameters": {
                    "symbol": symbol,
                    "fast_window": fast_window,
                    "slow_window": slow_window,
                    "start_date": start_date,
                    "end_date": end_date
                },
                "metrics": metrics,
                "trades": self._format_trades(portfolio.trades.records_readable)
            }

        except Exception as e:
            logger.error(f"Backtest failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def backtest_rsi_strategy(self,
                                    symbol: str,
                                    rsi_window: int = 14,
                                    rsi_lower: int = 30,
                                    rsi_upper: int = 70,
                                    start_date: str = None,
                                    end_date: str = None) -> Dict[str, Any]:
        """Backtest RSI Mean Reversion Strategy"""

        if not start_date:
            start_date = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        try:
            # Fetch data
            data = await self.fetch_historical_data(symbol, start_date, end_date)
            close = data.get('Close')

            # Calculate RSI
            rsi = vbt.RSI.run(close, window=rsi_window)

            # Generate signals
            entries = rsi.rsi_below(rsi_lower)
            exits = rsi.rsi_above(rsi_upper)

            # Run backtest
            portfolio = vbt.Portfolio.from_signals(
                close,
                entries,
                exits,
                init_cash=self.initial_capital,
                fees=self.commission,
                freq='1D'
            )

            # Calculate metrics
            metrics = self._calculate_metrics(portfolio)

            return {
                "success": True,
                "strategy": "RSI Mean Reversion",
                "parameters": {
                    "symbol": symbol,
                    "rsi_window": rsi_window,
                    "rsi_lower": rsi_lower,
                    "rsi_upper": rsi_upper,
                    "start_date": start_date,
                    "end_date": end_date
                },
                "metrics": metrics,
                "trades": self._format_trades(portfolio.trades.records_readable)
            }

        except Exception as e:
            logger.error(f"Backtest failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def backtest_custom_strategy(self,
                                       symbol: str,
                                       entries: pd.Series,
                                       exits: pd.Series,
                                       start_date: str,
                                       end_date: str) -> Dict[str, Any]:
        """Backtest custom strategy with provided signals"""

        try:
            # Fetch data
            data = await self.fetch_historical_data(symbol, start_date, end_date)
            close = data.get('Close')

            # Run backtest
            portfolio = vbt.Portfolio.from_signals(
                close,
                entries,
                exits,
                init_cash=self.initial_capital,
                fees=self.commission,
                freq='1D'
            )

            # Calculate metrics
            metrics = self._calculate_metrics(portfolio)

            return {
                "success": True,
                "strategy": "Custom Strategy",
                "parameters": {
                    "symbol": symbol,
                    "start_date": start_date,
                    "end_date": end_date
                },
                "metrics": metrics,
                "trades": self._format_trades(portfolio.trades.records_readable)
            }

        except Exception as e:
            logger.error(f"Backtest failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _calculate_metrics(self, portfolio: vbt.Portfolio) -> Dict[str, Any]:
        """Calculate comprehensive performance metrics"""

        stats = portfolio.stats()

        return {
            "total_return": float(portfolio.total_return() * 100),
            "annualized_return": float(portfolio.annualized_return() * 100),
            "sharpe_ratio": float(portfolio.sharpe_ratio()),
            "sortino_ratio": float(portfolio.sortino_ratio()),
            "calmar_ratio": float(portfolio.calmar_ratio()),
            "max_drawdown": float(portfolio.max_drawdown() * 100),
            "win_rate": float(portfolio.trades.win_rate * 100),
            "profit_factor": float(portfolio.trades.profit_factor),
            "total_trades": int(portfolio.trades.count()),
            "winning_trades": int((portfolio.trades.returns > 0).sum()),
            "losing_trades": int((portfolio.trades.returns < 0).sum()),
            "avg_win": float(portfolio.trades.winning.returns.mean() * 100) if portfolio.trades.count() > 0 else 0,
            "avg_loss": float(portfolio.trades.losing.returns.mean() * 100) if portfolio.trades.count() > 0 else 0,
            "largest_win": float(portfolio.trades.winning.returns.max() * 100) if portfolio.trades.count() > 0 else 0,
            "largest_loss": float(portfolio.trades.losing.returns.min() * 100) if portfolio.trades.count() > 0 else 0,
            "avg_holding_period": float(portfolio.trades.duration.mean()),
            "final_value": float(portfolio.final_value()),
            "total_return_dollars": float(portfolio.final_value() - self.initial_capital)
        }

    def _format_trades(self, trades_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Format trades for API response"""
        if trades_df.empty:
            return []

        trades = []
        for _, trade in trades_df.iterrows():
            trades.append({
                "entry_date": str(trade.get('Entry Date', '')),
                "exit_date": str(trade.get('Exit Date', '')),
                "entry_price": float(trade.get('Entry Price', 0)),
                "exit_price": float(trade.get('Exit Price', 0)),
                "return_pct": float(trade.get('Return', 0) * 100),
                "pnl": float(trade.get('PnL', 0)),
                "size": float(trade.get('Size', 0)),
                "duration": int(trade.get('Duration', 0))
            })

        return trades[:50]  # Return last 50 trades

    async def optimize_strategy(self,
                               symbol: str,
                               strategy_type: str,
                               param_ranges: Dict[str, List],
                               start_date: str,
                               end_date: str) -> Dict[str, Any]:
        """Optimize strategy parameters"""

        try:
            # Fetch data
            data = await self.fetch_historical_data(symbol, start_date, end_date)
            close = data.get('Close')

            if strategy_type == "sma_crossover":
                # Create parameter grid
                fast_windows = param_ranges.get('fast_window', [10, 20, 50])
                slow_windows = param_ranges.get('slow_window', [100, 150, 200])

                best_sharpe = -np.inf
                best_params = {}
                results = []

                for fast_w in fast_windows:
                    for slow_w in slow_windows:
                        if fast_w >= slow_w:
                            continue

                        # Calculate SMAs
                        fast_sma = vbt.MA.run(close, fast_w)
                        slow_sma = vbt.MA.run(close, slow_w)

                        # Generate signals
                        entries = fast_sma.ma_crossed_above(slow_sma)
                        exits = fast_sma.ma_crossed_below(slow_sma)

                        # Run backtest
                        portfolio = vbt.Portfolio.from_signals(
                            close,
                            entries,
                            exits,
                            init_cash=self.initial_capital,
                            fees=self.commission
                        )

                        sharpe = portfolio.sharpe_ratio()
                        total_return = portfolio.total_return()

                        results.append({
                            "fast_window": fast_w,
                            "slow_window": slow_w,
                            "sharpe_ratio": float(sharpe),
                            "total_return": float(total_return * 100)
                        })

                        if sharpe > best_sharpe:
                            best_sharpe = sharpe
                            best_params = {
                                "fast_window": fast_w,
                                "slow_window": slow_w
                            }

                return {
                    "success": True,
                    "best_parameters": best_params,
                    "best_sharpe_ratio": float(best_sharpe),
                    "optimization_results": sorted(results, key=lambda x: x['sharpe_ratio'], reverse=True)
                }

            else:
                return {
                    "success": False,
                    "error": "Strategy type not supported for optimization"
                }

        except Exception as e:
            logger.error(f"Optimization failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
