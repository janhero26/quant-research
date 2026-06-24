import sqlite3
import sys
sys.path.append(".")

from strategies.momentum import momentum_signals
from backtester.engine import run_backtest
from metrics.performance import compute_metrics

DB_PATH = "data/market.db"

def save_result(strategy, equity_curve, metrics):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    start_date = str(equity_curve["date"].iloc[0].date())
    end_date = str(equity_curve["date"].iloc[-1].date())

    cur.execute("""
        INSERT INTO backtest_results (strategy, start_date, end_date, sharpe, max_drawdown, cagr)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        strategy,
        start_date,
        end_date,
        float(metrics["sharpe"]),
        float(metrics["max_drawdown"]),
        float(metrics["cagr"])
    ))

    con.commit()
    con.close()
    print(f"Saved result for {strategy}")

if __name__ == "__main__":
    signals = momentum_signals()
    equity = run_backtest(signals)
    metrics = compute_metrics(equity)
    save_result("momentum", equity, metrics)