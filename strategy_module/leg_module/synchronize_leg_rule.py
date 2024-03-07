from strategy_module.leg_module.leg_rule import LegRule


class SynchronizeLegRule(LegRule):
    """
    Synchronize Leg Rule is a empty entity for holding LegRule that will be decorated by SynchronizeRule.
    """

    def __init__(self):
        super().__init__()
        self._leg_type = 'synchronize_leg'

    def execute(self):
        raise NotImplementedError("Parent class SynchronizeLegRule does not implement execute method.")
