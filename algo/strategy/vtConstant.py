# encoding: UTF-8

EMPTY_STRING = ''
EMPTY_UNICODE = u''
EMPTY_INT = 0
EMPTY_FLOAT = 0.0

# Below constants are for the defensive strategy

PORTFOLIO_ID = 'portfolioID'
ACCOUNT_ID = 'accountID'
VALID_CASH = 'initialFund'
USED_CASH = 'usedCash'
REMAINING_CASH = 'remainingCash'
INSTRUMENT_PROFITS = 'instrumentProfits'
PROFIT = 'profit'
PROFIT_PERCENTAGE = 'profitPercentage'
ORDER_RECORDS = 'orderRecords'
ORDERS = 'orders'
ORDER_ID = 'orderID'
EXCHANGE_ORDER_ID = 'exchangeOrderID'
INSTRUMENT_ID = 'instrumentID'
CREATE_DATE = 'createDate'
STATUS = 'status'
DIRECTION = 'direction'
TRADED_QTY = 'tradedQty'
QTY = 'qty'
PRICE = 'price'
VOLUME = 'volume'
STATUS_MESSAGE = 'statusMessage'
TAG = 'tag'
EXPIRATION_DATE = 'expirationDate'
OPEN_PRICE = 'openPrice'
OPEN_VOLUME = 'openVolume'
STOPLOSS_PRICE = 'stopLossPrice'
STOPLOSS_STATUS = 'stopLossStatus'
STOPLOSS_DATE = 'stopLossDate'
CLOSE_PARAMS = 'closeParams'
OPEN_STATUS = 'openStatus'
CLOSE_STATUS = 'closeStatus'
STOPLOSS_STATUS = 'stopLossStatus'
OPEN_STATUS_INITIAL = '0'                         # Strategy maybe not running or not trigger the open operation
OPEN_STATUS_REQ = '1'                            # Strategy trigger the open operation with a request
OPEN_STATUS_PARTIAL = '2'                        # Strategy trigger the open operation, and partially traded
OPEN_STATUS_FULL = '3'                           # Strategy trigger the open operation, and fully traded
CLOSE_STATUS_INITIAL = '0'                        # Strategy maybe not running or not trigger the close operation
CLOSE_STATUS_REQ = '1'                           # Strategy trigger the close operation with a request
CLOSE_STATUS_PARTIAL = '2'                       # Strategy trigger the close operation, but partially traded
CLOSE_STATUS_FULL = '3'                          # Strategy trigger the close operation, and fully traded
STOPLOSS_STATUS_INITIAL = '0'                     # Strategy not trigger stoploss condition
STOPLOSS_STATUS_TRIGGER = '1'                    # Strategy trigger the stoploss condition
DIRECTION_LONG = 'long'                         # Up Trend
DIRECTION_SHORT = 'short'                       # Down Trend
TAG_DEFAULT_VALUE = ''
CLOSE_PRICE_0 = 'close_price_0'                  # close price at the #1 time
CLOSE_VOLUME_0 = 'close_volume_0'                # close volume at the #1 time
CLOSE_PRICE_1 = 'close_price_1'                  # close price at the #2 time
CLOSE_VOLUME_1 = 'close_volume_1'                # close volume at the #2 time
CLOSE_PRICE_2 = 'close_price_2'                  # close price at the #3 time
CLOSE_VOLUME_2 = 'close_volume_2'                # close volume at the #3 time
CLOSE_PRICE_3 = 'close_price_3'                  # close price at the #4 time
CLOSE_VOLUME_3 = 'close_volume_3'                # close volume at the #4 time

DEFAULT_VALUE = '-1'

LOG_CONFIG_FILE = 'logconf.ini'
DEFENSIVE_LOGGER = 'defensive'                      #the section name in the logconf.ini

# Below are some message showing what happened to developer

EVENT_START = 'Event engine started'
EVENT_STOP = 'Event engine stopped'
EVENT_REGISTER = 'Registering the handler for the event[%s]'
EVENT_UNREGISTER = 'Unregistering the handler for the event[%s]'
EVENT_IN_QUEUE = "Event[%s] is putting in the event queue"

ACCOUNT_CONFIG = 'The account info of the portfolio[%s] is [%s]'
ACCOUNT_TRADE_UPDATED = 'The trade data of the order id[%s] under the account[%s] will be updated/added'
ACCOUNT_TRADE_DATA = 'All the trade data for all the accounts is [%s]'
ACCOUNT_TRADE_EVENT = 'The key,value of parameters in the event in the function[%s] are: [%s],[%s]'

ACCOUNT_PROFIT_CHANGED = 'The profile of the account[%s] under the portfolio[%s] is being changed ' \
                         'due to the price change, the current price of the instrument[%s] is [%s]'
ACCOUNT_PROFIT_PARAM_INS = 'The instrument ID in the _order_data is [%s], the compared instrument ID is [%s]'
ACCOUNT_PROFIT_CALC_PARAS = 'Current price:[%s], Old price:[%s], Traded QTY:[%s], Profit:[%s]'
ACCOUNT_PROFIT_PERC_PARAS = 'The percentage of profit is:[%s]'
ACCOUNT_CASH_CHANGE = 'The valid cash is being changed for the account[%s]'
ACCOUNT_CASH_CHANGE_PARAS = 'Portfolio ID:[%s], Account ID:[%s], Used Cash[%s]'
PORTFOLIO_ACCOUNT_LIST = 'The account list for the portfolio ID[%s] is [%s]'
PORTFOLIO_ACCOUNT_UPDATE = 'The parameters used to update the account information are: [%s]'
PORTFOLIO_ACCOUNT_UPDATE_PARAS = 'The key,value of parameters in the event in the function[%s] are: [%s],[%s]'
PORTFOLIO_CURR_ACCOUNT_LIST = 'The current account list in the portfolio is [%s]'

GET_PROFIT_INFO = 'Getting the profit info of the account ID[%s] under the portfolio ID[%s]'

GET_VALID_CASH = 'Getting the valid cash of the account ID[%s] under the portfolio ID[%s]'

GET_TRADED_QTY = 'Getting the traded quantity of the instrument ID[%s] in the account ID[%s] under the portfolio ID[%s]'
GET_TRADED_RECORDS = 'The traded data in the account ID[%s] is [%s]'

GET_NOT_FULLY_TRADED_QTY = 'Getting the not-traded quantity in the account ID[%s]'
GET_NOT_FULLY_TRADED_DATA = 'The traded data in the account ID[%s] is [%s]'


ERR_PORTFOLIO_EXISTING = 'The portfolio ID[%s] is not existing'
ERR_ACCOUNT_EXISTING = 'The account ID[%s] is not existing'

DEFENSIVE_SETTING_PARMS = 'The setting parameters for this strategy are: %s'
DEFENSIVE_TICK = 'The onTick function is being triggered with the event[%s]'
DEFENSIVE_BUY = 'The event[EVENT_BUY] is being triggered with the params[%s]'
DEFENSIVE_SELL = 'The event[EVENT_SELL] is being triggered with the params[%s]'
DEFENSIVE_BUY_PERFORM = 'The buy operation will be performed with the params[%s]'
DEFENSIVE_SELL_PERFORM = 'The sell operation will be performed with the params[%s]'
DEFENSIVE_CASH_CHANGE = 'The event[EVENT_CASHCHANGED] is being triggered with the params[%s]'
DEFENSIVE_PROFIT_CHANGE = 'The event[EVENT_PROFITCHANGED] is being triggered with the params[%s]'
DEFENSIVE_TRADE = 'The event[EVENT_TRADE] is being triggered with the params[%s]'
DEFENSIVE_INSTR_TRADED_QTY = 'The quantity of the instrument ID[%s] traded successfully is [%s]'
DEFENSIVE_GET_ORDER_STATUS = 'Getting the order''status in the account ID[%s]'

STRATEGY_CONFIG = 'The strategy is being configured'
STRATEGY_OPEN = 'The strategy will perform the open action'
STRATEGY_CLOSE = 'The strategy will perform the close action'





