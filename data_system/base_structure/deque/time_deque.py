from typing import Optional

from .auto_deque import AutoDeque
from .._enums import TimeUnit


class TimeDeque(AutoDeque):
    def __init__(self, max_time, unit: Optional[str | TimeUnit] = None):
        super().__init__()
        self._unit = TimeUnit.get(unit) if unit else None
        self._max_time = max_time

    def _has_element_to_remove(self):
        return self._max_time < (
                self.get(self.size() - 1).timestamp - self.get(0).timestamp
        )
