CREATE TABLE IF NOT EXISTS market_prices_silver (
    timestamp TIMESTAMP,
    ticker VARCHAR(20),

    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT,

    return_5m NUMERIC,
    sma20 NUMERIC,
    sma50 NUMERIC,
    volatility20 NUMERIC,

    PRIMARY KEY (timestamp, ticker)
);