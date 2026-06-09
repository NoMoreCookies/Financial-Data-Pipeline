import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:kacper@localhost:5432/market_data"
)

engine = create_engine(DATABASE_URL)


def save_to_postgres(df):
    df.to_sql(
        "market_prices",
        engine,
        if_exists="append",
        index=False
    )