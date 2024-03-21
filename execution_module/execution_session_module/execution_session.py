from typing import List, Optional

from market_data_system.backtest_simulation.backtest_data_session import BacktestDataSession
from execution_module.execution_session_module.action_manager import \
    ExecutionSessionActionManager
from execution_module.execution_session_module.signal_manager import \
    ExecutionSessionSignalManager
from execution_module.execution_portfolio import ExecutionPortfolioSession
from execution_module.execution_session_module.execution_signal import ExecutionSignal
from execution_module.execution_time_controller import ExecutionTimeController
from initialization_module.initialization_manager import InitializationManager
from strategics.repo.core.strategy.strategy_rule import StrategyRule
from global_utils import GlobalComponentIDGenerator


class ExecutionSession:

    def __init__(self, strategy_rule_instance: StrategyRule, execution_time_controller: ExecutionTimeController,
                 backtest_data_session: BacktestDataSession, execution_portfolio_session: ExecutionPortfolioSession):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._strategy_rule = strategy_rule_instance
        self._execution_time_controller = execution_time_controller
        self._backtest_data_session = backtest_data_session
        self._execution_portfolio_session = execution_portfolio_session
        self._signal_manager: Optional[ExecutionSessionSignalManager] = None
        self._action_manager: Optional[ExecutionSessionActionManager] = None

    @property
    def id(self):
        return self._id

    @property
    def execution_portfolio_session(self):
        return self._execution_portfolio_session

    @property
    def execution_time_controller(self):
        return self._execution_time_controller

    @property
    def strategy_rule(self):
        return self._strategy_rule

    def get_backtest_data_session(self):
        return self._backtest_data_session

    def request_quote_data(self):
        raise NotImplementedError("TODO: implement read_quote_board")

    def request_data_session_process_status(self):
        return self._backtest_data_session.get_data_session_process_status()

    def start_execution(self):
        while self._request_execution_status() == "RUNNING":
            self._run_execution()

    def initialize(self):
        InitializationManager.initialize_time_controller(self._execution_time_controller)

        # Initializes the signals and actions
        execution_signal_list, execution_action_list = self._strategy_rule.execute()
        InitializationManager.initialize_execution_session_signal_manager(signal_manager=self._signal_manager,
                                                                          execution_signal_list=execution_signal_list)
        InitializationManager.initialize_execution_session_action_manager(action_manager=self._action_manager,
                                                                          execution_action_list=execution_action_list)

    def _run_execution(self):
        TYPE_MESSAGE, quote_date, next_msd = self._request_next_time_message()
        if TYPE_MESSAGE == "SAME_QUOTE_DATE":
            self._run_same_quote_day_execution(quote_date, next_msd)
        elif TYPE_MESSAGE == "CHANGE_QUOTE_DATE":
            print('_run_execution', TYPE_MESSAGE, quote_date, next_msd)
            self._run_change_quote_day_execution(quote_date, next_msd)
        # TODO: ask execution_system session signal_generation manager if it should proceed with action or not
        #   (signal_generation manager will refresh status of all signals and return True or False)
        # TODO: If execution_system session signal_generation manager says yes, then proceed with action manager

    def _request_execution_status(self):
        return self._execution_time_controller.get_execution_status()

    def _request_next_time_message(self):
        return self._execution_time_controller.get_next_time_message()

    def _run_same_quote_day_execution(self, quote_date_message, next_msd):
        self._backtest_data_session.request_advance_time()

    def _run_change_quote_day_execution(self, quote_date, start_msd):
        self._backtest_data_session.advance_date(quote_date, start_msd)

    def _create_signal_session_list(self) -> List[ExecutionSignal]:
        signal_session_list = []
        for execution_signal in self._execution_signal_list:
            signal_session = self._create_signal_session(execution_signal)
            signal_session_list.append(signal_session)
        return signal_session_list

    def _create_signal_session(self, execution_signal: ExecutionSignal,
                               execution_singal_handler: ExecutionSignalCoordinator) -> ExecutionSignal:
        pass

    def set_execution_session_signal_manager(self, execution_session_signal_manager: ExecutionSessionSignalManager):
        if not isinstance(execution_session_signal_manager, ExecutionSessionSignalManager):
            raise ValueError("execution_session_signal_manager must be an instance of ExecutionSessionSignalManager")
        self._signal_manager = execution_session_signal_manager

    def set_execution_session_action_manager(self, execution_session_action_manager: ExecutionSessionActionManager):
        if not isinstance(execution_session_action_manager, ExecutionSessionActionManager):
            raise ValueError("execution_session_action_manager must be an instance of ExecutionSessionActionManager")
        self._action_manager = execution_session_action_manager
