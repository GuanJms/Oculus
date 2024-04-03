from utils.global_id import GlobalComponentIDGenerator
from strategics.repo.core.strategy.strategy_rule import StrategyRule
from session import Session


class ExecutionPortfolioSession(Session):

    def __init__(self, strategy_rule_instance: StrategyRule):
        super().__init__()
        self._strategy_rule = strategy_rule_instance
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))

    @property
    def id(self):
        return self._id

    def refresh_status(self):
        pass
