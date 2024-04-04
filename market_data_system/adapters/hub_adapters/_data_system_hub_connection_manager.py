from typing import Dict, Optional

from _enums import OperationMode
from market_data_system import DataSession
from market_data_system.session import MarketDataSessionFactory


class MarketDataSystemHubConnectionManger:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MarketDataSystemHubConnectionManger, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._market_data_sessions: Dict[
            str, DataSession] = dict()  # key: market_data_session_id, value: MarketDataSession
        self._hub_id_to_data_session_id: Dict[str, str] = dict()  # key: hub_id, value: data_session_id

    def create_data_session(self, hub_id: str, operation_mode: OperationMode):
        data_session = MarketDataSessionFactory.create_data_session(operation_mode=operation_mode)
        self.add_data_session(data_session)
        self._hub_id_to_data_session_id[hub_id] = data_session.id

    def add_data_session(self, data_session: DataSession):
        self._market_data_sessions[data_session.id] = data_session

    def find_data_session(self, hub_id: Optional[str] = None,
                          data_session_id: Optional[str] = None) -> None | DataSession:
        if all([x is None for x in [hub_id, data_session_id]]):
            return None
        if len([x for x in [hub_id, data_session_id] if x is not None]) != 1:
            raise ValueError(
                "Find data session requires exactly one of hub_id, data_session_id to be provided")
        if hub_id is not None:
            data_session_id = self._hub_id_to_data_session_id.get(hub_id, None)
            return self.find_data_session(data_session_id=data_session_id)
        if data_session_id is not None:
            return self._market_data_sessions.get(data_session_id, None)
        return None

    def find_data_session_id(self, hub_id: str) -> Optional[str]:
        return self._hub_id_to_data_session_id.get(hub_id, None)
