import logging
import os
import sys
import yfinance as yf

from ..logger import set_logger
from dotenv import load_dotenv

load_dotenv()

TICKERS = os.getenv("STOCKS", '').split(",")

class InputHandler:

    def __init__(self, tickers=TICKERS):
        self.logger = set_logger(__name__)
        self.tickers = tickers
    
    def validate_stocks(self):
        # check if there are enough stocks to analyze
        if len(self.tickers) < 2:
            self.logger.error("Not enough tickers provided")
            print("\nPlease provide at least two stocks to analyze.\n")
            sys.exit(1)
    
    def confirm_selection(self):
        # confirm the stocks the user has selected
        self.logger.info("Confirming stock selection")

        print("\nSTOCKS:")
        for stock in self.tickers:
            print(f"{stock:>5}")

        print("\nIf you'd like to change the stocks, please edit the .env file and restart the program.")

        user_input = input("\nPress ENTER to continue ")
        if user_input != "":
            self.logger.info("Exiting program")
            sys.exit(1)
        else:
            return True
    
    def preliminiary_analysis(self):
        self.logger.debug("Performing preliminary analysis")
        # perform preliminary analysis
        self.validate_stocks()
        self.confirm_selection()

    

    

        


    
