import logging
import pandas as pd

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine

from app.config import DATABASE_URL


logger = logging.getLogger(__name__)


if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL environment variable is not set.")


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


def save_to_postgres(
    df: pd.DataFrame,
    table_name: str = "market_prices",
    db_engine: Engine = engine,
) -> None:
    """Save market data to a PostgreSQL table.

    Duplicate records are ignored using the table primary key.

    Args:
        df: Clean market data to save.
        table_name: Name of the target PostgreSQL table.
        db_engine: SQLAlchemy database engine.

    Raises:
        ValueError: If the DataFrame is empty or missing required columns.
        RuntimeError: If saving data to PostgreSQL fails.
    """
    required_columns = [
        "timestamp",
        "ticker",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    if df is None or df.empty:
        raise ValueError("Cannot save empty DataFrame to PostgreSQL.")

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    try:
        logger.info("Loading %d rows into PostgreSQL", len(df))
        
        df_to_save = df[required_columns].copy()
        records = df_to_save.to_dict(orient="records")

        if not records:
            logger.warning("No records to save to PostgreSQL.")
            return

        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=db_engine)

        statement = insert(table).values(records)
        statement = statement.on_conflict_do_nothing(
            index_elements=["timestamp", "ticker"]
        )

        with db_engine.begin() as conn:
            result = conn.execute(statement)

        logger.info(
            "Inserted %s new rows into table '%s'.",
            result.rowcount,
            table_name,
        )

    except Exception as exc:
        logger.exception("Failed to save market data to PostgreSQL.")
        raise RuntimeError("Failed to save market data to PostgreSQL.") from exc