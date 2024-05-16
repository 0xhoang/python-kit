import dataclasses
from marshmallow import validate, Schema, fields, ValidationError
from marshmallow_dataclass import dataclass
from typing import Optional, Type, ClassVar, List
from dataclasses_json import DataClassJsonMixin

from constant.constant import ASC, DES


@dataclass
class SortCriterion(DataClassJsonMixin):
    field: str = dataclasses.field(default="", metadata={})
    order: str = dataclasses.field(
        default=ASC, metadata={"validate": validate.OneOf([ASC, DES])}
    )
    Schema: ClassVar[Type[Schema]] = Schema
