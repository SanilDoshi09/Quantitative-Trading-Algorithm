import logging
import datetime

class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    # ANSI colors for different log levels
    grey = "\x1b[38;21m"
    green = "\x1b[32m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: green + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def set_logger(name):
    # current date
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    # create logger with a specified name
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # file handler
    # file_handler = logging.FileHandler("../logs/{}_{}.log".format(name, date))
    # file_handler.setLevel(logging.DEBUG)
    # file_handler.setFormatter(CustomFormatter())

    # console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(CustomFormatter())

    # add the handlers to the logger
    # logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

