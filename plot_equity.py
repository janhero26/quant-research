import sys
sys.path.append(".")

import matplotlib.pyplot as plt

from strategies.momentum import momentum_signals
from strategies.mean_reversion import mean_reversion_signals
from strategies.benchmark import benchmark_signals
from strategies.low_volatility import low_volatility_signals
from backtester.engine import run_backtest

def plot():
    strategies = {
        "Benchmark": benchmark_signals,
        "Momentum": momentum_signals,
        "Mean-Reversion": mean_reversion_signals,
        "Low-Volatility": low_volatility_signals,
    }

    plt.figure(figsize=(10, 6))

    for name, signal_func in strategies.items():
        signals = signal_func()
        equity = run_backtest(signals)
        plt.plot(equity["date"], equity["equity"], label=name)

    plt.title("Equity Curves: Strategies vs Benchmark (2015-2023)")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig("equity_curves.png", dpi=120)
    print("Saved equity_curves.png")

if __name__ == "__main__":
    plot()