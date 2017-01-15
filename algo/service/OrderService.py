from algo.service.apiClient import place_order, get_order_status


def buy(account_id, portfolio_id, instrument_id, direction, price, qty, tag):
    """
    construct order data

    {"accountID": 13, "direction": "long", "instrumentID": 541, "portfolioID": 17, "price": 3110, "qty": 1, "tags": ["tag1"]}

    :return:
    """
    order_data = {'accountID': account_id,
                  'portfolioID': portfolio_id,
                  'instrumentID': instrument_id,
                  'direction': direction,
                  'price':  price,
                  'qty': qty,
                  'tag': tag
                  }
    place_order(order_data)


def sell(account_id, portfolio_id, instrument_id, direction, price, qty, tag):
    """
    construct order data
    {"accountID": 13, "direction": "long", "instrumentID": 541, "portfolioID": 17, "price": 3110, "qty": 1, "tags": ["tag1"]}
    :return:
    """
    order_data = {'accountID': account_id,
                  'portfolioID': portfolio_id,
                  'instrumentID': instrument_id,
                  'direction': direction,
                  'price': -price,
                  'qty': qty,
                  'tag': tag
                  }
    place_order(order_data)


def get_order_status(order_id):
    get_order_status(order_id)
