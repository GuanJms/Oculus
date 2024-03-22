from typing import Optional, Type

from execution_system.adapters.backtest import BacktestExecutionAdapter
from market_data_system.adaptors import BacktestMarketDataAdapter
from strategics.repo.core.strategy import StrategyRule
from global_utils import GlobalComponentIDGenerator, GlobalTimeGenerator
from execution_system import ExecutionStatusType


class BacktestPipeline:
    _backtest_param_keys = ['start_date', 'end_date', 'ticker_list', 'frequency']

    def __init__(self):
        self._id: str = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self.strategy_rule_cls: Optional[Type[StrategyRule]] = None
        self._execution_system_adapter = BacktestExecutionAdapter()
        self._market_data_system_adapter = BacktestMarketDataAdapter()



    @property
    def id(self) -> str:
        return self._id

    def _set_params(self, params: dict):
        for key, value in params.items():
            setattr(self, key, value)

    def _set_param(self, key: str, value):
        setattr(self, key, value)

    def get_params(self):
        return {key: getattr(self, key) for key in self.__dict__.keys()}

    def get_param(self, key: str):
        return getattr(self, key)

    def set_params(self, **params):
        for key in params.keys():
            if key in self._backtest_param_keys:
                self._set_param(key, params[key])
        pass

    def set_strategy_cls(self, strategy_rule_cls: Type[StrategyRule]):
        self.strategy_rule_cls = strategy_rule_cls

    def run(self,  **params):
        if self.strategy_rule_cls is None:
            raise ValueError("Strategy rule is not set yet.")
        # create strategu_rule_instance
        strategy_rule_instance = self.strategy_rule_cls(**params)
        self._execution_system_adapter.execute(strategy_rule_instance)
        while :
            execution_status = self.request_execution_status()
            if execution_status ==




