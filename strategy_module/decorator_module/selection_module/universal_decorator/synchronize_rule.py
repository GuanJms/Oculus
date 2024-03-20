from typing import Optional
from strategy_module.decorator_module.rule_decorator import RuleDecorator
from strategy_module.decorator_module.selection_module.universal_decorator.synchronize_rule_creator import \
    SynchronizeRuleCreator
from strategics.repo.rule import Rule


class SynchronizeStrikeRule(RuleDecorator):
    """
    SynchronizeStrikeRule is a decorator class for Rule.
    During the execution, the rule that is synchronized will execute with the same strike price as the rule to copy.

    If a rule has synchronized strike, the main and mirror rules will have the same root.

    """

    def __init__(self, main_rule: Rule, rule: Optional[Rule] = None):
        if not rule:
            rule = SynchronizeRuleCreator.create_synchronize_rule(main_rule)
        super().__init__(rule)
        self._main_rule = main_rule
        self.rule_type = 'synchronize'
        self.rule_name = 'SynchronizeRule'
        self._synchronize_rule = {}
        self._update_rule_param()

    @property
    def synchronize_rule(self):
        return self._synchronize_rule

    def execute(self):
        raise NotImplementedError("TODO: implement execution part")

    def _update_rule_param(self):
        synchronize_rule = {'rule_type': self.rule_type, 'rule_name': self.rule_name,
                            'sync_rule_id': self._main_rule.get_id(), 'sync_object': 'strike'}
        self._synchronize_rule.update(synchronize_rule)
        self.rule.add_param('synchronize_rule', self._synchronize_rule)
