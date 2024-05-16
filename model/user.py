from datetime import datetime
from sqlalchemy import Column, String, Boolean, Integer, DateTime, text
from must.db import db


class User(db.Model):
    __tablename__ = "user"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    email: str = Column(String(255), nullable=False, index=True)
    password: str = Column(String(255))
    name: str = Column(String(255), nullable=False)
    created_at: datetime = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: datetime = Column(
        DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )
