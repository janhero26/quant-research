# quant-research

Backtesting and strategy research framework for US equities.

## What it does

Loads historical price data, generates trading signals from a strategy, runs a backtest with transaction costs, and computes performance metrics. Results are stored in SQLite.

## Pipeline

1. `data/loader.py` - fetches price data via yfinance, stores it in SQLite
2. `strategies/momentum.py` - 12-month momentum signals, rebalanced monthly
3. `backtester/engine.py` - simulates trades with transaction costs
4. `metrics/performance.py` - Sharpe, CAGR, max drawdown
5. `results/store.py` - saves backtest metrics to the database

## Current results

Momentum strategy on a 10-stock universe (2015-2023):

| Metric | Value |
|--------|-------|
| CAGR | 44.5% |
| Sharpe | 1.17 |
| Max Drawdown | -44.6% |

## Known limitations

These numbers are not realistic and should not be read as a viable strategy. The current test universe is 10 hand-picked mega-cap tech stocks (AAPL, MSFT, NVDA, META, ...), all of which performed exceptionally well in this period. This is textbook survivorship bias: the result reflects the choice of universe, not the strategy.

To make the backtest meaningful, the universe needs to be the full S&P 500 as it was historically constituted, including stocks that later dropped out of the index. This is the main thing on the roadmap.

## Roadmap

- Expand universe to full S&P 500
- Handle index membership changes over time (avoid survivorship bias)
- Add a mean-reversion strategy for comparison
- Add unit tests

## Stack

Python, SQLite, yfinance, pandas