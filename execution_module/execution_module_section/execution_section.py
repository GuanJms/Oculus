from typing import List

from backtest_module.backtest_data_section import BacktestDataSection
from execution_module.execution_module_section.execution_action_module.exectuion_action import ExecutionAction
from execution_module.execution_module_section.execution_signal_module.execution_signal import ExecutionSignal
from execution_module.execution_portfolio import ExecutionPortfolioSection
from execution_module.execution_time_controller import ExecutionTimeController
from initialization_module.initialization_manager import InitializationManager
from strategy_module.strategy_rule import StrategyRule
from global_component_id_generator import GlobalComponentIDGenerator


class ExecutionSection:

    def __init__(self, strategy_rule_instance: StrategyRule, execution_time_controller: ExecutionTimeController,
                 backtest_data_section: BacktestDataSection, execution_portfolio_section: ExecutionPortfolioSection):
        self._execution_signal_list: List[ExecutionSignal] = []
        self._execution_action_list: List[ExecutionAction] = []
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._strategy_rule = strategy_rule_instance
        self._execution_time_controller = execution_time_controller
        self._backtest_data_section = backtest_data_section
        self._execution_portfolio_section = execution_portfolio_section

    @property
    def id(self):
        return self._id

    @property
    def execution_portfolio_section(self):
        return self._execution_portfolio_section

    @property
    def execution_time_controller(self):
        return self._execution_time_controller

    @property
    def strategy_rule(self):
        return self._strategy_rule

    def get_backtest_data_section(self):
        return self._backtest_data_section

    def request_quote_data(self):
        raise NotImplementedError("TODO: implement read_quote_board")

    def request_data_section_process_status(self):
        return self._backtest_data_section.get_data_section_process_status()

    def start_execution(self):
        self._execution_signal_list, self._execution_action_list = self._strategy_rule.execute()
        while self._request_execution_status() == "RUNNING":
            self._run_execution()

    def initialize(self):
        InitializationManager.initialize_time_controller(self._execution_time_controller)

    def _run_execution(self):
        TYPE_MESSAGE, quote_date, next_msd = self._request_next_time_message()
        if TYPE_MESSAGE == "SAME_QUOTE_DATE":
            self._run_same_quote_day_execution(quote_date, next_msd)
        elif TYPE_MESSAGE == "CHANGE_QUOTE_DATE":
            print('_run_execution', TYPE_MESSAGE, quote_date, next_msd)
            self._run_change_quote_day_execution(quote_date, next_msd)
        # TODO: exectue strategy

    def _request_execution_status(self):
        return self._execution_time_controller.get_execution_status()

    def _request_next_time_message(self):
        return self._execution_time_controller.get_next_time_message()

    def _run_same_quote_day_execution(self, quote_date_message, next_msd):
        self._backtest_data_section.request_advance_time()

    def _run_change_quote_day_execution(self, quote_date, start_msd):
        self._backtest_data_section.advance_date(quote_date, start_msd)
