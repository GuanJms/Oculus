import unittest

from data_system.hub._asset_data_hub import AssetDataHub
from data_system.security_basics import Stock
from data_system.time_basics import Timeline
from data_system.connection.api_request.stoculus.timeline_requester import (
    StoculusTimelineRequester,
)
from data_system.process.pipelines import StockDataPipeline


class TestProcessStockDataPipeline(unittest.TestCase):
    def setUp(self):
        self.hub = AssetDataHub()
        self.asset_list = []
        self.tickers = ["TSLA", "SPY"]
        for stock in self.tickers:
            asset = Stock(ticker=stock)
            self.asset_list.append(asset)
            self.hub.add_asset(asset=asset)

        self.timeline = Timeline()
        self.ms_of_day = 0
        self.date = 20230602
        self.timeline.set_time(ms_of_day=self.ms_of_day, date=self.date)
        self.hub.set_timeline(timeline=self.timeline)
        self.requester = StoculusTimelineRequester()
        self.hub._id = "123456"  # Fix hub id such that it wont open too much connection in Stoculus during testing
        self.requester.start_connection(self.hub)

    def test_setup_data_pipeline(self):
        # Request data from Stoculus
        update_time = 9.5 * 60 * 60 * 1000
        response = self.requester.read_upto_time(self.hub, update_time)
        print("Read upto time response:", update_time)
        data = response["data"]
        reading_status = response["status"]
        ms_of_day_list = [int(row[1]) for row in data[0]["data"]]
        print("Read upto time data:", ms_of_day_list)
        print("Read upto time status:", reading_status)
        print(response)


if __name__ == "__main__":
    unittest.main()
