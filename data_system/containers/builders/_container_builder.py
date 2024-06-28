from abc import ABC, abstractmethod


class ContainerBuilder(ABC):
    @abstractmethod
    def build(self, container, **kwargs):
        raise Exception("Build method should be implemented in the child class")
