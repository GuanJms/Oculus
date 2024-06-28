from collections import deque
from .auto_deque import AutoDeque


class MaximumLengthDeque(AutoDeque):
    def __init__(self, size):
        super().__init__()
        self._size = size

    def _has_element_to_remove(self):
        return self.size() > self._size
