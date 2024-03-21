import unittest

from global_component_id_generator import GlobalComponentIDGenerator
from strategics.repo.core.combo.combo_rule import ComboRule
from strategics.repo.decorator.option.selection.delta.delta_rule import DeltaRule
from strategics.repo.decorator.option.selection.moneyness.moneyness_rule import \
    MoneynessRule
from strategics.repo.decorator.universal.static_root_rule import StaticRootRule
from strategics.repo.decorator.option.selection.static.static_strike_rule import \
    StaticStrikeRule
from strategics.repo.core.leg.leg_rule import LegRule
from strategics.repo.core.leg.leg_template.delta_leg_rule import DeltaPutRule, DeltaCallRule
from strategics.repo.core.leg.option.option_leg_rule import OptionRule
from strategics.repo.core.leg.option.basics.call_rule import CallRule
from strategics.repo.core.leg.option.basics.put_rule import PutRule
from strategics.repo.rule import Rule
from strategics.repo.rule_class_checker import RuleClassChecker


class TestLegClasses(unittest.TestCase):
    def test_option_rule_id(self):
        last_id = GlobalComponentIDGenerator.get_last_id()
        put_rule = PutRule()
        self.assertEqual(f"PutRule-{last_id + 1}-{id(put_rule)}", put_rule.get_id())

        put_rule2 = PutRule()
        self.assertEqual(f"PutRule-{last_id + 2}-{id(put_rule2)}", put_rule2.get_id())

        call_rule = CallRule()
        self.assertEqual(f"CallRule-{last_id + 3}-{id(call_rule)}", call_rule.get_id())

    def test_option_rule_init_param(self):
        put_rule = PutRule()
        self.assertEqual('Put', put_rule.get_var('option_type'))
        self.assertEqual('option_leg', put_rule.get_var('leg_type'))

        call_rule = CallRule()
        self.assertEqual('Call', call_rule.get_var('option_type'))
        self.assertEqual('option_leg', call_rule.get_var('leg_type'))

    def test_option_rule_static_root_rule_param(self):  # tag: fbvafdasubtea
        put_rule = PutRule()
        put_rule = StaticRootRule(put_rule, 'SPY')
        put_rule_id = put_rule.get_id()

        self.assertEqual('Put', put_rule.get_var('option_type'))
        self.assertEqual('option_leg', put_rule.get_var('leg_type'))
        self.assertEqual({'rule_type': 'static', 'rule_name': 'StaticRootRule', 'rule_param': 'SPY'},
                         put_rule.get_var('root_rule'))

        call_rule = CallRule()
        call_rule = StaticRootRule(call_rule, 'TSLA')
        self.assertEqual('Call', call_rule.get_var('option_type'))
        self.assertEqual('option_leg', call_rule.get_var('leg_type'))
        self.assertEqual({'rule_type': 'static', 'rule_name': 'StaticRootRule', 'rule_param': 'TSLA'},
                         call_rule.get_var('root_rule'))

        put_rule = StaticRootRule(put_rule, 'QQQ')  # Overwrite the root rule
        self.assertEqual('Put', put_rule.get_var('option_type'))
        self.assertEqual('option_leg', put_rule.get_var('leg_type'))
        self.assertEqual({'rule_type': 'static', 'rule_name': 'StaticRootRule', 'rule_param': 'QQQ'},
                         put_rule.get_var('root_rule'))

        self.assertEqual(put_rule_id, put_rule.get_id())

    def test_option_rule_static_strike_rule_param(self):
        put_rule = PutRule()
        put_rule = StaticStrikeRule(put_rule, 100)  # Add a statitc strike rule
        self.assertEqual('Put', put_rule.get_var('option_type'))
        self.assertEqual('option_leg', put_rule.get_var('leg_type'))
        self.assertEqual({'rule_type': 'static', 'rule_name': 'StaticStrikeRule', 'rule_param': 100},
                         put_rule.get_var('strike_rule'))

    def test_multiple_rule_param(self):
        put_rule = PutRule()
        put_rule = StaticRootRule(put_rule, 'SPY')
        put_rule = StaticStrikeRule(put_rule, 100)
        self.assertEqual('Put', put_rule.get_var('option_type'))
        self.assertEqual('option_leg', put_rule.get_var('leg_type'))
        self.assertEqual({'rule_type': 'static', 'rule_name': 'StaticRootRule', 'rule_param': 'SPY'},
                         put_rule.get_var('root_rule'))
        self.assertEqual({'rule_type': 'static', 'rule_name': 'StaticStrikeRule', 'rule_param': 100},
                         put_rule.get_var('strike_rule'))

    def test_moneyness_rule_param(self):
        put_rule = PutRule()
        put_rule = MoneynessRule(put_rule, 0.9)
        put_rule = StaticRootRule(put_rule, 'SPY')
        self.assertEqual('Put', put_rule.get_var('option_type'))
        self.assertEqual('option_leg', put_rule.get_var('leg_type'))
        self.assertEqual({'rule_type': 'static', 'rule_name': 'StaticRootRule', 'rule_param': 'SPY'},
                         put_rule.get_var('root_rule'))
        self.assertEqual({'rule_type': 'dynamic', 'rule_name': 'MoneynessRule', 'rule_param': 0.9},
                         put_rule.get_var('strike_rule'))

    def test_delta_rule_param(self):
        put_rule = PutRule()
        put_rule = StaticRootRule(put_rule, 'SPY')
        put_rule = DeltaRule(put_rule, 25)
        self.assertEqual('Put', put_rule.get_var('option_type'))
        self.assertEqual('option_leg', put_rule.get_var('leg_type'))
        self.assertEqual({'rule_type': 'static', 'rule_name': 'StaticRootRule', 'rule_param': 'SPY'},
                         put_rule.get_var('root_rule'))
        self.assertEqual({'rule_type': 'dynamic', 'rule_name': 'DeltaRule', 'rule_param': -0.25},
                         put_rule.get_var('delta_rule'))

        """"
        Class Diagram:
        Rule
         |
        LegRule
         |
        OptionRule
         |\
         | \
        PutRule CallRule
        """

    def test_subclass(self):
        put_rule = PutRule()
        self.assertTrue(isinstance(put_rule, PutRule))
        self.assertFalse(isinstance(put_rule, CallRule))

        call_rule = CallRule()
        self.assertTrue(isinstance(call_rule, CallRule))
        self.assertFalse(isinstance(call_rule, PutRule))

        self.assertFalse(issubclass(PutRule, CallRule))
        self.assertTrue(issubclass(put_rule.__class__, PutRule))
        self.assertFalse(issubclass(put_rule.__class__, CallRule))
        self.assertTrue(issubclass(put_rule.__class__, OptionRule))
        self.assertTrue(issubclass(put_rule.__class__, LegRule))
        self.assertTrue(issubclass(put_rule.__class__, Rule))

        combo_rule = ComboRule()
        self.assertFalse(issubclass(combo_rule.__class__, OptionRule))

        put_rule = StaticRootRule(put_rule, 'SPY')
        self.assertTrue(RuleClassChecker.is_LegRule(put_rule, True))

        put_rule = StaticStrikeRule(put_rule, 100)
        self.assertTrue(RuleClassChecker.is_LegRule(put_rule, True))


class TestDecoratorClasses(unittest.TestCase):

    def test_combo_rule_wrapping_leg_rule(self):
        combo_rule = ComboRule()
        try:
            DeltaRule(combo_rule, 0.25)
        except TypeError as e:
            self.assertEqual("The rule must be a subclass of LegRule.", str(e))

        try:
            MoneynessRule(combo_rule, 0.9)
        except TypeError as e:
            self.assertEqual("The rule must be a subclass of LegRule.", str(e))


class TestDeltaCallPutClasses(unittest.TestCase):
    def test_init(self):
        delta_25_put_rule = DeltaPutRule(0.25)

        self.assertEqual('option_leg', delta_25_put_rule.get_var('leg_type'))
        self.assertEqual('Put', delta_25_put_rule.get_var('option_type'))
        delta_rule = delta_25_put_rule.get_var('delta_rule')
        self.assertEqual({'rule_type': 'dynamic',
                          'rule_name': 'DeltaRule',
                          'rule_param': -0.25}, delta_rule)

        delta_50_call_rule = DeltaCallRule(0.50)
        leg_type = delta_50_call_rule.get_var('leg_type')
        self.assertEqual('option_leg', leg_type)
        self.assertEqual('Call', delta_50_call_rule.get_var('option_type'))
        self.assertEqual({'rule_type': 'dynamic',
                          'rule_name': 'DeltaRule',
                          'rule_param': 0.50}, delta_50_call_rule.get_var('delta_rule'))


if __name__ == '__main__':
    unittest.main()
