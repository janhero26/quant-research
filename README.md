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

Two strategies on the S&P 500 universe, concentrated 20-stock portfolios, monthly rebalancing (2015-2023):

| Strategy | CAGR | Sharpe | Max Drawdown |
|----------|------|--------|--------------|
| Momentum | 22.8% | 0.95 | -28.9% |
| Mean-Reversion | 14.6% | 0.58 | -49.1% |

Momentum outperforms mean-reversion on both return and risk-adjusted return, and has a much smaller drawdown. This is consistent with the academic literature: cross-sectional momentum is one of the most robust documented factors, while naive monthly mean-reversion on single stocks tends to be weak.

Portfolio concentration matters a lot here. With wide portfolios (e.g. top 20% = ~100 stocks) both strategies collapse toward the market return and become indistinguishable. The signal only shows up with concentrated portfolios.

## Known limitations

The backtest uses the *current* S&P 500 constituents applied to historical data. Stocks that were in the index during the test period but later dropped out are missing. This is a milder but real form of survivorship bias: the universe is biased toward companies that survived and stayed in the index.

Removing this fully would require point-in-time index membership data, which is not freely available. The current results should be read with this caveat in mind.

## Roadmap

- Expand universe to full S&P 500
- Handle index membership changes over time (avoid survivorship bias)
- Add a mean-reversion strategy for comparison
- Add unit tests

## Stack

Python, SQLite, yfinance, pandas