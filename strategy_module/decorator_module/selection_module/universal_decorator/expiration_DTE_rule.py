from typing import Optional, Tuple, List

from execution_module.execution_session_module.exectuion_action import ExecutionAction
from execution_module.execution_session_module.execution_signal import ExecutionSignal
from strategy_module.coordinator_module.range_dte_signal import \
    RangeDTESignal
from strategy_module.coordinator_module.single_dte_signal import \
    SingleDTESignal
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

    def execute(self) -> Tuple[List[ExecutionSignal], List[ExecutionAction]]:
        execution_signal_list, execution_action_list = self.rule.execute()

    def signal_generator(self) -> List[ExecutionSignal]:
        type = self.get_dte_rule_type()
        if type == 'single':
            signal_list = self._generate_single_dte_signal()
            return signal_list
        if type == 'range':
            signal_list = self._generate_range_dte_signal()
            return signal_list

    def get_dte_rule_type(self) -> str:
        if self._dte is not None and self._dte_min is None and self._dte_max is None:
            return 'single'
        if self._dte_min is not None or self._dte_max is not None:
            return 'range'

    def _update_rule_param(self):
        expiration_rule = {'rule_type': self.rule_type, 'rule_name': self.rule_name,
                           'method': self._method, 'DTE': self._dte, 'DTE_min': self._dte_min, 'DTE_max': self._dte_max}
        self._expiration_rule.update(expiration_rule)

    def _generate_single_dte_signal(self) -> List[ExecutionSignal]:
        single_dte_signal = SingleDTESignal(self._dte)
        return [single_dte_signal]

    def _generate_range_dte_signal(self) -> List[ExecutionSignal]:
        range_dte_signal = RangeDTESignal(target_dte = self._dte, min_dte = self._dte_min, max_dte = self._dte_max)
        return [range_dte_signal]
