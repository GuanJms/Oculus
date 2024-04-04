from typing import Optional, Dict
from ...security_basics import Asset, MultiAsset
from ..._enums import AssetType, AssetCollectionType


class AssetCollection:
    def __init__(self):
        self._collections: Dict[str, Asset | MultiAsset] = {}
        self._asset_collection_type: Optional[AssetCollectionType] = None
        self._asset_type: Optional[AssetType] = None

    def check_type(self, asset: Asset):
        if asset.type != self._asset_type:
            raise ValueError(f"Asset type {asset.type} is not compatible with collection type {self._asset_type}")

    def add_asset(self, asset: Asset):
        self.check_type(asset)
        ticker = asset.ticker
        self._collections[ticker] = asset

    def get_asset(self, ticker: str) -> Optional[Asset]:
        return self._collections.get(ticker, None)

    def set_timeline(self, timeline):
        for asset in self._collections.values():
            asset.set_timeline(timeline)

    def _add_asset_single_collection_type(self, asset: Asset):
        # single_collection is just asset itself
        self._collections[asset.ticker] = asset

    def _add_asset_multiple_collection_type(self, asset: Asset):
        # ticker_collection is element of collections with key as ticker
        ticker_collection = self._collections.get(asset.ticker, None)
        if ticker_collection is None:
            ticker_collection = self.create_asset_collection(asset, self._asset_type, self._asset_collection_type)
            self._collections[asset.ticker] = ticker_collection
        ticker_collection.add_asset(asset)

    @staticmethod
    def create_asset_collection(asset: Asset, asset_type: AssetType, collection_type: AssetCollectionType):
        if asset_type == AssetType.OPTION and collection_type == AssetCollectionType.MultiAsset:
            from ...security_basics.option_basics import OptionChain
            from ...security_basics.option_basics.core import Option
            if not isinstance(asset, Option):
                raise ValueError(f"Asset is not an option")
            return OptionChain(ticker=asset.ticker, expiration=asset.expiration)
