from typing import Optional, Dict, List, Any

from ..instrument_finder import InstrumentFinder
from ...security_basics import Asset, AssetCollection
from ..._enums import AssetCollectionType, DomainEnum, EquityDomain

from abc import ABC, abstractmethod


class AssetCollectionHub(ABC):
    def __init__(self):
        self._collections: Dict[str, Asset | AssetCollection] = {}
        self._asset_collection_type: Optional[AssetCollectionType] = None
        self._domains: Optional[List[DomainEnum]] = None
        self._instrument_finder: InstrumentFinder = InstrumentFinder()

    def get_domains(self):
        return self._domains

    def check_type(self, asset: Asset):
        if set(asset.domains).intersection(self._domains) != set(self._domains):
            raise ValueError(
                f"Asset domain {asset.domains} is not compatible with collection domain {self._domains}"
            )

    def __has__(self, key: str):
        return key in self._collections

    def __get__(self, key: str):
        return self._collections.get(key, None)

    def __add__(self, key: str, asset: Asset | AssetCollection):
        if self.__has__(key):
            raise ValueError(f"Asset {key} already exists")
        self._collections[key] = asset

    def __get_not_create__(self, key: str):
        if not self.__has__(key):
            e = self.__create__(key)
            self.__add__(key, e)
        return self.__get__(key)

    def __add_asset__(self, asset: Any):
        raise NotImplementedError("Child class should implement this method")

    def add_asset(self, asset: Any):
        self.check_type(asset)
        self.__add_asset__(asset)

    @abstractmethod
    def __create__(self, key: str) -> Asset | AssetCollection:
        pass

    def inject(self, data, meta: Dict[str, Any] | None = None):
        if meta is None:
            print("Meta not found")
            return
        if "ticker" not in meta:
            print("Ticker not found in meta")
            return
        ticker = meta.get("ticker")
        # print(f"AssetCollectionHub Class - Node: {data} ...| Meta: {meta}")
        collection = self.__get_not_create__(ticker)
        # print(f"Collection: {collection}")
        collection.inject(data, meta)

    @abstractmethod
    def get_asset(self, params):
        pass
