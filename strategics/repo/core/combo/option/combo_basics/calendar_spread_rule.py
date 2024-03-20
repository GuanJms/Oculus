from strategics.repo.core.combo.combo_rule import ComboRule
from strategics.repo.rule import Rule
from strategics.repo.rule_class_checker import RuleClassChecker

"""
Calender Spread Rule
Sell near term option and buy long term option with same strike price and different expiration quote_date
"""


class CalendarSpreadRule(ComboRule):
    def __init__(self, long_term_leg_rule: Rule, short_term_leg_rule: Rule):
        RuleClassChecker.is_OptionRule(long_term_leg_rule)
        RuleClassChecker.is_OptionRule(short_term_leg_rule)
        super().__init__()
        self.long_term_leg_rule: Rule = long_term_leg_rule
        self.short_term_leg_rule: Rule = short_term_leg_rule
        self._combo_name = 'Calendar Spread'
        # Assuming both legs have the same position size but opposite positions
        self.add_leg_rule(long_term_leg_rule, 1)  # Long position
        self.add_leg_rule(short_term_leg_rule, -1)  # Short position
        #TODO: calendar spread has different expiration quote_date - add two strike rule and expiration quote_date rule(s)
        #TODO: Not sure if I should add one rule or two rules regarding expiration quote_date yet.
        raise NotImplementedError

    def add_leg_rule(self, leg_rule: Rule, position: int):
        super().add_leg_rule(leg_rule, position)
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError


