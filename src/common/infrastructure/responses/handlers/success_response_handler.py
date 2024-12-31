from src.common.domain.result.result import ResultInfo
from src.common.infrastructure.responses.info import ResponseInfo
from src.common.infrastructure.responses.response import Response


def success_response_handler(t, info: ResultInfo) -> Response:
    response_info = ResponseInfo(code=info.code, message=info.message, data=info.data)
    return Response(info=response_info, response=t).to_dict()
