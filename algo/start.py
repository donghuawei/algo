import logging.config

from flask import Flask, Blueprint
from algo import settings
from algo.api.route.app import ns as algo_app_namespace
from algo.api.route.subscriber import ns as algo_subscriber_namespace
from algo.api.route.order_mock import ns as algo_order_namespace
from algo.api.restplus import api
from service.algo_manager import algoMgr

app = Flask(__name__)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


def configure_app(flask_app):
    # flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SERVER_HOST'] = settings.FLASK_SERVER_HOST
    flask_app.config['SERVER_PORT'] = settings.FLASK_SERVER_PORT
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(algo_app_namespace)
    api.add_namespace(algo_subscriber_namespace)
    api.add_namespace(algo_order_namespace)
    flask_app.register_blueprint(blueprint)


def main():
    initialize_app(app)
    # log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(settings.FLASK_SERVER_HOST + ':' + settings.FLASK_SERVER_PORT))
    log.info('Algo Manager stauts: {}'.format(algoMgr.get_status()))
    app.run(host=settings.FLASK_SERVER_HOST, port=settings.FLASK_SERVER_PORT, debug=settings.FLASK_DEBUG)
    # app.run(debug=settings.FLASK_DEBUG)

if __name__ == "__main__":
    main()
