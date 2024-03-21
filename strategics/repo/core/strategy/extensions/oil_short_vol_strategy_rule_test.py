import unittest

from strategics.repo.core.combo.option.basics import IronCondorRule
from strategics.repo.decorator.option.selection.expiration.expiration_DTE_rule import ExpirationDTERule
from strategics.repo.decorator.universal.static_root_rule import StaticRootRule
from strategics.repo.decorator.option.selection.synchronize.synchronize_rule import SynchronizeStrikeRule
from strategics.repo.core.leg.leg_template.delta_leg_rule import DeltaCallRule, DeltaPutRule


class TestShortOilVolStrategy(unittest.TestCase):
    def setUp(self):
        self.delta25_call = DeltaCallRule(delta=0.25)
        self.delta10_call = DeltaCallRule(delta=0.10)
        self.delta25_put = DeltaPutRule(delta=0.25)
        self.delta10_put = DeltaPutRule(delta=0.10)
        self.test_IC_creation()

    def test_IC_creation(self):
        short_term_IC = IronCondorRule(long_call_rule=self.delta10_call, short_call_rule=self.delta25_call,
                                       long_put_rule=self.delta10_put, short_put_rule=self.delta25_put)
        long_term_IC = SynchronizeStrikeRule(main_rule=short_term_IC) # this should imply same root
        short_term_IC = ExpirationDTERule(rule=short_term_IC, method='DTE', dte=2)
        long_term_IC = ExpirationDTERule(rule=long_term_IC, method='DTE', dte=30)
        short_term_IC = StaticRootRule(rule=short_term_IC, root='USO')
        self.long_term_IC = long_term_IC
        self.short_term_IC = short_term_IC

    def test_strategy_creation(self):
        from strategics.repo.core.strategy.extensions.oil_short_vol_strategy_rule import OilShortVolStrategyRule
        short_term_IC = self.short_term_IC
        long_term_IC = self.long_term_IC

        strategy = OilShortVolStrategyRule(short_term_IC=short_term_IC, long_term_IC=long_term_IC)
        self.assertEqual('OilShortVolStrategy', strategy.strategy_name)
        self.assertEqual('short_vol', strategy.strategy_type)
        self.assertEqual(2, len(strategy.get_combo_list()))
        combo_list = strategy.get_combo_list()
        short_term_IC_item = combo_list.get(short_term_IC.get_id())
        long_term_IC_item = combo_list.get(long_term_IC.get_id())

        # check if the position_generation is correct
        self.assertEqual(1, short_term_IC_item.get('position_generation'))
        self.assertEqual(-1, long_term_IC_item.get('position_generation'))

        # check if the combo_param is correct
        self.assertEqual(short_term_IC.get_param(), short_term_IC_item.get('combo_param'))
        self.assertEqual(long_term_IC.get_param(), long_term_IC_item.get('combo_param'))

        # check if the expiration DTE is correct
        self.assertEqual(2, short_term_IC.get_var('expiration_rule').get('DTE'))
        self.assertEqual(30, long_term_IC.get_var('expiration_rule').get('DTE'))













if __name__ == '__main__':
    unittest.main()
