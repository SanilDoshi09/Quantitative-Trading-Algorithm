import logging
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from src.analysis.pair_analysis import PairAnalysis

from ..logger import set_logger

class Metrics:

    def __init__(self, spread):
        self.logger = set_logger(__name__)
        self.logger.info("Metrics initialized")

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
    
    # TODO: implement hurst exponent
        

        
        


    def run_metrics(self):

        self.logger.info("Metrics complete")