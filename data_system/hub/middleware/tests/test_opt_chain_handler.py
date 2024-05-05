import unittest

from data_system.hub.middleware import HubTicker
from data_system.hub.middleware.opt_chain_handler import HubOptionChainHandler
from data_system.utils.domain_operations import parse_domain


class TestOptionChainHandler(unittest.TestCase):

    def test_get_expirations(self):
        hubticker = HubTicker(ticker='TSLA', domains=parse_domain('EQUITY.OPTION', price_domina=False))
        expirations = HubOptionChainHandler.get_expirations(hubticker)
        self.assertIsNotNone(expirations)

        hubticker = HubTicker(ticker='TSLASLS', domains=parse_domain('EQUITY.OPTION', price_domina=False))
        exirations = HubOptionChainHandler.get_expirations(hubticker)
        self.assertEqual(exirations, [])





if __name__ == '__main__':
    unittest.main()
