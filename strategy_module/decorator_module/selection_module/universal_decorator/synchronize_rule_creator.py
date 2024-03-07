from strategy_module.rule import Rule
from strategy_module.rule_class_checker import RuleClassChecker
from strategy_module.combo_module.synchronize_combo_rule import SynchronizeComboRule
from strategy_module.leg_module.synchronize_leg_rule import SynchronizeLegRule


class SynchronizeRuleCreator:
    """
    SynchronizeRule is a rule that is used to synchronize the execution of the rule to copy.
    """

    @staticmethod
    def create_synchronize_rule(main_rule: Rule):
        if RuleClassChecker.is_LegRule(main_rule, sort_check=True):
            return SynchronizeRuleCreator._create_synchronize_leg_rule()
        elif RuleClassChecker.is_ComboRule(main_rule, sort_check=True):
            return SynchronizeRuleCreator._create_synchronize_combo_rule()
        else:
            raise TypeError(f"Rule to copy is not of type LegRule or ComboRule. Type: {type(main_rule)}")

    @staticmethod
    def _create_synchronize_leg_rule() -> SynchronizeLegRule:
        return SynchronizeLegRule()

    @staticmethod
    def _create_synchronize_combo_rule() -> SynchronizeComboRule:
        return SynchronizeComboRule()
