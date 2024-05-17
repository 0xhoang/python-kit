from typing import Optional

from injector import inject
from werkzeug.exceptions import BadRequest

from model.user import User
from repository.user import UserRepository
from serializers.req_user import UserReq
from serializers.resp_user import UserResponse


class UserService:
    @inject
    def __init__(
        self,
        user_repo: UserRepository,
    ):
        self.user_repo = user_repo

    def get(self, id: int) -> Optional[User]:
        return self.user_repo.get(id)

    def get_by_email(self, email) -> UserResponse:
        user = self.user_repo.get_by_email(email)
        if user is None:
            raise BadRequest(
                "User not found"
            )

        result = UserResponse().adapt_from_model(user)

        return result

    def update(self, req: UserReq) -> UserResponse:
        user = self.user_repo.get_by_email(req.email)
        if user is None:
            raise BadRequest(
                "User not found"
            )

        # todo: update user with req data
        result = UserResponse().adapt_from_model(user)

        return result
