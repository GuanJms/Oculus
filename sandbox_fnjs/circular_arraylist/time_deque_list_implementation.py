class TimeDequeList:
    def __init__(self, max_time, unit):
        self.max_time = max_time
        self.unit = unit
        self.deque = []

    def append(self, value):
        self.deque.append(value)
        self.__remove_extra__()

    def __remove_extra__(self):
        while self._has_element_to_remove():
            self.deque.pop(0)

    def _has_element_to_remove(self):
        return self.max_time < (
            self.deque[-1].timestamp - self.deque[0].timestamp
        )

    def size(self):
        return len(self.deque)

    def __str__(self):
        return str(self.deque)