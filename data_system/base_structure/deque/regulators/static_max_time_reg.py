from typing import Optional

from data_system._enums import TimeUnit
from data_system.base_structure.deque.regulators._regulator import Regulator


class StaticMaxTimeRegulator(Regulator):
    def __init__(self, max_time: float, unit: Optional[str | TimeUnit] = None):
        self._unit = TimeUnit.get(unit) if unit else None
        self._max_time = max_time

    def check(self, deque):
        return self._max_time < (
                deque.get(deque.size() - 1).timestamp - deque.get(0).timestamp
        )

