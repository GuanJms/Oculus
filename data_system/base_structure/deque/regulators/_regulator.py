from abc import ABC, abstractmethod


class Regulator(ABC):
    @abstractmethod
    def check(self, deque):
        raise Exception("Check method should be implemented in the child class")
