from typing import Optional

from strategics.repo.core.combo.combo_rule import ComboRule
from strategics.repo.rule import Rule
from strategics.repo.rule_class_checker import RuleClassChecker


class AdhocComboRule(ComboRule):

    def __init__(self, combo_type: Optional[str] = 'Adhoc Combo'):
        super().__init__()
        self._combo_type = combo_type

    def add_leg_rule(self, leg_rule: Rule, position: int):
        RuleClassChecker.is_LegRule(leg_rule)
        super().add_leg_rule(leg_rule, position)

    def execute(self):
        raise NotImplementedError
