from backtest_module.backtest_data_section import BacktestDataSection
from execution_module.execution_section import ExecutionSection
from execution_module.execution_time_controller import ExecutionTimeController
from strategy_module.strategy_rule import StrategyRule


class ExecutionSectionFactory:
    @classmethod
    def create_section(cls, strategy_rule_instance: StrategyRule,
                       execution_time_controller: ExecutionTimeController,
                       backtest_data_section: BacktestDataSection) -> ExecutionSection:
        section = ExecutionSection(strategy_rule_instance=strategy_rule_instance,
                                   execution_time_controller=execution_time_controller,
                                   backtest_data_section=backtest_data_section)
        return section
