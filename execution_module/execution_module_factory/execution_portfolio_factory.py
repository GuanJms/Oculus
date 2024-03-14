from execution_module.execution_portfolio import ExecutionPortfolio
from strategy_module.strategy_rule import StrategyRule


class ExecutionPortfolioFactory:

    @classmethod
    def create_execution_portfolio(cls, strategy_rule_instance: StrategyRule) -> ExecutionPortfolio:
        section = ExecutionPortfolio(strategy_rule_instance=strategy_rule_instance)
        return section
