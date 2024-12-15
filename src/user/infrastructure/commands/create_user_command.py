import dataclasses

from diator.requests import Request

from user.application.models.user import UserRole 

@dataclasses.dataclass(frozen=True, kw_only=True)
class CreateUserCommand(Request):
    username: str = dataclasses.field()
    password: str = dataclasses.field()
    first_name: str = dataclasses.field()
    last_name: str = dataclasses.field()
    email: str = dataclasses.field()
    role: UserRole = dataclasses.field()