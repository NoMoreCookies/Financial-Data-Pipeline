import os
import logging
from turtle import pd

from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.engine import Engine
from app.config import DATABASE_URL


load_dotenv()

logger = logging.getLogger(__name__)



if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping = True
)

def save_to_postgres(
        df : pd.DataFrame,
        table_name: str = "market_prices",
        db_engine: Engine = engine,
) -> None:
    """Save market data to a PostgreSQL table.

    Args:
        df: Market data to save.
        table_name: Name of the target PostgreSQL table.
        db_engine: SQLAlchemy database engine.

    Raises:
        ValueError: If the DataFrame is empty.
        RuntimeError: If saving data to PostgreSQL fails.
    """
    if df is None or df.empty:
        raise ValueError("Cannot save empty DataFrame to PostgreSQL.")

    try:
        df_to_save = df.reset_index()

        df_to_save.to_sql(
            table_name,
            db_engine,
            if_exists="append",
            index=False,
            chunksize=1000,
            method="multi",
        )

        logger.info("Saved %s rows to table '%s'.", len(df_to_save), table_name)

    except Exception as exc:
        logger.exception("Failed to save market data to PostgreSQL.")
        raise RuntimeError("Failed to save market data to PostgreSQL.") from exc