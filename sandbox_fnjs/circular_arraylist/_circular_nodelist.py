from typing import Optional


class CircularNodeList:
    def __init__(self):
        self._data = []
        self._start = 0
        self._count = 0
        self._display_sequential = False
        self._data_length_power = 0
        self._data_len_power: int = 0
        self._factory = None

    def __str__(self):
        if self._display_sequential:
            return f"Sequential Data: {str([self.get(i) for i in range(self._count)])}"
        else:
            return f"{self._data}"

    def size(self):
        return self._count

    def capacity(self):
        return len(self._data)

    def append(self, data):
        if self._count == len(self._data):
            self.set_capacity(self._count + 1)
        self._data[(self._start + self._count) & (len(self._data) - 1)].set(data)
        self._count += 1

    def pop_left(self):
        if self._count == 0:
            raise Exception("Can't remove elements from an empty list")
        element = self._data[self._start].pop()
        self._start = (self._start + 1) & (len(self._data) - 1)
        return element

    def set_capacity(self, new_size):
        new_size = self._find_next_capacity(new_size)
        if new_size == len(self._data):
            return
        if new_size < self._count:
            raise Exception(
                "Can't shrink list capacity to a size that is "
                + "less than current number of data points"
            )
        new_data = [None] * self._count + [self._factory.create() for _ in range(new_size - self._count)]

        for i in range(self._count):
            new_data[i] = self.get(i)
        self._data = new_data
        self._start = 0

    def _find_next_capacity(self, size):
        if size < 0:
            raise Exception("Illegal size")
        if size <= len(self._data):
            return len(self._data)
        if size == 0:
            return 1
        x = max(len(self._data), 1)
        while x < size:
            x *= 2
        return x

    def get(self, index):
        if index < 0:
            raise Exception("Illegal index")
        if index >= self._count:
            raise Exception("Index out of bounds")
        return self._data[(self._start + index) & (len(self._data) - 1)]

    def set_display_sequential(self, value: bool):
        if not isinstance(value, bool):
            raise Exception("Value must be a boolean")
        self._display_sequential = value

    def set_node_factory(self, factory):
        self._factory = factory
