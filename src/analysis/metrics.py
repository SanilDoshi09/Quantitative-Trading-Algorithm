import logging

from src.analysis.pair_analysis import PairAnalysis

from ..logger import set_logger

class Metrics:

    def __init__(self):
        self.logger = set_logger(__name__)
        self.pair_analysis = PairAnalysis()
        self.logger.info("Metrics initialized")

    # TODO: implement sharpe ratio
    
    # TODO: implement half life mean reversion
    
    # TODO: implement hurst exponent
        
    # TODO: implement beta test

    def run_metrics(self):
        self.logger.info("Running metrics...")

        self.logger.info("Metrics complete")