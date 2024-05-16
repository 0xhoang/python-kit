from typing import Optional

from injector import inject
from werkzeug.exceptions import Unauthorized

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

    def check_permission(
        self, user: User, permission_name=None, supplier_id=None, msg=None
    ):
        if not self.has_permission(user, permission_name, supplier_id):
            raise Unauthorized(msg)

    def has_permission(self, user: User, permission_name, supplier_id) -> bool:
        if user.is_admin:
            return True
        is_satisfied_permission = True
        is_satisfied_supplier = True
        supplier_id_set = set()
        if permission_name:
            permission_role = self.role_base_repository.get_permission(
                user.id, permission_name
            )
            is_satisfied_permission = permission_role is not None
        if supplier_id and user.is_supplier:
            supplier_users = user.suppliers
            for supplier_user in supplier_users:
                supplier_id_set.add(supplier_user.supplier_id)
            is_satisfied_supplier = supplier_id in supplier_id_set
        return is_satisfied_permission and is_satisfied_supplier

    def get_by_email(self, email) -> dict:
        user = self.user_repo.get_by_email(email)

        result = UserResponse()
        result.id = user.id
        result.name = user.name

        return result.to_dict()

    def map_sso_to_sp_user(self, sso_user_id) -> User:
        sso_user_info = self.tiki_service.get_user_info_by_id(sso_user_id)
        user = self.get_by_email(sso_user_info.email)
        user.sso_id = sso_user_id
        self.user_repo.merge(user)
        return user
