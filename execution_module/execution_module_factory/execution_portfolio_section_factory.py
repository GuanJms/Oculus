from execution_module.execution_portfolio import ExecutionPortfolioSection
from strategy_module.strategy_rule import StrategyRule


class ExecutionPortfolioSectionFactory:

    @classmethod
    def create_execution_portfolio(cls, strategy_rule_instance: StrategyRule) -> ExecutionPortfolioSection:
        section = ExecutionPortfolioSection(strategy_rule_instance=strategy_rule_instance)
        return section
