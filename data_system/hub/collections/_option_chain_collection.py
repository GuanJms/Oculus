from typing import List

from ._asset_collection import AssetCollection, AssetCollectionType
from ...security_basics.option_basics.core import Option
from ..._enums import AssetDomain, EquityDomain


class OptionChainCollection(AssetCollection):

    def __init__(self):
        super().__init__()
        self._domains = [AssetDomain.EQUITY, EquityDomain.OPTION]
        self._asset_collection_type = AssetCollectionType.MultiAsset

    def get_assets(self) -> List[Option]:
        option_chains = list(self._collections.values())
        options = []
        for option_chain in option_chains:
            options += option_chain.get_assets()
        return options





