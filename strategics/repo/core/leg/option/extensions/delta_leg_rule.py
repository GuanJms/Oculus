from strategics.repo.decorator.option.selection import DeltaRule
from strategics.repo.core.leg.option.basics import CallRule
from strategics.repo.core.leg.option.basics import PutRule


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
