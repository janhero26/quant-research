import sqlite3
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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

@app.get("/")
def index():
    return FileResponse("web/static/index.html")

app.mount("/static", StaticFiles(directory="web/static"), name="static")