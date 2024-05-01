from typing import List, Dict

from ._asset_collection_hub import AssetCollectionHub, AssetCollectionType
from ..middleware import HubTicker
from ...security_basics.option_basics import OptionChain, OptionChainCollection
from ..._enums import AssetDomain, EquityDomain


class OptionChainCollectionHub(AssetCollectionHub):

    def __init__(self):
        super().__init__()
        self._collections: Dict[str, OptionChainCollection] = {}  # key: ticker, value: OptionChain
        self._domains = [AssetDomain.EQUITY, EquityDomain.OPTION]
        self._asset_collection_type = AssetCollectionType.AssetCollection

    def _add(self, option_chain: OptionChain):
        """
        Add option chain to collection
        :param option_chain: OptionChain (ticker, expiration, assets)
        """
        ticker = option_chain.ticker
        _collection: OptionChainCollection = self.get_collection(collection_name=ticker)
        _collection.add(option_chain)

    def _create_base_collection(self, collection_name: str) -> OptionChainCollection:
        return OptionChainCollection(ticker=collection_name)

    def get_assets(self) -> List[OptionChain]:
        option_chains = list(self._collections.values())
        options = []
        for option_chain in option_chains:
            options += option_chain.get_assets()
        return options
