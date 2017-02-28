# encoding: UTF-8

from strategy.event.eventEngine import *
from strategy.defensive_strategy.defensiveStrategy import *
from strategy.account.accountInfo import AccountInfo
from strategy import StrategyLog
from strategy.vtConstant import *

# initial the logger for this strategy
defensive_logger = StrategyLog(LOG_CONFIG_FILE, DEFENSIVE_LOGGER)


global_event_engine = EventEngine(defensive_logger)
global_account_info = AccountInfo(defensive_logger)
global_dfs_strategy = DefensiveStrategy(defensive_logger)


def config(strategy_setting):
    global_account_info.config(global_event_engine, strategy_setting)
    global_dfs_strategy.config(global_event_engine, global_account_info, strategy_setting)


def start():
    global_dfs_strategy.start()


def stop():
    global_dfs_strategy.stop()
