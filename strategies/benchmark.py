import sqlite3
import pandas as pd

DB_PATH = "data/market.db"

def get_prices():
    con = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT ticker, date, close FROM prices", con, parse_dates=["date"])
    con.close()
    return df

def benchmark_signals():
    df = get_prices()
    prices = df.pivot(index="date", columns="ticker", values="close")
    monthly = prices.resample("ME").last()

    # jeden monat: kaufe alle aktien die an dem tag daten haben
    signals = {}
    for date, row in monthly.iterrows():
        available = row.dropna().index.tolist()
        if available:
            signals[date] = available

    return signals

if __name__ == "__main__":
    signals = benchmark_signals()
    last_date = list(signals.keys())[-1]
    print(f"{last_date.date()}: {len(signals[last_date])} stocks")