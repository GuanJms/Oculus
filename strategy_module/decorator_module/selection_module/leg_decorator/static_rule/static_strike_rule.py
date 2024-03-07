from strategy_module.decorator_module.rule_decorator import RuleDecorator
from strategy_module.leg_module.leg_rule import LegRule
from strategy_module.rule import Rule
from strategy_module.rule_class_checker import RuleClassChecker


class StaticStrikeRule(RuleDecorator):
    """
    StaticStrikeRule is a decorator that adds a static strike price of underlying to the put/call option rule.
    When rule is executed, only the option with the static strike price will be selected.
    """

    def __init__(self, rule: Rule, strike_price: int):
        RuleClassChecker.is_LegRule(rule)
        super().__init__(rule)
        self.rule_type = 'static'
        self.rule_name = 'StaticStrikeRule'
        self._strike_rule = {}
        self.rule_param = strike_price
        self._update_rule_param()

    @property
    def strike_rule(self):
        return self._strike_rule

    def execute(self):
        return self.rule.execute()

    def _update_rule_param(self):
        strike_rule = {'rule_type': self.rule_type, 'rule_name': self.rule_name,
                             'rule_param': self.rule_param}
        self.strike_rule.update(strike_rule)
        self.rule.add_param('strike_rule', self._strike_rule)
