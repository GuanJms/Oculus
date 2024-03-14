from typing import Optional, List

from global_component_id_generator import GlobalComponentIDGenerator


class Asset:

    def __init__(self):
        self._id: Optional[str] = None
        self._ticker: Optional[str] = None
        self._type: Optional[str] = None
        self._expiration: Optional[int] = None
        self._price: Optional[float] = None
        self._quantity: Optional[int] = None
        self._average_cost: Optional[float] = None
        self._cost: Optional[list[float]] = None
        self._execution_order_list: list[ExecutionOrder] = []
        self._market_price_time: Optional[str] = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def value(self) -> float:
        return self._price * self._quantity

    @property
    def ticker(self) -> str:
        return self._ticker

    @property
    def type(self) -> str:
        return self._type

    @property
    def price(self) -> float:
        return self._price

    @property
    def quantity(self) -> int:
        return self._quantity

    @property
    def average_cost(self) -> float:
        return self._average_cost

    @property
    def cost(self) -> List[float]:
        return self._cost

    @property
    def execution_order_list(self) -> List[ExecutionOrder]:
        return self._execution_order_list

    @property
    def market_price_time(self):
        return self._market_price_time
