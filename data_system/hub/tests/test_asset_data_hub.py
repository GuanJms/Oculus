import unittest

from data_system.security_basics import Stock
from .._asset_data_hub import AssetDataHub
from ...time_basics import Timeline


class TestAssetDataHub(unittest.TestCase):
    def setUp(self):
        self.hub = AssetDataHub()

    def test_hub_stock_adding(self):
        hub = self.hub
        stocks = ['TSLA', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB', 'NFLX', 'NVDA', 'PYPL', 'ADBE']
        for stock in stocks:
            hub.add_asset(Stock(ticker=stock))
        self.assertEqual(len(hub.get_assets()), len(stocks))
        print(hub.get_assets())

    def test_timeline_setting(self):
        timeline = Timeline()
        ms_of_day = 9.5 * 60 * 1000 * 60
        date = 20210101
        timeline.set_time(ms_of_day=ms_of_day, date=date)
        self.hub.set_timeline(timeline)
        self.assertEqual(self.hub.get_timeline(), timeline)
        self.assertAlmostEquals(self.hub.get_timeline().get_time(time_type='ms_of_day'), ms_of_day)
        self.assertEqual(self.hub.get_timeline().get_date(), date)


if __name__ == '__main__':
    unittest.main()
