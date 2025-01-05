
from src.order.application.info.codes.order_info import OrderCodes
from src.common.domain.result.result import result_info_factory


set_order_status_info = result_info_factory(
    code=OrderCodes.SET_ORDER_STATUS, message="Order status set succesfully"
)
