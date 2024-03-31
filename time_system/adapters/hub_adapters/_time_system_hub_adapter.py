from abc import ABC, abstractmethod
from time_system.adapters.hub_adapters import TimelineHubConnectionManager
from time_system import TimelineType


class TimeSystemHubAdapter(ABC):

    @property
    @abstractmethod
    def connection_manager(self) -> 'TimelineHubConnectionManager':
        pass

    @property
    @abstractmethod
    def timeline_type(self) -> 'TimelineType':
        pass

    @abstractmethod
    def request_session(self, hub_id: str):
        pass

    @abstractmethod
    def get_session_id(self, hub_id: str) -> str:
        pass

    @abstractmethod
    def set_timeline_setting(self, **kwargs):
        pass

