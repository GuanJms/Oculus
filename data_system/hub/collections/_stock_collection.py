from typing import List

from ._asset_collection import AssetCollection
from ..._enums import DomainEnum, EquityDomain, AssetDomain, AssetCollectionType
from ...security_basics import Asset


class StockCollection(AssetCollection):

    def __init__(self):
        super().__init__()
        self._domains = [AssetDomain.EQUITY, EquityDomain.STOCK]
        self._asset_collection_type = AssetCollectionType.SingleAsset

    def get_assets(self) -> List[Asset]:
        return list(self._collections.values())
