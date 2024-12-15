import dataclasses
from diator.response import Response

from user.application.models.user import UserRole, UserStatus

@dataclasses.dataclass(frozen=True, kw_only=True)
class FindOneUserReponse(Response):
    id: str = dataclasses.field(default=1)
    username: str = dataclasses.field()
    first_name: str = dataclasses.field()
    last_name: str = dataclasses.field()
    email: str = dataclasses.field()
    role: UserRole = dataclasses.field()
    status: UserStatus = dataclasses.field()