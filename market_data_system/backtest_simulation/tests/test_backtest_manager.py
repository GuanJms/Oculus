import unittest

from strategics.repo.core.strategy.extensions.oil_short_vol_strategy_rule import OilShortVolStrategyRule


class TestStarter(unittest.TestCase):
    def setUp(self):
        tickers = ['SPY']
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

    def test_backtest_manager_init(self):
        from market_data_system.backtest_simulation._backtest_manager import HubAdaptor
        backtest_manager = HubAdaptor()
        backtest_manager.add_backtest_params(self.backtest_params)
        self.assertEqual(backtest_manager.start_date, 20230101)
        self.assertEqual(backtest_manager.end_date, 20230131)
        self.assertEqual(backtest_manager.ticker_list, ['SPY'])

    def test_backtest_manager_runs_strategy_init(self):
        from market_data_system.backtest_simulation._backtest_manager import HubAdaptor
        backtest_manager = HubAdaptor()
        backtest_manager.add_backtest_params(self.backtest_params)
        backtest_manager.run_strategy(self.oil_short_vol_strategy)
        strategy_result = backtest_manager.get_result(self.oil_short_vol_strategy)




if __name__ == '__main__':
    unittest.main()
