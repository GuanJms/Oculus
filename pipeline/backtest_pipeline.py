import time
from typing import Optional, Type

from execution_system.adapters.backtest import BacktestExecutionAdapter
from market_data_system.adaptors import BacktestMarketDataAdapter
from strategics.repo.core.strategy import StrategyRule
from global_utils import GlobalComponentIDGenerator, GlobalTimeGenerator
from pipeline import PipelineStatusType


class BacktestPipeline:
    _backtest_param_keys = ['start_date', 'end_date', 'ticker_list', 'frequency']

    def __init__(self):
        self._id: str = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self.strategy_rule_cls: Optional[Type[StrategyRule]] = None
        self._execution_system_adapter = BacktestExecutionAdapter()
        self._market_data_system_adapter = BacktestMarketDataAdapter()
        self._status = PipelineStatusType.UNINITIATED
        self._runnable = False


    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status: PipelineStatusType):
        self._status = status

    @property
    def id(self) -> str:
        return self._id

    def _set_params(self, params: dict):
        for key, value in params.items():
            setattr(self, key, value)

    def _set_param(self, key: str, value):
        setattr(self, key, value)

    def get_params(self) -> dict:
        return {key: getattr(self, key) for key in self.__dict__.keys()}

    def get_param(self, key: str) -> Optional:
        return getattr(self, key)

    def set_params(self, **params):
        for key in params.keys():
            if key in self._backtest_param_keys:
                self._set_param(key, params[key])
        if all([hasattr(self, key) for key in self._backtest_param_keys]):
            self._runnable = True

    def set_strategy_cls(self, strategy_rule_cls: Type[StrategyRule]):
        self.strategy_rule_cls = strategy_rule_cls
        self.status = PipelineStatusType.IDLE

    def run(self, **params):
        if not self.status.is_initiated():
            raise Exception("Pipeline is not initiated")
        if not self._runnable:
            raise Exception("Pipeline is not runnable")
        if not self.status == PipelineStatusType.IDLE or self.status == PipelineStatusType.PROCESSING
            raise Exception("Pipeline is not in IDLE or is already running")
        if not self._market_data_system_adapter.is_runnable():
            self._market_data_system_adapter.set_backtest_setting(
                **{key: getattr(self, key) for key in self._backtest_param_keys})
        if not self._market_data_system_adapter.is_runnable():
            raise Exception("Execution system is not runnable")

        # create strategy_rule_instance
        strategy_rule_instance = self.strategy_rule_cls(**params)
        self._execution_system_adapter.execute(strategy_rule_instance)
        while self._execution_system_adapter.status.is_running():
            if self._execution_system_adapter.status.is_data_requesting():
                data_request_query = self._execution_system_adapter.get_data_request_query()
                self._market_data_system_adapter.simulation.next()
                new_data = self._market_data_system_adapter.request_data(data_request_query)
                self._execution_system_adapter.feed(data=new_data)
            else:
                time.sleep(0.01)
