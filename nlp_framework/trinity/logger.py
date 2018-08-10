import logging
import sys


class Logger:
    @classmethod
    def get_logger(cls, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        console_logger = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_logger.setFormatter(formatter)
        logger.addHandler(console_logger)
        return logger