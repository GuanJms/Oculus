from typing import List

from ._asset_collection_hub import AssetCollectionHub
from ..._enums import DomainEnum, EquityDomain, AssetDomain, AssetCollectionType
from ...security_basics import Asset


class StockCollectionHub(AssetCollectionHub):

    def __init__(self):
        super().__init__()
        self._domains = [AssetDomain.EQUITY, EquityDomain.STOCK]
        self._asset_collection_type = AssetCollectionType.Asset

    def get_assets(self) -> List[Asset]:
        return list(self._collections.values())


