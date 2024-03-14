from global_component_id_generator import GlobalComponentIDGenerator
from strategy_module.strategy_rule import StrategyRule
from section import Section


class ExecutionPortfolioSection(Section):

    def __init__(self, strategy_rule_instance: StrategyRule):
        super().__init__()
        self._strategy_rule = strategy_rule_instance
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))

    @property
    def id(self):
        return self._id

    def refresh_status(self):
        pass
