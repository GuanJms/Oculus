from typing import Optional

from sandbox.circular_arraylist.node_auto_deque import NodeAutoDeque
from sandbox.circular_arraylist._enums import TimeUnit


class NodeTimeDeque(NodeAutoDeque):
    def __init__(self, max_time, unit: Optional[str | TimeUnit] = None):
        super().__init__()
        self._unit = TimeUnit.get(unit) if unit else None
        self._max_time = max_time

    def _has_element_to_remove(self):
        return self._max_time < (
                self.get(self.size() - 1).timestamp - self.get(0).timestamp
        )
