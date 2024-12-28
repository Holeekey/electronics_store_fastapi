from common.application.error.application_error import application_error_factory
from user.application.errors.codes.user_error_codes import UserErrorCodes


user_credentials_not_matching_error = application_error_factory(
  code= UserErrorCodes.INCORRECT_CREDENTIALS.value, message= "Credentials for user in request did not match"
)