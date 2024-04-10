from typing import List, Optional

from .._enums import AssetCollectionType
from ._asset import Asset
from utils.global_id import GlobalComponentIDGenerator
from ..time_basics import Time


class MultiAsset:

    def __init__(self):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._asset_list: List[Asset] = []
        self._type: Optional[AssetCollectionType] = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def asset_list(self) -> List[Asset]:
        return self._asset_list

    @property
    def type(self) -> AssetCollectionType:
        return self._type

    def add_asset(self, asset: Asset):
        self._asset_list.append(asset)

    def get_assets(self) -> List[Asset]:
        return self._asset_list
