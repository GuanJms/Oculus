from backtest_module.backtest_data_section import BacktestDataSection
from execution_module.execution_module_section.execution_section import ExecutionSection
from strategy_module.strategy_rule import StrategyRule
from execution_module.execution_module_factory.execution_portfolio_section_factory import ExecutionPortfolioSectionFactory
from execution_module.execution_module_factory.execution_time_controller_factory import ExecutionTimeControllerFactory


class ExecutionSectionFactory:
    @classmethod
    def create_section(cls, strategy_rule_instance: StrategyRule,
                       time_params: dict,
                       backtest_data_section: BacktestDataSection) -> ExecutionSection:
        execution_time_controller = ExecutionTimeControllerFactory.create_execution_time_controller(time_params)
        execution_portfolio = ExecutionPortfolioSectionFactory.create_execution_portfolio(strategy_rule_instance)
        section = ExecutionSection(strategy_rule_instance=strategy_rule_instance,
                                   execution_time_controller=execution_time_controller,
                                   backtest_data_section=backtest_data_section,
                                   execution_portfolio_section=execution_portfolio)
        return section
