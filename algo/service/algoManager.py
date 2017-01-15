"""
Algo manager
"""
from enum import Enum


Status = Enum('Status', ('Idle', 'Running', 'Stopped', 'Suspended'))


class AlgoManager:
    __status = Status.Idle
    config = {}
    strategies = []
    account = None
    instrument = None

    def __init__(self):
        self.__status = Status.Idle

    def get_status(self):
        return self.__status;

    def set_status_running(self):
        self.__status = Status.Running

    def set_status_stopped(self):
        self.__status = Status.Running

    def set_status_suspended(self):
        self.__status = Status.Suspended

    """
    Operations on app
    """
    def start_app(self, config):
        self.config = config
        #self.account = config["account"]
        #self.instrument = config["instrument"]
        """
        init strategy based on config
        """
        for strategy in self.strategies:
            strategy.init()
        self.set_status_running()

    def stop_app(self):
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
