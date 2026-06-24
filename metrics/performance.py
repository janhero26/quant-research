import numpy as np
import pandas as pd

def compute_metrics(equity_curve, periods_per_year=12):
    equity = equity_curve["equity"].values

    # periodische returns
    returns = pd.Series(equity).pct_change().dropna()

    if len(returns) == 0:
        return None

    # CAGR
    total_return = equity[-1] / equity[0]
    years = len(equity) / periods_per_year
    cagr = total_return ** (1 / years) - 1

    # Sharpe (annualisiert, risk-free rate = 0)
    sharpe = 0
    if returns.std() != 0:
        sharpe = (returns.mean() / returns.std()) * np.sqrt(periods_per_year)

    # Max Drawdown
    cumulative = pd.Series(equity)
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()

    return {
        "cagr": round(cagr, 4),
        "sharpe": round(sharpe, 4),
        "max_drawdown": round(max_drawdown, 4)
    }

if __name__ == "__main__":
    import sys
    sys.path.append(".")
    from strategies.momentum import momentum_signals
    from backtester.engine import run_backtest

    signals = momentum_signals()
    equity = run_backtest(signals)
    metrics = compute_metrics(equity)
    print(metrics)