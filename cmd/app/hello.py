from flask import Response, request
from injector import inject
from cmd.app.base import BaseResource
from serializers.req_user import UserReq
from service.user import UserService


class HelloController(BaseResource):
    @inject
    def __init__(self, user_svc: UserService):
        super().__init__()
        self.user_svc = user_svc

    def get(self):
        user = self.user_svc.get_by_email("abc@yahoo.com")

        return Response(
            response=user.to_json(),
            status=200,
            mimetype="application/json"
        )

    def post(self):
        body = UserReq.from_dict(request.get_json())
        user = self.user_svc.update(body)

        return Response(
            response=user.to_json(),
            status=200,
            mimetype="application/json"
        )
