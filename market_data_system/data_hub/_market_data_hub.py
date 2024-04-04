"""
This collection class contains OptionChainCollection, EquityCollection and IndexCollection (and possibly more in the future)
Each DataSession should contain one MarketDataCollection object. All oject on the MarketDataCollection should be updated
with same Timeline manner.
"""
from typing import Optional

from market_data_system.data_hub.collections._option_chain_collection import OptionChainCollection
from market_data_system.data_hub.collections._equity_collection import EquityCollection
from market_data_system.security_basics import Asset
from market_data_system.time_basics import Timeline
from market_data_system._enums import AssetType


class AssetDataHub:
    def __init__(self):
        self._option_chain_collection: OptionChainCollection = OptionChainCollection()
        self._equity_collection: EquityCollection = EquityCollection()
        self._timeline: Optional[Timeline] = None

    def set_timeline(self, timeline: Timeline):
        self._option_chain_collection.set_timeline(timeline)
        self._equity_collection.set_timeline(timeline)

    def add_asset(self, asset: Asset):
        match asset.type:
            case AssetType.EQUITY:
                self._equity_collection.add_asset(asset)
            case AssetType.OPTION:
                self._option_chain_collection.add_asset(asset)
            case _:
                raise ValueError(f"Asset type {asset.type} is not supported")
