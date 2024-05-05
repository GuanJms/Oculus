from .auto_deque import AutoDeque
from .regulators._regulator import Regulator


class RegulatorDeque(AutoDeque):
    def __init__(self):
        super().__init__()
        self._regulators = []

    def add_regulator(self, regulator: Regulator):
        self._regulators.append(regulator)

    def remove_regulator(self, regulator: Regulator):
        self._regulators.remove(regulator)

    def _has_element_to_remove(self):
        if not self._regulators:
            return False
        for regulator in self._regulators:
            if regulator.check(self):
                return True
        return False
