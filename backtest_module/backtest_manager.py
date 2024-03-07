from typing import Optional, List

from execution_module.execution_manager import ExecutionManager
from global_component_id_generator import GlobalComponentIDGenerator
from strategy_module.strategy_rule import StrategyRule


class BacktestManager:
    def __init__(self):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._backtest_params: dict = {}
        self._start_date: Optional[int] = None
        self._end_date: Optional[int] = None
        self._ticker_list: Optional[str] = None
        self._strategy_rule_list: List[StrategyRule] = []
        self._frequency: Optional[int] = None

        self._execution_manager = None
        self._backtest_data_manager = None

    @property
    def id(self):
        return self._id

    @property
    def execution_manager(self):
        return self._execution_manager

    @execution_manager.setter
    def execution_manager(self, execution_manager: ExecutionManager):
        self._execution_manager = execution_manager


    @property
    def backtest_data_manager(self):
        return self._backtest_data_manager

    @backtest_data_manager.setter
    def backtest_data_manager(self, backtest_data_manager):
        self._backtest_data_manager = backtest_data_manager

    @property
    def backtest_params(self):
        return self._backtest_params

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def ticker_list(self):
        return self._ticker_list

    @property
    def strategy_list(self):
        return self._strategy_rule_list

    @property
    def frequency(self):
        return self._frequency

    def add_backtest_params(self, backtest_params: dict):
        self._backtest_params.update(backtest_params)
        self._start_date = backtest_params.get('start_date', None)
        self._end_date = backtest_params.get('end_date', None)
        self._ticker_list = backtest_params.get('ticker_list', None)
        self._frequency = backtest_params.get('frequency_ms', None)
        # TODO: check quote_date format and validate input

    def run_strategy(self, oil_short_vol_strategy):
        self._strategy_rule_list.append(oil_short_vol_strategy)
        print(f"Running strategy: {oil_short_vol_strategy.strategy_name}")


