from abc import ABC, abstractmethod


class DataInjector(ABC):

    def __init__(self):
        self._container = None

    @property
    def container(self):
        return self._container

    def set_container(self, container):
        self._container = container

    @abstractmethod
    def inject(self, data: dict):
        pass


