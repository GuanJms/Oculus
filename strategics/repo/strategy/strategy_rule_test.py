import unittest


class MyTestCase(unittest.TestCase):
    def test_strategy_id(self):
        from strategics.repo.strategy.strategy_rule import StrategyRule
        strategy = StrategyRule()
        self.assertEqual(strategy._id, f"StrategyRule-1-{id(strategy)}")




if __name__ == '__main__':
    unittest.main()
