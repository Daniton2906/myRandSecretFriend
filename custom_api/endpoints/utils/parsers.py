from flask_restplus import reqparse


login_arguments_parser = reqparse.RequestParser()
login_arguments_parser.add_argument('Credentials', type=str, required=True, help='Username and password are required',
                                    location='json')
