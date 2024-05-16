from typing import Optional

from injector import inject
from model.user import User
from repository.user import UserRepository
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

    def get_by_email(self, email) -> dict:
        user = self.user_repo.get_by_email(email)
        result = UserResponse()
        result.id = user.id
        result.name = user.name

        return result.to_dict()
