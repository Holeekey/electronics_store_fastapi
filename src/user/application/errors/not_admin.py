from common.application.error.application_error import application_error_factory
from user.application.errors.codes.user_error_codes import UserErrorCodes

user_is_not_admin_error = application_error_factory(
    code=UserErrorCodes.NOT_ADMIN.value, message="User is not an admin"
)
