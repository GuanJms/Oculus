from .auto_deque import AutoDeque


class AccDeque(AutoDeque):
    def _has_element_to_remove(self):
        return False
