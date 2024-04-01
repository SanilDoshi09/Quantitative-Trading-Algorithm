import logging
import sys
import os
import pandas as pd

from ..logger import set_logger
from statsmodels.tsa.stattools import adfuller
from src.database import queries
from src.database.db_manager import Database
from src.program_handler.error_handler import ErrorHandler
from src.utils.utility import print_pairs, choose_pair
from dotenv import load_dotenv

load_dotenv()

THRESHOLD = float(os.getenv("THRESHOLD"))
PVALUE = float(os.getenv("PVALUE"))

class PairAnalysis:

    def __init__(self, data, tickers, threshold=THRESHOLD, pvalue=PVALUE):
        self.logger = set_logger(__name__) # set logger
        self.data = data # set data
        self.tickers = tickers # set tickers
        self.threshold = threshold # set threshold
        self.pvalue = pvalue # set ideal p-value

        self.error_handler = ErrorHandler() # initialize error handler
        self.db = Database() # initialize database manager

        self.pair_info = {} # dictionary to store pairs and their coefficients / p-values

    def calculate_spread(self, pair):
        # :param pair: A tuple containing the two stock symbols.

        self.logger.debug(f"Calculating spread for {pair[0]} and {pair[1]}")
        spread = self.data[pair[0]] - self.data[pair[1]]
        return spread # return pandas series containing spread
    
    # correlation matrix calculation
    def correlation_matrix(self):
        self.logger.debug("Calculating correlation matrix")
        return self.data.corr() # return pandas dataframe 

    def potential_pairs(self):
        """
        Identifies potential pairs of stocks based on the correlation matrix.

        :param threshold: The minimum correlation value to consider a pair.
        :return: A list of tuples containing the potential pairs.
        """
        self.logger.debug(f"Identifying potential pairs with threshold {self.threshold}")

        correlation_matrix = self.correlation_matrix()
        coefficients = {} # dictionary store coefficients

        for i in range(len(correlation_matrix.columns)):
            for j in range(i):
                corr_value = abs(correlation_matrix.iloc[i, j]) # correlation coefficient
                pair = (correlation_matrix.columns[i], correlation_matrix.columns[j]) # identify pair

                coefficients[pair] = corr_value # store coefficient in dictionary
                
                if corr_value > self.threshold:
                    self.pair_info[pair] = (corr_value, None) # store coefficient, p-value is None for now
                    self.logger.info(f"Pair found: {pair[0]} and {pair[1]}")
        
        # if no pairs are found, handle error
        if not self.pair_info:
            self.error_handler.handle_error('corr', coefficients)

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
        self.potential_pairs()
        self.logger.debug(f"Performing cointegration test on {len(self.pair_info)} pairs")

        valid_pairs = 0 # count valid pairs for error handling

        for pair in self.pair_info.keys():
            spread = self.calculate_spread(pair)
            p_value = self.check_cointegration(spread, pair)
            
            # retrieve coefficient from pair_info dictionary
            coefficient = self.pair_info[pair][0]
            # update dictionary with p-value
            self.pair_info[pair] = (coefficient, p_value)
            
            if p_value <= self.pvalue:
                valid_pairs += 1
                self.logger.info(f"{pair[0]}, {pair[1]}: Cointegrated (p-value: {p_value:.2f})")
            else:
                self.logger.info(f"{pair[0]}, {pair[1]}: Not cointegrated (p-value: {p_value:.2f})")
        
        # if no valid pairs are found, handle error
        if valid_pairs == 0:
            return self.error_handler.handle_error('coint', self.pair_info)
        
        print('\nSuccessfully passed the Augmented Dickey Fuller Cointegration test!')
        mapped_pairs = print_pairs(self.pair_info, self.pvalue) # map pairs to display index and print pairs
        chosen_pair = choose_pair(mapped_pairs) # return the selected pair

        # insert stocks into database
        for ticker in chosen_pair:
            stock_id = self.db.execute_query(queries.insert_stock,(ticker,))
            self.logger.info(f"Inserted {ticker} with stock ID: {stock_id} into database")

        return chosen_pair
    
    def run_analysis(self):
        self.logger.debug("Running pair analysis...")
        chosen_pair = self.cointegration_test()
        print(chosen_pair)
        print(f"Chosen pair: {chosen_pair[0]}, {chosen_pair[1]}")
        return chosen_pair # return the final pair_info dictionary
     