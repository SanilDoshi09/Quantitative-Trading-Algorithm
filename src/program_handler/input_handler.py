import logging

from ..logger import set_logger
from src.analysis.pair_analysis import PairAnalysis

class InputHandler:

    def __init__(self):
        self.logger = set_logger(__name__)