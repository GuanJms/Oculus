from abc import ABC, abstractmethod
from typing import Optional


class ExecutionSystemHubAdapter(ABC):
    @property
    @abstractmethod
    def connection_manager(self):
        pass

    @abstractmethod
    def get_session_id(self, hub_session_id: str) -> str:
        pass

    @abstractmethod
    def get_session_ids(
        self, hub_session_ids: Optional[list] = None, hub_id: Optional[str] = None
    ) -> dict:
        pass

    @abstractmethod
    def request_sessions(self, hub_id: str, hub_session_ids: list):
        pass
