import os
import logging 
import warnings
import time

import yfinance as yf
import pandas as pd
import os

from ..logger import set_logger
from dotenv import load_dotenv

load_dotenv()

# dates for fetching data
STARTDATE = os.getenv("STARTDATE")
ENDDATE = os.getenv("ENDDATE")

class DataFetcher:

    def __init__(self, tickers, start_date=STARTDATE, end_date=ENDDATE):
        self.logger = set_logger(__name__)
        self.start_date = start_date
        self.end_date = end_date
        self.logger.info("Data fetcher object initialized") 

        # Suppress warnings
        warnings.simplefilter(action='ignore', category=FutureWarning)
        # Set yfinance logger to error only
        yf_logger = logging.getLogger('yfinance')
        yf_logger.setLevel(logging.ERROR)

        self.tickers = tickers
    
    def fetch_data(self):
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
                ticker_data = yf.download(ticker, self.start_date, self.end_date)
                if not ticker_data.empty: # makes sure the data is not empty
                    data[ticker] = ticker_data['Adj Close'] # adds the data to the DataFrame
                    self.logger.debug(f"Fetched data for {ticker}")
                else:
                    self.logger.warning(f"No data found for {ticker}")
            except Exception as e:
                self.logger.error(f"Error fetching data for {ticker}: {e}")
            time.sleep(1) # pause for 1 second to avoid rate limiting
        
        return data
        
        