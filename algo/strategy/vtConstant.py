# encoding: UTF-8

EMPTY_STRING = ''
EMPTY_UNICODE = u''
EMPTY_INT = 0
EMPTY_FLOAT = 0.0

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


