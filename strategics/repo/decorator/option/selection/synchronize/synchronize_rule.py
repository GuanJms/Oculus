from typing import Optional

from strategics.repo.core.combo.option.specialties.synchronize_combo_rule import SynchronizeComboRule
from strategics.repo.core.leg.specialties.synchronize_leg_rule import SynchronizeLegRule
from strategics.repo.rule_class_checker import RuleClassChecker
from strategics.repo.decorator.rule_decorator import RuleDecorator
from strategics.repo.rule import Rule


class SynchronizeStrikeRule(RuleDecorator):
    """
    SynchronizeStrikeRule is a decorator class for Rule.
    During the execution_system, the rule that is synchronized will execute with the same strike price as the rule to copy.

    If a rule has synchronized strike, the main and mirror rules will have the same root.

    """

    def __init__(self, main_rule: Rule, rule: Optional[Rule] = None):
        if not rule:
            rule = self._create_synchronize_rule(main_rule)
        super().__init__(rule)
        self._main_rule = main_rule
        self.rule_type = 'synchronize'
        self.rule_name = 'SynchronizeRule'
        self._synchronize_rule = {}
        self._update_rule_param()

    @property
    def synchronize_rule(self):
        return self._synchronize_rule

    def execute(self):
        raise NotImplementedError("TODO: implement execution_system part")

    def _update_rule_param(self):
        synchronize_rule = {'rule_type': self.rule_type, 'rule_name': self.rule_name,
                            'sync_rule_id': self._main_rule.get_id(), 'sync_object': 'strike'}
        self._synchronize_rule.update(synchronize_rule)
        self.rule.add_param('synchronize_rule', self._synchronize_rule)

    @staticmethod
    def _create_synchronize_leg_rule() -> SynchronizeLegRule:
        return SynchronizeLegRule()

    @staticmethod
    def _create_synchronize_combo_rule() -> SynchronizeComboRule:
        return SynchronizeComboRule()

    @staticmethod
    def _create_synchronize_rule(main_rule: Rule):
        if RuleClassChecker.is_LegRule(main_rule, sort_check=True):
            return SynchronizeStrikeRule._create_synchronize_leg_rule()
        elif RuleClassChecker.is_ComboRule(main_rule, sort_check=True):
            return SynchronizeStrikeRule._create_synchronize_combo_rule()
        else:
            raise TypeError(f"Rule to copy is not of type LegRule or ComboRule. Type: {type(main_rule)}")
