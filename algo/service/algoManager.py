"""
Algo manager
"""
from enum import Enum
from algo.strategy.strategyEntry import start, config, stop


Status = Enum('Status', ('Idle', 'Initialized', 'Running', 'Stopped', 'Suspended'))


class AlgoManager:
    __status = Status.Idle
    config = {}
    strategies = []
    #account = None
    #instrument = None

    def __init__(self):
        self.__status = Status.Idle

    def get_status(self):
        return self.__status

    def set_status_running(self):
        self.__status = Status.Running

    def set_status_stopped(self):
        self.__status = Status.Stopped

    def set_status_suspended(self):
        self.__status = Status.Suspended

    def set_status_initialized(self):
        self.__status = Status.Initialized

    """
    Operations on app
    """
    def initialize_app(self, setting):
        """
        TODO ==> init strategy
        """
        # config in strategyEntry
        config(setting)
        self.set_status_initialized()

    def start_app(self):
        self.set_status_running()

        # start in strategyEntry
        start()
        """
        init strategy based on config
        comment out first
        """
        # for strategy in self.strategies:
        #     strategy.init()
        # self.set_status_running()

    def stop_app(self):
        # stop in strategyEntry
        stop()
        self.set_status_stopped()

    def suspend_app(self):
        self.set_status_suspended()

    def resume_app(self):
        self.set_status_running()

    def update_instrument(self, instrument):
        # update instrument only if the app is in running status
        if Status.Running == self.__status:
            for strategy in self.strategies:
                strategy.update(instrument)

algoMgr = AlgoManager()
