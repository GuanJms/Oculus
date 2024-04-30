from data_system.facade import SimulationMarketDataFacade, RealtimeMarketDataFacade
from data_system.connection import MarketDataSystemConnectionManager
from data_system.session._data_session_manager import DataSessionManager
from data_system.utils import convert_timeline_type_to_operation_mode
from .._enums import TimelineType, OperationMode


class MarketDataSystemFacade:

    def __new__(cls, *args, **kwargs):
        # Singleton pattern
        if not hasattr(cls, 'instance'):
            cls.instance = super(MarketDataSystemFacade, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._simulation_market_data_facade = SimulationMarketDataFacade()
        self._realtime_market_data_facade = RealtimeMarketDataFacade()
        self._connection_manager = MarketDataSystemConnectionManager()
        self._session_manager = DataSessionManager()

    def connect(self, **kwargs):
        input_keys = set(kwargs.keys())
        if input_keys == {'connector_id', 'connector_type'}:
            match kwargs['connector_type']:
                case TimelineType.REALTIME:
                    raise NotImplementedError
                case TimelineType.SIMULATION:
                    operation_mode = convert_timeline_type_to_operation_mode(TimelineType.SIMULATION)
                    self.create_session(kwargs['connector_id'], operation_mode)

    def create_session(self, hub_id: str, operation_mode: OperationMode):
        self._session_manager.create_session(hub_id, operation_mode)

