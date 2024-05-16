from flask import Response
from injector import inject
from werkzeug.exceptions import BadRequest

from cmd.app.base import BaseResource
from service.user import UserService


class HelloController(BaseResource):
    @inject
    def __init__(self, user_svc: UserService):
        super().__init__()
        self.user_svc = user_svc

    def get(self):
        """
        Get promo purchase price by given condition
        ----
        tags:
            - Purchase Price
        parameters:
            - name: product_id
              in: query
              required: true
              description: the product id
            - name: supplier_id
              in: query
              required: true
              description: the supplier id
            - name: limit
              in: query
              required: true
              in: query
              required: false
            - name: page
              in: query
              required: false
            - name: order_by
              in: query
              required: false
        responses:
            200:
                description: The list of promo purchase price
                schema:
                    $ref: '#/definitions/PaginatedPurchaseUnitPrice'
        """
        user = self.user_svc.get_by_email("abc@yahoo.com")
        if user is None:
            raise BadRequest(
                "User not found"
            )

        return Response(
            response=user.to_json(),
            status=200,
            mimetype="application/json"
        )
