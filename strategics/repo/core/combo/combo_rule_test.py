import unittest

from global_component_id_generator import GlobalComponentIDGenerator
from strategics.repo.core.combo.option.combo_basics.adhoc_combo_rule import AdhocComboRule
from strategics.repo.core.combo.combo_rule import ComboRule
from strategics.repo.core.combo.option.combo_basics.iron_condor_rule import IronCondorRule
from strategics.repo.core.combo.option.combo_basics.spread_combo_rule import CallSpreadRule, PutSpreadRule
from strategy_module.decorator_module.selection_module.universal_decorator.static_root_rule import StaticRootRule
from strategics.repo.core.leg.leg_template.delta_leg_rule import DeltaPutRule, DeltaCallRule


class TestCaseCoreComboRule(unittest.TestCase):

    def test_combo_rule_init(self):
        last_id = GlobalComponentIDGenerator.get_last_id()
        combo_rule = ComboRule()
        self.assertEqual(f"ComboRule-{last_id + 1}-{id(combo_rule)}", combo_rule.get_id())
        self.assertEqual(f"ComboRule-{last_id + 1}-{id(combo_rule)}", combo_rule.id)

        combo_rule2 = ComboRule()
        self.assertEqual(f"ComboRule-{last_id + 2}-{id(combo_rule2)}", combo_rule2.get_id())


class TestCaseForAdhocComboRule(unittest.TestCase):
    def test_combo_rule_id(self):
        last_id = GlobalComponentIDGenerator.get_last_id()
        adhoc_combo_rule = AdhocComboRule()
        self.assertEqual(f"AdhocComboRule-{last_id + 1}-{id(adhoc_combo_rule)}", adhoc_combo_rule.get_id())

        adhoc_combo_rule2 = AdhocComboRule()
        self.assertEqual(f"AdhocComboRule-{last_id + 2}-{id(adhoc_combo_rule2)}", adhoc_combo_rule2.get_id())

    def test_combo_rule_add_leg_rule(self):
        adhoc_combo_rule = AdhocComboRule()
        self.assertEqual({}, adhoc_combo_rule._combo_param['leg_list'])
        delta_25_call = DeltaPutRule(25)
        delta_15_call = DeltaPutRule(15)
        adhoc_combo_rule.add_leg_rule(delta_25_call, -1)
        adhoc_combo_rule.add_leg_rule(delta_15_call, 1)
        delta_50_call = DeltaPutRule(10)
        adhoc_combo_rule.add_leg_rule(delta_50_call, -1)
        self.assertEqual(3, len(adhoc_combo_rule._combo_param['leg_list']))


class TestCallSpreadCombo(unittest.TestCase):
    def test_call_spread_init(self):
        delta_25_call = DeltaCallRule(25)
        delta_15_call = DeltaCallRule(15)
        call_spread_combo = CallSpreadRule(delta_25_call, delta_15_call)
        self.assertEqual(2, len(call_spread_combo.combo_param['leg_list']))
        leg_list = call_spread_combo.combo_param['leg_list']

        delta25_param = leg_list[delta_25_call.get_id()]
        self.assertEqual(delta_25_call.get_param(), delta25_param['leg_param'])
        self.assertEqual(1, delta25_param['position'])

        delta15_param = leg_list[delta_15_call.get_id()]
        self.assertEqual(delta_15_call.get_param(), delta15_param['leg_param'])
        self.assertEqual(1, delta15_param['position'])

    def test_call_spread_wrap_root(self):
        delta_25_put = DeltaPutRule(25)
        delta_15_put = DeltaPutRule(15)
        put_spread_combo = PutSpreadRule(delta_25_put, delta_15_put)

        put_spread_combo = StaticRootRule(put_spread_combo, 'QQQ')
        # pprint(put_spread_combo.get_param())
        self.assertEqual({'rule_name': 'StaticRootRule',
                          'rule_param': 'QQQ',
                          'rule_type': 'static'}, put_spread_combo.get_param()['root_rule'])


import unittest


class TestIronCondorCombo(unittest.TestCase):
    def setUp(self):
        # Setup for each test case
        self.delta_high_call = DeltaCallRule(30)
        self.delta_low_call = DeltaCallRule(25)
        self.delta_high_put = DeltaPutRule(20)
        self.delta_low_put = DeltaPutRule(15)

        self.iron_condor_combo = IronCondorRule(
            long_call_rule=self.delta_low_call,
            short_call_rule=self.delta_high_call,
            long_put_rule=self.delta_low_put,
            short_put_rule=self.delta_high_put
        )

    def test_iron_condor_init(self):
        # Check if all four legs are correctly added
        self.assertEqual(4, len(self.iron_condor_combo._combo_param['leg_list']))
        leg_list = self.iron_condor_combo._combo_param['leg_list']

        # Check if the long call leg is correctly added
        delta_low_call_param = leg_list[self.delta_low_call.get_id()]
        self.assertEqual(self.delta_low_call.get_param(), delta_low_call_param['leg_param'])
        self.assertEqual(1, delta_low_call_param['position'])

        # Check if the short call leg is correctly added
        delta_high_call_param = leg_list[self.delta_high_call.get_id()]
        self.assertEqual(self.delta_high_call.get_param(), delta_high_call_param['leg_param'])
        self.assertEqual(-1, delta_high_call_param['position'])

        # Check if the long put leg is correctly added
        delta_low_put_param = leg_list[self.delta_low_put.get_id()]
        self.assertEqual(self.delta_low_put.get_param(), delta_low_put_param['leg_param'])
        self.assertEqual(1, delta_low_put_param['position'])

        # Check if the short put leg is correctly added
        delta_high_put_param = leg_list[self.delta_high_put.get_id()]
        self.assertEqual(self.delta_high_put.get_param(), delta_high_put_param['leg_param'])
        self.assertEqual(-1, delta_high_put_param['position'])


    def test_iron_condor_wrap_root(self):
        # Example test case to wrap the iron condor in a root rule, such as an underlying stock or index
        self.iron_condor_combo = StaticRootRule(self.iron_condor_combo, 'SPY')

        # Check that the root rule is correctly applied
        self.assertEqual({'rule_name': 'StaticRootRule', 'rule_param': 'SPY', 'rule_type': 'static'},
                         self.iron_condor_combo.get_var('root_rule'))

        # Additional tests can be added to check for specific behaviors of the iron condor combo


if __name__ == '__main__':
    unittest.main()
