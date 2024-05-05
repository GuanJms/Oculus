from abc import ABC, abstractmethod
from typing import List

from data_system._enums import DomainEnum
from data_system.tracker.cores.container_manager import ContainerManager
from data_system.utils.domain_operations import domain_to_chains


class DataInjector(ABC):
    def __init__(self, domains: List[DomainEnum] | None = None):
        self.container_manager: ContainerManager | None = None
        self._domains = domains  # All container_manager should have the same domains
        self._domains_chain: str = domain_to_chains(domains)
        self._preprocessor = None

    def set_params(self, **kwargs):
        # TODO: Untested - likely to be wrong
        params_keys = kwargs.keys()
        # parse the parameters by the processor name follow by the parameter name
        for key in params_keys:
            if "__" not in key:
                setattr(self, key, kwargs[key])
            name, param_name = key.split("__", 1)
            if hasattr(self, name):
                instance = getattr(self, name)
                instance.set_params(**{param_name: kwargs[key]})

    def set_domains(self, domains: List[DomainEnum]):
        self._domains = domains
        self._domains_chain = domain_to_chains(domains)

    def get_container_manager(self):
        return self.container_manager

    def set_container(self, container_manager):
        self.container_manager = container_manager
        if self._domains is None:
            raise ValueError("Domains should be set before setting tracker")
        self.container_manager.set_domains(self._domains)

    def is_right_domains(self, data) -> bool:
        # check if the domains are correct
        data_domains = data.get("domains", None)
        if data_domains:
            return data_domains == self._domains_chain
        return False

    @abstractmethod
    def inject(self, data: dict):
        pass

    def _preprocess(self, data: dict):
        raise NotImplementedError(
            "Pre-inject process method should be implemented in the child class"
        )
