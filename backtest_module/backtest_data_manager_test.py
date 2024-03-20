import unittest
from backtest_module.backtest_data_manager import BacktestDataManager
from global_component_id_generator import GlobalComponentIDGenerator


class MyTestCaseBacktestDataManager(unittest.TestCase):
    def setUp(self):
        from initialization_module.initialization_manager import InitializationManager
        self.tickers = ['USO']
        self.backtest_params = {
            'start_date': 20230101,
            'end_date': 20230131,
            'ticker_list': self.tickers,
            'frequency': 60000}
        self.backtest_manager_session = InitializationManager.create_backtest_session(self.backtest_params)
        self.backtest_data_manager = self.backtest_manager_session.backtest_data_manager

    def test_init(self):
        last_id = GlobalComponentIDGenerator.get_last_id()
        self.assertEqual(self.backtest_data_manager.frequency, 60000)
        self.assertEqual(f'BacktestDataManager-{last_id}-{id(self.backtest_data_manager)}', self.backtest_data_manager.id)
        self.assertEqual(self.tickers, self.backtest_data_manager.ticker_list)














if __name__ == '__main__':
    unittest.main()
