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
        self.response = {
            "data": [
                {
                    "date": 20230602,
                    "ticker": "TSLA",
                    "domains": "EQUITY.STOCK.QUOTE",
                    "data": [
                        [
                            "0",
                            "34200000",
                            "4",
                            "1",
                            "210.01",
                            "0",
                            "1",
                            "65",
                            "210.2",
                            "0",
                            "20230602",
                        ]
                    ],
                    "header": [
                        "",
                        "ms_of_day",
                        "bid_size",
                        "bid_exchange",
                        "bid",
                        "bid_condition",
                        "ask_size",
                        "ask_exchange",
                        "ask",
                        "ask_condition",
                        "date",
                    ],
                },
                {
                    "date": 20230602,
                    "ticker": "SPY",
                    "domains": "EQUITY.STOCK.QUOTE",
                    "data": [
                        [
                            "0",
                            "34200000",
                            "20",
                            "1",
                            "424.46",
                            "0",
                            "9",
                            "1",
                            "424.5",
                            "0",
                            "20230602",
                        ]
                    ],
                    "header": [
                        "",
                        "ms_of_day",
                        "bid_size",
                        "bid_exchange",
                        "bid",
                        "bid_condition",
                        "ask_size",
                        "ask_exchange",
                        "ask",
                        "ask_condition",
                        "date",
                    ],
                },
                {
                    "date": 20230602,
                    "ticker": "FAKE",
                    "domains": "EQUITY.OPTION.QUOTE",
                    "data": [
                        [
                            "0",
                            "34200000",
                            "20",
                            "1",
                            "424.46",
                            "0",
                            "9",
                            "1",
                            "424.5",
                            "0",
                            "20230602",
                        ]
                    ],
                    "header": [
                        "",
                        "ms_of_day",
                        "bid_size",
                        "bid_exchange",
                        "bid",
                        "bid_condition",
                        "ask_size",
                        "ask_exchange",
                        "ask",
                        "ask_condition",
                        "date",
                    ],
                },
            ],
            "status": "DONE",
        }
        self.dp = StockDataPipeline(
            steps=[],
            domains=None,
            verbose=False,
        )

    def test_setup_data_pipeline(self):
        multi_data = self.response["data"]
        data = self.response["data"][0]
        domains = data["domains"]
        self.dp.process(data, price_domain=domains[-1])
        self.dp.multi_process(multi_data, price_domain=domains[-1])


if __name__ == "__main__":
    unittest.main()
