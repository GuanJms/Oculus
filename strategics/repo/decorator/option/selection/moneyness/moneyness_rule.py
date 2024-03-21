from strategics.repo.decorator.rule_decorator import RuleDecorator
from strategics.repo.rule_class_checker import RuleClassChecker


class MoneynessRule(RuleDecorator):
    """
    MoneynessRule is a decorator that adds a moneyness filter to the put/call option rule.
    When the rule is executed, only options matching the closest moneyness condition is selected.
    """

    def __init__(self, rule, moneyness: float):
        RuleClassChecker.is_LegRule(rule)
        super().__init__(rule)
        self.rule_type = 'dynamic'
        self.rule_name = 'MoneynessRule'
        self.rule_param = moneyness  # Moneyness is a float value
        self._strike_rule = {}
        self._update_rule_param()

    @property
    def strike_rule(self):
        return self._strike_rule

    def execute(self):
        return self.rule.execute()

    def _update_rule_param(self):
        strike_rule = {'rule_type': self.rule_type, 'rule_name': self.rule_name,
                       'rule_param': self.rule_param}
        self._strike_rule.update(strike_rule)
        self.rule.add_param('strike_rule', self._strike_rule)
