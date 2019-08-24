import logging
from custom_api.restplus import api
from flask_restplus import Resource, cors
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from custom_api.endpoints.utils.parsers import login_arguments_parser
from custom_api.endpoints.utils import mongo_to_dict
from custom_api.models.user import UserBot
import os


log = logging.getLogger(__name__)
ns = api.namespace('auth', description='Authentication endpoint')


@ns.route('/')
class Index(Resource):

    @api.expect(login_arguments_parser, validate=True)
    @cors.crossdomain(origin='*')
    def post(self):
        '''

        return: this functions is used to actually generate the token
        '''
        args = request.json
        username = args.get('username', None)
        password = args.get('password', None)
        loading_user = UserBot.get_user_with_username_and_password(username, password)
        if loading_user is None:
            response = jsonify({"msg": "Error en usuario o contraseña", "code": 401})
            response.status_code = 401
            return response

        if not loading_user.active:
            response = jsonify({"msg": "El usuario ha sido bloqueado", "code": 401})
            response.status_code = 401
            return response

        response = jsonify({'access_token': create_access_token(identity=loading_user.username), "code": 200})
        response.status_code = 200
        return response

    def options(self):
        return {'Allow': 'POST'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                "Access-Control-Allow-Headers":
                    "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
                }
