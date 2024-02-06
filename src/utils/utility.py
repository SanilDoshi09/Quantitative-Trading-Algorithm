import logging
import os
import sys

from ..logger import set_logger
from dotenv import load_dotenv

load_dotenv()

Threshold = float(os.getenv("THRESHOLD"))
Pvalue = float(os.getenv("PVALUE"))

divider = ("-" * 20)

logger = set_logger(__name__)

# Function to print the threshold and p-value
def print_thresholds(divider="-" * 20):
        print(f'\nCONSTRAINTS:')
        print(f'Threshold > {Threshold}')
        print(f'P-value < {Pvalue}')
        print(divider, '\nTEST RESULTS:')

# Function to print the pairs and their coefficients and p-values
def print_pairs(pairs_info, pvalue_threshold=None):

    print_thresholds()
    mapped_pairs = {} # maps displayed index to pair keys
    display_index = 1 # start number from 1 for user display
   

    # list all the pairs in numbered format with their coefficients and p-values
    for pair in pairs_info.keys():
        coefficient, p_value = pairs_info[pair]
        if pvalue_threshold is None or p_value <= pvalue_threshold:
            print(f"{display_index}. {pair[0]}, {pair[1]}: {coefficient:.4f}, {p_value:.4f}")
            mapped_pairs[display_index] = pair  # Map display index to pair
            display_index += 1
    
    print(divider, '\n')
    return mapped_pairs

# Function to handle user input for selecting a pair
def choose_pair(pairs_list):

    while True: # Loop to handle user input
        user_input = input("Enter the correspondng number of the pair you'd like to select " +
                            "or type 'q' to exit: ").strip().lower()
        
        if user_input == 'q':
            logger.info("Exiting program")
            sys.exit(1) # quit program
        
        if user_input.isdigit():
            chosen_index = int(user_input)
            if chosen_index in pairs_list:
                chosen_pair = pairs_list[chosen_index]
                logger.info(f"Selected pair: {chosen_pair[0]}, {chosen_pair[1]}")
                return chosen_pair  # Return the selected pair