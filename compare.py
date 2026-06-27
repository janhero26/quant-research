import sys
sys.path.append(".")

from strategies.momentum import momentum_signals
from strategies.mean_reversion import mean_reversion_signals
from backtester.engine import run_backtest
from metrics.performance import compute_metrics

def compare():
    strategies = {
        "momentum": momentum_signals,
        "mean_reversion": mean_reversion_signals,
    }

    results = {}
    for name, signal_func in strategies.items():
        signals = signal_func()
        equity = run_backtest(signals)
        metrics = compute_metrics(equity)
        results[name] = metrics

    # tabelle ausgeben
    print(f"\n{'Strategy':<16} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8}")
    print("-" * 42)
    for name, m in results.items():
        print(f"{name:<16} {m['cagr']:>8.2%} {m['sharpe']:>8.2f} {m['max_drawdown']:>8.2%}")

if __name__ == "__main__":
    compare()