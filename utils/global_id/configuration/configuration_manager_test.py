import unittest

from utils.global_id.configuration.configuration_manager import ConfigurationManager
from market_data_system.data_process_module.transaction import Transaction
from quote_module.quote_module_factory.quote_manager_factory import QuoteManagerFactory


class MyTestCase(unittest.TestCase):
    def test_init_once(self):
        transaction_list = []
        quote_manager_list = []
        for _ in range(10):
            transaction = Transaction()
            transaction_list.append(transaction)
            quote_manager = QuoteManagerFactory.create_quote_manager(1000)
            quote_manager_list.append(quote_manager)

        self.assertEqual(ConfigurationManager.get_initialized_num(), 1)

    def test_get_root_path(self):
        import os
        self.assertEqual(os.path.join(os.path.dirname(__file__), 'configuration_files'),
                         ConfigurationManager.get_root_path())

    def test_quote_folder_name(self):
        self.assertEqual('raw_traded_quote', ConfigurationManager.get_quote_folder_name())

    def test_get_MSD_COL_NAME(self):
        self.assertEqual('ms_of_day', ConfigurationManager.get_MSD_COL_NAME())

    def test_get_MSD_COL_NAME_SECONDARY(self):
        self.assertEqual('ms_of_day2', ConfigurationManager.get_MSD_COL_NAME_SECONDARY())


if __name__ == '__main__':
    unittest.main()
