from ._asset_collection import AssetCollection
from ..._enums import DomainEnum, EquityDomain, AssetDomain


class StockCollection(AssetCollection):

    def __init__(self):
        super().__init__()
        self._domains = [AssetDomain.EQUITY, EquityDomain.STOCK]
z