from utils.global_id import GlobalComponentIDGenerator
from strategics.repo.rule import Rule
from strategics.repo.rule_class_checker import RuleClassChecker


class ComboRule(Rule):

    def __init__(self):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._combo_param = {'id': self._id, 'leg_list' : {}}
        self._combo_type = None
        self._combo_name = None

    @property
    def id(self):
        return self._id

    def get_id(self):
        return self._id

    @property
    def combo_type(self):
        return self._combo_type

    @property
    def combo_name(self):
        return self._combo_name

    @property
    def combo_param(self):
        return self._combo_param

    @combo_name.setter
    def combo_name(self, combo_name: str):
        self._combo_name = combo_name
        self._update_rule_param()

    @combo_type.setter
    def combo_type(self, combo_type: str):
        self._combo_type = combo_type
        self._update_rule_param()

    def execute(self):
        raise NotImplementedError("Parent class ComboRule does not implement execute method.")

    def add_leg_rule(self, leg_rule: Rule, position: int):
        RuleClassChecker.is_LegRule(leg_rule)
        leg_param = leg_rule.get_param()
        leg_list = self._combo_param.get('leg_list')
        leg_list[leg_rule.get_id()] = {'leg_param': leg_param, 'position_generation': position}

    def get_param(self):
        return self._combo_param

    def _update_rule_param(self):
        combo_param = {'combo_type': self._combo_type, 'combo_name': self._combo_name}
        self._combo_param.update(combo_param)

    def add_param(self, rule_name: str, rule_param: dict):
        rule_param_if_exist = self._combo_param.get(rule_name, {})
        rule_param_if_exist.update(rule_param)
        self._combo_param[rule_name] = rule_param_if_exist
