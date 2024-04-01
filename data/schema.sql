CREATE TABLE stocks (
    stock_id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL
);

CREATE TABLE historical_prices (
    price_id SERIAL PRIMARY KEY,
    stock_id INTEGER REFERENCES stocks(stock_id),
    date DATE NOT NULL,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    adjusted_close NUMERIC,
    volume BIGINT
);

CREATE TABLE pair_analysis (
    pair_id SERIAL PRIMARY KEY,
    stock1_id INTEGER REFERENCES stocks(stock_id),
    stock2_id INTEGER REFERENCES stocks(stock_id),
    correlation_coefficient NUMERIC,
    cointegration_p_value NUMERIC,
    mean_reversion_half_life NUMERIC,
    hurst_exponent NUMERIC,
    beta NUMERIC,
    sharpe_ratio NUMERIC,
    last_updated TIMESTAMP
);

