from abc import ABCMeta, abstractmethod
from typing import Optional, List

from src.common.domain.result.result import Result
from src.product.domain.product import Product
from src.product.domain.value_objects.product_id import ProductId
from src.product.domain.value_objects.product_name import ProductName


class IProductRepository(metaclass=ABCMeta):

    @abstractmethod
    async def find_one(self, id: ProductId) -> Optional[Product]:
        pass

    @abstractmethod
    async def find_many(self, page:int = 1, per_page:int = 5) -> List[Product]:
        pass

    @abstractmethod
    async def find_by_name(self, name: ProductName) -> Optional[Product]:
        pass

    @abstractmethod
    async def update(self, id: ProductId, new_product: Product) -> Result[Product]:
        pass

    @abstractmethod
    async def save(self, product: Product) -> Result[Product]:
        pass

    @abstractmethod
    async def delete(self, product: Product) -> Result[str]:
        pass