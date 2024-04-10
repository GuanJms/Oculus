from typing import Optional

from data_system.backtest_simulation._backtest_data_manager import BacktestDataManager
from data_system.backtest_simulation._backtest_data_session import BacktestDataSession
from execution_system.execution_manager import ExecutionManager
from utils.global_id import GlobalComponentIDGenerator, GlobalTimeGenerator
from strategics.repo.core.strategy.strategy_rule import StrategyRule

"""
BacktestManager contains the bactkest information
"""


class HubAdaptor:
    def __init__(self):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._backtest_params: dict = {}
        self._start_date: Optional[int] = None
        self._end_date: Optional[int] = None
        self._ticker_list: Optional[str] = None
        self._frequency: Optional[int] = None
        self._start_ms_of_day: Optional[int] = None
        self._end_ms_of_day: Optional[int] = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def execution_manager(self) -> ExecutionManager:
        return self._execution_manager

    @execution_manager.setter
    def execution_manager(self, execution_manager: ExecutionManager):
        self._execution_manager = execution_manager

    @property
    def backtest_data_manager(self) -> BacktestDataManager:
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

    @property
    def start_ms_of_day(self):
        return self._start_ms_of_day

    @property
    def end_ms_of_day(self):
        return self._end_ms_of_day

    def add_backtest_params(self, backtest_params: dict):
        self._backtest_params.update(backtest_params)
        self._start_date = int(backtest_params.get('start_date'))
        self._end_date = backtest_params.get('end_date', None)
        if self._end_date is not None:
            self._end_date = int(self._end_date)
        if not self._end_date:
            self._end_date = GlobalTimeGenerator.generate_current_date_integer()

        self._ticker_list = backtest_params.get('ticker_list', None)
        self._frequency = int(backtest_params.get('frequency', 60_000))
        self._start_ms_of_day = int(backtest_params.get('start_ms_of_day', 34_200_000))
        self._end_ms_of_day = int(backtest_params.get('end_ms_of_day', 57_600_000))

        # TODO: check quote_date format and validate input

    def run_strategy(self, oil_short_vol_strategy: StrategyRule):
        self._strategy_rule_list.append(oil_short_vol_strategy)
        self.execution_manager.execute_strategy(oil_short_vol_strategy)

    def set_backtest_data_manager(self, backtest_data_manager: BacktestDataManager):
        self._backtest_data_manager = backtest_data_manager

    def set_execution_manager(self, execution_manager: ExecutionManager):
        self._execution_manager = execution_manager

    def get_backtest_time_params(self):
        time_params = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'frequency': self.frequency,
            'start_ms_of_day': self.start_ms_of_day,
            'end_ms_of_day': self.end_ms_of_day
        }
        return time_params

    def get_backtest_ticker_params(self):
        ticker_params = {
            'ticker_list': self.ticker_list
        }
        return ticker_params

    def get_result(self, strategy):
        # TODO: return result
        pass

    def request_backtest_data_session(self) -> Optional[BacktestDataSession]:
        return self.backtest_data_manager.request_backtest_data_session()
