from dataclasses import field
from dataclasses_json import DataClassJsonMixin
from marshmallow_dataclass import dataclass


@dataclass
class UserReq(DataClassJsonMixin):
    id: int = field(default=False)
    email: str = field(default=False)
    name: str = field(default=False)
