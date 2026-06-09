import yfinance as yf
import logging

from typing import Sequence
import pandas as pd
from app.config import TICKERS

logger = logging.getLogger(__name__)




def download_market_data(\
        tickers: Sequence[str] = TICKERS,
        period: str = "1d",
        interval: str="5m",
        timeout: int = 10,
        ) -> pd.DataFrame:
    """Download market data from Yahoo Finance.

        Args:
            tickers: Ticker symbols to download, e.g. ["AAPL", "NVDA"].
            period: Download period, e.g. "1d", "5d", "1mo".
            interval: Data interval, e.g. "5m", "1h", "1d".
            timeout: Request timeout in seconds.

        Returns:
            Downloaded market data as a pandas DataFrame.

        Raises:
            ValueError: If no tickers are provided or downloaded data is empty.
            RuntimeError: If yfinance download fails.
    """
    if not tickers:
        raise ValueError("At least one ticker must be provided.")

    try:
        data = yf.download(
            tickers=list(tickers),
            period=period,
            interval=interval,
            group_by="ticker",
            auto_adjust=True,
            progress=False,
            timeout=timeout,
            threads=True,
            multi_level_index=True,
        )

    except Exception as exc:
        logger.exception("Failed to download market data.")
        raise RuntimeError("Failed to download market data.") from exc

    if data is None or data.empty:
        raise ValueError(f"No market data downloaded for tickers: {tickers}")

    return data