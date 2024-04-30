from typing import Optional, Dict, List, Any
from ...security_basics import Asset, AssetCollection
from ..._enums import AssetCollectionType, DomainEnum, EquityDomain


class AssetCollectionHub:
    def __init__(self):
        self._collections: Dict[str, Asset | AssetCollection] = {}
        self._asset_collection_type: Optional[AssetCollectionType] = None
        self._domains: Optional[List[DomainEnum]] = None

    def check_type(self, asset: Asset):
        if set(asset.domains).intersection(self._domains) != set(self._domains):
            raise ValueError(f"Asset domain {asset.domains} is not compatible with collection domain {self._domains}")

    def add(self, asset: Any):
        self.check_type(asset)
        self._add(asset)

    def _add(self, asset: Any):
        raise NotImplementedError("Child class should implement this method")

    def get_collection(self, collection_name: str):
        _collection = self._collections.get(collection_name, None)
        if _collection is None:
            _collection = self._construct_collection_if_not_exists(collection_name)
            self._collections[collection_name] = _collection
        return _collection

    def _construct_collection_if_not_exists(self, collection_name: str):
        raise NotImplementedError("Child class should implement this method")