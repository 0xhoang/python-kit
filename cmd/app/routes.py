from cmd.app.base import rest_api
from cmd.app.hello import HelloController

rest_api.add_resource(HelloController, "/hello")
