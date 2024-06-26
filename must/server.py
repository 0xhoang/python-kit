import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask import Response
from flask_injector import FlaskInjector, request
from flask_sqlalchemy import SQLAlchemy
from injector import singleton

from .json_encoder import CustomJSONEncoder
from cmd.app import api, public_api
from cmd.app.base import rest_public_api, rest_api
from .db import init_db, db

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

cors = CORS(expose_headers=["Content-Type", "Authorization", "X-Request-ID"])

pythonkit_injector = None


def create_app(config_name="config.config.AppConfig", **kwargs):
    app = Flask(__name__)
    app.config.from_object(config_name)
    app.config["RESTFUL_JSON"] = {"cls": CustomJSONEncoder}
    app.json_encoder = CustomJSONEncoder

    init_db(app)
    init_cors(app)
    # init_swagger(app)
    # metrics = PrometheusMetrics(app)

    app.register_blueprint(api)
    app.register_blueprint(public_api)

    rest_api.init_app(app)
    rest_public_api.init_app(app)

    modules = kwargs.get("modules")
    injector = kwargs.get("injector")
    init_flask_injector(app, modules=modules, injector=injector)

    return app


def init_cors(app):
    cors.init_app(app)


def injector_default(binder):
    binder.bind(SQLAlchemy, to=db, scope=singleton)
    binder.bind(Response, to=Response, scope=request)


def init_flask_injector(app, modules=None, injector=None):
    global pythonkit_injector

    injected_modules = [injector_default]
    if modules:
        injected_modules = modules

    pythonkit_injector = FlaskInjector(app=app, modules=injected_modules, injector=injector)
    app.injector = pythonkit_injector
