import unittest


class MyTestCaseForInitialziationManager(unittest.TestCase):
    def setUp(self):
        tickers = ['SPY']
        backtest_params = {
            'start_date': 20230101,
            'end_date': 20230131,
            'ticker_list': tickers,
            'frequency': 60000}
        self.backtest_params = backtest_params

    def test_initialize_manager(self):
        from initialization_module.initialization_manager import InitializationManager
        backtest_manager_list = []
        N = 10
        for _ in range(N):
            backtest_manager_list.append(InitializationManager.create_backtest_session(self.backtest_params))
        self.assertEqual(len(backtest_manager_list), N)
        for backtest_manager in backtest_manager_list:
            self.assertTrue(backtest_manager in InitializationManager.get_backtest_manager_list())

    def test_initialize_connection_one_manager(self):
        from initialization_module.initialization_manager import InitializationManager
        backtest_manager = InitializationManager.create_backtest_session(self.backtest_params)
        backtest_data_manager = backtest_manager.backtest_data_manager
        execution_manager = backtest_manager.execution_manager
        self.assertEqual(backtest_data_manager.get_backtest_manager(), backtest_manager)
        self.assertEqual(execution_manager.get_backtest_manager(), backtest_manager)






if __name__ == '__main__':
    unittest.main()
