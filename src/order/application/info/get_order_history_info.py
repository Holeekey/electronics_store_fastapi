
from src.order.application.info.codes.order_info import OrderCodes
from src.common.domain.result.result import result_info_factory


get_order_history_info = result_info_factory(
    code=OrderCodes.GET_ORDER_HISTORY, message="Order history found succesfully"
)
