from strategy_module.decorator_module.selection_module.leg_decorator.dynamic_rule.delta_rule import DeltaRule
from strategy_module.leg_module.option_leg_rule import PutRule, CallRule


class DeltaPutRule(DeltaRule):
    def __init__(self, delta: float):
        if delta > 1:
            delta = delta / 100
        if delta > 0:
            delta = -delta
        rule = PutRule()
        super().__init__(rule, delta)


class DeltaCallRule(DeltaRule):
    def __init__(self, delta: float):
        if delta > 1:
            delta = delta / 100
        rule = CallRule()
        super().__init__(rule, delta)
