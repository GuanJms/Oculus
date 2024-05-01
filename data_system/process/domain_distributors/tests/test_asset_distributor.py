import unittest
from unittest.mock import MagicMock

from data_system.process.domain_distributors import AssetDistributor
from data_system.process.pipelines import StockDataPipeline


class TestAssetDistributor(unittest.TestCase):
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
        self.distributor = AssetDistributor()
        self.dp_mock = MagicMock()
        dp_mock = self.dp_mock
        dp_mock.process.value = "mocked process"
        self.distributor.set_stock_data_pipeline(dp_mock)

    def test_asset_distributor(self):
        response1 = self.response["data"][0]
        response2 = self.response["data"][1]
        fake_response = self.response["data"][2]
        self.distributor.distribute(fake_response)
        self.dp_mock.process.assert_not_called()
        self.distributor.distribute(response1)
        self.distributor.distribute(response2)
        self.dp_mock.process.assert_called()
        self.assertEqual(self.dp_mock.process.call_count, 2)


if __name__ == "__main__":
    unittest.main()
