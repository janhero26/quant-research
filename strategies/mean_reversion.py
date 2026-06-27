import sqlite3
import pandas as pd

DB_PATH = "data/market.db"

def get_prices():
    con = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT ticker, date, close FROM prices", con, parse_dates=["date"])
    con.close()
    return df

def mean_reversion_signals(lookback_months=1, n_stocks=20):
    df = get_prices()
    prices = df.pivot(index="date", columns="ticker", values="close")
    monthly = prices.resample("ME").last()
    returns = monthly.pct_change(lookback_months)

    signals = {}
    for date, row in returns.iterrows():
        row = row.dropna()
        if row.empty:
            continue
        # die n schwaechsten
        buy = row.nsmallest(n_stocks).index.tolist()
        signals[date] = buy

    return signals

if __name__ == "__main__":
    signals = mean_reversion_signals()
    for date, tickers in list(signals.items())[-3:]:
        print(f"{date.date()}: {len(tickers)} stocks")