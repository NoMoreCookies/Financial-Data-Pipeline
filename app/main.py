import logging

from app.config import INTERVAL, PERIOD, TICKERS
from app.etl.extract import download_market_data
from app.etl.transform import prepare_data
from app.etl.load import save_to_postgres

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


def run_pipeline() -> None:
    """Run the full market data ETL pipeline.

    The pipeline consists of three steps:
        1. Extract raw market data from Yahoo Finance.
        2. Transform raw market data into a normalized table format.
        3. Load transformed data into PostgreSQL.

    Raises:
        RuntimeError: If any pipeline step fails.
    """
    try:
        logger.info("Starting market data ETL pipeline.")

        raw_data = download_market_data(tickers=TICKERS)
        logger.info("Downloaded raw market data.")

        clean_data = prepare_data(raw_data, tickers=TICKERS)
        logger.info("Prepared market data. Rows: %s", len(clean_data))

        save_to_postgres(clean_data)

        logger.info("Market data ETL pipeline finished successfully.")

    except Exception as exc:
        logger.exception("Market data ETL pipeline failed.")
        raise RuntimeError("Market data ETL pipeline failed.") from exc


def main() -> None:
    """Entry point for running the market data ETL pipeline."""
    run_pipeline()


if __name__ == "__main__":
    main()