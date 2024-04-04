import unittest
from market_data_system.data_hub._market_data_hub import AssetDataHub

class TestCaseMarketDataCollection(unittest.TestCase):

    def setUp(self):
        self.market_data_collection = AssetDataHub()


    def test_spy_equity(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
