# encoding: UTF-8

from strategy.common.utils import *
from strategy.event.eventType import *
from strategy.event.eventEngine import *
from strategy import StrategyLog

import sys


class AccountInfo:

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, logger):
        # __tradedRecords will be with the following format: { accountID : tradeData }
        # tradeData is a dictionary type with the following format:{'accountID':'accountIDValue',
        #                                                           'portfolioID':'portfolioIDValue',
        #                                                           'orderRecords': 'orderRecordsValue'}
        # orderRecordsValue is of List type with items defined as Dictionary Type { 'orderID': 'orderIDValue',
        #                                                                   'exchangeOrderID':'exchangeOrderIDValue',
        #                                                                    'instrumentID' : 'instrumentIDValue',
        #                                                                    'createDate':'createDateValue'
        #                                                                     'status':'statusValue',
        #                                                                     'direction':'directionValue',
        #                                                                     'tradedQty':'tradedQtyValue','qty':'qtyValue',
        #                                                                     'price':'priceValue',
        #                                                                     'statusMessage': 'statusMessageValue'
        #                                                                     'expirationDate': 'expirationDateValue'}
        #
        self.__traded_records = {}

        # __portfolio_accounts will save all the accounts under it with the format { portfolioID, accounts }
        # accounts is of List type with the items defined as Dictionary Type { 'accountID': 'accountIDValue',
        #                                                                     'validCash': 'validCashValue',
        #                                                                     'instrumentProfits':'instrumentProfitsValue'}
        # instrumentProfitsValue is of List type with the items {"instrumentID': 'instrumentIDValue',
        #                                                        'profit':'profitValue',
        #                                                        'profitPercentage':'profitPercentageValue'}
        self.__portfolio_accounts = {}
        self.__portfolio_accounts_item_name = [ACCOUNT_ID, VALID_CASH]
        self.__portfolio_account_profit_item_name = [INSTRUMENT_ID, DIRECTION, PRICE, QTY, TRADED_QTY,
                                                     PROFIT, PROFIT_PERCENTAGE]

        self.__stop_loss_setting = {}
        self.__stop_loss_para_list = [STOPLOSS_PRICE, STOPLOSS_STATUS, STOPLOSS_DATE]

        self.__account_related_item_name = [ACCOUNT_ID, PORTFOLIO_ID]
        self.__order_related_item_name = [ORDER_ID, EXCHANGE_ORDER_ID, INSTRUMENT_ID, CREATE_DATE, STATUS, DIRECTION,
                                          TRADED_QTY, QTY, PRICE, STATUS_MESSAGE, EXPIRATION_DATE]
        self.__event_engine = None
        self.__logger = logger

    def config(self, event_engine, account_properties):
        """
        This function is used to configure all the account-related information for the specific strategy
        :param event_engine: used to handle any registered event
        :param account_properties: all the necessary account-related properties for the specific strategy
        :return: None
        """
        account_list_ = []
        account_profit_list_ = []
        account_info_ = {}
        account_profit_info_ = {}
        self.__event_engine = event_engine
        if account_properties:
            account_data_list_ = dict_get(self.__portfolio_accounts, account_properties[PORTFOLIO_ID], DEFAULT_VALUE)
            if account_data_list_ == DEFAULT_VALUE:
                for key in account_properties:
                    if key in self.__portfolio_accounts_item_name:
                        account_info_[key] = account_properties[key]
                    elif key in self.__portfolio_account_profit_item_name:
                        account_profit_info_[key] = account_properties[key]
                if account_profit_info_:
                    account_profit_list_.append(account_profit_info_)
                    account_info_[INSTRUMENT_PROFITS] = account_profit_list_
                account_list_.append(account_info_)
                self.__portfolio_accounts[account_properties[PORTFOLIO_ID]] = account_list_

        self.__logger.info(ACCOUNT_CONFIG, account_properties[PORTFOLIO_ID], account_list_)
        self.__register()

    # -----------------------------------------------------------------------------------------------------------------
    def on_trade_data_update(self, event):
        """
        This function will be triggered every change on the price of the target listened.
        :param event: event includes some parameters which is used to update the existing trade_data
                       , or add a new trade_data for the specific account
        :return: None
        """
        event_data_ = event.even_param_
        order_data_list_ = []
        order_data_item_ = {}
        trade_data_ = {}

        try:
            self.__logger.debug(ACCOUNT_TRADE_DATA, self.__traded_records)
            self.__logger.info(ACCOUNT_TRADE_UPDATED, event_data_[ACCOUNT_ID], event_data_[ORDER_ID])
            trade_data_ = self.__traded_records[event_data_[ACCOUNT_ID]]
            is_order_id_exist = False
            update_order_data_item_ = {}
            new_order_data_item_ = {}
            order_data_list_ = trade_data_[ORDER_RECORDS]
            for order_data_item_ in order_data_list_:
                if order_data_item_[ORDER_ID] == event_data_[ORDER_ID]:
                    is_order_id_exist = True
                    update_order_data_item_ = order_data_item_
                    break

            for key, value in event_data_.items():
                self.__logger.debug(ACCOUNT_TRADE_EVENT, sys._getframe().f_code.co_name, key, value)
                if key in self.__account_related_item_name:
                    trade_data_[key] = value
                elif key in self.__order_related_item_name:
                    if is_order_id_exist:
                        update_order_data_item_[key] = value
                    else:
                        new_order_data_item_[key] = value
            if not is_order_id_exist:
                order_data_list_.append(new_order_data_item_)
        except KeyError:
            for key, value in event_data_.items():
                self.__logger.warning(ACCOUNT_TRADE_EVENT, sys._getframe().f_code.co_name, key, value)
                if key in self.__account_related_item_name:
                    trade_data_[key] = value
                elif key in self.__order_related_item_name:
                    order_data_item_[key] = value
            order_data_list_.append(order_data_item_)
            trade_data_[ORDER_RECORDS] = order_data_list_
            self.__traded_records[event_data_[ACCOUNT_ID]] = trade_data_

    # -----------------------------------------------------------------------------------------------------------------
    def on_profit_changed(self, event):
        """
        When the price of the target is changed, but not triggers any buy/sell operation,
        this function will be triggered
        :param event: event includes some parameters which is used to calculate profit/loss, then update the data
                       structure __portfolio_accounts
        :return: None
        """
        if event.even_param_:
            portfolio_id_ = event.even_param_[PORTFOLIO_ID]
            account_id_ = event.even_param_[ACCOUNT_ID]
            instrument_id_ = event.even_param_[INSTRUMENT_ID]
            current_price_ = event.even_param_[PRICE]
            self.__logger.info(ACCOUNT_PROFIT_CHANGED, account_id_, portfolio_id_, instrument_id_, current_price_)
            trade_data_ = self.__traded_records[account_id_]
            order_records_list_ = trade_data_[ORDER_RECORDS]
            for order_data_ in order_records_list_:
                self.__logger.debug(ACCOUNT_PROFIT_PARAM_INS, order_data_[INSTRUMENT_ID], instrument_id_)
                if order_data_[INSTRUMENT_ID] == instrument_id_:
                    profit_ = (current_price_ - order_data_[PRICE]) * order_data_[TRADED_QTY]
                    self.__logger.debug(ACCOUNT_PROFIT_CALC_PARAS, current_price_, order_data_[PRICE],
                                        order_data_[TRADED_QTY], profit_)
                    profit_percentage_ = format(profit_/(order_data_[PRICE] * order_data_[TRADED_QTY]), '.00%')
                    self.__logger.debug(ACCOUNT_PROFIT_PERC_PARAS, profit_percentage_)
                    profit_info_ = {PORTFOLIO_ID: portfolio_id_, ACCOUNT_ID: account_id_,
                                    INSTRUMENT_ID: instrument_id_, DIRECTION: order_data_[DIRECTION],
                                    PRICE: order_data_[PRICE], QTY: order_data_[QTY],
                                    TRADED_QTY: order_data_[TRADED_QTY],
                                    PROFIT: profit_, PROFIT_PERCENTAGE: profit_percentage_}
                    self.__update_portfolio_account(profit_info_)

    # -----------------------------------------------------------------------------------------------------------------
    def on_valid_cash_changed(self, event):
        """
        This function is to update the valid cash after the buy/sell operation
        :param event: event includes some parameters which is used to identify some one account
        :return: None
        """
        self.__logger.info(ACCOUNT_CASH_CHANGE, event.even_param_[ACCOUNT_ID])
        if event.even_param_:
            portfolio_id_ = event.even_param_[PORTFOLIO_ID]
            account_id_ = event.even_param_[ACCOUNT_ID]
            used_cash_ = event.even_param_[USED_CASH]
            account_list_ = self.__portfolio_accounts[portfolio_id_]
            self.__logger.debug(ACCOUNT_CASH_CHANGE_PARAS, portfolio_id_, account_id_, used_cash_)
            self.__logger.debug(PORTFOLIO_ACCOUNT_LIST, portfolio_id_, account_list_)
            for account_info_ in account_list_:
                if account_info_[ACCOUNT_ID] == account_id_:
                    account_info_[VALID_CASH] = account_info_[VALID_CASH] - used_cash_

    # -----------------------------------------------------------------------------------------------------------------
    def __update_portfolio_account(self, profit_info):
        """
        This function is used to update the account-related information under the some portfolio
        :param profit_info: some profit-related information is used to update the data structure __portfolio_accounts
        :return: None
        """
        self.__logger.info(PORTFOLIO_ACCOUNT_UPDATE, profit_info)
        if profit_info:
            account_data_list_ = dict_get(self.__portfolio_accounts, profit_info[PORTFOLIO_ID], DEFAULT_VALUE)
            self.__logger.debug(PORTFOLIO_ACCOUNT_LIST, account_data_list_)
            account_list_ = []
            account_profit_list_ = []
            account_info_ = {}
            account_profit_info_ = {}
            if account_data_list_ == DEFAULT_VALUE:
                for key, value in profit_info.items():
                    self.__logger.warning(PORTFOLIO_ACCOUNT_UPDATE_PARAS, sys._getframe().f_code.co_name, key, value)
                    if key in self.__portfolio_accounts_item_name:
                        account_info_[key] = profit_info[key]
                    elif key in self.__portfolio_account_profit_item_name:
                        account_profit_info_[key] = profit_info[key]

                account_profit_list_.append(account_profit_info_)
                account_info_[INSTRUMENT_PROFITS] = account_profit_list_
                account_list_.append(account_info_)
                self.__portfolio_accounts[profit_info[PORTFOLIO_ID]] = account_list_
            else:
                is_account_exist_ = False
                is_instrument_profit_exist_ = False
                for account_data_ in account_data_list_:
                    if account_data_[ACCOUNT_ID] == profit_info[ACCOUNT_ID]:
                        for key, value in profit_info.items():
                            self.__logger.debug(PORTFOLIO_ACCOUNT_UPDATE_PARAS, sys._getframe().f_code.co_name, key,
                                                value)
                            if key in self.__portfolio_accounts_item_name:
                                account_data_[key] = value
                            elif key in self.__portfolio_account_profit_item_name:
                                account_profit_list_ = account_data_[INSTRUMENT_PROFITS]
                                for account_profit_info_ in account_profit_list_:
                                    if account_profit_info_[INSTRUMENT_ID] == profit_info[INSTRUMENT_ID]:
                                        account_profit_info_[key] = profit_info[key]
                                        is_instrument_profit_exist_ = True
                        is_account_exist_ = True
                        break

                if not is_instrument_profit_exist_:
                    for key, value in profit_info.items():
                        if key in self.__portfolio_account_profit_item_name:
                            account_profit_info_[key] = value
                    if not is_account_exist_:
                        for key, value in profit_info.items():
                            if key in self.__portfolio_accounts_item_name:
                                account_info_[key] = value
                        account_profit_list_.append(account_profit_info_)
                        account_info_[INSTRUMENT_PROFITS] = account_profit_list_
                        account_data_list_.append(account_info_)
                    else:
                        account_profit_list_.append(account_profit_info_)

        self.__logger.debug(PORTFOLIO_CURR_ACCOUNT_LIST, self.__portfolio_accounts)

    def __register(self):
        """
        This function is used to register the event into the event engine.
        :return: None
        """
        self.__event_engine.register(EVENT_TRADE, self.on_trade_data_update)
        self.__event_engine.register(EVENT_PROFITCHANGED, self.on_profit_changed)
        self.__event_engine.register(EVENT_CASHCHANGED, self.on_valid_cash_changed)

    # -----------------------------------------------------------------------------------------------------------------
    def get_profit_info(self, portfolio_id, account_id):
        """
        This function is to get the account-related information based on the 2 parameters below
        :param portfolio_id: some portfolio ID
        :param account_id: some account ID
        :return: the valid cash for some account ID and the profit information about some instrument ID, and None if
                  portfolio ID or account ID is not existing
        """
        self.__logger.info(GET_PROFIT_INFO, account_id, portfolio_id)
        try:
            account_list_ = self.__portfolio_accounts[portfolio_id]
            self.__logger.debug(PORTFOLIO_ACCOUNT_LIST, portfolio_id, account_list_)
            for account_info_ in account_list_:
                if account_info_[ACCOUNT_ID] == account_id:
                    valid_cash_ = account_info_[VALID_CASH]
                    instrument_profit_ = account_info_[INSTRUMENT_PROFITS]
                    return {REMAINING_CASH: valid_cash_, ORDERS: instrument_profit_}

        except KeyError:
            self.__logger.error(ERR_PORTFOLIO_EXISTING, portfolio_id)
            return None

        return None

    # -----------------------------------------------------------------------------------------------------------------
    def get_valid_cash(self, portfolio_id, account_id):

        """
        This function is to get valid cash based on the 2 parameters below
        :param portfolio_id: some portfolio ID
        :param account_id: some account ID
        :return: the valid cash for some account ID
        """
        self.__logger.info(GET_VALID_CASH, account_id, portfolio_id)
        try:
            account_list_ = self.__portfolio_accounts[portfolio_id]
            self.__logger.debug(PORTFOLIO_ACCOUNT_LIST, portfolio_id, account_list_)
            for account_info_ in account_list_:
                if account_info_[ACCOUNT_ID] == account_id:
                    return account_info_[VALID_CASH]
        except KeyError:
            self.__logger.error(ERR_PORTFOLIO_EXISTING, portfolio_id)
            return 0

        return 0

    # -----------------------------------------------------------------------------------------------------------------
    def get_traded_qty(self, portfolio_id, account_id, instrument_id, direction=DIRECTION_LONG):

        """
        This function is used to get the traded quantity based on the 4 parameters below
        :param portfolio_id: some portfolio ID
        :param account_id: some account ID
        :param instrument_id: some instrument ID
        :param direction: LONG or SHORT
        :return:the traded quantity for some instrument
        """
        self.__logger.info(GET_TRADED_QTY, instrument_id, account_id, portfolio_id)
        try:
            trade_data_ = self.__traded_records[account_id]
            self.__logger.debug(GET_TRADED_RECORDS, account_id, trade_data_)
            order_list_ = trade_data_[ORDER_RECORDS]
            for order_info_ in order_list_:
                if order_info_[INSTRUMENT_ID] == instrument_id and order_info_[DIRECTION] == direction:
                    return order_info_[TRADED_QTY]
        except KeyError:
            self.__logger.error(ERR_ACCOUNT_EXISTING, account_id)
            return 0

        return 0

    # -----------------------------------------------------------------------------------------------------------------
    def get_not_fully_traded_orders(self, account_id):

        """
        This function is used to get those order ID which is not traded fully based on the account ID
        :param account_id: some account ID
        :return: order ID list which is not traded fully
        """
        order_id_list_ = []
        self.__logger.info(GET_NOT_FULLY_TRADED_QTY, account_id)
        try:
            trade_data_ = self.__traded_records[account_id]
            self.__logger.debug(GET_NOT_FULLY_TRADED_DATA, account_id, trade_data_)
            order_list = trade_data_[ORDER_RECORDS]
            for order_info_ in order_list:
                try:
                    if order_info_[QTY] != order_info_[TRADED_QTY]:
                        order_id_list_.append(order_info_[ORDER_ID])
                except KeyError:
                    order_id_list_.append(order_info_[ORDER_ID])
        except KeyError:
            self.__logger.error(ERR_ACCOUNT_EXISTING, account_id)
            pass

        return order_id_list_

# ----------------------------------------------------------------------------------------------------------------------
# The function test is used for the unit test


def test():
    defensive_logger = StrategyLog(".\..\logconf.ini", DEFENSIVE_LOGGER)
    ee = EventEngine(defensive_logger)
    # initial the logger for this strategy
    account_properties = {PORTFOLIO_ID: '01', ACCOUNT_ID: '00001', INSTRUMENT_ID: '2001', VALID_CASH: '100'}
    account_info = AccountInfo(defensive_logger)
    account_info.config(ee, account_properties)
    print(account_info.get_valid_cash(account_properties[PORTFOLIO_ID], account_properties[ACCOUNT_ID]))
    order_properties = {PORTFOLIO_ID: '01', ACCOUNT_ID: '00002', INSTRUMENT_ID: '2001', ORDER_ID: '1'}
    trade_event = AQIStrategyEvent(EVENT_PROFITCHANGED, order_properties)
    account_info.on_trade_data_update(trade_event)
    order_properties = {PORTFOLIO_ID: '01', ACCOUNT_ID: '00002', INSTRUMENT_ID: '2001', ORDER_ID: '1', QTY: 5}
    trade_event = AQIStrategyEvent(EVENT_PROFITCHANGED, order_properties)
    account_info.on_trade_data_update(trade_event)
    order_properties = {PORTFOLIO_ID: '01', ACCOUNT_ID: '00002', INSTRUMENT_ID: '2001', ORDER_ID: '2', QTY: 5}
    trade_event = AQIStrategyEvent(EVENT_PROFITCHANGED, order_properties)
    account_info.on_trade_data_update(trade_event)
    order_properties = {PORTFOLIO_ID: '01', ACCOUNT_ID: '00002', INSTRUMENT_ID: '2003', ORDER_ID: '3', QTY: 5}
    trade_event = AQIStrategyEvent(EVENT_PROFITCHANGED, order_properties)
    account_info.on_trade_data_update(trade_event)
    print(account_info.get_not_fully_traded_orders(order_properties[ACCOUNT_ID]))


if __name__ == '__main__':
    test()
