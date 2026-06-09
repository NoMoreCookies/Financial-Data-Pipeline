CREATE TABLE market_prices_silver (
    timestamp TIMESTAMP,
    ticker VARCHAR(20),
    close NUMERIC,
    volume BIGINT,
    return_5m NUMERIC,
    sma20 NUMERIC,
    sma50 NUMERIC,
    volatility_20 NUMERIC,
    PRIMARY KEY (timestamp, ticker)
);