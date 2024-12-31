from src.common.domain.error.error import Error


class ApplicationError(Error):
    def __init__(self, message: str, code: str, info=None):
        super().__init__(message=message, code=code, kind="DOMAIN", info=info)


def application_error_factory(code: str, message: str):
    def func(info=None):
        return ApplicationError(message=message, code=code, info=info)

    return func
