import unittest

import requests
from data_system.hub._asset_data_hub import AssetDataHub
from data_system.security_basics import Stock
from data_system.time_basics import Timeline
from data_system.connection.api_request.stoculus.timeline_requester import StoculusTimelineRequester


class TestRequester(unittest.TestCase):
    def setUp(self):
        self.BASE = 'http://108.5.104.157:1999'
        self.hub = AssetDataHub()
        self.asset_list = []
        self.tickers = ['TSLA', 'AAPL']
        for stock in self.tickers:
            asset = Stock(ticker=stock)
            self.asset_list.append(asset)
            self.hub.add_asset(asset=asset)

        self.timeline = Timeline()
        self.ms_of_day = 0
        self.date = 20230602
        self.timeline.set_time(ms_of_day=self.ms_of_day, date=self.date)
        self.hub.set_timeline(timeline=self.timeline)
        self.requester = StoculusTimelineRequester(IP='108.5.104.157', PORT=1999)
        self.hub._id = '123456'
        self.requester.start_connection(self.hub)

    def test_check_status(self):
        response = self.requester.check_connection(self.hub)
        print("test_check_status:", response)

    def test_server_reader_tickers(self):
        url = f'{self.BASE}/timeline/status/tickers/'
        params = {'public_token': self.hub.public_token, 'private_key': self.hub.private_key}
        response = requests.get(url, params=params)
        print("test_server_reader_tickers:", response.json())


    def test_hub_read_upto_time(self):
        response = self.requester.read_upto_time(self.hub, 9.6 * 60 * 60 * 1000)
        data = response['data']
        reading_status = response['status']
        # dict keys: ['data', 'status']
        # data a list
        # each element of data is a dictionary
        # keys of each element: ['date', 'ticker', 'domains', 'data', 'header']
        # data is a list of list
        print("test_hub_read_upto_time:", reading_status)
        print("Length of data:", len(data))
        print("Length of each data:", len(data[0]))
        print("sample data type:", type(data[0]))
        print(("sample data keys:", data[0].keys()))
        print("sample data ticker:", data[0]['ticker'])
        print("sample data domains:", data[0]['domains'])
        print("sample data date:", data[0]['date'])
        print("sample data length:", len(data[0]['data']))
        print("sample header:", data[0]['header'])
        print("sample tick data:", data[0]['data'][0])






if __name__ == '__main__':
    unittest.main()
