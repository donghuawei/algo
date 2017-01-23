"""
API client to invoke platform, to get account value/ positions...etc
"""
import requests
import json


def get_base_url():
    return "http://localhost:9000"


def place_order_api(order_data):
    url = get_base_url() + "/orders/mock"
    headers = {'content-type': 'application/json'}
    # get account and instrument information from algo_manager
    # data = {"accountID": 13, "direction": "long", "instrumentID": 541,
    # "portfolioID": 17, "price": 3110, "qty": 1, "tags": ["tag1"]}

    payload = json.dumps(order_data)
    response = requests.post(url, data=payload, headers=headers)
    return response.json()


def get_all_order_status_api():
    url = get_base_url() + "/orders"
    response = requests.get(url)
    return response.json()


def get_order_status_api(order_id):
    url = get_base_url() + "/orderByID?orderID=" + order_id
    response = requests.get(url)
    return response.json()


def cancel_order_api(order_id):
    url = get_base_url() + "/orders?ids=" + order_id
    requests.delete(url)

