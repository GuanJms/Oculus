import unittest

from strategics.repo.core.combo.option.extensions import DeltaIronCondorRule
from strategics.repo.decorator.option.selection.synchronize.synchronize_rule import SynchronizeStrikeRule
from strategics.repo.core.leg.option.extensions import DeltaPutRule
from strategics.repo.core.leg.option.basics import PutRule


class TestSynchronizeDecorator(unittest.TestCase):

    def test_leg_synchronize_decorator(self):
        delta_25_put_rule = DeltaPutRule(0.25)
        synchronized_delta_put_rule = PutRule()
        synchronized_delta_put_rule = SynchronizeStrikeRule(main_rule=delta_25_put_rule,
                                                            rule=synchronized_delta_put_rule)

        self.assertEqual(delta_25_put_rule.get_id(), synchronized_delta_put_rule.synchronize_rule.get('sync_rule_id'))

    def test_combo_synchronize_decorator(self):
        delta_25_15_IC_combo_rule = DeltaIronCondorRule(long_call_delta=0.15, short_call_delta=0.25,
                                                        long_put_delta=0.15, short_put_delta=0.25)
        synchronized_delta_25_15_IC_combo_rule = SynchronizeStrikeRule(main_rule=delta_25_15_IC_combo_rule)
        self.assertEqual(synchronized_delta_25_15_IC_combo_rule.synchronize_rule.get('sync_rule_id'),
                         delta_25_15_IC_combo_rule.get_id())

    def test_overwrite_synchronize_decorator(self):
        delta_25_put_rule = DeltaPutRule(0.25)
        delta_45_put_rule = DeltaPutRule(0.45)
        synchronized_delta_put_rule = PutRule()
        synchronized_delta_put_rule = SynchronizeStrikeRule(main_rule=delta_25_put_rule,
                                                            rule=synchronized_delta_put_rule)
        self.assertEqual(delta_25_put_rule.get_id(), synchronized_delta_put_rule.synchronize_rule.get('sync_rule_id'))
        self.assertEqual(delta_25_put_rule.get_id(),
                         synchronized_delta_put_rule.get_param().get('synchronize_rule').get('sync_rule_id'))

        synchronized_delta_put_rule = SynchronizeStrikeRule(main_rule=delta_45_put_rule,
                                                            rule=synchronized_delta_put_rule)
        self.assertEqual(delta_45_put_rule.get_id(), synchronized_delta_put_rule.synchronize_rule.get('sync_rule_id'))
        self.assertEqual(delta_45_put_rule.get_id(),
                         synchronized_delta_put_rule.get_param().get('synchronize_rule').get('sync_rule_id'))


if __name__ == '__main__':
    unittest.main()
