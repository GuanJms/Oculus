from ._queue_calculator import QueueCalculator


class MaxMinCalculator(QueueCalculator):

    def __init__(self, target_param):
        super().__init__()
        self._max = None
        self._min = None
        self._max_node = None
        self._min_node = None
        self._target_param = target_param

    def add(self, node):
        super().add(node)
        value = self.get_value(node)
        if value is None:
            return
        if self._max is None or value > self._max:
            self._max = value
            self._max_node = node
        if self._min is None or value < self._min:
            self._min = value
            self._min_node = node

    def remove(self, node):
        super().remove(node)
        if node == self._max_node:
            self._max, self._max_node = self._find_max()
        if node == self._min_node:
            self._min, self._min_node = self._find_min()

    def _find_max(self):
        max = None
        max_node = None
        for node in self._queue:
            value = self.get_value(node)
            if max is None or value > max:
                max = value
                max_node = node
        return max, max_node

    def _find_min(self):
        min = None
        min_node = None
        for node in self._queue:
            value = self.get_value(node)
            if min is None or value < min:
                min = value
                min_node = node
        return min, min_node

    def get_value(self, node):
        return getattr(node, self._target_param, None)

    def __str__(self):
        return f"MinMaxCalculator: Max: {self._max}, Min: {self._min}"

    def __repr__(self):
        return self.__str__()
