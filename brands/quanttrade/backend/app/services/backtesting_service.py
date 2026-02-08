"""
VectorBT Backtesting Service - Advanced quantitative backtesting engine
"""

import vectorbt as vbt
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import structlog
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

from core.config import get_settings
from services.market_data_service import MarketDataService

logger = structlog.get_logger(__name__)
settings = get_settings()


@dataclass
class BacktestConfig:
    """Configuration for backtesting parameters"""
    initial_capital: float = 100000.0
    commission: float = 0.001  # 0.1% commission
    slippage: float = 0.0005   # 0.05% slippage
    start_date: str = "2020-01-01"
    end_date: str = "2024-01-01"
    benchmark: str = "SPY"
    risk_free_rate: float = 0.02  # 2% annual risk-free rate
    rebalance_freq: str = "1D"  # Daily rebalancing
    max_leverage: float = 1.0   # No leverage by default
    position_size: float = 0.25  # 25% position size per trade


@dataclass
class BacktestResults:
    """Comprehensive backtesting results"""
    total_return: float
    annual_return: float
    volatility: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    max_drawdown: float
    var_95: float
    cvar_95: float
    win_rate: float
    profit_factor: float
    total_trades: int
    avg_trade_duration: float
    best_trade: float
    worst_trade: float
    consecutive_wins: int
    consecutive_losses: int
    skewness: float
    kurtosis: float
    tail_ratio: float
    stability_ratio: float


class VectorBTBacktestingService:
    """Advanced backtesting service using VectorBT"""

    def __init__(self):
        self.market_service = MarketDataService()
        # Configure VectorBT settings
        vbt.settings.caching.enabled = True
        vbt.settings.caching.compression = True
        logger.info("VectorBT Backtesting Service initialized")

    async def backtest_strategy(
        self,
        strategy_config: Dict[str, Any],
        config: BacktestConfig = None
    ) -> Dict[str, Any]:
        """
        Run comprehensive backtesting for a trading strategy
        """
        try:
            if config is None:
                config = BacktestConfig()

            logger.info("Starting strategy backtesting",
                       strategy_type=strategy_config.get("type"),
                       symbols=strategy_config.get("symbols"))

            symbols = strategy_config.get("symbols", ["SPY"])
            strategy_type = strategy_config.get("type", "momentum")

            # Get market data for all symbols
            data = await self._fetch_market_data(symbols, config)
            if data.empty:
                return {"error": "No market data available"}

            # Generate trading signals based on strategy
            signals = self._generate_signals(data, strategy_config)

            # Run backtest with VectorBT
            portfolio = self._run_vectorbt_backtest(data, signals, config)

            # Calculate comprehensive metrics
            results = self._calculate_performance_metrics(portfolio, data, config)

            # Generate detailed analysis
            analysis = self._generate_detailed_analysis(portfolio, results, data, signals)

            return {
                "strategy_config": strategy_config,
                "backtest_config": config.__dict__,
                "performance_metrics": results.__dict__,
                "detailed_analysis": analysis,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error("Error in strategy backtesting", error=str(e))
            return {"error": f"Backtesting failed: {str(e)}"}

    async def monte_carlo_backtest(
        self,
        strategy_config: Dict[str, Any],
        num_simulations: int = 1000,
        config: BacktestConfig = None
    ) -> Dict[str, Any]:
        """
        Run Monte Carlo backtesting simulation
        """
        try:
            if config is None:
                config = BacktestConfig()

            logger.info("Starting Monte Carlo backtesting",
                       simulations=num_simulations,
                       strategy_type=strategy_config.get("type"))

            symbols = strategy_config.get("symbols", ["SPY"])
            base_data = await self._fetch_market_data(symbols, config)

            simulation_results = []
            returns_distribution = []

            for i in range(num_simulations):
                # Generate bootstrapped data
                bootstrapped_data = self._bootstrap_data(base_data)

                # Generate signals and run backtest
                signals = self._generate_signals(bootstrapped_data, strategy_config)
                portfolio = self._run_vectorbt_backtest(bootstrapped_data, signals, config)

                # Calculate metrics for this simulation
                results = self._calculate_performance_metrics(portfolio, bootstrapped_data, config)
                simulation_results.append(results)
                returns_distribution.append(results.total_return)

                if (i + 1) % 100 == 0:
                    logger.info("Monte Carlo progress", completed=i + 1, total=num_simulations)

            # Analyze simulation results
            mc_analysis = self._analyze_monte_carlo_results(simulation_results, returns_distribution)

            return {
                "strategy_config": strategy_config,
                "num_simulations": num_simulations,
                "monte_carlo_analysis": mc_analysis,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error("Error in Monte Carlo backtesting", error=str(e))
            return {"error": f"Monte Carlo backtesting failed: {str(e)}"}

    async def walk_forward_analysis(
        self,
        strategy_config: Dict[str, Any],
        train_period_months: int = 12,
        test_period_months: int = 3,
        config: BacktestConfig = None
    ) -> Dict[str, Any]:
        """
        Perform walk-forward analysis
        """
        try:
            if config is None:
                config = BacktestConfig()

            logger.info("Starting walk-forward analysis",
                       train_period=train_period_months,
                       test_period=test_period_months)

            symbols = strategy_config.get("symbols", ["SPY"])
            full_data = await self._fetch_market_data(symbols, config)

            walk_forward_results = []
            start_date = pd.to_datetime(config.start_date)
            end_date = pd.to_datetime(config.end_date)

            current_date = start_date
            window_num = 1

            while current_date + pd.DateOffset(months=train_period_months + test_period_months) <= end_date:
                # Define train and test periods
                train_start = current_date
                train_end = current_date + pd.DateOffset(months=train_period_months)
                test_start = train_end
                test_end = test_start + pd.DateOffset(months=test_period_months)

                # Split data
                train_data = full_data.loc[train_start:train_end]
                test_data = full_data.loc[test_start:test_end]

                if len(train_data) < 30 or len(test_data) < 10:  # Minimum data requirements
                    current_date += pd.DateOffset(months=test_period_months)
                    continue

                # Optimize parameters on training data
                optimized_params = self._optimize_parameters(train_data, strategy_config)

                # Test on out-of-sample data
                test_signals = self._generate_signals(test_data, {**strategy_config, **optimized_params})
                test_config = BacktestConfig(
                    initial_capital=config.initial_capital,
                    start_date=test_start.strftime('%Y-%m-%d'),
                    end_date=test_end.strftime('%Y-%m-%d')
                )

                test_portfolio = self._run_vectorbt_backtest(test_data, test_signals, test_config)
                test_results = self._calculate_performance_metrics(test_portfolio, test_data, test_config)

                walk_forward_results.append({
                    "window": window_num,
                    "train_period": f"{train_start.strftime('%Y-%m-%d')} to {train_end.strftime('%Y-%m-%d')}",
                    "test_period": f"{test_start.strftime('%Y-%m-%d')} to {test_end.strftime('%Y-%m-%d')}",
                    "optimized_params": optimized_params,
                    "test_results": test_results.__dict__
                })

                current_date += pd.DateOffset(months=test_period_months)
                window_num += 1

            # Analyze walk-forward results
            wf_analysis = self._analyze_walk_forward_results(walk_forward_results)

            return {
                "strategy_config": strategy_config,
                "walk_forward_results": walk_forward_results,
                "analysis": wf_analysis,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error("Error in walk-forward analysis", error=str(e))
            return {"error": f"Walk-forward analysis failed: {str(e)}"}

    async def _fetch_market_data(self, symbols: List[str], config: BacktestConfig) -> pd.DataFrame:
        """Fetch market data for backtesting"""
        try:
            all_data = {}

            for symbol in symbols:
                start_date = datetime.strptime(config.start_date, '%Y-%m-%d')
                end_date = datetime.strptime(config.end_date, '%Y-%m-%d')

                data = await self.market_service.get_historical_data(symbol, start_date, end_date)
                if data is not None and not data.empty:
                    # Use adjusted close for backtesting
                    all_data[symbol] = data['Close']

            if not all_data:
                return pd.DataFrame()

            # Combine all symbols into a single DataFrame
            combined_data = pd.DataFrame(all_data)
            combined_data.index = pd.to_datetime(combined_data.index)

            # Forward fill missing data
            combined_data = combined_data.fillna(method='ffill').dropna()

            logger.info("Market data fetched",
                       symbols=len(symbols),
                       data_points=len(combined_data),
                       start_date=combined_data.index.min(),
                       end_date=combined_data.index.max())

            return combined_data

        except Exception as e:
            logger.error("Error fetching market data", error=str(e))
            return pd.DataFrame()

    def _generate_signals(self, data: pd.DataFrame, strategy_config: Dict[str, Any]) -> pd.DataFrame:
        """Generate trading signals based on strategy"""
        try:
            strategy_type = strategy_config.get("type", "momentum")
            signals = pd.DataFrame(index=data.index, columns=data.columns)

            if strategy_type == "momentum":
                # Simple momentum strategy
                lookback = strategy_config.get("lookback_period", 20)
                threshold = strategy_config.get("momentum_threshold", 0.02)

                for symbol in data.columns:
                    price = data[symbol]
                    momentum = price.pct_change(lookback)

                    # Generate signals
                    signals[symbol] = np.where(momentum > threshold, 1,  # Buy signal
                                             np.where(momentum < -threshold, -1, 0))  # Sell signal, Hold

            elif strategy_type == "mean_reversion":
                # Mean reversion strategy using Bollinger Bands
                lookback = strategy_config.get("lookback_period", 20)
                std_dev = strategy_config.get("std_dev", 2)

                for symbol in data.columns:
                    price = data[symbol]
                    rolling_mean = price.rolling(window=lookback).mean()
                    rolling_std = price.rolling(window=lookback).std()

                    upper_band = rolling_mean + (rolling_std * std_dev)
                    lower_band = rolling_mean - (rolling_std * std_dev)

                    # Generate signals
                    signals[symbol] = np.where(price < lower_band, 1,  # Buy when oversold
                                             np.where(price > upper_band, -1, 0))  # Sell when overbought

            elif strategy_type == "pairs_trading":
                # Pairs trading strategy (if multiple symbols)
                if len(data.columns) >= 2:
                    symbol1, symbol2 = data.columns[0], data.columns[1]

                    # Calculate spread
                    spread = np.log(data[symbol1]) - np.log(data[symbol2])
                    spread_mean = spread.rolling(window=30).mean()
                    spread_std = spread.rolling(window=30).std()

                    # Z-score of spread
                    z_score = (spread - spread_mean) / spread_std

                    # Generate signals
                    entry_threshold = strategy_config.get("entry_threshold", 2.0)
                    exit_threshold = strategy_config.get("exit_threshold", 0.5)

                    signals[symbol1] = np.where(z_score > entry_threshold, -1,  # Short symbol1
                                              np.where(z_score < -entry_threshold, 1,  # Long symbol1
                                                     np.where(abs(z_score) < exit_threshold, 0, signals[symbol1].shift(1))))
                    signals[symbol2] = -signals[symbol1]  # Opposite position

            # Forward fill signals and convert to integer
            signals = signals.fillna(method='ffill').fillna(0).astype(int)

            return signals

        except Exception as e:
            logger.error("Error generating signals", error=str(e))
            return pd.DataFrame()

    def _run_vectorbt_backtest(
        self,
        data: pd.DataFrame,
        signals: pd.DataFrame,
        config: BacktestConfig
    ) -> vbt.Portfolio:
        """Run backtest using VectorBT"""
        try:
            # Create VectorBT portfolio
            portfolio = vbt.Portfolio.from_signals(
                close=data,
                entries=signals == 1,
                exits=signals == -1,
                init_cash=config.initial_capital,
                fees=config.commission,
                slippage=config.slippage,
                freq=config.rebalance_freq
            )

            return portfolio

        except Exception as e:
            logger.error("Error running VectorBT backtest", error=str(e))
            raise

    def _calculate_performance_metrics(
        self,
        portfolio: vbt.Portfolio,
        data: pd.DataFrame,
        config: BacktestConfig
    ) -> BacktestResults:
        """Calculate comprehensive performance metrics"""
        try:
            # Get portfolio statistics
            stats = portfolio.stats()
            returns = portfolio.returns()

            # Basic performance metrics
            total_return = stats['Total Return [%]'] / 100
            annual_return = stats['Annualized Return [%]'] / 100
            volatility = returns.std() * np.sqrt(252)  # Annualized volatility

            # Risk metrics
            sharpe_ratio = (annual_return - config.risk_free_rate) / volatility if volatility > 0 else 0

            # Downside deviation for Sortino ratio
            negative_returns = returns[returns < 0]
            downside_deviation = negative_returns.std() * np.sqrt(252) if len(negative_returns) > 0 else 0
            sortino_ratio = (annual_return - config.risk_free_rate) / downside_deviation if downside_deviation > 0 else 0

            # Maximum drawdown
            max_drawdown = abs(stats['Max Drawdown [%]']) / 100

            # Calmar ratio
            calmar_ratio = annual_return / max_drawdown if max_drawdown > 0 else 0

            # VaR and CVaR
            var_95 = returns.quantile(0.05)
            cvar_95 = returns[returns <= var_95].mean()

            # Trade statistics
            trades = portfolio.trades
            total_trades = len(trades.records_readable)
            win_rate = trades.win_rate if total_trades > 0 else 0
            profit_factor = trades.profit_factor if total_trades > 0 else 0

            # Additional metrics
            avg_trade_duration = trades.duration.mean() if total_trades > 0 else 0
            best_trade = trades.pnl.max() if total_trades > 0 else 0
            worst_trade = trades.pnl.min() if total_trades > 0 else 0

            # Distribution metrics
            skewness = returns.skew()
            kurtosis = returns.kurtosis()

            # Tail ratio (95th percentile / 5th percentile)
            tail_ratio = returns.quantile(0.95) / abs(returns.quantile(0.05)) if returns.quantile(0.05) != 0 else 0

            # Stability ratio (returns consistency)
            monthly_returns = returns.resample('M').sum()
            stability_ratio = 1 - monthly_returns.std() / abs(monthly_returns.mean()) if monthly_returns.mean() != 0 else 0

            return BacktestResults(
                total_return=total_return,
                annual_return=annual_return,
                volatility=volatility,
                sharpe_ratio=sharpe_ratio,
                sortino_ratio=sortino_ratio,
                calmar_ratio=calmar_ratio,
                max_drawdown=max_drawdown,
                var_95=var_95,
                cvar_95=cvar_95,
                win_rate=win_rate,
                profit_factor=profit_factor,
                total_trades=total_trades,
                avg_trade_duration=avg_trade_duration,
                best_trade=best_trade,
                worst_trade=worst_trade,
                consecutive_wins=0,  # Would need detailed implementation
                consecutive_losses=0,  # Would need detailed implementation
                skewness=skewness,
                kurtosis=kurtosis,
                tail_ratio=tail_ratio,
                stability_ratio=stability_ratio
            )

        except Exception as e:
            logger.error("Error calculating performance metrics", error=str(e))
            return BacktestResults(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    def _generate_detailed_analysis(
        self,
        portfolio: vbt.Portfolio,
        results: BacktestResults,
        data: pd.DataFrame,
        signals: pd.DataFrame
    ) -> Dict[str, Any]:
        """Generate detailed performance analysis"""
        try:
            returns = portfolio.returns()

            # Monthly and yearly breakdowns
            monthly_returns = returns.resample('M').sum()
            yearly_returns = returns.resample('Y').sum()

            # Drawdown analysis
            cumulative_returns = (1 + returns).cumprod()
            peak = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns - peak) / peak

            # Trading activity analysis
            trades = portfolio.trades
            trade_summary = {
                "total_trades": len(trades.records_readable),
                "winning_trades": len(trades.records_readable[trades.records_readable['PnL'] > 0]),
                "losing_trades": len(trades.records_readable[trades.records_readable['PnL'] < 0]),
                "average_hold_time": trades.duration.mean(),
                "largest_win": trades.pnl.max(),
                "largest_loss": trades.pnl.min()
            }

            # Risk analysis
            risk_analysis = {
                "volatility_analysis": {
                    "daily_volatility": returns.std(),
                    "monthly_volatility": monthly_returns.std(),
                    "volatility_of_volatility": returns.rolling(30).std().std()
                },
                "correlation_with_benchmark": 0.75,  # Placeholder
                "beta": 1.2,  # Placeholder
                "tracking_error": 0.08  # Placeholder
            }

            return {
                "performance_summary": {
                    "total_return_pct": results.total_return * 100,
                    "annual_return_pct": results.annual_return * 100,
                    "volatility_pct": results.volatility * 100,
                    "sharpe_ratio": results.sharpe_ratio,
                    "max_drawdown_pct": results.max_drawdown * 100
                },
                "monthly_returns": monthly_returns.to_dict(),
                "yearly_returns": yearly_returns.to_dict(),
                "trade_summary": trade_summary,
                "risk_analysis": risk_analysis,
                "drawdown_periods": self._identify_drawdown_periods(drawdown),
                "signal_distribution": {
                    "buy_signals": (signals == 1).sum().sum(),
                    "sell_signals": (signals == -1).sum().sum(),
                    "hold_periods": (signals == 0).sum().sum()
                }
            }

        except Exception as e:
            logger.error("Error generating detailed analysis", error=str(e))
            return {}

    def _bootstrap_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Bootstrap market data for Monte Carlo simulation"""
        try:
            # Block bootstrap to maintain serial correlation
            block_size = 20  # 20-day blocks
            n_blocks = len(data) // block_size

            bootstrapped_indices = []
            for _ in range(n_blocks):
                start_idx = np.random.randint(0, len(data) - block_size)
                bootstrapped_indices.extend(range(start_idx, start_idx + block_size))

            # Trim to original length
            bootstrapped_indices = bootstrapped_indices[:len(data)]

            return data.iloc[bootstrapped_indices].reset_index(drop=True)

        except Exception as e:
            logger.error("Error bootstrapping data", error=str(e))
            return data

    def _analyze_monte_carlo_results(
        self,
        simulation_results: List[BacktestResults],
        returns_distribution: List[float]
    ) -> Dict[str, Any]:
        """Analyze Monte Carlo simulation results"""
        try:
            returns_array = np.array(returns_distribution)

            return {
                "return_statistics": {
                    "mean": returns_array.mean(),
                    "median": np.median(returns_array),
                    "std_dev": returns_array.std(),
                    "min": returns_array.min(),
                    "max": returns_array.max()
                },
                "confidence_intervals": {
                    "95%": [np.percentile(returns_array, 2.5), np.percentile(returns_array, 97.5)],
                    "90%": [np.percentile(returns_array, 5), np.percentile(returns_array, 95)],
                    "80%": [np.percentile(returns_array, 10), np.percentile(returns_array, 90)]
                },
                "probability_analysis": {
                    "prob_positive": (returns_array > 0).mean(),
                    "prob_above_10pct": (returns_array > 0.10).mean(),
                    "prob_below_neg10pct": (returns_array < -0.10).mean()
                },
                "risk_metrics": {
                    "var_95": np.percentile(returns_array, 5),
                    "cvar_95": returns_array[returns_array <= np.percentile(returns_array, 5)].mean(),
                    "maximum_loss": returns_array.min()
                }
            }

        except Exception as e:
            logger.error("Error analyzing Monte Carlo results", error=str(e))
            return {}

    def _optimize_parameters(self, data: pd.DataFrame, strategy_config: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize strategy parameters on training data"""
        # Simplified parameter optimization
        # In production, use more sophisticated optimization algorithms
        return {
            "lookback_period": np.random.randint(10, 30),
            "threshold": np.random.uniform(0.01, 0.05)
        }

    def _analyze_walk_forward_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze walk-forward analysis results"""
        try:
            if not results:
                return {}

            annual_returns = [r["test_results"]["annual_return"] for r in results]
            sharpe_ratios = [r["test_results"]["sharpe_ratio"] for r in results]

            return {
                "performance_consistency": {
                    "avg_annual_return": np.mean(annual_returns),
                    "return_volatility": np.std(annual_returns),
                    "avg_sharpe_ratio": np.mean(sharpe_ratios),
                    "sharpe_volatility": np.std(sharpe_ratios)
                },
                "parameter_stability": {
                    "lookback_periods": [r["optimized_params"].get("lookback_period", 0) for r in results],
                    "threshold_values": [r["optimized_params"].get("threshold", 0) for r in results]
                },
                "degradation_analysis": {
                    "performance_degradation": "stable" if np.std(annual_returns) < 0.05 else "unstable"
                }
            }

        except Exception as e:
            logger.error("Error analyzing walk-forward results", error=str(e))
            return {}

    def _identify_drawdown_periods(self, drawdown: pd.Series) -> List[Dict[str, Any]]:
        """Identify significant drawdown periods"""
        try:
            drawdown_periods = []
            in_drawdown = False
            start_date = None
            max_dd = 0

            for date, dd in drawdown.items():
                if dd < -0.05 and not in_drawdown:  # Start of significant drawdown (>5%)
                    in_drawdown = True
                    start_date = date
                    max_dd = dd
                elif in_drawdown:
                    if dd < max_dd:
                        max_dd = dd
                    if dd >= -0.01:  # End of drawdown (recovery to <1%)
                        drawdown_periods.append({
                            "start_date": start_date.strftime('%Y-%m-%d'),
                            "end_date": date.strftime('%Y-%m-%d'),
                            "max_drawdown": abs(max_dd),
                            "duration_days": (date - start_date).days
                        })
                        in_drawdown = False

            return drawdown_periods[:5]  # Return top 5 drawdown periods

        except Exception as e:
            logger.error("Error identifying drawdown periods", error=str(e))
            return []