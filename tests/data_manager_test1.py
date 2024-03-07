import unittest

from quote_module.quote_manager import QuoteManager
from data_process_module.traded_quote_data_manager import TradedQuoteDataManager
import json
class MyTestCase(unittest.TestCase):

    def test_data_manager_config(self):
        config_file = 'config.json'
        with open(config_file, 'r') as file:
            config_json = json.load(file)
        data_root = config_json.get('root_system', None)
        data_manager = TradedQuoteDataManager(config_file)
        self.assertEqual(data_manager.root_system, data_root)

    def test_data_manager_file_reading(self):
        config_file = 'config.json'
        data_manager = TradedQuoteDataManager(config_file)
        self.assertTrue(data_manager.is_connected())


if __name__ == '__main__':
    unittest.main()
