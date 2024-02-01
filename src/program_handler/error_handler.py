import sys
import logging
import os

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
        self.divider = ("-" * 20)
    
    def print_pairs(self, pairs, dictionary):
        self.logger.info("Printing pairs")
        for pair in pairs:
            print(f"{pair[0]}, {pair[1]}: {dictionary[pair]:.4f}")
    
    # Handles the case where no pairs passed the Augmented Dickey Fuller Cointegration test
    def handle_coint_error(self, pairs_info):
        """
        Handles the case where no pairs passed the Augmented Dickey Fuller Cointegration test.
        Allows users to still select a pair if they choose to.

        :param pairs_info: A dictionary containing the potential pairs and their coefficients.
        """

        print('\nNo pairs passed the Augmented Dickey Fuller Cointegration test...')
        print(f'\nTHRESHOLD: {self.threshold}')
        print(f'P-VALUE: {self.pvalue}')
        print(self.divider, '\nTEST RESULTS (Coefficient, P-value):')

        pairs_list = list(pairs_info.keys()) # convert dictionary keys to list

        # list all the pairs in numbered format with their coefficients and p-values
        for index, pair in enumerate(pairs_list, start=1):
            coefficient, p_value = pairs_info[pair]
            print(f"{index}. {pair[0]}, {pair[1]}: {coefficient:.4f}, {p_value:.4f}")
        
        print(self.divider, '\nIdeally, we are looking for a pair with a p-value < 0.05.\n')
        
        # Ask the user to select a pair from the list of potential pairs or exit the program
        while True: # Loop to handle user input
            
            user_input = input("Enter the correspondng number of the pair you'd like to select " +
                                "or type 'q' to exit: ").strip().lower()
            
            if user_input == 'q':
                self.logger.info("Exiting program")
                sys.exit(1) # quit program
            
            if user_input.isdigit():
                chosen_index = int(user_input)
                if 1 <= chosen_index <= len(pairs_list):
                    chosen_pair = pairs_list[chosen_index - 1]
                    self.logger.info(f"Selected pair: {chosen_pair[0]}, {chosen_pair[1]}")
                    return chosen_pair  # Return the selected pair

    # Handles the case where no pairs were found based on the correlation matrix
    def handle_corr_error(self, pairs_info):
        print('\nNo pairs found...')
        print(f'\nTHRESHOLD: {self.threshold}')
        print(self.divider, '\nCOEFFICIENT TABLE:')

        for pair, value in pairs_info.items():
            if value != 1:
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
    