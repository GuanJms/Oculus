from abc import abstractmethod
from decimal import Decimal
from typing import Optional, List

from ..time_basics import Time, Timeline
from .._enums import AssetType
from ..utils import value_to_decimal_class
from utils.global_id import GlobalComponentIDGenerator


class Asset:

    def __init__(self):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._ticker: Optional[str] = None
        self._type: Optional[AssetType] = None
        self._expiration: Optional[int] = None
        self._price: Optional['Decimal'] = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def ticker(self) -> str:
        return self._ticker

    @property
    def type(self) -> AssetType:
        return self._type

    @property
    def price(self) -> Decimal:
        return self._price

    def set_tick(self, tick: str):
        self._ticker = tick

    def set_price(self, price: int | float | str | Decimal):
        self._price = value_to_decimal_class(price)
