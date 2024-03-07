from global_component_id_generator import GlobalComponentIDGenerator
from strategy_module.rule import Rule


class LegRule(Rule):

    def __init__(self):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._leg_type = None
        self._leg_param = {'id': self._id}
        self._update_rule_param()

    @property
    def leg_type(self):
        return self._leg_type

    def get_id(self):
        return self._id

    @property
    def id(self):
        return self._id

    def execute(self):
        raise NotImplementedError("Parent class LegRule does not implement execute method.")

    def get_param(self):
        return self._leg_param

    def add_param(self, rule_name, rule_param):
        rule_param_if_exist = self._leg_param.get(rule_name, {})
        rule_param_if_exist.update(rule_param)
        self._leg_param[rule_name] = rule_param_if_exist

    def _update_rule_param(self):
        rule_param = {'leg_type': self._leg_type}
        self._leg_param.update(rule_param)
