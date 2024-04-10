import unittest

import requests
from data_system.hub._asset_data_hub import AssetDataHub
from data_system.security_basics import Stock
from data_system.time_basics import Timeline
from .._stoculus_request_maker import StoculusRequestMaker
from .._stoculus_requester import StoculusRequester


class TestRequester(unittest.TestCase):
    def setUp(self):
        self.hub = AssetDataHub()
        self.asset_list = []
        self.tickers = ['TSLA', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NFLX', 'NVDA', 'PYPL', 'ADBE']
        for stock in self.tickers:
            asset = Stock(ticker=stock)
            self.asset_list.append(asset)
            self.hub.add_asset(asset=asset)

        self.timeline = Timeline()
        self.ms_of_day = 0
        self.date = 20230602
        self.timeline.set_time(ms_of_day=self.ms_of_day, date=self.date)
        self.hub.set_timeline(timeline=self.timeline)
        self.requester = StoculusRequester(IP='108.5.104.157', PORT=1999)
        self.hub._id = '123456'

        try:
            response = self.requester.check_connection(self.hub)
        except Exception as e:
            pass

    def test_base_url(self):
        response = requests.get(self.requester.get_base_url())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())
        self.assertEqual(response.json(), {'message': 'Welcome to Stoculus!'})

    def test_timeline_url(self):
        url = self.requester.get_url(prefix='timeline', endpoints=['start'])
        self.assertEqual(url, "http://108.5.104.157:1999/timeline/start/")


    def test_token_status(self):
        self.requester.start_connection(self.hub)
        print(self.hub.public_token, self.hub.private_key)
        response = self.requester.check_connection(self.hub)
        print(response)



if __name__ == '__main__':
    unittest.main()
