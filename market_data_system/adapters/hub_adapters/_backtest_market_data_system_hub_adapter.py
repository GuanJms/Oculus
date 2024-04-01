from typing import Optional
from utils.global_id import GlobalComponentIDGenerator

from market_data_system.facade import MarketDataSystemFacade
from market_data_system.adapters.hub_adapters import MarketDataSystemHubConnectionManger
from ._market_data_system_hub_adapter import MarketDataSystemHubAdapter
from _enums import OperationMode


class BacktestMarketDataHubSystemHubAdapter(MarketDataSystemHubAdapter):

    def __init__(self):
        self._id: str = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        # self._market_data_system = MarketDataSystemFacade() # TODO: Refactor; No need facade here
        self._operation_mode = OperationMode.BACKTEST
        # self._runnable: bool = False
        self.start_ms_of_day: Optional[int] = None
        self.end_ms_of_day: Optional[int] = None

    @property
    def connection_manager(self):
        return MarketDataSystemHubConnectionManger()

    @property
    def id(self) -> str:
        return self._id


    def request_data(self, *args, **kwargs):
        pass

    def request_session(self, hub_id: str):
        self.connection_manager.create_data_session(hub_id=hub_id, operation_mode=self._operation_mode)

    def get_session_id(self, hub_id: str):
        """
        Get data session id
        :param hub_id:
        :return: data session id
        """
        self.connection_manager.find_data_session_id(hub_id=hub_id)

    def advance_simulation_timestep(self):
        self._market_data_system.request_advance_simulation_timestep(adapter_id=self.id)

    # def is_runnable(self) -> bool:
    #     return self._runnable

    # def set_backtest_setting(self, **params):
    #     for key, value in params.items():
    #         if key in self._int_backtest_param_keys:
    #             value = int(value)
    #         setattr(self, key, value)
    #     if all([hasattr(self, key) for key in self._backtest_param_keys]):
    #         self._runnable = True

    def set_market_data_setting(self, **kwargs):
        keys = set(kwargs.keys())
        if ticker_list := keys.intersection({'ticker_list'}):
            #TODO: SET COMPOENT TAHT CAN HANDLE TICKER LIST
