
class RuleClassChecker:

    @staticmethod
    def _checkDecoratorRule(rule):
        from strategy_module.decorator_module.rule_decorator import RuleDecorator
        while issubclass(rule.__class__, RuleDecorator):
            rule = rule.rule
        return rule

    @classmethod
    def is_LegRule(cls, rule, sort_check: bool = False):
        from strategics.repo.core.leg import LegRule
        rule = cls._checkDecoratorRule(rule)

        if not issubclass(rule.__class__, LegRule):
            # check if rule is subclass of LegRule
            if sort_check:
                return False
            raise TypeError("The rule must be a subclass of LegRule.")
        return True

    @classmethod
    def is_ComboRule(cls, rule, sort_check: bool = False):
        from strategics.repo.core.combo.combo_rule import ComboRule
        rule = cls._checkDecoratorRule(rule)
        if not issubclass(rule.__class__, ComboRule):
            if sort_check:
                return False
            raise TypeError("The rule must be a subclass of ComboRule.")
        return True

    @classmethod
    def is_CallRule(cls, rule, sort_check: bool = False):
        from strategics.repo.core.leg.option.leg_basics.call_rule import CallRule
        rule = cls._checkDecoratorRule(rule)
        if not issubclass(rule.__class__, CallRule):
            if sort_check:
                return False
            raise TypeError("The rule must be a subclass of CallRule.")
        return True

    @classmethod
    def is_PutRule(cls, rule, sort_check: bool = False):
        from strategics.repo.core.leg.option.leg_basics.put_rule import PutRule
        rule = cls._checkDecoratorRule(rule)
        if not issubclass(rule.__class__, PutRule):
            if sort_check:
                return False
            raise TypeError("The rule must be a subclass of PutRule.")
        return True

    @classmethod
    def is_OptionRule(cls, rule, sort_check: bool = False):
        from strategics.repo.core.leg.option.option_leg_rule import OptionRule
        rule = cls._checkDecoratorRule(rule)
        if not issubclass(rule.__class__, OptionRule):
            if sort_check:
                return False
            raise TypeError("The rule must be a subclass of OptionRule.")
        return True
