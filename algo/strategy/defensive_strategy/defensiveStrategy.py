# encoding: UTF-8

from strategy.account.accountInfo import *
from utils import *
from threading import *
from time import *
#from algo.service.OrderService import *
from strategy import StrategyLog
from strategy.vtConstant import *

class DefensiveStrategy:
    # The name of Strategy
    # The name of Author
    class_name = 'DefensiveStrategy'
    author = u''

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, logger):

        #initial the log setting
        self.__logger = logger

        # Setting for this strategy
        self.__strategy_setting__ = {}
        self.__strategy_setting_item_name = [ACCOUNT_ID, PORTFOLIO_ID, INSTRUMENT_ID, OPEN_PRICE, OPEN_VOLUME,
                                           STOPLOSS_PRICE, CLOSE_PARAMS]

        self.__logger.debug(DEFENSIVE_SETTING_PARMS, self.__strategy_start_item_name)

        self.__strategy_close_params = {}
        # openStatus: 0 -- not open, 1 -- open request, 2 -- partially open, 3 -- fully open
        # closeStatus: 0 -- not close, 1 -- close request, 2 -- partially close, 3 -- fully close
        # stopLossStatus: 0 -- Not Triggered StopLoss, 1 -- Triggered StopLoss
        self.__strategy_state = {OPEN_STATUS: OPEN_STATUS_INITIAL, CLOSE_STATUS: CLOSE_STATUS_INITIAL,
                                 STOPLOSS_STATUS: STOPLOSS_STATUS_INITIAL}

        self.__query_thread = Thread(target=self.__run)
        self.__thread_condition = Condition()
        self.__active = False
        self.__event_engine = None
        self.__account_info = None

    def config(self, event_engine, account_info, strategy_setting):
        """
        This function is used to configure some other classes which work with itself to do some strategy-related things
        :param event_engine: Event Engine
        :param account_info: Account entity used to trace the trade
        :param strategy_setting: some strategy-related parameters used to trigger some strategy-related actions
        :return: None
        """
        self.__logger.info(STRATEGY_CONFIG)
        self.__event_engine = event_engine
        self.__account_info = account_info
        if strategy_setting:
            for key in self.__strategy_start_item_name:
                if key in strategy_setting:
                    self.__strategy_setting__[key] = strategy_setting[key]
        if self.__strategy_setting__[CLOSE_PARAMS]:
            self.__strategy_close_params = self.__strategy_setting__[CLOSE_PARAMS]

        self.__logger.debug(DEFENSIVE_SETTING_PARMS, self.__strategy_setting__)
        self.__register()
    # ------------------------------------------------------------------------------------------------------------------

    def on_tick(self, event):

        self.__logger.info(DEFENSIVE_TICK, event.even_param_)
        if event.even_param_[PRICE] == dict_get(self.__strategy_setting__, OPEN_PRICE, 0) \
                and self.__strategy_state[OPEN_STATUS] == OPEN_STATUS_INITIAL:
            self.__logger.info(STRATEGY_OPEN)
            self.__strategy_state[OPEN_STATUS] = OPEN_STATUS_REQ
            buy_para_ = {ACCOUNT_ID: self.__strategy_setting__[ACCOUNT_ID],
                         PORTFOLIO_ID: self.__strategy_setting__[PORTFOLIO_ID],
                         INSTRUMENT_ID: self.__strategy_setting__[INSTRUMENT_ID],
                         DIRECTION: DIRECTION_LONG,
                         PRICE: self.__strategy_setting__[OPEN_PRICE], QTY: self.__strategy_setting__[OPEN_VOLUME],
                         TAG: TAG_DEFAULT_VALUE}
            self.__logger.debug(DEFENSIVE_BUY, buy_para_)
            buy_event_ = AQIStrategyEvent(EVENT_BUY, buy_para_)
            self.__event_engine.put(buy_event_)

            cash_para_ = {PORTFOLIO_ID: self.__strategy_setting__[PORTFOLIO_ID],
                          ACCOUNT_ID: self.__strategy_setting__[ACCOUNT_ID],
                          USED_CASH: self.__strategy_setting__[OPEN_PRICE] * self.__strategy_setting__[OPEN_VOLUME]}
            self.__logger.debug(DEFENSIVE_CASH_CHANGE, cash_para_)
            cash_event_ = AQIStrategyEvent(EVENT_CASHCHANGED, cash_para_)
            self.__event_engine.put(cash_event_)

            self.__thread_condition.acquire()
            self.__thread_condition.notify_all()
            self.__thread_condition.release()

        elif event.even_param_[PRICE] == dict_get(self.__strategy_setting__, STOPLOSS_PRICE, 0):
            traded_qty_ = self.__account_info.get_traded_qty(self.__strategy_setting__[PORTFOLIO_ID],
                                                             self.__strategy_setting__[ACCOUNT_ID],
                                                             self.__strategy_setting__[INSTRUMENT_ID])
            self.__logger.debug(DEFENSIVE_INSTR_TRADED_QTY, self.__strategy_setting__[INSTRUMENT_ID], traded_qty_)
            if traded_qty_ > 0:
                self.__strategy_state[STOPLOSS_STATUS] = STOPLOSS_STATUS_TRIGGER
                sell_para_ = {ACCOUNT_ID: self.__strategy_setting__[ACCOUNT_ID],
                              PORTFOLIO_ID: self.__strategy_setting__[PORTFOLIO_ID],
                              INSTRUMENT_ID: self.__strategy_setting__[INSTRUMENT_ID], DIRECTION: DIRECTION_LONG,
                              PRICE: event.even_param_[PRICE], QTY: traded_qty_,
                              TAG: TAG_DEFAULT_VALUE}
                self.__logger.debug(DEFENSIVE_SELL, sell_para_)
                sell_event_ = AQIStrategyEvent(EVENT_SELL, sell_para_)
                self.__event_engine.put(sell_event_)

                self.__thread_condition.acquire()
                self.__thread_condition.notify_all()
                self.__thread_condition.release()

        elif self.__strategy_state[OPEN_STATUS] != OPEN_STATUS_INITIAL \
                and self.__strategy_state[CLOSE_STATUS] != CLOSE_STATUS_FULL:
            is_sell_operation_ = False
            for close_cond_ in self.__strategy_close_params:
                if close_cond_[PRICE] == event.even_param_[PRICE]:
                    self.__logger.info(STRATEGY_CLOSE)
                    is_sell_operation_ = True
                    traded_qty_ = self.__account_info.get_traded_qty(self.__strategy_setting__[PORTFOLIO_ID],
                                                                     self.__strategy_setting__[ACCOUNT_ID],
                                                                     self.__strategy_setting__[INSTRUMENT_ID])

                    self.__logger.debug(DEFENSIVE_INSTR_TRADED_QTY, self.__strategy_setting__[INSTRUMENT_ID],
                                        traded_qty_)
                    if traded_qty_ > 0:
                        self.__strategy_state[CLOSE_STATUS] = CLOSE_STATUS_REQ
                        sell_para_ = {ACCOUNT_ID: self.__strategy_setting__[ACCOUNT_ID],
                                      PORTFOLIO_ID: self.__strategy_setting__[PORTFOLIO_ID],
                                      INSTRUMENT_ID: self.__strategy_setting__[INSTRUMENT_ID],
                                      DIRECTION: DIRECTION_LONG,
                                      PRICE: close_cond_[PRICE], QTY: close_cond_[VOLUME],
                                      TAG: TAG_DEFAULT_VALUE}
                        self.__logger.debug(DEFENSIVE_SELL, sell_para_)
                        sell_event_ = AQIStrategyEvent(EVENT_SELL, sell_para_)
                        self.__event_engine.put(sell_event_)

            if not is_sell_operation_:
                profit_para_ = {PORTFOLIO_ID: self.__strategy_setting__[PORTFOLIO_ID],
                                ACCOUNT_ID: self.__strategy_setting__[ACCOUNT_ID],
                                INSTRUMENT_ID: self.__strategy_setting__[INSTRUMENT_ID],
                                PRICE: event.even_param_[PRICE]}
                self.__logger.debug(DEFENSIVE_PROFIT_CHANGE, profit_para_)
                profit_event_ = AQIStrategyEvent(EVENT_PROFITCHANGED, profit_para_)
                self.__event_engine.put(profit_event_)

            self.__thread_condition.acquire()
            self.__thread_condition.notify_all()
            self.__thread_condition.release()

    # ------------------------------------------------------------------------------------------------------------------
    def on_buy(self, event):
        """
        This function is to invoke the buy function provided CTP
        :param event: event includes some parameters needed by buy operation
        :return: None
        """

        self.__logger.debug(DEFENSIVE_BUY_PERFORM, event.even_param_)
        buy_result_ = buy(event.even_param_[ACCOUNT_ID], event.even_param_[PORTFOLIO_ID],
                          event.even_param_[INSTRUMENT_ID], event.even_param_[DIRECTION],
                          event.even_param_[PRICE], event.even_param_[QTY],
                          event.even_param_[TAG])
        self.__event_engine.put(AQIStrategyEvent(EVENT_TRADE,buy_result_))

    # ------------------------------------------------------------------------------------------------------------------
    def on_sell(self, event):
        """
        This function is to invoke the sell function provided by CTP
        :param event: event includes some parameters needed by sell operation
        :return: None
        """
        self.__logger.debug(DEFENSIVE_SELL_PERFORM, event.even_param_)
        sell_result_ = sell(event.even_param_[ACCOUNT_ID], event.even_param_[PORTFOLIO_ID],
                            event.even_param_[INSTRUMENT_ID], event.even_param_[DIRECTION],
                            event.even_param_[PRICE], event.even_param_[QTY],
                            event.even_param_[TAG])
        self.__event_engine.put(AQIStrategyEvent(EVENT_TRADE, sell_result_))

    # ------------------------------------------------------------------------------------------------------------------
    def __register(self):
        """
        This function is to register the functions responding some events
        :return: None
        """
        self.__event_engine.register(EVENT_MARKETDATA, self.on_tick)
        self.__event_engine.register(EVENT_BUY, self.on_buy)
        self.__event_engine.register(EVENT_SELL, self.on_sell)

    # ------------------------------------------------------------------------------------------------------------------
    def __query_order_status(self):
        """
        This function is to get the latest order's status by invoking the function get_order_status provided by CTP
        :return:None
        """
        self.__thread_condition.acquire()
        # order_id_list_ = self.__account_info.get_not_fully_traded_orders(self.__strategy_setting__[PORTFOLIO_ID],
        #                                                                  self.__strategy_setting__[ACCOUNT_ID],
        #                                                                  self.__strategy_setting__[INSTRUMENT_ID])
        order_id_list_ = self.__account_info.get_not_fully_traded_orders(self.__strategy_setting__[ACCOUNT_ID])
        self.__logger.debug(DEFENSIVE_GET_ORDER_STATUS, self.__strategy_setting__[ACCOUNT_ID])
        if not order_id_list_:
            self.__thread_condition.wait()

        self.__thread_condition.release()

        # order_id_list_ = self.__account_info.get_not_fully_traded_orders(self.__strategy_setting__[PORTFOLIO_ID],
        #                                                                  self.__strategy_setting__[ACCOUNT_ID],
        #                                                                  self.__strategy_setting__[INSTRUMENT_ID])
        order_id_list_ = self.__account_info.get_not_fully_traded_orders(self.__strategy_setting__[ACCOUNT_ID])
        self.__logger.debug(DEFENSIVE_GET_ORDER_STATUS, self.__strategy_setting__[ACCOUNT_ID])

        for order_id_ in order_id_list_:
            order_status_ = get_order_status(order_id_)
            self.__logger.debug(DEFENSIVE_TRADE, order_status_)
            trade_event_ = AQIStrategyEvent(EVENT_TRADE, order_status_)
            self.__event_engine.put(trade_event_)

    # ------------------------------------------------------------------------------------------------------------------
    def __run(self):
        """
        This is a main function for a seperate thread, which is used to check the status of order
        :return: None
        """
        while self.__active:
            try:
                self.__query_order_status()
            except Empty:
                pass

    # ------------------------------------------------------------------------------------------------------------------
    def start(self):
        """
        This function is to start the strategy
        :return: None
        """
        self.__active = True
        self.__query_thread.start()
        self.__event_engine.start()

    # ------------------------------------------------------------------------------------------------------------------
    def stop(self):
        """
        This function is to stop the strategy
        :return: None
        """
        self.__thread_condition.acquire()
        self.__thread_condition.notify_all()
        self.__thread_condition.release()
        self.__active = False
        self.__query_thread.join()
        self.__event_engine.stop()

    # ------------------------------------------------------------------------------------------------------------------
    def suspend(self):
        """
        This function is to suspend the strategy
        :return: None
        """
        self.__active = False
        self.__suspend = True

    # ------------------------------------------------------------------------------------------------------------------
    def resume(self):
        """
        This function is to resume the strategy
        :return: None
        """
        self.__active = True
        self.__suspend = False

# ----------------------------------------------------------------------------------------------------------------------
"""
Below are some code for the unit testing
"""
def test():
    ee = EventEngine()
    strategy_entry = DefensiveStrategy()
    ee.start()
    ee.put(AQIStrategyEvent(EVENT_LOG))

if __name__ == '__main__':
    test()
