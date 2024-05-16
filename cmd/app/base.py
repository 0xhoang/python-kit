import logging
from flask import current_app, jsonify
from flask_restful import Resource, reqparse, Api
from werkzeug.exceptions import HTTPException

from cmd.app import api, public_api


class BaseResource(Resource):
    """
    Base Resource for making REST API authenticated and authorized.
    """

    def __init__(self):
        super(BaseResource, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.is_testing = current_app.config.get
        self.logger = logging.getLogger(__name__)
        self.sso_user_id = None
        self.user_id = None
        self.user_email = None
        self.user = None
        self.jwt_token = None
        # self.py_jwk_client: PyJWKClient = current_app.injector.injector.get(PyJWKClient)

        # self.user_service: UserService = current_app.injector.injector.get(UserService)

        # self.init_session()


class CustomAPI(Api):
    def handle_error(self, e):
        if isinstance(e, HTTPException):
            response = {
                "code": e.code,
                "message": e.description,
            }
            return jsonify(response), e.code

        # default error handling
        response = {
            "code": 500,
            "message": "internal server error",
        }

        logging.error('internal server error: %s', e)

        return jsonify(response), 500


rest_api = CustomAPI(api, decorators=[])
rest_public_api = CustomAPI(public_api, decorators=[])
