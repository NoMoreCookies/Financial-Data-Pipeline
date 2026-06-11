import logging
from typing import Sequence

import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


def prepare_data(
    data: pd.DataFrame,
    tickers: Sequence[str],
) -> pd.DataFrame:
    """Prepare raw market data downloaded from yfinance for database storage.

    Converts yfinance multi-ticker market data into a normalized long format:

        timestamp | ticker | open | high | low | close | volume

    Args:
        data: Raw market data returned by yfinance.download().
        tickers: Sequence of ticker symbols to extract from the raw data.

    Returns:
        A normalized and validated DataFrame ready for PostgreSQL.

    Raises:
        ValueError: If input data is invalid.
        RuntimeError: If transformation fails.
    """
    if data is None or data.empty:
        raise ValueError("Input market data is empty.")

    if not tickers:
        raise ValueError("At least one ticker must be provided.")

    frames = []

    try:
        logger.info("Starting transformation")
        
        for ticker in tickers:
            if ticker not in data.columns.get_level_values(0):
                raise ValueError(
                    f"Ticker '{ticker}' not found in downloaded data."
                )

            ticker_df = data[ticker].copy()

            missing_columns = [
                column
                for column in REQUIRED_COLUMNS
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

        # Timestamp normalization
        result["timestamp"] = (
            pd.to_datetime(
                result["timestamp"],
                utc=True,
                errors="coerce",
            )
            .dt.tz_localize(None)
        )

        # Numeric conversion
        numeric_columns = [
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]

        for column in numeric_columns:
            result[column] = pd.to_numeric(
                result[column],
                errors="coerce",
            )

        rows_before = len(result)

        # Remove null values
        result = result.dropna(
            subset=[
                "timestamp",
                "ticker",
                "open",
                "high",
                "low",
                "close",
                "volume",
            ]
        )

        # Basic market data validation
        result = result[result["volume"] >= 0]
        result = result[result["high"] >= result["low"]]

        # OHLC consistency validation
        result = result[
            (result["high"] >= result["open"])
            & (result["high"] >= result["close"])
            & (result["low"] <= result["open"])
            & (result["low"] <= result["close"])
        ]

        result["volume"] = result["volume"].astype("int64")

        rows_removed = rows_before - len(result)

        logger.info(
            "Validation removed %s invalid rows.",
            rows_removed,
        )

        logger.info(
            "Prepared %s rows of market data.",
            len(result),
        )

        return result

    except Exception as exc:
        logger.exception("Failed to prepare market data.")
        raise RuntimeError(
            "Failed to prepare market data."
        ) from exc