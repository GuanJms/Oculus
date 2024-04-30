import unittest

from data_system.connection.api_request.stoculus.option_requester import StoculusOptionRequester


class TestOptionRequester(unittest.TestCase):
    def setUp(self):
        self.start_requester = StoculusOptionRequester()

    def test_get_exps(self):
        ticker = 'TSLA'
        response = self.start_requester.get_exps(ticker=ticker)
        print("test_get_exps:", response)



if __name__ == '__main__':
    unittest.main()
