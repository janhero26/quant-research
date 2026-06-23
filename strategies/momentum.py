import sqlite3
import pandas as pd

DB_PATH = "data/market.db"

def get_prices():
    con = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT ticker, date, close FROM prices", con, parse_dates=["date"])
    con.close()
    return df

def momentum_signals(lookback_months=12, top_pct=0.2):
    df = get_prices()

    # pivot: rows = dates, columns = tickers
    prices = df.pivot(index="date", columns="ticker", values="close")

    # monatliche resampling
    monthly = prices.resample("ME").last()

    # 12-Monats-Return für jeden Ticker
    returns = monthly.pct_change(lookback_months)

    # für jeden Monat: top 20% = buy, rest = ignore
    signals = {}
    for date, row in returns.iterrows():
        row = row.dropna()
        if row.empty:
            continue
        threshold = row.quantile(1 - top_pct)
        buy = row[row >= threshold].index.tolist()
        signals[date] = buy

    return signals

if __name__ == "__main__":
    signals = momentum_signals()
    for date, tickers in list(signals.items())[-3:]:
        print(f"{date.date()}: {tickers}")