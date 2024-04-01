import logging
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from src.analysis.pair_analysis import PairAnalysis

from ..logger import set_logger

class Metrics:

    def __init__(self, data, pair_info, spread):
        self.logger = set_logger(__name__)
        self.logger.info("Metrics initialized")

        self.data = data # set data
        self.pair_info = pair_info # set pair info
        self.spread = spread # set spread
    
    # calculate half life
    def calculate_half_life(self):
        # :param spread: A pandas series containing the spread between two stocks.
        self.logger.debug("Calculating half life")

        spread_lag = self.spread.shift(1).dropna()
        spread_lag_constant = sm.add_constant(spread_lag)
        spread_diff = self.spread.diff().dropna()

        # Convert column names to string if they are not, to avoid TypeError
        spread_lag_constant.columns = spread_lag_constant.columns.astype(str)

        # Perform linear regression
        self.logger.debug("Performing linear regression")
        lin_reg = LinearRegression()
        lin_reg.fit(spread_lag_constant, spread_diff)

        # Calculate half life
        half_life = -np.log(2) / lin_reg.coef_[1]
        self.logger.info(f"Half life calculated: {half_life}")
        return half_life
    
    @staticmethod
    def calculate_hurst_exponent(time_series):
        """
        Calculate the Hurst Exponent of a given time series.
        
        Parameters:
            time_series (pandas.Series): The time series to analyze.
        
        Returns:
            float: The Hurst Exponent.
        """
        lags = range(2, 100)
        epsilon = 1e-10  # Small constant to avoid log(0)
        tau = [np.sqrt(np.std(np.subtract(time_series[lag:], time_series[:-lag]))) for lag in lags]
        tau = [x if x > 0 else epsilon for x in tau]  # Ensure tau values are positive
        poly = np.polyfit(np.log(lags), np.log(tau), 1)
        return poly[0] * 2.0

    def calculate_pair_hurst_exponent(self):

        self.logger.debug("Calculating Hurst Exponent")
        ticker1, ticker2 = self.pair_info[0], self.pair_info[1]

        # Extract the 'Adj Close' prices for the two tickers
        log_prices1 = np.log(self.data[ticker1])
        log_prices2 = np.log(self.data[ticker2])
        
        # Ensure both series are aligned by date
        combined = pd.concat([log_prices1, log_prices2], axis=1).dropna()
        log_prices1_aligned, log_prices2_aligned = combined.iloc[:, 0], combined.iloc[:, 1]
        
        # Calculate the spread
        timeseries = log_prices1_aligned - log_prices2_aligned
        
        # Calculate Hurst Exponent
        hurst_exponent = self.calculate_hurst_exponent(timeseries)
        self.logger.info(f"The Hurst Exponent calculated: {hurst_exponent}")
        return hurst_exponent
        
        
    def run_metrics(self):

        self.logger.debug("Calculating metrics")
        self.calculate_half_life()
        self.calculate_pair_hurst_exponent()
        self.logger.info("Metrics complete")