from typing import Set, Dict, Any

from execution_system.adapters.backtest import BacktestExecutionHubAdapter
from market_data_system.adaptors import BacktestMarketDataHubSystemHubAdapter
from ._enums import InitializationStatusType, RunningStatusType, HubType
from ._integration_hub import Hub


class BacktestHub(Hub):

    def __init__(self):
        super().__init__()
        self._hub_type = HubType.BACKTESTING
        self._execution_system = BacktestExecutionHubAdapter()
        self._market_data_system = BacktestMarketDataHubSystemHubAdapter()
        self._protected_class_param_keys = ['start_date', 'end_date', 'ticker_list', 'frequency']
        self._int_backtest_param_keys = ['start_date', 'end_date', 'frequency']

    def check_init(self):
        if self._init_status == InitializationStatusType.READY:
            return
        match True:
            case _ if not all([hasattr(self, key) for key in self._protected_class_param_keys]):
                raise Exception("Not all required parameters are set")
            case _ if not all([isinstance(getattr(self, key), int) for key in self._int_backtest_param_keys]):
                raise Exception("Invalid parameter type")
            case _ if not all([isinstance(getattr(self, key), list) for key in ['ticker_list']]):
                raise Exception("Invalid parameter type")
            case _ if not all([getattr(self, key) >= 0 for key in self._int_backtest_param_keys]):
                raise Exception(
                    [f"Invalid parameter value: {key} must be greater than 0" for key in self._int_backtest_param_keys
                     if getattr(self, key) < 0])
            case _ if self.strategy_rule_cls is None:
                raise Exception("Strategy rule class is not set")
        self._init_status = InitializationStatusType.READY

    def run(self, strategy_param_set: Set[Dict[str, Any]]):
        if self._running_status == RunningStatusType.ACTIVE:
            raise Exception(f"Pipeline is active | {self.id} ")
        self.check_init()
        if self._init_status != InitializationStatusType.READY:
            raise Exception("[SHOULD NOT BE RUN] Pipeline is not correctly initialized")
        self.run_config(strategy_param_set)

    def run_config(self, strategy_param_set: Set[Dict[str, Any]]):
        """
        This function should create HubConnection for each time the strategy is run with a set of strategy_params.
        Configuration include
        TODO: create HubSession for each strategy_params
        TODO: create Timeline for Hub (all HubSessions should share the same timeline)
        TODO: create DataSession for Hub (all HubSessions should share the same data session)
        """
        for strategy_params in strategy_param_set:
            self.create_hub_session(strategy_params=strategy_params)  # create hub session for each strategy_params

        self.execution_system.request_session(self.id)  # request execution session
        self.market_data_system.request_session(self.id)  # request data session










        #
        # if self.market_data_system
        #
        # if not self._market_data_system.is_runnable():
        #     self._market_data_system.set_backtest_setting(
        #         **{key: getattr(self, key) for key in self._backtest_param_keys})
        # if not self._market_data_system.is_runnable():
        #     raise Exception("Execution system is not runnable")
        #
        # # create strategy_rule_instance
        # strategy_rule_instance = self.strategy_rule_cls(**params)
        # self._execution_system.execute(strategy_rule_instance)

        # while self._execution_system_adapter.status.is_running():
        #     if self._execution_system_adapter.status.is_data_requesting():
        #         data_request_query = self._execution_system_adapter.get_data_query() #TODO: find a better funtion name
        #         self._market_data_system_adapter.advance_simulation_timestep()
        #         new_data = self._market_data_system_adapter.request_data(data_request_query)
        #         self._execution_system_adapter.feed(data=new_data)
        #     else:
        #         time_system.sleep(0.01)
