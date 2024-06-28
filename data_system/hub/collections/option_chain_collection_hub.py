from typing import List, Dict

from .asset_collection_hub import AssetCollectionHub, AssetCollectionType
from ..instrument_finder import InstrumentFinder
from ..middleware import HubTicker
from ...security_basics.option_basics import OptionChain, OptionChainCollection
from ..._enums import AssetDomain, EquityDomain, SingleAssetType
from ...security_basics.option_basics.core import Option


class OptionChainCollectionHub(AssetCollectionHub):
    def __init__(self, **kwargs):
        super().__init__()
        self._collections: Dict[
            str, OptionChainCollection
        ] = {}  # key: ticker, value: OptionChain
        self._domains = [AssetDomain.EQUITY, EquityDomain.OPTION]
        self._asset_collection_type = AssetCollectionType.AssetCollection
        self._live_iv_mode: bool = kwargs.get("live_iv_mode", False)
        self._live_greek_mode: bool = kwargs.get("live_greek_mode", False)

    def __add_asset__(self, asset: Option):
        """
        Add option chain to collection
        :param option_chain: OptionChain (ticker, expiration, assets)
        """
        ticker = asset.ticker
        _collection: OptionChainCollection = self.__get__(key=ticker)
        _collection.add_asset(asset)

    def inject(self, data, meta: Dict[str, any] | None = None):
        super().inject(data, meta)

    def __create__(self, key: str):
        e = OptionChainCollection(ticker=key, live_iv_mode=self._live_iv_mode,
                                  live_greek_mode=self._live_greek_mode)
        # get underlying for option chain collection
        finder = InstrumentFinder()
        underlying = finder.find_asset(ticker=key, asset_type=SingleAssetType.STOCK)
        # print(f"Underlying: {underlying}")
        e.set_underlying_asset(underlying)
        return e

    def get_assets(self) -> List[OptionChain]:
        option_chain_collections = list(self._collections.values())
        options = []
        for option_chain_collection in option_chain_collections:
            options += option_chain_collection.get_assets()
        return options

    def get_asset(self, params):
        # TODO: figure out if there is need to merge get_asset and get_option
        ticker = params.get("ticker")
        expiration = params.get("expiration")
        strike = params.get("strike")
        right = params.get("right")
        option_chain_collection: OptionChainCollection = self.__get_not_create__(ticker)
        return option_chain_collection.get_option(expiration, strike, right)

    def get_option(self, ticker, expiration, strike, right):
        option_chain_collection: OptionChainCollection = self.__get_not_create__(ticker)
        return option_chain_collection.get_option(expiration, strike, right)

    def set_live_mode(self, params):
        # params should contain 'live_iv_mode' key
        if "live_iv_mode" in params:
            self._live_iv_mode = params.get("live_iv_mode")
        for collection in self._collections.values():
            collection.set_live_mode(params)

    def get_option_chain(self, ticker: str, expiration: int):
        option_chain_collection: OptionChainCollection = self.__get_not_create__(ticker)
        return option_chain_collection.get_option_chain(expiration)