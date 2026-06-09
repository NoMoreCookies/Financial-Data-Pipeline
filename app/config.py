import os
from typing import Tuple

from dotenv import load_dotenv

load_dotenv()


TICKERS: Tuple[str, ...] = (
    "AAPL",
    "NVDA",
    "GOOGL",
    "BTC-USD",
)

PERIOD: str = "1d"
INTERVAL: str = "5m"
DATABASE_URL: str | None = os.getenv("DATABASE_URL")


if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL environment variable is not set.")