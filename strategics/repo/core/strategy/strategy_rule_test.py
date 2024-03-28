import unittest
from utils.global_id import GlobalComponentIDGenerator

class MyTestCase(unittest.TestCase):
    def test_strategy_id(self):
        from strategics.repo.core.strategy.strategy_rule import StrategyRule
        strategy = StrategyRule()
        self.assertEqual(strategy._id, f"StrategyRule-{GlobalComponentIDGenerator.get_last_class_id()}"
                                       f"-{GlobalComponentIDGenerator.get_last_id()}-{id(strategy)}")




if __name__ == '__main__':
    unittest.main()
