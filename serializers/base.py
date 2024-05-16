from typing import Type

from dataclasses_json import DataClassJsonMixin
from flask_sqlalchemy.model import Model
from marshmallow_dataclass import dataclass


@dataclass
class BaseModelSchema(DataClassJsonMixin):
    @classmethod
    def adapt_from_model(cls, model: Type[Model]):
        if not model:
            return None
        dto = cls()
        for key, value in model.__dict__.items():
            setattr(dto, key, value)
        return dto
