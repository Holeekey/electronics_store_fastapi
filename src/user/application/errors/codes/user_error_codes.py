from enum import Enum


class UserErrorCodes(Enum):
    USERNAME_ALREADY_EXISTS = "US-E-001"
    EMAIL_ALREADY_EXISTS = "US-E-002"
    INVALID_CREDENTIALS = "US-E-003"
    INCORRECT_CREDENTIALS = "US-E-004"
    NOT_MANAGER = "US-E-005"
    NOT_FOUND = "US-E-NF"
    SUSPENDED = "US-E-UN"
