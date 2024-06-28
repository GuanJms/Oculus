import unittest

from ..stock import Stock
from data_system._enums import *

class TestCaseAssetStock(unittest.TestCase):
    def setUp(self):
        self.stock = Stock(ticker='TSLA')

    def test_domains(self):
        self.assertEqual(self.stock.domains, [AssetDomain.EQUITY, EquityDomain.STOCK])
        self.assertEqual(self.stock.get_domain_chain_str(), 'EQUITY.STOCK')

        try:
            self.assertEqual(self.stock.get_domain_chain_str(price_domain=EquityDomain.OPTION), 'EQUITY.STOCK')
        except ValueError as e:
            self.assertEqual(str(e), 'price_domain must be a PriceDomain enum')

        self.assertEqual(self.stock.get_domain_chain_str(price_domain=PriceDomain.QUOTE), 'EQUITY.STOCK.QUOTE')
        self.assertEqual(self.stock.get_domain_chain_str(price_domain=PriceDomain.TRADED), 'EQUITY.STOCK.TRADED')













if __name__ == '__main__':
    unittest.main()
