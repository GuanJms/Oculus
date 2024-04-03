from typing import Set, Dict, Any

from execution_system.adapters.backtest import BacktestExecutionHubAdapter
from market_data_system.adapters import BacktestMarketDataHubSystemHubAdapter
from time_system.adapters.hub_adapters import BacktestTimeSystemHubAdapter
from ._enums import InitializationStatusType, RunningStatusType, HubType
from ._integration_hub import Hub


class BacktestHub(Hub):

    def __init__(self):
        super().__init__()
        self._hub_type = HubType.BACKTESTING
        self._execution_system = BacktestExecutionHubAdapter()
        self._market_data_system = BacktestMarketDataHubSystemHubAdapter()
        self._time_system = BacktestTimeSystemHubAdapter()
        self._protected_class_param_keys = ['start_date', 'end_date', 'ticker_list', 'frequency',
                                            'start_ms_of_day', 'end_ms_of_day']
        self._int_backtest_param_keys = ['start_date', 'end_date', 'frequency',
                                         'start_ms_of_day', 'end_ms_of_day']

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
        self.request_sessions(strategy_param_set)
        self.configure_backtest_params()  # TODO: configure

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

    def request_sessions(self, strategy_param_set: Set[Dict[str, Any]]):
        """
        This function should create HubConnection for each time the strategy is run with a set of strategy_params.
        Configuration include creating HubSession(s), Timeline, DataSession, ExecutionSession
        """
        for strategy_params in strategy_param_set:
            self.create_hub_session(strategy_params=strategy_params)  # create hub session for each strategy_params

        self.execution_system.request_sessions(hub_id=self.id,
                                               hub_session_ids=self.get_hub_session_ids())  # request execution session
        self.market_data_system.request_session(self.id)  # request data session
        self.time_system.request_session(self.id)  # request timeline

        timeline_id = self.time_system.get_session_id(self.id)  # get timeline id
        execution_session_id_dict = self.execution_system.get_session_ids(hub_id=self.id)  # get execution session ids
        # dict: {hub_session_id: execution_session_id}
        data_session_id = self.market_data_system.get_session_id(self.id)  # get data session id
        self.hub_connection_manager.create_hub_connection(hub_id=self.id, hub_session_ids=self.get_hub_session_ids(),
                                                          timeline_id=timeline_id, data_session_id=data_session_id,
                                                          execution_session_id_dict=execution_session_id_dict)

    def configure_backtest_params(self):
        """
        Configure session settings including
        # TODO: configure time system settings from backtest settings (start_date, end_date, frequency)
        # TODO: configure data system settings from backtest settings (ticker_list)
        # TODO: configure execution system settings from backtest settings (ticker_list)
        """
        self.time_system.set_timeline_setting(start_date=self.get_param('start_date'),
                                              end_date=self.get_param('end_date'),
                                              frequency=self.get_param('frequency'),
                                              start_ms_of_day=self.get_param('start_ms_of_day'),
                                              end_ms_of_day=self.get_param('end_ms_of_day'))
        # self.market_data_system.set_market_data_setting(ticker_list=self.get_param('ticker_list'))
        # Let us set

