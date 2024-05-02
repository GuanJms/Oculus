from sandbox.circular_arraylist.auto_deque import AutoDeque


class FixedSizeDeque(AutoDeque):
    def __init__(self, max_size):
        super().__init__()
        self._max_size = max_size
        self.set_capacity(max_size + 1)

    def _has_element_to_remove(self):
        return self._count > self._max_size

    def is_full(self):
        return self.size == self._max_size
