from typing import Optional, Any, List, Type

from hub._enums import RunningStatusType, InitializationStatusType
from strategics.repo.core.strategy import StrategyRule
from utils.global_id import GlobalComponentIDGenerator


class Hub:
    def __init__(self):
        self._id: str = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self.strategy_rule_cls: Optional[Type[StrategyRule]] = None
        self._running_status = RunningStatusType.INACTIVE
        self._init_status = InitializationStatusType.UNINITIATED
        self._protected_class_param_keys: List[str] = []
        self._execution_system: Optional[Any] = None
        self._market_data_system: Optional[Any] = None

    @property
    def status(self):
        return self._running_status

    @property
    def id(self) -> str:
        return self._id

    @property
    def execution_system(self):
        return self._execution_system

    @property
    def market_data_system(self):
        return self._market_data_system

    def _set_params(self, params: dict):
        for key, value in params.items():
            setattr(self, key, value)

    def _set_param(self, key: str, value):
        setattr(self, key, value)

    def get_params(self) -> dict:
        return {key: getattr(self, key) for key in self.__dict__.keys()}

    def get_param(self, key: str) -> Optional[Any]:
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

