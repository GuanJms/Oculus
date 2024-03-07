from strategy_module.combo_module.combo_rule import ComboRule
from strategy_module.rule import Rule
from strategy_module.rule_class_checker import RuleClassChecker


class CallSpreadRule(ComboRule):

    def __init__(self, long_leg_rule: Rule, short_leg_rule: Rule):
        RuleClassChecker.is_CallRule(long_leg_rule)
        RuleClassChecker.is_CallRule(short_leg_rule)
        super().__init__()
        self.long_leg_rule: Rule = long_leg_rule
        self.short_leg_rule: Rule = short_leg_rule
        self._combo_name = 'Call Spread'
        for leg_rule in [long_leg_rule, short_leg_rule]:
            self.add_leg_rule(leg_rule, 1)

    def add_leg_rule(self, leg_rule: Rule, position: int):
        super().add_leg_rule(leg_rule, position)

    def execute(self):
        raise NotImplementedError


class PutSpreadRule(ComboRule):

    def __init__(self, long_leg_rule: Rule, short_leg_rule: Rule):
        RuleClassChecker.is_PutRule(long_leg_rule)
        RuleClassChecker.is_PutRule(short_leg_rule)
        super().__init__()
        self.long_leg_rule: Rule = long_leg_rule
        self.short_leg_rule: Rule = short_leg_rule
        self._combo_name = 'Put Spread'
        for leg_rule in [long_leg_rule, short_leg_rule]:
            self.add_leg_rule(leg_rule, 1)

    def add_leg_rule(self, leg_rule: Rule, position: int):
        super().add_leg_rule(leg_rule, position)

    def execute(self):
        raise NotImplementedError
