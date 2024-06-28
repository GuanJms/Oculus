from typing import List, Optional, Dict, Any

from abc import ABC, abstractmethod

from .._enums import AssetCollectionType
from ._asset import Asset
from utils.global_id import GlobalComponentIDGenerator


class AssetCollection(ABC):
    def __init__(self):
        self._ticker: Optional[str] = None
        self._id = GlobalComponentIDGenerator.generate_unique_id(
            self.__class__.__name__, id(self)
        )
        self._assets: Dict[Any, Asset | "AssetCollection"] = {}
        self._asset_collection_type: Optional[AssetCollectionType] = None
        self._underlying_asset: Optional[Asset] = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def ticker(self) -> str:
        raise "MultiAsset ticker function should be implemented in the child class"

    @property
    def type(self) -> AssetCollectionType:
        return self._asset_type

    def set_underlying_asset(self, asset: Asset):
        self._underlying_asset = asset
        for asset in self._assets.values():
            asset.set_underlying_asset(asset)

    def __has__(self, key: Any) -> bool:
        return key in self._assets

    def __get__(self, key: Any):
        return self._assets.get(key, None)

    def __add__(self, key: Any, asset: Asset | Any):
        if self.__has__(key):
            raise ValueError(f"Asset {key} already exists")
        self._assets[key] = asset

    def __get_not_create__(self, key: Any):
        if not self.__has__(key):
            e = self.__create__(key)
            self.__add__(key, e)
        return self.__get__(key)

    def add_asset(self, asset: Asset):
        raise "MultiAsset add_asset function should be implemented in the child class"

    def get_assets(self) -> List[Asset]:
        if self._asset_collection_type == AssetCollectionType.Asset:
            return list(self._assets.values())
        elif self._asset_collection_type == AssetCollectionType.AssetCollection:
            assets = []
            for asset in self._assets.values():
                assets += asset.get_assets()
            return assets
        else:
            raise ValueError("Asset type is not supported")

    @abstractmethod
    def __create__(self, key: str | int | Any):
        pass

    def inject(self, data, meta: Dict[str, Any] | None = None):
        if not self.__check_inject_meta__(meta):
            # invalid meta
            return
        key = self.__meta_key__(meta)
        e = self.__get_not_create__(key)
        e.inject(data, meta)
        # print(f"{self.__class__.__name__} injected: {data} ...| Meta: {meta}")
        # print(f"Collection: {e}")

    @abstractmethod
    def __check_inject_meta__(self, meta) -> bool:
        pass

    @abstractmethod
    def __meta_key__(self, meta) -> Any:
        pass
