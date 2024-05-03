from abc import ABC, abstractmethod


class DataInjector(ABC):
    def __init__(self):
        self._container_manager = None

    def get_container_manager(self):
        return self._container_manager

    def set_container(self, container_manager):
        self._container_manager = container_manager

    @abstractmethod
    def inject(self, data: dict):
        pass
