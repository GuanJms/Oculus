import unittest

from strategy_module.strategy_template.zero_DTE_strategy_rule import ZeroDTEStrategyRule


class MyTestCase(unittest.TestCase):
    def test_strategy_id(self):
        from strategy_module.strategy_rule import StrategyRule
        strategy = StrategyRule()
        self.assertEqual(strategy._id, f"StrategyRule-1-{id(strategy)}")




if __name__ == '__main__':
    unittest.main()
