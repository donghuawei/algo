# encoding: UTF-8

from accountInfo import *
from utils import *
from threading import *
from time import *
from algo.service.OrderService import *


class DefensiveStrategy:
    # The name of Strategy
    # The name of Author
    class_name = 'DefensiveStrategy'
    author = u''

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self):
        # Setting for this strategy
        self.__strategy_setting__ = {}
        self.__strategy_start_item_name = [ACCOUNT_ID, PORTFOLIO_ID, INSTRUMENT_ID, OPEN_PRICE, OPEN_VOLUME,
                                           STOPLOSS_PRICE, CLOSE_PARAMS]
        self.__strategy_close_params = {}
        # openStatus: 0 -- not open, 1 -- open request, 2 -- partially open, 3 -- fully open
        # closeStatus: 0 -- not close, 1 -- close request, 2 -- partially close, 3 -- fully close
        # stopLossStatus: 0 -- Not Triggered StopLoss, 1 -- Triggered StopLoss
        self.__strategy_state = {OPEN_STATUS: OPEN_STATUS_INITIAL, CLOSE_STATUS: CLOSE_STATUS_INITIAL,
                                 STOPLOSS_STATUS: STOPLOSS_STATUS_INITIAL}
        # Setting for this strategy
        self.__strategy_setting__ = {}
        self.__strategy_start_item_name = [ACCOUNT_ID, PORTFOLIO_ID, INSTRUMENT_ID, OPEN_PRICE, OPEN_VOLUME,
                                      STOPLOSS_PRICE, CLOSE_PARAMS]
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
        self.__event_engine = event_engine
        self.__account_info = account_info
        if strategy_setting:
            strategy_setting_items_ = self.__strategy_setting__
            for key in self.__strategy_start_item_name:
                if key in strategy_setting:
                    strategy_setting_items_[key] = strategy_setting[key]
        if self.__strategy_setting__[CLOSE_PARAMS]:
            self.__strategy_close_params = self.__strategy_setting__[CLOSE_PARAMS]

        self.__register()
    # ------------------------------------------------------------------------------------------------------------------

    def on_tick(self, event):

        print("on_tick")
        if event.even_param_[PRICE] == dict_get(self.__strategy_setting__, OPEN_PRICE, 0) \
                and self.__strategy_state[OPEN_STATUS] == OPEN_STATUS_INITIAL:
            self.__strategy_state[OPEN_STATUS] = OPEN_STATUS_REQ
            buy_para_ = {ACCOUNT_ID: self.__strategy_setting__[ACCOUNT_ID],
                         PORTFOLIO_ID: self.__strategy_setting__[PORTFOLIO_ID],
                         INSTRUMENT_ID: self.__strategy_setting__[INSTRUMENT_ID],
                         DIRECTION: DIRECTION_LONG,
                         PRICE: self.__strategy_setting__[OPEN_PRICE], QTY: self.__strategy_setting__[OPEN_VOLUME],
                         TAG: TAG_DEFAULT_VALUE}
            buy_event_ = AQIStrategyEvent(EVENT_BUY, buy_para_)
            self.__event_engine.put(buy_event_)

            cash_para_ = {PORTFOLIO_ID: self.__strategy_setting__[PORTFOLIO_ID],
                          ACCOUNT_ID: self.__strategy_setting__[ACCOUNT_ID],
                          USED_CASH: self.__strategy_setting__[OPEN_PRICE] * self.__strategy_setting__[OPEN_VOLUME]}
            cash_event_ = AQIStrategyEvent(EVENT_CASHCHANGED, cash_para_)
            self.__event_engine.put(cash_event_)

            self.__thread_condition.acquire()
            self.__thread_condition.notify_all()
            self.__thread_condition.release()

        elif event.even_param_[PRICE] == dict_get(self.__strategy_setting__, STOPLOSS_PRICE, 0):
            traded_qty_ = self.__account_info.get_traded_qty(self.__strategy_setting__[PORTFOLIO_ID],
                                                             self.__strategy_setting__[ACCOUNT_ID],
                                                             self.__strategy_setting__[INSTRUMENT_ID])
            if traded_qty_ > 0:
                self.__strategy_state[STOPLOSS_STATUS] = STOPLOSS_STATUS_TRIGGER
                sell_para_ = {ACCOUNT_ID: self.__strategy_setting__[ACCOUNT_ID],
                              PORTFOLIO_ID: self.__strategy_setting__[PORTFOLIO_ID],
                              INSTRUMENT_ID: self.__strategy_setting__[INSTRUMENT_ID], DIRECTION: DIRECTION_LONG,
                              PRICE: event.even_param_[PRICE], QTY: traded_qty_,
                              TAG: TAG_DEFAULT_VALUE}
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
                    is_sell_operation_ = True
                    traded_qty_ = self.__account_info.get_traded_qty(self.__strategy_setting__[PORTFOLIO_ID],
                                                                     self.__strategy_setting__[ACCOUNT_ID],
                                                                     self.__strategy_setting__[INSTRUMENT_ID])
                    if traded_qty_ > 0:
                        self.__strategy_state[CLOSE_STATUS] = CLOSE_STATUS_REQ
                        sell_para_ = {ACCOUNT_ID: self.__strategy_setting__[ACCOUNT_ID],
                                      PORTFOLIO_ID: self.__strategy_setting__[PORTFOLIO_ID],
                                      INSTRUMENT_ID: self.__strategy_setting__[INSTRUMENT_ID],
                                      DIRECTION: DIRECTION_LONG,
                                      PRICE: close_cond_[PRICE], QTY: close_cond_[VOLUME],
                                      TAG: TAG_DEFAULT_VALUE}
                        sell_event_ = AQIStrategyEvent(EVENT_SELL, sell_para_)
                        self.__event_engine.put(sell_event_)

                        self.__thread_condition.acquire()
                        self.__thread_condition.notify_all()
                        self.__thread_condition.release()
            if not is_sell_operation_:
                profit_para_ = {PORTFOLIO_ID: self.__strategy_setting__[PORTFOLIO_ID],
                                ACCOUNT_ID: self.__strategy_setting__[ACCOUNT_ID],
                                INSTRUMENT_ID: self.__strategy_setting__[INSTRUMENT_ID],
                                PRICE: event.even_param_[PRICE]}
                profit_event_ = AQIStrategyEvent(EVENT_PROFITCHANGED, profit_para_)
                self.__event_engine.put(profit_event_)

    # ------------------------------------------------------------------------------------------------------------------
    def on_buy(self, event):
        buy_result_ = buy(event.even_param_[ACCOUNT_ID], event.even_param_[PORTFOLIO_ID],
                          event.even_param_[INSTRUMENT_ID], event.even_param_[DIRECTION],
                          event.even_param_[PRICE], event.even_param_[QTY],
                          event.even_param_[TAG])
        self.__event_engine.put(AQIStrategyEvent(EVENT_TRADE,buy_result_))

    # ------------------------------------------------------------------------------------------------------------------
    def on_sell(self, event):
        sell_result_ = sell(event.even_param_[ACCOUNT_ID], event.even_param_[PORTFOLIO_ID],
                            event.even_param_[INSTRUMENT_ID], event.even_param_[DIRECTION],
                            event.even_param_[PRICE], event.even_param_[QTY],
                            event.even_param_[TAG])
        self.__event_engine.put(AQIStrategyEvent(EVENT_TRADE, sell_result_))

    # ------------------------------------------------------------------------------------------------------------------
    def __register(self):
        self.__event_engine.register(EVENT_MARKETDATA, self.on_tick)
        self.__event_engine.register(EVENT_BUY, self.on_buy)
        self.__event_engine.register(EVENT_SELL, self.on_sell)

    # ------------------------------------------------------------------------------------------------------------------
    def __query_order_status(self):
        self.__thread_condition.acquire()
        # order_id_list_ = self.__account_info.get_not_fully_traded_orders(self.__strategy_setting__[PORTFOLIO_ID],
        #                                                                  self.__strategy_setting__[ACCOUNT_ID],
        #                                                                  self.__strategy_setting__[INSTRUMENT_ID])
        order_id_list_ = self.__account_info.get_not_fully_traded_orders(self.__strategy_setting__[ACCOUNT_ID])
        if not order_id_list_:
            self.__thread_condition.wait(1)

        self.__thread_condition.release()

        # order_id_list_ = self.__account_info.get_not_fully_traded_orders(self.__strategy_setting__[PORTFOLIO_ID],
        #                                                                  self.__strategy_setting__[ACCOUNT_ID],
        #                                                                  self.__strategy_setting__[INSTRUMENT_ID])
        order_id_list_ = self.__account_info.get_not_fully_traded_orders(self.__strategy_setting__[ACCOUNT_ID])

        for order_id_ in order_id_list_:
            order_status_ = get_order_status(order_id_)
            trade_event_ = AQIStrategyEvent(EVENT_TRADE, order_status_)
            self.__event_engine.put(trade_event_)

    # ------------------------------------------------------------------------------------------------------------------
    def __run(self):
        while self.__active:
            try:
                sleep(0.2)
                self.__query_order_status()
            except Empty:
                pass

    # ------------------------------------------------------------------------------------------------------------------
    def start(self):
        self.__active = True
        self.__query_thread.start()
        self.__event_engine.start()

    # ------------------------------------------------------------------------------------------------------------------
    def stop(self):
        self.__thread_condition.acquire()
        self.__thread_condition.notify_all()
        self.__thread_condition.release()
        self.__active = False
        self.__query_thread.join()
        self.__event_engine.stop()

# ----------------------------------------------------------------------------------------------------------------------


def test():
    ee = EventEngine()
    strategy_entry = DefensiveStrategy(ee)
    ee.start()
    ee.put(AQIStrategyEvent(EVENT_LOG))

if __name__ == '__main__':
    test()
