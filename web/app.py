import sqlite3
import sys
sys.path.append(".")

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from strategies.momentum import momentum_signals
from strategies.mean_reversion import mean_reversion_signals
from strategies.benchmark import benchmark_signals
from strategies.low_volatility import low_volatility_signals
from backtester.engine import run_backtest

DB_PATH = "data/market.db"

app = FastAPI()

@app.get("/api/results")
def get_results():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT strategy, start_date, end_date, sharpe, max_drawdown, cagr FROM backtest_results")
    rows = [dict(r) for r in cur.fetchall()]
    con.close()
    return rows

@app.get("/api/equity")
def get_equity():
    strategies = {
        "benchmark": benchmark_signals,
        "momentum": momentum_signals,
        "mean_reversion": mean_reversion_signals,
        "low_volatility": low_volatility_signals,
    }
    result = {}
    for name, func in strategies.items():
        equity = run_backtest(func())
        result[name] = {
            "dates": [str(d.date()) for d in equity["date"]],
            "equity": [float(e) for e in equity["equity"]],
        }
    return result

@app.get("/")
def index():
    return FileResponse("web/static/index.html")

app.mount("/static", StaticFiles(directory="web/static"), name="static")