import sqlite3
import pandas as pd

DB_PATH = "data/market.db"

def get_prices():
    con = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT ticker, date, close FROM prices", con, parse_dates=["date"])
    con.close()
    return df

def run_backtest(signals, initial_capital=100000, transaction_cost=0.001):
    df = get_prices()
    prices = df.pivot(index="date", columns="ticker", values="close")

    capital = initial_capital
    portfolio = {}
    equity_curve = []

    for date in sorted(signals.keys()):
        buy_tickers = signals[date]
        if not buy_tickers:
            continue

        # naechsten verfuegbaren Handelstag finden
        available = prices.index[prices.index >= date]
        if available.empty:
            continue
        trade_date = available[0]

        # verkaufe alles
        for ticker, shares in portfolio.items():
            if ticker in prices.columns:
                price = prices.loc[trade_date, ticker]
                if pd.notna(price):
                    capital += shares * float(price) * (1 - transaction_cost)
        portfolio = {}

        # kaufe gleichgewichtet
        valid_tickers = [t for t in buy_tickers if t in prices.columns and pd.notna(prices.loc[trade_date, t])]
        if not valid_tickers:
            continue

        per_ticker = capital / len(valid_tickers)
        capital = 0

        for ticker in valid_tickers:
            price = float(prices.loc[trade_date, ticker])
            shares = (per_ticker * (1 - transaction_cost)) / price
            portfolio[ticker] = shares

        # portfolio wert
        total = sum(
            portfolio[t] * float(prices.loc[trade_date, t])
            for t in portfolio
        )
        equity_curve.append({"date": trade_date, "equity": total})

    return pd.DataFrame(equity_curve)

if __name__ == "__main__":
    import sys
    sys.path.append(".")
    from strategies.momentum import momentum_signals
    signals = momentum_signals()
    equity = run_backtest(signals)
    print(equity.tail())