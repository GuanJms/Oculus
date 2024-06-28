from abc import ABC, abstractmethod
from typing import List

from data_system._enums import DomainEnum


class Container(ABC):

    def __init__(self, **kwargs):
        self.description = kwargs.get("description", "")
        self._domains: List[DomainEnum] = []

    def set_domains(self, domains: List[DomainEnum]):
        self._domains = domains

    def get_domains(self):
        return self._domains

    @abstractmethod
    def inject(self, data, meta=None):
        pass
