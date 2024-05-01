import unittest

from data_system.connection.api_request.stoculus.option_requester import (
    StoculusOptionRequester,
)


class TestOptionRequester(unittest.TestCase):
    def setUp(self):
        self.start_requester = StoculusOptionRequester()

    def test_get_exps(self):
        ticker = "TSLA"
        response = self.start_requester.get_exps(ticker=ticker)
        print("test_get_exps:", response)

        response = self.start_requester.get_exps(ticker="AAPL")
        print("test_get_exps:", response)

    def test_get_all_available_tickers(self):
        response = self.start_requester.get_tickers()
        print("test_get_all_available_tickers:", response)

    def test_get_exp_strike(self):
        ticker = "TSLA"
        exp = 20240503
        response = self.start_requester.get_strikes(ticker=ticker, exp=exp)
        print("test_get_exp_strike:", response)

        response = self.start_requester.get_strikes(ticker="SPY", exp=20240430)
        print("test_get_exp_strike:", response)


if __name__ == "__main__":
    unittest.main()
