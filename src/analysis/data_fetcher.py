import os
import logging 
import warnings
import time

import yfinance as yf
import pandas as pd

from ..logger import set_logger

class DataFetcher:

    def __init__(self, tickers):
        self.logger = set_logger(__name__)
        self.logger.info("Data fetcher object initialized") 

        # Suppress warnings
        warnings.simplefilter(action='ignore', category=FutureWarning)
        # Set yfinance logger to error only
        yf_logger = logging.getLogger('yfinance')
        yf_logger.setLevel(logging.ERROR)

        self.tickers = tickers
        self.print_tickers()

    def print_tickers(self):
        # prints the list of tickers
        print("The stocks we are analyzing are:")
        print(", ".join(self.tickers))
    
    def fetch_data(self, start_date, end_date):
        """
        Fetches historical data for the specified tickers between start_date and end_date.

        :param start_date: The start date for the data in 'YYYY-MM-DD' format.
        :param end_date: The end date for the data in 'YYYY-MM-DD' format.
        :return: A pandas DataFrame containing the historical data.
        """

        self.logger.info("Fetching data from Yahoo Finance")
        
        data = pd.DataFrame()
        for ticker in self.tickers:
            try:
                # fetch data from yfinance
                ticker_data = yf.download(ticker, start=start_date, end=end_date)
                if not ticker_data.empty: # makes sure the data is not empty
                    data[ticker] = ticker_data['Adj Close'] # adds the data to the DataFrame
                    self.logger.debug(f"Fetched data for {ticker}")
                else:
                    self.logger.warning(f"No data found for {ticker}")
            except Exception as e:
                self.logger.error(f"Error fetching data for {ticker}: {e}")
            time.sleep(1) # pause for 1 second to avoid rate limiting
        
        return data
        
        