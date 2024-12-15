import dataclasses
from diator.requests import Request

@dataclasses.dataclass(frozen=True, kw_only=True)
class FindOneUserQuery(Request):
    id: str = dataclasses.field(default=1)