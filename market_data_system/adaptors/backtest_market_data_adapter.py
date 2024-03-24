from typing import Optional
from global_utils import GlobalComponentIDGenerator


from market_data_system import MarketDataMediator
from ._market_data_adapter import MarketDataAdapter
from ..enums import OperationMode


class BacktestMarketDataAdapter(MarketDataAdapter):

    _backtest_param_keys = ['start_date', 'end_date', 'ticker_list', 'frequency']
    _int_backtest_param_keys = ['start_date', 'end_date', 'frequency']

    def __init__(self):
        self._id: str = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._market_data_mediator = MarketDataMediator()
        self._operation_mode = OperationMode.BACKTESTING
        self._runnable: bool = False
        self.start_ms_of_day: Optional[int] = None
        self.end_ms_of_day: Optional[int] = None

    @property
    def id(self) -> str:
        return self._id

    def request_data(self, *args, **kwargs):
        pass

    def request_create_session(self):
        adapter_id = self.id
        operation_mode = self._operation_mode
        self._market_data_mediator.create_session(adapter_id=adapter_id, operation_mode=operation_mode)

    def request_delete_session(self):
        adapter_id = self.id
        self._market_data_mediator.delete_session(adapter_id)

    def _configure(self, *args, **kwargs):

        pass

    def advance_simulation_timestep(self):
        self._market_data_mediator.request_advance_simulation_timestep(adapter_id=self.id)

    def is_runnable(self) -> bool:
        return self._runnable

    def set_backtest_setting(self, **params):
        for key, value in params.items():
            if key in self._int_backtest_param_keys:
                value = int(value)
            setattr(self, key, value)
        if all([hasattr(self, key) for key in self._backtest_param_keys]):
            self._runnable = True



