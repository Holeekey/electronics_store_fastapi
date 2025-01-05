
from src.order.application.info.codes.order_info import OrderCodes
from src.common.domain.result.result import result_info_factory


get_order_detail_info = result_info_factory(
    code=OrderCodes.GET_ORDER_DETAIL, message="Order detail found succesfully"
)
