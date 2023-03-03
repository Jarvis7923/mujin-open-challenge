#!/usr/bin/env python
import logging


class Logger:

    def __init__(self, name):

        # create logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter(
            '[%(asctime)s] %(name)s - %(levelname)s: %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        # 'application' code
        self.logger = logger

    def warning(self, msg, *args):
        self.logger.warning(msg, *args)

    def critical(self, msg, *args):
        self.logger.critical(msg, *args)

    def error(self, msg, *args):
        # self.logger.error(msg)
        self.logger.error(msg, *args)

    def debug(self, msg, *args):
        self.logger.debug(msg, *args)

    def info(self, msg, *args):
        self.logger.info(msg, *args)