from uuid import UUID
from product.domain.value_objects.product_id import ProductId
from shopping_cart.domain.value_objects.shopping_cart_item_quantity import ShoppingCartItemQuantity
from src.common.domain.value_object.value_object import ValueObject
from src.user.domain.client.errors.invalid_client_id import invalid_client_id_error


class ShoppingCartItem(ValueObject):
    def __init__(
        self,
        product_id: ProductId,
        quantity: ShoppingCartItemQuantity
    ) -> None:
        self._product_id = product_id
        self._quantity = quantity
        self.validate()

    @property
    def quantity(self) -> ShoppingCartItemQuantity:
        return self._quantity
    
    @property
    def product_id(self) -> ProductId:
        return self._product_id

    def validate(self) -> None:
        self._product_id.validate()
        self._quantity.validate()

    def __eq__(self, other: "ShoppingCartItem") -> bool:
        return self._quantity == other.quantity and self._product_id == other.product_id 