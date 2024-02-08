
# Insert query for stocks table
insert_stock = """
    INSERT INTO stocks (ticker) 
    VALUES (%s) RETURNING stock_id;
    """

insert_histrical_data = """
    INSERT INTO historical_data (stock_id, date, open, high, low, close, adj_close, volume)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """

insert_pair_data = """
    INSERT INTO pair_analysis (stock1_id, stock2_id, correlation_coefficient, cointegration_p_value, mean_reversion_half_life, hurst_exponent, last_updated) 
    VALUES (%s, %s, %s, %s);
    """