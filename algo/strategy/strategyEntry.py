# encoding: UTF-8

from eventEngine import *
from defensiveStrategy import *
from accountInfo import *

global_event_engine = EventEngine()
global_account_info = AccountInfo()
global_dfs_strategy = DefensiveStrategy()


def config(strategy_setting):
    global_account_info.config(global_event_engine, strategy_setting)
    global_dfs_strategy.config(global_event_engine, global_account_info, strategy_setting)


def start():
    global_dfs_strategy.start()


def stop():
    global_dfs_strategy.stop()
