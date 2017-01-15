import logging

import json
from flask import request
from flask_restplus import Resource
from algo.api.restplus import api
from algo.api.serializers import status, payload
from algo.service.algoManager import algoMgr


log = logging.getLogger(__name__)

ns = api.namespace('app', description='Operations related to AQI app')


@ns.route('/start')
class StartApp(Resource):

    @api.marshal_with(status)
    @api.expect(payload)
    def post(self):
        """
        Start the app.
        """
        params = request.json
        log.info(params)
        algoMgr.start_app(params['config'])
        return {'status': algoMgr.get_status()}, 200


@ns.route('/stop')
class StopApp(Resource):

    @api.marshal_with(status)
    @api.expect(payload)
    def post(self):
        """
        Stop the app.
        """
        params = request.json
        log.info(params)
        algoMgr.stop_app()
        return {'status': algoMgr.get_status()}, 200


@ns.route('/suspend')
class SuspendApp(Resource):

    @api.marshal_with(status)
    def post(self):
        """
        Suspend the app.
        """
        algoMgr.suspend_app()
        return {'status': algoMgr.get_status()}


@ns.route('/resume')
class ResumeApp(Resource):

    @api.marshal_with(status)
    def post(self):
        """
        Resume the app to start the app again
        """
        algoMgr.resume_app()
        return {'status': algoMgr.get_status()}, 200


@ns.route('/status')
class Status(Resource):

    @api.marshal_with(status)
    def get(self):
        """
        Return the app status.
        """
        log.info(algoMgr.get_status())
        data = {'status': algoMgr.get_status()}
        return data, 200


@ns.route('/init')
class Status(Resource):

    @api.marshal_with(status)
    @api.expect(payload)
    def post(self):
        """
        initialise app, by setting configuration.
        """
        params = request.json
        log.info(params)

        log.info(algoMgr.get_status())
        data = {'status': algoMgr.get_status()}
        return data, 200


@ns.route('/config/update')
class Status(Resource):

    @api.marshal_with(status)
    @api.expect(payload)
    def post(self):
        """
        update app configuration .
        """
        params = request.json
        log.info(params)

        log.info(algoMgr.get_status())
        data = {'status': algoMgr.get_status()}
        return data, 200

