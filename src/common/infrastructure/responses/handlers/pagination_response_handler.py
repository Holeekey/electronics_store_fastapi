from src.common.domain.result.result import ResultInfo
from src.common.infrastructure.responses.info import ResponseInfo
from src.common.infrastructure.responses.pagination_response import PaginationInfo, PaginationResponse


def pagination_response_handler(
        t,
        info: ResultInfo,
        pagination_info: PaginationInfo
    ):
    response_info = ResponseInfo(code=info.code, message=info.message, data=info.data)
    return PaginationResponse(
        info=response_info,
        pagination_info=pagination_info,
        response=t
    ).to_dict()