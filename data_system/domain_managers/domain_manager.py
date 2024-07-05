from abc import ABC, abstractmethod


class DomainManager(ABC):

    def __init__(self, **kwargs):
        self._domains = kwargs.get("domains", [])

    @abstractmethod
    def inject(self, node, domains: list = None, meta: dict = None):
        pass
