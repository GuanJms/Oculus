from data_system.base_structure.deque.regulators._regulator import Regulator


class StaticMaxSizeRegulator(Regulator):
    def __init__(self, max_size: int):
        if max_size < 1 or not isinstance(max_size, int):
            raise ValueError("Max size cannot be less than 1 or not an integer.")
        self._max_size = max_size

    def check(self, deque):
        return self._max_size < len(deque)
