from strategics.repo.decorator.rule_decorator import RuleDecorator


class StaticRootRule(RuleDecorator):
    """"
    StaticRootRule is a decorator that adds a static root to a rule.
    The rule can only be executed if the root is present in the input.
    """

    def __init__(self, rule, root: str):
        super().__init__(rule)
        self.rule_type = 'static'
        self.rule_name = 'StaticRootRule'
        self._root_rule = {}
        self.rule_param = root
        self._update_rule_param()

    @property
    def root_rule(self):
        return self._root_rule

    def execute(self):
        return self.rule.execute()

    def _update_rule_param(self):
        root_rule = {'rule_type': self.rule_type, 'rule_name': self.rule_name,
                     'rule_param': self.rule_param}
        self._root_rule.update(root_rule)
        self.rule.add_param('root_rule', self._root_rule)
