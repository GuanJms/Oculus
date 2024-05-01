from typing import Dict, Optional, Union

from data_system.session._data_session import DataSession
from weakref import WeakSet
from data_system.backtest_simulation import BacktestDataSession
from .._enums import OperationMode


class DataSessionManager:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(DataSessionManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._data_session_map: Dict[str, DataSession] = {}  # hub_id: DataSession
        # TODO: Add connection manager
        self._backtest_session_set: WeakSet[BacktestDataSession] = WeakSet()

    def create_session(self, hub_id: str, operation_mode: OperationMode):
        data_session = None  # type: Optional[DataSession]
        if operation_mode == OperationMode.BACKTEST:
            data_session = BacktestDataSession()
        if data_session is not None:
            self._data_session_map[hub_id] = data_session
            return data_session
        raise ValueError("Invalid session type")

    def delete_session(self, hub_id: str):
        data_session = self.find_session(hub_id)
        if data_session is not None:
            data_session.close()
            self._data_session_map.pop(hub_id)
        else:
            raise ValueError("Session not found")

    def request_advance_simulation_timestep(self, hub_id: str):
        data_session = self.find_session(hub_id)
        if data_session is None:
            raise ValueError("Session not found")
        if data_session.session_type() == OperationMode.BACKTEST:
            data_session.request_advance_time()
        else:
            raise ValueError(
                "Session type not supported for this operation - advance_simulation_timestep"
            )

    def find_session(self, hub_id) -> Optional[Union[DataSession, BacktestDataSession]]:
        return self._data_session_map.get(hub_id, None)

    # TODO: find_session is confusing. Should it be able to use hub_id, data_session_id! Use another class to keep track that
