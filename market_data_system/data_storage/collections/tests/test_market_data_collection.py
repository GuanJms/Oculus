import unittest
from .._market_data_collection import MarketDataCollection

class TestCaseMarketDataCollection(unittest.TestCase):

    def setUp(self):
        self.market_data_collection = MarketDataCollection()


    def test_spy_equity(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
