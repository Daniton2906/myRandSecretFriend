import logging
import traceback
from flask_restplus import Api, cors
from flask import current_app, url_for, render_template
from mongoengine import DoesNotExist

log = logging.getLogger(__name__)

api = Api(version='0.1', title='Api Template',
          description='A description for a custom custom_api with swagger library ')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not current_app.config['DEBUG']:
        return {'message': message}, 500


@api.errorhandler(DoesNotExist)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404


@api.documentation
@cors.crossdomain(origin='*')
def custom_ui():
    specs_path = url_for(api.endpoint('specs'))
    return render_template('swagger-ui.html', title=api.title,
                           specs_url=specs_path)
