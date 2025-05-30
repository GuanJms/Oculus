from typing import Tuple, List

from strategics.repo import SignalGenerator, ActionGenerator
from strategics.repo.core.combo.option.basics import IronCondorRule
from strategics.repo.decorator.option.selection.expiration.expiration_DTE_rule import ExpirationDTERule
from strategics.repo.decorator.option.selection.synchronize.synchronize_rule import SynchronizeStrikeRule
from strategics.repo.core.leg.option.extensions import DeltaCallRule, DeltaPutRule
from strategics.repo.core.strategy.strategy_rule import StrategyRule


class OilShortVolStrategyRule(StrategyRule):
    def __init__(self, long_call_delta: float, short_call_delta: float, long_put_delta: float, short_put_delta: float,
                 short_term_DTE: int, long_term_DTE: int, short_term_DTE_range: (int, int),
                 long_term_DTE_range: (int, int)):
        super().__init__()
        self._long_call_delta = DeltaCallRule(delta=long_call_delta)
        self._short_call_delta = DeltaCallRule(delta=short_call_delta)
        self._long_put_delta = DeltaPutRule(delta=long_put_delta)
        self._short_put_delta = DeltaPutRule(delta=short_put_delta)
        self._short_term_DTE = short_term_DTE
        self._long_term_DTE = long_term_DTE
        self._short_term_DTE_range = short_term_DTE_range
        self._long_term_DTE_range = long_term_DTE_range

        self._short_term_IC = IronCondorRule(long_call_rule=self._long_call_delta,
                                             short_call_rule=self._short_call_delta,
                                             long_put_rule=self._long_put_delta, short_put_rule=self._short_put_delta)

        self._long_term_IC = SynchronizeStrikeRule(main_rule=self._short_term_IC)
        self._short_term_IC = ExpirationDTERule(rule=self._short_term_IC, method='DTE_range', dte=short_term_DTE,
                                                dte_min=short_term_DTE_range[0], dte_max=short_term_DTE_range[1])
        self._long_term_IC = ExpirationDTERule(rule=self._long_term_IC, method='DTE_range', dte=long_term_DTE,
                                               dte_min=long_term_DTE_range[0], dte_max=long_term_DTE_range[1])

        self.strategy_name = 'OilShortVolStrategy'
        self.strategy_type = 'short_vol'

        self.add_combo_rule(self._short_term_IC, 1)
        self.add_combo_rule(self._long_term_IC, -1)

    @property
    def short_term_IC(self):
        return self._short_term_IC

    @property
    def long_term_IC(self):
        return self._long_term_IC

    def execute(self) -> Tuple[List[SignalGenerator], List[ActionGenerator]]:
        execution_signal_list = []
        execution_action_list = []
        for combo_rule in self._combo_rule_dict.keys():
            combo_signal_list, base_combo_action_list = combo_rule.execute()

            for base_combo_action in base_combo_action_list:
                base_combo_action.set_position(self._combo_rule_dict[combo_rule])

            execution_signal_list.extend(combo_signal_list)
            execution_action_list.extend(base_combo_action_list)

        return execution_signal_list, execution_action_list
