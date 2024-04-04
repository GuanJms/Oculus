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
        self._bid: Optional['Decimal'] = None
        self._ask: Optional['Decimal'] = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def bid(self) -> Decimal:
        return self._bid

    @property
    def ask(self) -> Decimal:
        return self._ask

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

    def set_bid(self, bid: int | float | str | Decimal):
        self._bid = value_to_decimal_class(bid)

    def set_ask(self, ask: int | float | str | Decimal):
        self._ask = value_to_decimal_class(ask)
