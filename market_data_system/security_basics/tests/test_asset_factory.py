import unittest
from .._asset_factory import AssetFactory


class TestAssetFactory(unittest.TestCase):
    def test_factory(self):
        factory = AssetFactory()
        asset = factory.create_asset(domain_chain_str='EQUITY.STOCK', ticker='TSLA', date=20240301)
        print(asset.ticker)
        print(asset.get_params())


if __name__ == '__main__':
    unittest.main()
