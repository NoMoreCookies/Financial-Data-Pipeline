import yfinance as yf

TICKERS = ["AAPL", "NVDA", "GOOGL", "BTC-USD"]


def download_market_data(tickers=TICKERS):
    data = yf.download(
        tickers=tickers,
        period="1d",
        interval="5m",
        group_by="ticker",
        auto_adjust=True,
        progress=False
    )

    return data