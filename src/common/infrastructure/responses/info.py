from src.common.domain.utils.is_not_none import is_not_none


class ResponseInfo:
    def __init__(self, code: str, message: str, data=None):
        self.code = code
        self.message = message
        self.data = data

    def to_dict(self):

        return (
            {"code": self.code, "message": self.message, "data": self.data}
            if is_not_none(self.data)
            else {"code": self.code, "message": self.message}
        )
