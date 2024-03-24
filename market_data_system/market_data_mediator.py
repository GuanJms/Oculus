from typing import Dict, Type, Optional

from ._data_session import DataSession
from ._data_session_manager import DataSessionManager
from .adaptors import MarketDataAdapter
from .backtest_simulation import BacktestDataSession
from .enums import OperationMode


class MarketDataMediator:
    instance = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MarketDataMediator, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._session_manager = DataSessionManager()
        self._registered_adapters: Dict[str, MarketDataAdapter] = {}

    def register_adapter(self, adapter_id: str, adapter: MarketDataAdapter):
        self._registered_adapters[adapter_id] = adapter

    def create_session(self, adapter_id: str, operation_mode: OperationMode):
        self._session_manager.create_session(adapter_id, operation_mode)

    def delete_session(self, adapter_id):
        self._session_manager.delete_session(adapter_id)

    def request_advance_simulation_timestep(self, adapter_id):
        self._session_manager.request_advance_simulation_timestep(adapter_id)
