from typing import Optional

from strategy_module.decorator_module.rule_decorator import RuleDecorator


def _method_checker(method: Optional[str] = None):
    if method not in ['DTE', 'DTE_range']:
        raise ValueError("method must be either 'DTE' or 'DTE_range'")


class ExpirationDTERule(RuleDecorator):
    """
    ExpirationRule is a decorator that adds expiration DTE to a rule.
    The rule can only be executed if the expiration quote_date is at DTE or a range of boundaries of DTE.
    """

    def __init__(self, rule, method: Optional[str] = None, dte: Optional[int] = None,
                 dte_min: Optional[int] = None, dte_max: Optional[int] = None):
        _method_checker(method)
        super().__init__(rule)
        self.rule_type = 'dynamic'
        self.rule_name = 'ExpirationDTERule'
        self._method = method
        self._dte = dte
        self._dte_min = dte_min
        self._dte_max = dte_max
        self._expiration_rule = {}
        self._update_rule_param()

    @property
    def expiration_rule(self):
        return self._expiration_rule

    def execute(self):
        raise NotImplementedError("TODO: implement execution part")

    def _update_rule_param(self):
        expiration_rule= {'rule_type': self.rule_type, 'rule_name': self.rule_name,
                          'method': self._method, 'DTE': self._dte, 'DTE_min': self._dte_min, 'DTE_max': self._dte_max}
        self._expiration_rule.update(expiration_rule)

