import sys
import logging
import os

from ..logger import set_logger

class ErrorHandler:

    def __init__(self):
        self.logger = set_logger(__name__)
        self.divider = ("-" * 20)
    
    def print_pairs(self, pairs, dictionary):
        self.logger.info("Printing pairs")
        for pair in pairs:
            print(f"{pair[0]}, {pair[1]}: {dictionary[pair]:.4f}")
    
    def handle_coint_error(self, pairs_info):

        print('\nNo pairs passed the Augmented Dickey Fuller Cointegration test...')
        print(self.divider, '\nPAIRS TABLE:')

        for pair, (coefficient, p_value) in pairs_info.items():
            print(f"{pair[0]:>5}, {pair[1]}: {coefficient:.4f}, {p_value:.4f}")
        
        print(self.divider, '\nPick a stock or try a different set of stocks.\n')
        self.logger.error("Exiting program")
        sys.exit(1)

    def handle_corr_error(self, threshold, pairs_info):
        print('\nNo pairs found...')
        print(f'\nTHRESHOLD: {threshold}')
        print(self.divider, '\nCOEFFICIENT TABLE:')

        for pair, value in pairs_info.items():
            if value != 1:
                print(f"{pair[0]:>5}, {pair[1]}: {value:.4f}")
        
        print(self.divider, '\nChange the threshold or try a different set of stocks.\n')
        self.logger.error("Exiting program")
        sys.exit(1)
    
    def handle_error(self, keyword, value, pairs_info):
        self.logger.error("No pairs found")

        if keyword == 'coint':
            self.handle_coint_error(pairs_info)
        elif keyword == 'corr':
            self.handle_corr_error(value, pairs_info)
        else:
            self.logger.error("Invalid keyword argument")
            sys.exit(1)
        
    
    # def validate_stocks(self, tickers):

    #     if len(tickers) < 2:
    #         self.logger.error("Not enough tickers provided")
    #         print("\nPlease provide at least two tickers to analyze.\n")
    #         return False
    #         sys.exit(1)      
        
    #     while True:
    #         response = input("Would you like to continue? [Y/n]: ").strip().lower()
        
    #         if response in ('y', 'yes', ''):
    #             return True
    #         elif response in ('n', 'no'):
    #             return False
    #         else:
    #             continue
    
    # def select_pair(self, pairs_info):
    #     """
    #     Ask the user to select a pair from the list of potential pairs.

    #     :param pairs_info: A dictionary containing the potential pairs and their coefficients.
    #     """
    #     for index, (pair, value) in enumerate(pairs_info.items(), start=1):
    #         print(f"{index + 1}: {pair[0]}, {pair[1]}: {value:.4f}")