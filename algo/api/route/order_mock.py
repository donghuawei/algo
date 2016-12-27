import logging

from flask import request
from flask_restplus import Resource
from algo.api.restplus import api
from algo.api.serializers import status, payload
from algo.service.algo_manager import algoMgr
from algo.service.api_client import place_order, get_order_status

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
        orders = place_order(order_data)
        return orders, 200

    def get(self):
        """
        get order status.
        """
        orders = get_order_status()
        return orders, 200

