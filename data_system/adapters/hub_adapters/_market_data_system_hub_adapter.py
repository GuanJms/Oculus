from abc import ABC, abstractmethod


class MarketDataSystemHubAdapter(ABC):
    @property
    @abstractmethod
    def connection_manager(self):
        pass

    @abstractmethod
    def request_data(self, *args, **kwargs):
        pass

    @abstractmethod
    def request_session(self, hub_id: str):
        pass

    @abstractmethod
    def get_session_id(self, hub_id: str):
        pass

    @abstractmethod
    def set_market_data_setting(self, **kwargs):
        pass
