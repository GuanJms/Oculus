from strategics.repo.decorator.rule_decorator import RuleDecorator
from strategics.repo.rule import Rule

from strategics.repo.rule_class_checker import RuleClassChecker



class DeltaRule(RuleDecorator):
    """
    DeltaRule is a concrete decorator that adds a delta rule to the the put/call option rule for selection.
    When the rule is executed, only the option with the delta value close to the target delta will be selected.
    """

    def __init__(self, rule: Rule, delta: float):
        RuleClassChecker.is_LegRule(rule)
        super().__init__(rule)
        self.rule_type = 'dynamic'
        self.rule_name = 'DeltaRule'

        delta = self.standardized_delta(delta)
        if RuleClassChecker.is_PutRule(rule, sort_check=True):
            if delta > 0:
                delta = -delta
        self._delta = delta

        self._delta_rule = None
        self._update_rule_param()

    @property
    def delta(self):
        return self._delta

    @property
    def delta_rule(self):
        return self._delta_rule

    def execute(self):
        # In a real implementation, this method would filter options based on the target delta value.
        # This could involve selecting options whose delta values are close to the specified target_delta.
        #TODO:
        # DeltaRuleHandler.execute(self.rule, self.delta)
        return self.rule.execute()

    def _update_rule_param(self):
        self._delta_rule = {'rule_type': self.rule_type, 'rule_name': self.rule_name,
                            'rule_param': self.delta}
        self.rule.add_param('delta_rule', self._delta_rule)

    def standardized_delta(self, delta: float):
        if delta > 1:
            delta = delta / 100

        if RuleClassChecker.is_PutRule(self.rule, sort_check=True):
            if delta > 0:
                delta = -delta

        return delta
