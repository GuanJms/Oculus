from abc import ABC, abstractmethod


class DomainDistributor(ABC):

    @abstractmethod
    def tag(self, data):
        pass

    @abstractmethod
    def distribute(self, data):
        pass
