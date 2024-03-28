from typing import Dict, Any

from market_data_system._data_session_manager import DataSessionManager
from market_data_system.adaptors import MarketDataAdapter
from market_data_system._enums import OperationMode
from utils._transmittable_interface import _EventSubscriber


class MarketDataFacade(_EventSubscriber):

    instance = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MarketDataFacade, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._session_manager = DataSessionManager()
        self._registered_adapters: Dict[str, MarketDataAdapter] = {}

    def register_adapter(self, adapter_id: str, adapter: MarketDataAdapter):
        self._registered_adapters[adapter_id] = adapter

    def request_advance_simulation_timestep(self, adapter_id):
        self._session_manager.request_advance_simulation_timestep(adapter_id)

    def receive_event(self, event: Any, event_data: Any):
        pass

