import os
import logging

from src.analysis.pair_analysis import PairAnalysis
from src.logger import set_logger

def main():

    logger = set_logger("main")

    logger.info("Beginning program")
    not_working = ["SPY", "GOOG"]
    ticks = ["GME", "SPY", "WMT", "BA"] # test data
    tickers = ["DPZ", "AAPL", "GOOG", "AMD", "GME", "SPY", "NFLX", "BA", "WMT","DASH","GS","XOM","NKE","AMZN", "META","BRK-B", "MSFT"] # test data
    pair_analysis = PairAnalysis(tickers)

    pair_analysis.run_analysis()

if __name__ == "__main__":
    main()