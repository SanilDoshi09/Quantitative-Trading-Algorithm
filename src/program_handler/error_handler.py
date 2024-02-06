import sys
import logging
import os

from src.utils.utility import print_thresholds, print_pairs, choose_pair
from ..logger import set_logger
from dotenv import load_dotenv

load_dotenv()

THRESHOLD = float(os.getenv("THRESHOLD"))
PVALUE = float(os.getenv("PVALUE"))

class ErrorHandler:

    def __init__(self, threshold=THRESHOLD, pvalue=PVALUE):
        self.logger = set_logger(__name__)
        self.threshold = threshold
        self.pvalue = pvalue
    
    # Handles the case where no pairs passed the Augmented Dickey Fuller Cointegration test
    def handle_coint_error(self, pairs_info):


        print('\nNo pairs passed the Augmented Dickey Fuller Cointegration test...')

        pairs_list = print_pairs(pairs_info)

        return choose_pair(pairs_list)

    # Handles the case where no pairs were found based on the correlation matrix
    def handle_corr_error(self, pairs_info):
        print('\nNo pairs found...')
        print_thresholds()

        for pair, value in pairs_info.items():
            if value != 1: # ignore direct pairs (i.e AAPL:APPL) as they are not useful
                print(f"{pair[0]:>5}, {pair[1]}: {value:.4f}")
        
        print(self.divider, '\nChange the threshold or try a different set of stocks.\n')
        self.logger.error("Exiting program")
        sys.exit(1)
    
    def handle_error(self, keyword, pairs_info): 
        self.logger.error("No pairs found")

        if keyword == 'coint':
            return self.handle_coint_error(pairs_info) # return the selected pair if the user chose to do so
        elif keyword == 'corr':
            self.handle_corr_error(pairs_info)
        else:
            self.logger.error("Invalid keyword argument")
            sys.exit(1)
    