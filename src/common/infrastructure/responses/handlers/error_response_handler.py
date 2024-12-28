from fastapi import HTTPException

from common.domain.error.error import Error


def error_response_handler(error: Error) -> Exception:

    status_code: int

    if error.code.endswith("NF"):
        status_code = 404
    elif error.code.endswith("UN"):
        status_code = 401
    else:
        status_code = 400

    detail = (
        {"code": error.code, "message": error.message, "info": error.info}
        if error.info
        else {
            "code": error.code,
            "message": error.message,
        }
    )

    return HTTPException(status_code=status_code, detail=detail)
