from typing import Optional

from data_system._enums import DomainEnum
from abc import ABC, abstractmethod


# TODO: restructure the container mangaer such that it will processs differnet functionality of contianers
# TODO: think through by _containsers should be dinctionary and what the keys should be

# TODO: make accumulation factory that will create the accumulation container
class ContainerManager(ABC):
    def __init__(self, **kwargs):
        self._containers = {}
        self._domains = kwargs.get("domains", None)

    @abstractmethod
    def inject(self, data, meta=None):
        raise Exception("Inject method should be implemented in the child class")

    @abstractmethod
    def create_container(self, key, **kwargs):
        pass

    def get_containers(self):
        return self._containers

    def has_key(self, key):
        return key in self._containers

    def get_container(self, key=None):
        return self._containers.get(key, None)

    def set_domains(self, domains: DomainEnum):
        self._domains = domains

    def set_container(self, key, container):
        if hasattr(container, "set_domains"):
            container.set_domains(self._domains)
        self._containers[key] = container

    def add_node(self, node, meta, **kwargs):
        raise NotImplementedError("Child class should implement this method")
