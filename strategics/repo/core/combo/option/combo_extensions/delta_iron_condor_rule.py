from strategics.repo.core.combo.option.combo_basics.iron_condor_rule import IronCondorRule
from strategics.repo.core.leg.leg_template.delta_leg_rule import DeltaCallRule, DeltaPutRule


class DeltaIronCondorRule(IronCondorRule):

    def __init__(self, long_call_delta: float, short_call_delta: float, long_put_delta: float, short_put_delta: float):
        long_call_rule = DeltaCallRule(delta=long_call_delta)
        short_call_rule = DeltaCallRule(delta=short_call_delta)
        long_put_rule = DeltaPutRule(delta=long_put_delta)
        short_put_rule = DeltaPutRule(delta=short_put_delta)
        super().__init__(long_call_rule=long_call_rule,
                         short_call_rule=short_call_rule,
                         long_put_rule=long_put_rule,
                         short_put_rule=short_put_rule)





