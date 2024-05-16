from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(
    session_options={"autoflush": True, "expire_on_commit": False}
)


def init_db(app):
    db.init_app(app)
    db.app = app

    from sqlalchemy.orm import configure_mappers
    configure_mappers()
