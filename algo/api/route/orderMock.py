import logging

from flask import request
from flask_restplus import Resource
from algo.api.restplus import api
from algo.api.serializers import status, payload
from algo.service.algoManager import algoMgr
from algo.service.apiClient import place_order_api, get_all_order_status_api

log = logging.getLogger(__name__)

ns = api.namespace('order_mock', description='mock order request against raduga')


@ns.route('/order')
class Order(Resource):

    @api.expect(payload)
    def post(self):
        """
        place order.
        """
        order_data = request.json
        orders = place_order_api(order_data)
        return orders, 200

    def get(self):
        """
        get order status.
        """
        orders = get_all_order_status_api()
        return orders, 200

