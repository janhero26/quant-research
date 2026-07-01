import sys
sys.path.append(".")

import sqlite3
from strategies.momentum import momentum_signals
from strategies.mean_reversion import mean_reversion_signals
from strategies.benchmark import benchmark_signals
from strategies.low_volatility import low_volatility_signals
from backtester.engine import run_backtest
from metrics.performance import compute_metrics

DB_PATH = "data/market.db"

def save_result(strategy, equity, metrics):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    start_date = str(equity["date"].iloc[0].date())
    end_date = str(equity["date"].iloc[-1].date())
    cur.execute("""
        INSERT INTO backtest_results (strategy, start_date, end_date, sharpe, max_drawdown, cagr)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (strategy, start_date, end_date, float(metrics["sharpe"]),
          float(metrics["max_drawdown"]), float(metrics["cagr"])))
    con.commit()
    con.close()

def main():
    strategies = {
        "benchmark": benchmark_signals,
        "momentum": momentum_signals,
        "mean_reversion": mean_reversion_signals,
        "low_volatility": low_volatility_signals,
    }

    # alte ergebnisse loeschen damit nichts doppelt drin ist
    con = sqlite3.connect(DB_PATH)
    con.execute("DELETE FROM backtest_results")
    con.commit()
    con.close()

    for name, func in strategies.items():
        signals = func()
        equity = run_backtest(signals)
        metrics = compute_metrics(equity)
        save_result(name, equity, metrics)
        print(f"Saved {name}: {metrics}")

if __name__ == "__main__":
    main()