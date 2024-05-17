from flask import Blueprint

api = Blueprint("api", "app", url_prefix="/v1")
public_api = Blueprint("public_api", "app", url_prefix="/v1/public")

from cmd.app import routes
