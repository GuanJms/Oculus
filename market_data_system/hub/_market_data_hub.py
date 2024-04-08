"""
This collection class contains OptionChainCollection, EquityCollection and IndexCollection (and possibly more in the future)
Each DataSession should contain one MarketDataCollection object. All oject on the MarketDataCollection should be updated
with same Timeline manner.
"""
from typing import Optional

from .collections import OptionChainCollection, StockCollection
from ..security_basics import Asset
from ..time_basics import Timeline
from .._enums import *


class AssetDataHub:
    def __init__(self):
        self._option_chain_collection: OptionChainCollection = OptionChainCollection()
        self._equity_collection: StockCollection = StockCollection()
        self._timeline: Optional[Timeline] = None

    def set_timeline(self, timeline: Timeline):
        self._option_chain_collection.set_timeline(timeline)
        self._equity_collection.set_timeline(timeline)

    def add_asset(self, asset: Asset):
        domains = set(asset.domains)
        if domains == {AssetDomain.EQUITY, EquityDomain.STOCK}:
            self._equity_collection.add_asset(asset)
        elif domains == {AssetDomain.EQUITY, EquityDomain.OPTION}:
            self._option_chain_collection.add_asset(asset)
        else:
            raise ValueError(f"Asset domains {asset.domains} is not supported")
