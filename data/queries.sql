INSERT INTO stocks (ticker) 
VALUES (%s) ON CONFLICT (ticker) DO NOTHING;

INSERT INTO historical_data (stock_id, date, open, high, low, close, adj_close, volume)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);

INSERT INTO pair_analysis (stock1_id, stock2_id, correlation_coefficient, cointegration_p_value, mean_reversion_half_life, hurst_exponent, last_updated) 
VALUES (%s, %s, %s, %s);