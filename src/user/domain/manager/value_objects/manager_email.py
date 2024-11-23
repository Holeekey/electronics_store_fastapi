from common.domain.value_object.value_object import ValueObject
from ..errors.invalid_manager_email import invalid_manager_email_error

import re

EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"
# EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


class ManagerEmail(ValueObject):
    def __init__(self, email: str) -> None:
        self.value = email
        self.validate()

    @property
    def email(self) -> str:
        return self.value

    def validate(self) -> None:
        if not re.fullmatch(EMAIL_REGEX, self.email):
            raise invalid_manager_email_error()

    def __eq__(self, other: "ManagerEmail") -> bool:
        return self.value == other.id
