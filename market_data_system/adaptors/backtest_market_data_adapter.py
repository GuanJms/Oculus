from typing import Optional


class BacktestMarketDataAdapter:

    _backtest_param_keys = ['start_date', 'end_date', 'ticker_list', 'frequency']
    _int_backtest_param_keys = ['start_date', 'end_date', 'frequency']

    def __init__(self):
        self.simulation = None
        self._runnable: bool = False
        self.start_ms_of_day: Optional[int] = None
        self.end_ms_of_day: Optional[int] = None

    def request_data(self, data_request_query):
        pass

    def is_runnable(self) -> bool:
        return self._runnable

    def set_backtest_setting(self, **params):
        for key, value in params.items():
            if key in self._int_backtest_param_keys:
                value = int(value)
            setattr(self, key, value)
        if all([hasattr(self, key) for key in self._backtest_param_keys]):
            self._runnable = True



