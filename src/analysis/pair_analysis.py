import logging
import sys
import pandas as pd

from ..logger import set_logger
from statsmodels.tsa.stattools import adfuller
from .data_fetcher import DataFetcher

class PairAnalysis:

    def __init__(self, tickers):
        self.logger = set_logger(__name__)
        if len(tickers) < 2:
            self.logger.error("Not enough tickers provided")
            print("\nPlease provide at least two tickers to analyze.")
            sys.exit(1)
        data_fetcher = DataFetcher(tickers)

        self.data = data_fetcher.fetch_data(start_date="2020-10-27", end_date="2021-10-27")
        self.logger.debug("Data loaded successfully")

    # handle errors 
    def handle_error(self, pairs_info=None):
        self.logger.error("No pairs found")
        print('\n')
        if pairs_info:
            for pair, value in pairs_info.items():
                print(f"{pair[0]}, {pair[1]}: {value:.4f}")
        sys.exit(1)
    
    def print_pairs(self, pairs, dictionary):
        for pair in pairs:
            print(f"{pair[0]}, {pair[1]}: {dictionary[pair]:.4f}")


    def calculate_spread(self, pair):
        # :param pair: A tuple containing the two stock symbols.

        self.logger.info(f"Calculating spread for {pair[0]} and {pair[1]}")
        spread = self.data[pair[0]] - self.data[pair[1]]
        return spread # return pandas series containing spread
    
    # correlation matrix calculation
    def correlation_matrix(self):
        self.logger.info("Calculating correlation matrix")
        return self.data.corr() # return pandas dataframe 

    def potential_pairs(self, threshold=0.95):
        """
        Identifies potential pairs of stocks based on the correlation matrix.

        :param threshold: The minimum correlation value to consider a pair.
        :return: A list of tuples containing the potential pairs.
        """
        self.logger.info(f"Identifying potential pairs with threshold {threshold}")

        correlation_matrix = self.correlation_matrix()
        pairs = [] # list of valid pairs
        coefficients = {} # store coefficients for each pair

        for i in range(len(correlation_matrix.columns)):
            for j in range(i):
                corr_value = abs(correlation_matrix.iloc[i, j]) # correlation coefficient
                pair = (correlation_matrix.columns[i], correlation_matrix.columns[j]) # identify pair
                coefficients[pair] = corr_value # store coefficient for pair
                
                if corr_value > threshold:
                    pairs.append(pair) # add pair to list
                    self.logger.debug(f"Pair found: {pair[0]} and {pair[1]}")
        
        if not pairs:
            self.handle_error(coefficients)
        else:
            self.print_pairs(pairs, coefficients)
            return pairs
        
    def check_cointegration(self, spread, pair):
        """
        Method to check cointegration by performing Augmented Dickey-Fuller test.
        """
        # perform the Augmented Dickey-Fuller test
        try:
            self.logger.debug(f"Performing ADF test for {pair[0]} and {pair[1]}")
            adf_result = adfuller(spread)
            return adf_result[1]
        except Exception as e:
            self.logger.error(f"Error performing ADF test for {pair[0]} and {pair[1]}: {e}")
            return None

    def cointegration_test(self):
        """
        Performs the cointegration test on the potential pairs.

        :param pairs: A list of tuples containing the potential pairs.
        :return: A pandas DataFrame containing the p-value of the cointegration test.
        """
        pairs = self.potential_pairs()
        self.logger.info(f"Performing cointegration test on {len(pairs)} pairs")

        cointegrated_pairs = []
        pairs_info= {} # dictionary storing p-values for each pair

        for pair in pairs:
            spread = self.calculate_spread(pair)
            p_value = self.check_cointegration(spread, pair)
            pairs_info[pair] = p_value # add p-value to dictionary
            
            if p_value < 0.05:
                cointegrated_pairs.append(pair)
                self.logger.debug(f"{pair[0]}, {pair[1]}: Cointegrated (p-value: {p_value:.2f})")
            else:
                self.logger.debug(f"{pair[0]}, {pair[1]}: Not cointegrated (p-value: {p_value:.2f})")
        
        if not cointegrated_pairs:
            self.handle_error(pairs_info)
        else: 
            self.print_pairs(cointegrated_pairs, pairs_info)
            return cointegrated_pairs
     