import sqlite3
import pandas as pd

DB_PATH = "data/market.db"

def get_prices():
    con = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT ticker, date, close FROM prices", con, parse_dates=["date"])
    con.close()
    return df

def low_volatility_signals(lookback_months=6, n_stocks=20):
    df = get_prices()
    prices = df.pivot(index="date", columns="ticker", values="close")

    # taegliche returns
    daily_returns = prices.pct_change()

    # monatliche resampling der preise (fuer die rebalancing-termine)
    monthly = prices.resample("ME").last()

    signals = {}
    lookback_days = lookback_months * 21  # ca 21 handelstage pro monat

    for date in monthly.index:
        # fenster der letzten N tage vor dem rebalancing
        window = daily_returns.loc[:date].tail(lookback_days)
        if len(window) < lookback_days // 2:
            continue

        # standardabweichung pro aktie
        vol = window.std()
        vol = vol.dropna()
        if vol.empty:
            continue

        # die n mit der niedrigsten vola
        buy = vol.nsmallest(n_stocks).index.tolist()
        signals[date] = buy

    return signals

if __name__ == "__main__":
    signals = low_volatility_signals()
    last_date = list(signals.keys())[-1]
    print(f"{last_date.date()}: {signals[last_date][:10]}")