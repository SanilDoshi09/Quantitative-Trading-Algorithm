import os
import logging

from src.program_handler.program import Program
from src.logger import set_logger

def main():

    program = Program()
    program.run()



if __name__ == "__main__":
    main()