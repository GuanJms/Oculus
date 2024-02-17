import unittest

from Backtest.QuoteManager import QuoteManager
from DataProcess.TradedQuoteDataManager import TradedQuoteDataManager

class MyTestCase(unittest.TestCase):

   def quote_manager_test1(self):
       datamanager = TradedQuoteDataManager()
       quote_manager = QuoteManager(data_manager=datamanager)

       pass

if __name__ == '__main__':
    unittest.main()
