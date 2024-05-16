from dataclasses import field as fields
from typing import Type, ClassVar

from marshmallow import validate, Schema
from marshmallow_dataclass import dataclass
from dataclasses_json import DataClassJsonMixin

from constant.constant import ASC, DES


@dataclass
class SortCriterion(DataClassJsonMixin):
    field: str = fields(default="", metadata={})
    order: str = fields(default=ASC, metadata={"validate": validate.OneOf([ASC, DES])})
    Schema: ClassVar[Type[Schema]] = Schema
