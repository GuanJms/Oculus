from typing import Optional, Any, List, Type, Dict

from hub._enums import RunningStatusType, InitializationStatusType, HubType
from strategics.repo.core.strategy import StrategyRule
from utils.global_id import GlobalComponentIDGenerator
from ._hub_session import HubSession
from ._hub_session_factory import HubSessionFactory
from .connection import HubConnectionManager
from execution_system.adapters import ExecutionSystemHubAdapter
from market_data_system.adapters import MarketDataSystemHubAdapter
from time_system.adapters.hub_adapters import TimeSystemHubAdapter


class Hub:
    def __init__(self):
        self._id: str = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._hub_connection_manager: HubConnectionManager = HubConnectionManager()
        self.strategy_rule_cls: Optional[Type[StrategyRule]] = None
        self._running_status = RunningStatusType.INACTIVE
        self._init_status = InitializationStatusType.UNINITIATED
        self._protected_class_param_keys: List[str] = []
        self._execution_system: Optional[ExecutionSystemHubAdapter] = None
        self._market_data_system: Optional[MarketDataSystemHubAdapter] = None
        self._time_system: Optional[TimeSystemHubAdapter] = None
        self._hub_type: Optional[HubType] = None
        self._hub_sessions: Dict[str, HubSession] = {}

    @property
    def status(self):
        return self._running_status

    @property
    def id(self) -> str:
        return self._id

    @property
    def execution_system(self) -> ExecutionSystemHubAdapter:
        return self._execution_system

    @property
    def market_data_system(self) -> MarketDataSystemHubAdapter:
        return self._market_data_system

    @property
    def time_system(self) -> TimeSystemHubAdapter:
        return self._time_system

    @property
    def hub_connection_manager(self) -> HubConnectionManager:
        return self._hub_connection_manager

    def _set_params(self, params: dict):
        for key, value in params.items():
            setattr(self, key, value)

    def _set_param(self, key: str, value):
        setattr(self, key, value)

    def get_params(self) -> dict:
        return {key: getattr(self, key) for key in self.__dict__.keys()}

    def get_param(self, key: str) -> Optional[Any]:
        if key not in self.__dict__.keys():
            return None
        return getattr(self, key)

    def set_params(self, **params):
        for key in params.keys():
            self._init_status = InitializationStatusType.INITIATED
            if key in self._protected_class_param_keys:
                self._set_param(key, params[key])

    def set_strategy_cls(self, strategy_rule_cls: Type[StrategyRule]):
        self.strategy_rule_cls = strategy_rule_cls

    def run(self, **params):
        raise NotImplementedError("run method must be implemented in subclass")

    def check_init(self):
        raise NotImplementedError("check_init method must be implemented in subclass")

    def create_hub_session(self, strategy_params: Optional[Any] = None):
        if self.strategy_rule_cls is None:
            raise Exception("Strategy rule class is not set")
        hub_session = HubSessionFactory.create(hub_type=self._hub_type, strategy_rule_cls=self.strategy_rule_cls,
                                               strategy_params=strategy_params)
        self._hub_sessions[hub_session.id] = hub_session

    def get_hub_sessions(self) -> Dict[str, HubSession]:
        return self._hub_sessions

    def get_hub_session_ids(self) -> List[str]:
        return list(self._hub_sessions.keys())
