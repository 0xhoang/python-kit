from typing import Optional, List

from flask_sqlalchemy import SQLAlchemy
from injector import inject
from sqlalchemy import text

from model.user import User
from repository.base import BaseRepository


class UserRepository(BaseRepository[User]):
    @inject
    def __init__(self, db: SQLAlchemy):
        super(UserRepository, self).__init__(db)

    def get_by_email(self, email) -> Optional[User]:
        query = self._get_base_query()
        query = query.filter(User.email == email)

        return query.one_or_none()

    def _get_base_query(self):
        query = self.db.session.query(User)
        return query

    def find_emails_by_permission(self, permission):
        query = """
        select u.email, u.name
        from user as u
        inner join user_role as ur on u.id = ur.user_id
        inner join permission_role as pr on ur.role_id = pr.role_id
        inner join permissions p on pr.permission_id = p.id
        where p.name = :permission
        and u.status = 1"""

        return self.db.engine.execute(text(query), {"permission": permission})

    def find_users_of_suppliers(self, supplier_id: int) -> List[User]:
        # query = self.db.session.query(User)
        # query = query.join(UserSupplier, UserSupplier.user_id == User.id).filter(
        #     UserSupplier.supplier_id == supplier_id
        # )
        # return query.all()
        return []
