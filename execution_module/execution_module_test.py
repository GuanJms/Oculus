import unittest
from execution_module.execution_manager import ExecutionManager
from initialization_module.initialization_manager import InitializationManager
from strategy_module.strategy_rule import StrategyRule
from strategy_module.strategy_template.oil_short_vol_strategy_rule import OilShortVolStrategyRule


class TestStarter(unittest.TestCase):
    def setUp(self):
        tickers = ['USO']
        backtest_params = {
            'start_date': 20230101,
            'end_date': 20230131,
            'ticker_list': tickers,
            'frequency': 60000}
        self.backtest_params = backtest_params
        self.oil_short_vol_strategy = OilShortVolStrategyRule(long_call_delta=0.1, short_call_delta=0.2,
                                                              long_put_delta=0.1, short_put_delta=0.2,
                                                              short_term_DTE=2, long_term_DTE=30,
                                                              short_term_DTE_range=(0, 7), long_term_DTE_range=(20, 40))
        self.backtest_manager = InitializationManager.create_backtest_section(backtest_params)
        self.execution_manager = self.backtest_manager.execution_manager

    def test_execution_manager_filed(self):
        self.assertIsInstance(self.execution_manager, ExecutionManager)
        self.assertTrue(self.execution_manager.get_backtest_manager() is not None)
        self.assertEqual(self.execution_manager.get_backtest_manager().id, self.backtest_manager.id)
        execution_manager = self.execution_manager
        self.assertEqual(0, len(execution_manager.get_execution_section_dict()))
        self.assertFalse(execution_manager.get_backtest_time_params() is None)

        execution_manager.execute_strategy(self.oil_short_vol_strategy)
        self.assertTrue(1, execution_manager.get_execution_section_dict())
        self.assertTrue(execution_manager.get_execution_section_dict().keys()[0], self.oil_short_vol_strategy.id)

        print(self.execution_manager.get_backtest_time_params())


if __name__ == '__main__':
    unittest.main()
