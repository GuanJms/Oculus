from typing import Optional

from backtest_module.backtest_data_section import BacktestDataSection
from execution_module.execution_module_factory.execution_section_factory import ExecutionSectionFactory
from execution_module.execution_module_section.execution_section import ExecutionSection
from global_component_id_generator import GlobalComponentIDGenerator
from initialization_module.initialization_manager import InitializationManager
from strategy_module.strategy_rule import StrategyRule

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backtest_module.backtest_manager import BacktestManager


class ExecutionManager:

    def __init__(self, ):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._backtest_manager: Optional[BacktestManager] = None
        self._execution_section_dict: dict[str, ExecutionSection] = {}
        self._strategy_id_to_execution_section_id_dict: dict[str, str] = {}

    @property
    def id(self):
        return self._id

    def get_backtest_time_params(self):
        return self._backtest_manager.get_backtest_time_params()

    def get_backtest_ticker_params(self) -> dict:
        return self._backtest_manager.get_backtest_ticker_params()

    def get_execution_section(self, strategy_rule_instance: StrategyRule) -> Optional[ExecutionSection]:
        return self._execution_section_dict.get(strategy_rule_instance.id)

    def get_execution_section_dict(self):
        return self._execution_section_dict

    def _initialize_section(self, strategy_rule_instance: StrategyRule,
                            backtest_data_section: BacktestDataSection) -> ExecutionSection:
        time_params = self.get_backtest_time_params()
        tickers = self.get_backtest_ticker_params()

        backtest_data_section.set_ticker_params(tickers)
        expiration_params = strategy_rule_instance.export_expiration_params()
        InitializationManager.initialize_backtest_data_section(backtest_data_section, time_params, expiration_params)
        execution_section = ExecutionSectionFactory.create_section(strategy_rule_instance,
                                                                   time_params,
                                                                   backtest_data_section)
        InitializationManager.initialize_execute_section(execution_section)

        self._execution_section_dict[execution_section.id] = execution_section
        self._strategy_id_to_execution_section_id_dict[strategy_rule_instance.id] = execution_section.id
        return execution_section

    def execute_strategy(self, strategy_rule_instance: StrategyRule):
        backtest_data_section = self._backtest_manager.request_backtest_data_section()
        execution_section = self._initialize_section(strategy_rule_instance, backtest_data_section)
        execution_section.start_execution()

    def set_backtest_manager(self, backtest_manager: 'BacktestManager'):
        self._backtest_manager = backtest_manager

    def get_backtest_manager(self) -> 'BacktestManager':
        return self._backtest_manager


