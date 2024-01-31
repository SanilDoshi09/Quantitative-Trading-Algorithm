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
        # self.logger.debug(f"Type of fetched data: {type(self.data)}")

        self.logger.debug("Data loaded successfully")

    def calculate_spread(self, pair):
        """
        Calculates the spread between two stocks.

        :param pair: A tuple containing the two stock symbols.
        :return: A pandas Series containing the spread.
        """
        self.logger.info(f"Calculating spread for {pair[0]} and {pair[1]}")
        spread = self.data[pair[0]] - self.data[pair[1]]
        return spread
    
    def correlation_matrix(self):
        """
        Calculates the correlation matrix for the data.

        :return: A pandas DataFrame containing the correlation matrix.
        """
        self.logger.info("Calculating correlation matrix")
        return self.data.corr()

    def potential_pairs(self, threshold=0.95):
        """
        Identifies potential pairs of stocks based on the correlation matrix.

        :param correlation_matrix: A pandas DataFrame containing the correlation matrix.
        :param threshold: The minimum correlation value to consider a pair.
        :return: A list of tuples containing the potential pairs.
        """
        correlation_matrix = self.correlation_matrix()
        self.logger.info(f"Identifying potential pairs with threshold {threshold}")
        pairs = [] # list of identified pairs
        coefficients = [] # store coefficients for each pair
        for i in range(len(correlation_matrix.columns)):
            for j in range(i):
                corr_value = abs(correlation_matrix.iloc[i, j]) # correlation coefficient
                if corr_value > threshold:
                    pair = (correlation_matrix.columns[i], correlation_matrix.columns[j])

                    pairs.append(pair) # add pair to list
                    coefficients.append(f"{pair[0]}, {pair[1]}: {corr_value:.2f}")
                    self.logger.debug(f"Pair found: {correlation_matrix.columns[i]} and {correlation_matrix.columns[j]}")
        
        if not pairs:
            self.logger.error("No potential pairs found")
            print("No potential pairs found, try changing the threshold or testing different stocks.")
            sys.exit(1)
        else:
            print(f"\nIdentified Pairs with Correlation Coefficients greater than {threshold}:")
            for info in coefficients:
                print(info)
            return pairs
    
    @staticmethod
    def check_cointegration(spread, pair):
        """
        Static method to perform Augmented Dickey-Fuller test.
        """
        # perform the Augmented Dickey-Fuller test
        try:
            adf_result = adfuller(spread)
            return adf_result[1]
        except Exception as e:
            logging.error(f"Error performing ADF test for {pair[0]} and {pair[1]}: {e}")
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
            p_value = PairAnalysis.check_cointegration(spread, pair)
            pairs_info[pair] = p_value
            if p_value < 0.05:
                cointegrated_pairs.append(pair)
                self.logger.debug(f"Pair {pair[0]} and {pair[1]} cointegrated. P-value: {p_value:.2f}")
            else:
                self.logger.debug(f"Pair {pair[0]} and {pair[1]} not cointegrated. P-value: {p_value:.2f}")
        
        if not cointegrated_pairs:
            self.logger.error("No cointegrated pairs found")
            print("No cointegrated pairs found (Need p-value < 0.05). Full list of pairs and p-values:")
            for pair, p_value in pairs_info.items():
                print(f"{pair[0]}, {pair[1]}: {p_value:.4f}")
            sys.exit(1)
        else: 
            print("\nCointegrated Pairs with P-value < 0.05:")
            for pair in cointegrated_pairs:
                print(f"{pair[0]}, {pair[1]}: {pairs_info[pair]:.4f}")
            return cointegrated_pairs
     