
import os
import logging
import pandas as pd

from ..logger import set_logger
from dotenv import load_dotenv
from src.analysis.pair_analysis import PairAnalysis
from src.program_handler.input_handler import InputHandler
from src.analysis.data_fetcher import DataFetcher
from src.analysis.metrics import Metrics

load_dotenv()

TICKERS = os.getenv("STOCKS", '').split(",")

class Program:

    def __init__(self, tickers=TICKERS):
        self.logger = set_logger(__name__)
        self.logger.info("Program initialized")

        self.tickers = tickers
        self.pair_info = {}
        self.data = pd.DataFrame()
        self.spread = pd.Series()
    
    def fetch_data(self):
        data_fetcher = DataFetcher(self.tickers)
        self.data = data_fetcher.fetch_data()
        self.logger.info("Data loaded successfully")
    
    def perform_preliminary_analysis(self):
        input_handler = InputHandler()
        input_handler.preliminiary_analysis()
    
    def perform_pair_analysis(self):
        pair_analysis = PairAnalysis(self.data, self.tickers)
        self.pair_info = pair_analysis.run_analysis()
        self.spread = pair_analysis.calculate_spread(self.pair_info)

    def calculate_metrics(self):
        metrics = Metrics(self.spread)
        self.logger.debug("Calculating metrics")
\
    def run(self):
        self.logger.debug("Running program...")
        self.perform_preliminary_analysis()
        self.fetch_data()
        self.perform_pair_analysis()
        self.calculate_metrics()
