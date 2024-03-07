import unittest


class MyTestCaseForInitialziationManager(unittest.TestCase):
    def test_initilization_manager(self):
        from initialization_module.initialization_manager import InitializationManager
        backtest_manager_list = []
        N = 10
        for _ in range(N):
            backtest_manager_list.append(InitializationManager.create_backtest_section())
        self.assertEqual(len(backtest_manager_list), N)
        for backtest_manager in backtest_manager_list:
            self.assertTrue(backtest_manager in InitializationManager.get_backtest_manager_list())

    def test_initilziation_connection_one_manager(self):
        from initialization_module.initialization_manager import InitializationManager
        backtest_manager = InitializationManager.create_backtest_section()
        backtest_data_manager = backtest_manager.backtest_data_manager
        execution_manager = backtest_manager.execution_manager
        self.assertEqual(backtest_data_manager.backtest_manager, backtest_manager)
        self.assertEqual(execution_manager.backtest_manager, backtest_manager)


if __name__ == '__main__':
    unittest.main()
