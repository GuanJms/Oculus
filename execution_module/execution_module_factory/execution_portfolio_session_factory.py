from execution_module.execution_portfolio import ExecutionPortfolioSession
from strategics.repo.core.strategy.strategy_rule import StrategyRule


class ExecutionPortfolioSessionFactory:

    @classmethod
    def create_execution_portfolio(cls, strategy_rule_instance: StrategyRule) -> ExecutionPortfolioSession:
        session = ExecutionPortfolioSession(strategy_rule_instance=strategy_rule_instance)
        return session
