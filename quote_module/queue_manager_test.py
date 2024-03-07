import unittest

from quote_module.quote_manager import QuoteManager
from data_process_module.traded_quote_data_manager import TradedQuoteDataManager

class MyTestCase(unittest.TestCase):

   def quote_manager_test1(self):
       config_file = '../tests/config.json'
       queue_manager = TradedQuoteDataManager(config_file)
       datamanager = TradedQuoteDataManager()
       print(queue_manager.root_system)
       quote_manager = QuoteManager(data_manager=datamanager)

       pass

if __name__ == '__main__':
    unittest.main()
