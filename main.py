import os
import logging

from src.analysis.pair_analysis import PairAnalysis
from src.program_handler.input_handler import InputHandler
from src.logger import set_logger

def main():

    logger = set_logger("main")
    logger.info("Starting program...")

    pair_analysis = PairAnalysis()
    pair_analysis.run_analysis()


if __name__ == "__main__":
    main()