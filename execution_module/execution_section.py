from backtest_module.backtest_data_section import BacktestDataSection
from execution_module.execution_time_controller import ExecutionTimeController
from initialization_module.initialization_manager import InitializationManager
from strategy_module.strategy_rule import StrategyRule
from global_component_id_generator import GlobalComponentIDGenerator
from utils.system_optimize import track_memory_usage


class ExecutionSection:

    def __init__(self, strategy_rule_instance: StrategyRule, execution_time_controller: ExecutionTimeController,
                 backtest_data_section: BacktestDataSection):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._strategy_rule = strategy_rule_instance
        self._execution_time_controller = execution_time_controller
        self._backtest_data_section = backtest_data_section

    @property
    def id(self):
        return self._id

    @property
    def execution_time_controller(self):
        return self._execution_time_controller

    @property
    def strategy_rule(self):
        return self._strategy_rule

    def get_backtest_data_section(self):
        return self._backtest_data_section

    def execute(self):
        """
        Brainstrome: StrategyRule will take roots to execute. If strategyRull has a specified StaticRootRule, then it
        it will request the data from the backtest_data_manager. If it does not have a specified StaticRootRule, then
        it will execute the strategy based on all tickers in the backtest_data_manager.
        TODO: implement StaticRootRule handling
        """
        raise NotImplementedError("TODO: implement execution part")

    def request_quote_data(self):
        raise NotImplementedError("TODO: implement read_quote_board")

    def request_data_section_process_status(self):
        return self._backtest_data_section.get_data_section_process_status()

    def start_execution(self):
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
        #TODO: exectue strategy

    def _request_execution_status(self):
        return self._execution_time_controller.get_execution_status()

    def _request_next_time_message(self):
        return self._execution_time_controller.get_next_time_message()

    def _run_same_quote_day_execution(self, quote_date_message, next_msd):
        self._backtest_data_section.request_advance_time()

    def _run_change_quote_day_execution(self, quote_date, start_msd):
        self._backtest_data_section.advance_date(quote_date, start_msd)
