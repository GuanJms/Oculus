from abc import ABC, abstractmethod


class MarketDataAdapter(ABC):

    @abstractmethod
    def request_data(self, *args, **kwargs):
        pass

    @abstractmethod
    def request_create_session(self, *args, **kwargs):
        pass

    @abstractmethod
    def request_delete_session(self, *args, **kwargs):
        pass

    @abstractmethod
    def _configure(self, *args, **kwargs):
        pass
