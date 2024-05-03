from data_system._enums import DomainEnum


class ContainerManager:
    def __init__(self):
        self._container = None
        self._domains = None

    def inject(self):
        raise Exception("Inject method should be implemented in the child class")

    def get_container(self):
        return self._container

    def set_domains(self, domains: DomainEnum):
        self._domains = domains
