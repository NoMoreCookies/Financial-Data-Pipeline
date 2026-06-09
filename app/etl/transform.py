import pandas as pd


def prepare_data(data, tickers):
    frames = []

    for ticker in tickers:
        df = data[ticker].reset_index()

        df.columns = [
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume"
        ]

        df["ticker"] = ticker
        frames.append(df)

    result = pd.concat(frames, ignore_index=True)

    return result[
        ["timestamp", 
         "ticker", 
         "open", 
         "high", 
         "low", 
         "close", 
         "volume"]
    ]