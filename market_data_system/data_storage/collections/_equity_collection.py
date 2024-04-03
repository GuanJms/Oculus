from ._asset_collection import AssetCollection
from ..._enums import AssetType


class EquityCollection(AssetCollection):

    def __init__(self):
        super().__init__()
        self._asset_type = AssetType.EQUITY
