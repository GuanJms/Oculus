from typing import List, Any, Dict

from .asset_collection_hub import AssetCollectionHub
from ..._enums import DomainEnum, EquityDomain, AssetDomain, AssetCollectionType
from ...security_basics import Asset, Stock
from ...security_basics.factory.stock_factory import StockFactory


class StockCollectionHub(AssetCollectionHub):
    def __init__(self):
        super().__init__()
        self._domains = [AssetDomain.EQUITY, EquityDomain.STOCK]
        self._asset_collection_type = AssetCollectionType.Asset

    def __create__(self, key: str):
        # collection_name is ticker
        new_stock = StockFactory.create_stock(ticker=key)
        return new_stock

    def get_assets(self) -> List[Asset]:
        return list(self._collections.values())

    def __add_asset__(self, asset: Stock):
        key = asset.ticker  # Higher level adding asset to the collection
        self.__add__(key, asset)

    def get_asset(self, params):
        ticker = params.get("ticker")
        return self.get_stock(ticker)

    def get_stock(self, ticker: str) -> Stock:
        return self.__get_not_create__(ticker)
