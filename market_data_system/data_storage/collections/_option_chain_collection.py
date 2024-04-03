from ._asset_collection import AssetCollection, AssetCollectionType
from ..._enums import AssetType
from ...security_basics.option_basics import OptionChain


class OptionChainCollection(AssetCollection):

    def __init__(self):
        super().__init__()
        self._asset_type = AssetType.OPTION
        self._asset_collection_type = AssetCollectionType.MultiAssetCollection

