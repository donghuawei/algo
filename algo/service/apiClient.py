"""
API client to invoke platform, to get account value/ positions...etc
"""
import requests
import json
from algo.service.algoManager import algoMgr

base_url = "http://localhost:9000"


def place_order(order_data):
    url = base_url + "/orders"
    headers = {'content-type': 'application/json'}
    # get account and instrument information from algo_manager
    # data = {"accountID": 13, "direction": "long", "instrumentID": 541,
    # "portfolioID": 17, "price": 3110, "qty": 1, "tags": ["tag1"]}

    payload = json.dumps([order_data])
    response = requests.post(url, data=payload, headers=headers)
    return response.json()


def get_order_status(order_id):
    url = base_url + "/orders?orderIDs" + order_id
    headers = {'content-type': 'application/json'}
    response = requests.get(url)
    return response.json()

