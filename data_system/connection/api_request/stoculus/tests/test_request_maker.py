import json
import unittest
import urllib.request

import requests
from data_system.hub.asset_data_hub import AssetDataHub
from data_system.security_basics import Stock
from data_system.time_basics import Timeline
from data_system.connection.api_request.stoculus._request_maker import StoculusRequestMaker


class TestRequestMaker(unittest.TestCase):

    def setUp(self):
        self.server_test = True
        self.BASE = 'http://108.5.104.157:1999'
        self.hub = AssetDataHub()
        self.asset_list = []
        self.tickers = ['TSLA', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NFLX', 'NVDA', 'PYPL', 'ADBE']
        for stock in self.tickers:
            asset = Stock(ticker=stock)
            self.asset_list.append(asset)
            self.hub.add_asset(asset=asset)

        self.timeline = Timeline()
        self.ms_of_day = 9.5 * 60 * 1000 * 60
        self.date = 20240301
        self.timeline.set_time(ms_of_day=self.ms_of_day, date=self.date)
        self.hub.set_timeline(timeline=self.timeline)
        if self.server_test:
            response = requests.get(self.BASE + '/')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json())
            self.assertEqual(response.json(), {'message': 'Welcome to Stoculus!'})

    def test_asset_maker(self):
        test_asset = self.asset_list[0]
        asset_start_request = StoculusRequestMaker.get_asset_connection_request(asset=test_asset, date=self.date)
        self.assertEqual(asset_start_request, {'TSLA': {'DOMAINS': 'EQUITY.STOCK.QUOTE', 'DATE': self.date}})

    def test_multiple_asset_maker(self):

        request = StoculusRequestMaker.get_assets_connection_request(assets=self.asset_list, date=self.date)
        expected_request = {ticker: {'DOMAINS': 'EQUITY.STOCK.QUOTE', 'DATE': self.date} for ticker in self.tickers}
        self.assertEqual(request, expected_request)

    def test_hub_starter_request_construction(self):
        request = StoculusRequestMaker.get_asset_data_hub_ticker_info_starter_request(asset_data_hub=self.hub)
        expected_request = {ticker: {'DOMAINS': 'EQUITY.STOCK.QUOTE', 'DATE': self.date} for ticker in self.tickers}
        self.assertEqual(request, expected_request)

    # def test_simple_starter_request_with_server(self):
    #     url = f'{self.BASE}/timeline/start/'
    #     ticker_info = {
    #         'TSLA': {
    #             'DOMAINS': 'EQUITY.STOCK.QUOTE',
    #             'DATE': self.date
    #         }
    #     }
    #     data = json.dumps(ticker_info).encode('utf-8')
    #     req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    #     with urllib.request.urlopen(req) as response:
    #         response_data = response.read()
    #         data = json.loads(response_data)
    #     print(data)

    def test_hub_starter_request_with_server(self):
        if not self.server_test: return

        ticker_info = StoculusRequestMaker.get_asset_data_hub_ticker_info_starter_request(asset_data_hub=self.hub)
        url = f'{self.BASE}/timeline/start/'
        data = json.dumps(ticker_info).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            response_data = response.read()
            connection_data_json = json.loads(response_data)
        print(connection_data_json)


if __name__ == '__main__':
    unittest.main()
