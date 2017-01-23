from algo.service.apiClient import place_order_api, get_order_status_api, cancel_order_api


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
    return place_order_api(order_data)


def sell(account_id, portfolio_id, instrument_id, direction, price, qty, tag):
    """
    construct order data
    :return:
    """
    order_data = {'accountID': account_id,
                  'portfolioID': portfolio_id,
                  'instrumentID': instrument_id,
                  'direction': direction,
                  'price': price,
                  'qty': -qty,
                  'tag': tag
                  }
    return place_order_api(order_data)

def cancel_order(order_id):
    cancel_order_api(order_id)


def get_order_status(order_id):
    return get_order_status_api(order_id)
