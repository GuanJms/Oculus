import unittest

from data_system._enums import EquityDomain, SingleAssetType
from data_system.hub import AssetDataHub
from data_system.process.domain_distributors import AssetDistributor
from data_system.hub.instrument_finder import InstrumentFinder
from data_system.process.pipelines.equity_data_pipeline_factory import (
    EquityDataPipelineFactory,
)
from data_system.security_basics.volatility_manager import VolatilityManager


class MyInstrumentFinderTest(unittest.TestCase):
    def setUp(self):
        self.data_hub = AssetDataHub()
        equity_data_pipeline_factory = EquityDataPipelineFactory(self.data_hub)
        self.asset_distributor = AssetDistributor()
        stock_pipe = equity_data_pipeline_factory.create_equity_data_pipeline(
            equity_domain=EquityDomain.STOCK
        )
        option_pipe = equity_data_pipeline_factory.create_equity_data_pipeline(
            equity_domain=EquityDomain.OPTION
        )
        self.asset_distributor.set_data_pipeline(stock_pipe, price_type="TRADED")
        self.asset_distributor.set_data_pipeline(option_pipe, price_type="TRADED")

        self.instrument_finder = InstrumentFinder()
        self.option_hub = self.data_hub._option_chain_collection_hub
        self.stock_hub = self.data_hub._stock_collection_hub

        self.option_meta = {
            "date": 20240528,
            "ticker": "TSLA",
            "domains": "EQUITY.OPTION.TRADED",
            "mode": "live",
            "timezone": "US/Eastern",
            "date_timestamp": 1716868800000,
            "expiration": 20240531,
            "strike": 180000,
            "right": "C",
        }

    def test_hub_init(self):
        print(self.instrument_finder._hubs)
        self.assertEqual(
            self.instrument_finder._hubs[EquityDomain.OPTION], self.option_hub
        )
        self.assertEqual(
            self.instrument_finder._hubs[EquityDomain.STOCK], self.stock_hub
        )

    def test_init(self):
        stock_meta = {
            "date": 20240528,
            "ticker": "TSLA",
            "domains": "EQUITY.STOCK.TRADED",
            "mode": "live",
            "timezone": "US/Eastern",
            "date_timestamp": 1716868800000,
        }
        stock = self.instrument_finder.find_asset(
            stock_meta, asset_type=SingleAssetType.STOCK
        )
        print(stock)

        stock = self.instrument_finder.find_asset(
            self.option_meta, asset_type=SingleAssetType.STOCK
        )
        print(stock)

        option = self.instrument_finder.find_asset(
            self.option_meta, asset_type=SingleAssetType.OPTION
        )
        print(option)

    def test_injection(self):
        # After injecting the stock or option data, and when the find_asset method is called, the asset should be found with the injected data.
        stock1 = self.instrument_finder.find_asset(
            self.option_meta, asset_type=SingleAssetType.STOCK
        )
        print(stock1)
        stock_record = {
            "date": 20240528,
            "ticker": "TSLA",
            "domains": "EQUITY.STOCK.TRADED",
            "contract": {"security_type": "STOCK", "root": "TSLA"},
            "data": {
                "ms_of_day": 55613847,
                "sequence": 37924999,
                "size": 96,
                "condition": 115,
                "price": 176.3605,
                "exchange": 57,
                "date": 20240528,
            },
            "mode": "live",
        }
        self.asset_distributor.distribute(stock_record)
        stock2 = self.instrument_finder.find_asset(
            self.option_meta, asset_type=SingleAssetType.STOCK
        )
        print(stock1)
        print("ID", id(stock1) == id(stock2))
        print(stock2)

        option_record = {
            "date": 20240528,
            "ticker": "TSLA",
            "domains": "EQUITY.OPTION.TRADED",
            "contract": {
                "security_type": "OPTION",
                "root": "TSLA",
                "expiration": 20240531,
                "strike": 180000,
                "right": "C",
            },
            "data": {
                "ms_of_day": 55610295,
                "sequence": -1091185300,
                "size": 2,
                "condition": 131,
                "price": 1.64,
                "exchange": 5,
                "date": 20240528,
            },
            "mode": "live",
        }
        self.asset_distributor.distribute(option_record)

        option = self.instrument_finder.find_asset(
            self.option_meta, asset_type=SingleAssetType.OPTION
        )

        print(option)
        print(option._underlying_asset)

        vol_manager: VolatilityManager = option._volatility_manager
        sigma = vol_manager.get_last_trade_iv()
        vol_node = vol_manager.get_last_trade_vol_node()
        print("Sigma ", sigma)
        print("vol_node:", vol_node)




if __name__ == "__main__":
    unittest.main()
