# encoding: UTF-8

from event_engine import *
from defensiveStrategy import *
from accountInfo import *

global_event_engine = EventEngine()
global_account_info = AccountInfo(strategy_setting)

def start(strategy_setting):
    dfs_strategy = DefensiveStrategy(global_event_engine,strategy_setting)
    dfs_strategy.start()

