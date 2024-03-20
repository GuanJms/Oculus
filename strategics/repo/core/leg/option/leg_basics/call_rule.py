from strategics.repo.core.leg.option.option_leg_rule import OptionRule


class CallRule(OptionRule):
    def __init__(self):
        super().__init__()
        self.option_type = 'Call'

    def execute(self):
        raise NotImplementedError
