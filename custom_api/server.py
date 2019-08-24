import logging.config
import os
from flask import Flask, Blueprint
from flask_compress import Compress
from custom_api.endpoints.auth import ns as ns_initial
from custom_api.utils import bcrypt
from custom_api.utils import mail
from custom_api.restplus import api
from flask_jwt_extended import JWTManager
from werkzeug.contrib.fixers import ProxyFix
import datetime


def create_app(config=None, logging_config=None):
    """
    Crea la aplicacion
    :param config: path del archivo de configuracion
    """

    app = Flask(
        __name__,
        static_url_path='',
        static_folder="./static",
        template_folder="./static",
    )
    if logging_config is None:
        logging.config.fileConfig('custom_api/logging.conf', disable_existing_loggers=False)
    if config is None:
        config = os.path.join(os.getcwd(), 'custom_api/config.ini')
    elif os.path.exists(os.path.join(os.getcwd(), config)):
        config = os.path.join(os.getcwd(), config)
    else:
        raise FileExistsError('config.ini not found')
    app.config.from_pyfile(config)
    # setting environ variables for mongo db (using forge module)
    if 'MONGO_DB' not in os.environ:
        os.environ['MONGO_DB'] = app.config['MONGODB_SETTINGS'][0]['db']
    if 'MONGO_HOST' not in os.environ:
        os.environ['MONGO_HOST'] = app.config['MONGODB_SETTINGS'][0]['host']

    if not app.config['SHOW_DOCUMENTATION']:
        api._doc = False
    blueprint = Blueprint('custom_api', __name__, url_prefix='/custom_api')
    api.init_app(blueprint)
    add_namespaces(api)
    app.register_blueprint(blueprint)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=10)
    jwt = JWTManager(app)
    bcrypt.init_app(app)
    set_email_params(app)
    mail.init_app(app)
    Compress(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    return app


def add_namespaces(my_api):
    my_api.add_namespace(ns_initial)


def set_email_params(app):
    app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME'] if 'MAIL_USERNAME' in os.environ \
        else app.config['MAIL_USERNAME']
    app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD'] if 'MAIL_PASSWORD' in os.environ \
        else app.config['MAIL_PASSWORD']
    app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER'] if 'MAIL_SERVER' in os.environ \
        else app.config['MAIL_SERVER']
    app.config['MAIL_PORT'] = os.environ['MAIL_PORT'] if 'MAIL_PORT' in os.environ \
        else app.config['MAIL_PORT']

    tls = app.config['MAIL_USE_TLS']
    ssl = app.config['MAIL_USE_SSL']

    if 'MAIL_USE_TLS' in os.environ and os.environ['MAIL_USE_TLS'] == 'False':
        tls = False
    if 'MAIL_USE_TLS' in os.environ and os.environ['MAIL_USE_TLS'] == 'True':
        tls = True

    if 'MAIL_USE_SSL' in os.environ and os.environ['MAIL_USE_SSL'] == 'False':
        ssl = False
    if 'MAIL_USE_SSL' in os.environ and os.environ['MAIL_USE_SSL'] == 'True':
        ssl = True

    app.config['MAIL_USE_TLS'] = tls
    app.config['MAIL_USE_SSL'] = ssl
