from abc import ABC, abstractmethod


class MarketDataAdapter(ABC):
    @abstractmethod
    def get_data(self, *args, **kwargs):
        pass

    @abstractmethod
    def create_data_session(self, *args, **kwargs):
        pass

    @abstractmethod
    def end_data_session(self, *args, **kwargs):
        pass

    @abstractmethod
    def _configure(self, *args, **kwargs):
        pass
