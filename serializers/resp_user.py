from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin


@dataclass
class UserResponse(DataClassJsonMixin):
    id: int = field(default=False)
    name: str = field(default=False)
