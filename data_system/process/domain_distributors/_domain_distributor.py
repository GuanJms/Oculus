from abc import ABC, abstractmethod


class DomainDistributor(ABC):
    @abstractmethod
    def distribute(self, data: dict):
        pass
