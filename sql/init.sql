CREATE TABLE IF NOT EXISTS market_prices (

    timestamp TIMESTAMP,
    ticker VARCHAR(20),

    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,

    volume BIGINT,

    PRIMARY KEY(timestamp, ticker)
);