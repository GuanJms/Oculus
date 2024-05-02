from collections import deque
from ._circular_arraylist import CircularArrayList


class AutoDeque(CircularArrayList):
    def __init__(self):
        super().__init__()
        self._removed = deque()

    def __remove_extra__(self):
        self._removed.clear()
        while self._has_element_to_remove():
            self._removed.append(super().pop_left())
            self._count -= 1
        return self._removed

    def append(self, value):
        super().append(value)
        return self.__remove_extra__()

    def _has_element_to_remove(self):
        raise Exception("Implemented by subclass")

    def pop_left(self):
        raise Exception("Can't call pop left on an AutoDeque")
