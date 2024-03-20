from typing import Tuple, List

from execution_module.execution_session_module.exectuion_action import ExecutionAction
from execution_module.execution_session_module.execution_signal import ExecutionSignal
from global_component_id_generator import GlobalComponentIDGenerator
from strategics.repo.rule import Rule
from strategics.repo.rule_class_checker import RuleClassChecker


class StrategyRule(Rule):

    def __init__(self):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._strategy_param = {'id': self._id, 'combo_list': {}}
        self._strategy_name = None
        self._strategy_type = None
        self._combo_rule_dict: dict[Rule, float] = dict()

    @property
    def id(self):
        return self._id

    @property
    def strategy_name(self):
        return self._strategy_name

    @property
    def strategy_type(self):
        return self._strategy_type

    @strategy_name.setter
    def strategy_name(self, strategy_name: str):
        self._strategy_name = strategy_name
        self._update_rule_param()

    @strategy_type.setter
    def strategy_type(self, strategy_type: str):
        self._strategy_type = strategy_type
        self._update_rule_param()

    def execute(self) -> Tuple[List[ExecutionSignal], List[ExecutionAction]]:
        raise NotImplementedError("Execute method must be implemented by subclasses.")

    def get_param(self):
        return self._strategy_param

    def add_combo_rule(self, combo_rule: Rule, position: int):
        RuleClassChecker.is_ComboRule(combo_rule)
        combo_param = combo_rule.get_param()
        combo_list = self._strategy_param.get('combo_list')
        combo_list[combo_rule.get_id()] = {'combo_param': combo_param, 'position': position}
        self._combo_rule_dict[combo_rule] = position


    def get_id(self):
        return self._id

    def _update_rule_param(self):
        strategy_param = {'strategy_type': self._strategy_type, 'strategy_name': self._strategy_name}
        self._strategy_param.update(strategy_param)

    def add_param(self, rule_name: str, rule_param: dict):
        rule_param_if_exist = self._strategy_param.get(rule_name, {})
        rule_param_if_exist.update(rule_param)
        self._strategy_param[rule_name] = rule_param_if_exist

    def get_combo_list(self):
        return self._strategy_param['combo_list']

    def export_expiration_params(self):
        return {}