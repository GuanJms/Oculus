from typing import Optional, Tuple, List
from strategics.repo import SignalGenerator, ActionGenerator, Rule


class RuleDecorator(Rule):

    def __init__(self, rule: Optional[Rule]) -> None:
        self._rule = rule

    @property
    def rule(self) -> Rule:
        return self._rule

    def execute(self) -> Tuple[List[SignalGenerator], List[ActionGenerator]]:
        raise NotImplementedError("Parent class RuleDecorator does not implement execute method.")

    def get_param(self):
        return self._rule.get_param()

    def add_param(self, rule_name: str, rule_param: dict):
        self._rule.add_param(rule_name, rule_param)

    def _update_rule_param(self):
        raise NotImplementedError("Parent class RuleDecorator does not implement _update_rule_param method.")

    def get_id(self):
        return self._rule.get_id()

    def get_var(self, var_name: str):
        if hasattr(self, var_name):
            return getattr(self, var_name)
        elif hasattr(self, '_rule'):
            return self._rule.get_var(var_name)
        else:
            return None
