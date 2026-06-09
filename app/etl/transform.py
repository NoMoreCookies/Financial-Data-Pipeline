import logging
from typing import Sequence

import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


def prepare_data(
        data: pd.DataFrame,
        tickers: Sequence[str]
        ) -> pd.DataFrame:
    """Prepare raw market data downloaded from yfinance for database storage.

    Converts yfinance multi-ticker market data into a normalized long format:

        timestamp | ticker | open | high | low | close | volume

    Args:
        data: Raw market data returned by yfinance.download().
        tickers: Sequence of ticker symbols to extract from the raw data.

    Returns:
        A normalized pandas DataFrame ready to be saved to PostgreSQL.

    Raises:
        ValueError: If input data is empty, tickers are missing, or required columns are absent.
        RuntimeError: If data preparation fails unexpectedly.
    """
    if data is None or data.empty:
        raise ValueError("Input market data is empty.")

    if not tickers:
        raise ValueError("At least one ticker must be provided.")

    frames = []

    try:
        for ticker in tickers:
            if ticker not in data.columns.get_level_values(0):
                raise ValueError(f"Ticker '{ticker}' not found in downloaded data.")

            ticker_df = data[ticker].copy()

            missing_columns = [
                column for column in REQUIRED_COLUMNS
                if column not in ticker_df.columns
            ]

            if missing_columns:
                raise ValueError(
                    f"Ticker '{ticker}' is missing columns: {missing_columns}"
                )

            ticker_df = ticker_df[REQUIRED_COLUMNS].reset_index()

            ticker_df = ticker_df.rename(
                columns={
                    ticker_df.columns[0]: "timestamp",
                    "Open": "open",
                    "High": "high",
                    "Low": "low",
                    "Close": "close",
                    "Volume": "volume",
                }
            )

            ticker_df["ticker"] = ticker

            frames.append(ticker_df)

        result = pd.concat(frames, ignore_index=True)

        result = result[
            [
                "timestamp",
                "ticker",
                "open",
                "high",
                "low",
                "close",
                "volume",
            ]
        ]

        logger.info("Prepared %s rows of market data.", len(result))

        return result

    except Exception as exc:
        logger.exception("Failed to prepare market data.")
        raise RuntimeError("Failed to prepare market data.") from exc