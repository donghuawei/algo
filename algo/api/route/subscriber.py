import logging

from flask import request
from flask_restplus import Resource
from algo.api.restplus import api
from algo.api.serializers import status, payload
from algo.service.algoManager import algoMgr
from algo.service.SubscriberService import subscribeInstrument


log = logging.getLogger(__name__)

ns = api.namespace('subscriber', description='subscribe data from platform')


@ns.route('/instrument')
class UpdateInstrument(Resource):

    @api.expect(payload)
    def post(self):
        """
        update instrument data.
        """
        params = request.json
        #log.log("get latest instrument: {}".format(params))
        subscribeInstrument(params)
        return None, 200


@ns.route('/account')
class UpdateAccount(Resource):

    @api.expect(payload)
    def post(self):
        """
        update account, cash value... etc
        """
        params = request.json
        log.log("get latest account information: {}".format(params))
        return None, 200


@ns.route('/position')
class UpdatePosition(Resource):

    @api.expect(payload)
    def post(self):
        """
        update position.
        """
        params = request.json
        log.log("get latest position: {}".format(params))
        return None, 200

