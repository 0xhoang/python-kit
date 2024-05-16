from dataclasses import field
from dataclasses_json import DataClassJsonMixin
from marshmallow_dataclass import dataclass

from serializers.base import BaseModelSchema


@dataclass
class UserResponse(BaseModelSchema):
    id: int = field(default=False)
    name: str = field(default=False)
