import yfinance as yf
import pandas as pd
from schema import get_connection

# S&P 500 tickers von Wikipedia
def get_sp500_tickers():
    url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
    df = pd.read_csv(url)
    tickers = df["Symbol"].tolist()
    # yfinance braucht - statt . bei Tickern wie BRK.B
    tickers = [t.replace(".", "-") for t in tickers]
    return tickers

def fetch_and_store(ticker, start="2015-01-01", end="2024-01-01"):
    df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)

    if df.empty:
        print(f"No data for {ticker}")
        return

    # flatten MultiIndex columns
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    con = get_connection()
    cur = con.cursor()

    for date, row in df.iterrows():
        cur.execute("""
            INSERT OR IGNORE INTO prices (ticker, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            ticker,
            str(date.date()),
            float(row["Open"]),
            float(row["High"]),
            float(row["Low"]),
            float(row["Close"]),
            int(row["Volume"])
        ))

    con.commit()
    con.close()
    print(f"Stored {ticker}")

if __name__ == "__main__":
    tickers = get_sp500_tickers()
    print(f"Loading {len(tickers)} tickers...")
    for i, t in enumerate(tickers):
        print(f"[{i+1}/{len(tickers)}] {t}")
        fetch_and_store(t)