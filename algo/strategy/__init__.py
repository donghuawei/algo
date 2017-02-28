# encoding: UTF-8

# This is for the log functionality. All the setting will be configured in the configuration file named "logconf.ini"

import os, sys, logging, logging.config, logging.handlers


class StrategyLog:

    """
    This class is an encapsulation for the system logging class

    """
    def __init__(self, log_conf_file_name, logger_name):
        logging.config.fileConfig(log_conf_file_name)
        self.__logger = logging.getLogger(logger_name)

    def debug(self, log_msg, *args, **kwargs):
        self.__logger.debug(log_msg,*args, **kwargs)

    def info(self, log_msg, *args, **kwargs):
        self.__logger.info(log_msg, *args, **kwargs)

    def warning(self, log_msg, *args, **kwargs):
        self.__logger.warning(log_msg, *args, **kwargs)

    def error(self, log_msg, msg, *args, **kwargs):
        self.__logger.error(log_msg, *args, **kwargs)


def test():
    strategy_log = StrategyLog("logconf.ini", "defensive")
    strategy_log.debug("xxx")

if __name__ == '__main__':
    test()
