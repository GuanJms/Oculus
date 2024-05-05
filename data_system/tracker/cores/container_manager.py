from data_system._enums import DomainEnum
from abc import ABC, abstractmethod


class ContainerManager:
    def __init__(self):
        self._containers = {}
        self._domains = None

    @abstractmethod
    def inject(self, data, meta, **kwargs):
        raise Exception("Inject method should be implemented in the child class")

    def has_key(self, key):
        return key in self._containers

    def get_container(self, key):
        return self._containers.get(key, None)

    def set_domains(self, domains: DomainEnum):
        self._domains = domains

    def set_container(self, key, container):
        if hasattr(container, "set_domains"):
            container.set_domains(self._domains)
        self._containers[key] = container
