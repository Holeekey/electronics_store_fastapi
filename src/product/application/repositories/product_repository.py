from abc import ABCMeta, abstractmethod
from typing import Optional

from common.domain.result.result import Result
from product.domain.product import Product
from product.domain.value_objects.product_id import ProductId
from product.domain.value_objects.product_name import ProductName


class IProductRepository(metaclass=ABCMeta):

    @abstractmethod
    async def find_one(self, id: ProductId) -> Optional[Product]:
        pass

    @abstractmethod
    async def find_by_name(self, name: ProductName) -> Optional[Product]:
        pass

    @abstractmethod
    async def save(self, product: Product) -> Result[Product]:
        pass
