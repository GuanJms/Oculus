from strategy_module.combo_module.combo_rule import ComboRule
from strategy_module.rule import Rule
from strategy_module.rule_class_checker import RuleClassChecker


class IronCondorRule(ComboRule):

    def __init__(self, long_call_rule: Rule, short_call_rule: Rule, long_put_rule: Rule, short_put_rule: Rule):
        # Verify the rule types
        RuleClassChecker.is_CallRule(long_call_rule)
        RuleClassChecker.is_CallRule(short_call_rule)
        RuleClassChecker.is_PutRule(long_put_rule)
        RuleClassChecker.is_PutRule(short_put_rule)

        super().__init__()
        self.combo_type = 'option_combo'
        self.combo_name = 'IronCondor'

        self.long_call_rule: Rule = long_call_rule
        self.short_call_rule: Rule = short_call_rule
        self.long_put_rule: Rule = long_put_rule
        self.short_put_rule: Rule = short_put_rule

        # Add each leg with its position to the combo
        self.add_leg_rule(long_call_rule, 1)
        self.add_leg_rule(short_call_rule, -1)  # Assuming negative position indicates 'short'
        self.add_leg_rule(long_put_rule, 1)
        self.add_leg_rule(short_put_rule, -1)

    def add_leg_rule(self, leg_rule: Rule, position: int):
        super().add_leg_rule(leg_rule, position)

    def execute(self):
        raise NotImplementedError



