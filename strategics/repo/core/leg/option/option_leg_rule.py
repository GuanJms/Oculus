from strategics.repo.core.leg.leg_rule import LegRule


class OptionRule(LegRule):
    def __init__(self):
        super().__init__()
        self._option_type = None
        self._leg_type = 'option_leg'

    @property
    def option_type(self):
        return self._option_type

    @option_type.setter
    def option_type(self, option_type: str):
        self._option_type = option_type
        self._leg_param['option_type'] = self._option_type
        self._update_rule_param()

    def get_option_type(self):
        return self.option_type

    def execute(self):
        raise NotImplementedError("Parent class OptionRule does not implement execute method.")


