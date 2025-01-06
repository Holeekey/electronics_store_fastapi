
from src.order.application.info.codes.order_info import OrderCodes
from src.common.domain.result.result import result_info_factory


create_order_info = result_info_factory(
    code=OrderCodes.ORDER_CREATED, message="Order created succesfully"
)
