from typing import Dict, Type, Optional, Union

from market_data_system._data_session import DataSession
from weakref import WeakSet
from backtest_simulation import BacktestDataSession
from market_data_system.enums import OperationMode


class DataSessionManager:
    instance = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataSessionManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._adapterSessionMap: Dict[str, DataSession] = {}  # adapter_id: DataSession
        self._backtest_session_set: WeakSet[BacktestDataSession] = WeakSet()

    def create_session(self, adapter_id: str, operation_mode: OperationMode):
        data_session = None  # type: Optional[DataSession]
        if operation_mode == OperationMode.BACKTESTING:
            data_session = BacktestDataSession()
        if data_session is not None:
            self._adapterSessionMap[adapter_id] = data_session
            return data_session
        raise ValueError("Invalid session type")

    def delete_session(self, adapter_id):
        data_session = self.find_session(adapter_id)
        if data_session is not None:
            data_session.close()
            self._adapterSessionMap.pop(adapter_id)
        else:
            raise ValueError("Session not found")

    def request_advance_simulation_timestep(self, adapter_id: str):
        data_session = self.find_session(adapter_id)
        if data_session is None:
            raise ValueError("Session not found")
        if data_session.get_session_type() == OperationMode.BACKTESTING:
            data_session.request_advance_time()
        else:
            raise ValueError("Session type not supported for this operation - advance_simulation_timestep")

    def find_session(self, adapter_id) -> Optional[Union[DataSession, BacktestDataSession]]:
        return self._adapterSessionMap.get(adapter_id, None)
