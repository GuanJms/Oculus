from data_system._enums import DomainEnum


class HubTicker:
    def __init__(self, ticker, domains: list[DomainEnum]):
        self._ticker = ticker
        self._domains = domains

    @property
    def ticker(self):
        return self._ticker

    @property
    def domains(self):
        return self._domains
