from typing import List, Optional, Dict, Any

from .._enums import AssetCollectionType
from ._asset import Asset
from utils.global_id import GlobalComponentIDGenerator
from ..time_basics import Time


class AssetCollection:

    def __init__(self):
        self._ticker: Optional[str] = None
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._assets: Dict[Any, Asset | AssetCollection] = {}
        self._asset_type: Optional[AssetCollectionType] = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def ticker(self) -> str:
        raise "MultiAsset ticker function should be implemented in the child class"

    @property
    def type(self) -> AssetCollectionType:
        return self._asset_type

    def add_asset(self, asset: Asset):
        raise "MultiAsset add_asset function should be implemented in the child class"

    def get_assets(self) -> dict:
        return self._assets
