import json
import os
from sqlalchemy.pool import QueuePool

from must.json_encoder import CustomJSONEncoder

full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)


class Config:
    """Base configuration."""
    DEBUG = bool(os.getenv("DEBUG", 0))
    DB_SCHEMA = os.getenv("DB_SCHEMA", "mysql+mysqldb")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "12345678")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "byteweaver")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        "%s://%s:%s@%s:%s/%s?charset=utf8"
        % (DB_SCHEMA, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME),
    )

    SQLALCHEMY_ENGINE_OPTIONS = {
        "poolclass": QueuePool,
        "pool_size": 3,
        "pool_recycle": 3600,
        "pool_pre_ping": True,
        "json_serializer": lambda obj: json.dumps(
            obj, ensure_ascii=False,
            cls=CustomJSONEncoder
        ),
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SWAGGER = {
        "version": "1.0.1",
        "title": "Optimus Supplier Portal",
        "description": "The new backend service of Supplier Portal",
    }

    SENTRY_DSN = os.environ.get("SENTRY_DSN", "")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "DEVELOP").upper()


class WorkerConfig(Config):
    pass
