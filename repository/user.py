from typing import Optional, List

from flask_sqlalchemy import SQLAlchemy
from injector import inject

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
