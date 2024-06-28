"""
This is class is a AssetCollection of OptionChain objects. It is a subclass of AssetCollection. It is used to store
OptionChain objects.
"""
from typing import Dict

from data_system._enums import AssetCollectionType
from data_system.security_basics import AssetCollection
from data_system.security_basics.factory.option_chain_factory import OptionChainFactory
from data_system.security_basics.option_basics import OptionChain
from data_system.security_basics.option_basics.core import Option


class OptionChainCollection(AssetCollection):
    def __init__(self, ticker: str, **kwargs):
        super().__init__()
        self._ticker = ticker
        self._asset_collection_type = AssetCollectionType.AssetCollection
        self._live_iv_mode: bool = kwargs.get("live_iv_mode", False)
        self._live_greek_mode: bool = kwargs.get("live_greek_mode", False)
        self._assets: Dict[int, OptionChain] = {}  # key: expiration, value: OptionChain
        # TODO: adding underlying asset to OptionChainCollection and make it able
        #  to pass in the underlying asset to the next level object as well

    def __str__(self):
        return f"OptionChainCollection: {self._ticker} - {self._assets}"

    def __check_inject_meta__(self, meta) -> bool:
        return "expiration" in meta

    def __meta_key__(self, meta) -> int:
        return meta["expiration"]

    def add_asset(self, option: Option):
        expiration = option.expiration
        option_chain: OptionChain = self.__get_not_create__(expiration)
        option_chain.add_asset(option)

    def get_option(self, expiration, strike: int, right: str):
        option_chain: OptionChain = self.__get_not_create__(expiration)
        return option_chain.get_option(strike, right)

    def __create__(self, expiration: int):
        return OptionChainFactory.create_option_chain(
            ticker=self._ticker,
            expiration=expiration,
            strikes=[],
            underlying_asset=self._underlying_asset,
            live_iv_mode=self._live_iv_mode,
            live_greek_mode=self._live_greek_mode,
        )

    def set_live_mode(self, params):
        # params should contain 'live_iv_mode' key
        if "live_iv_mode" in params:
            self._live_iv_mode = params.get("live_iv_mode")
        for option_chain in self._assets.values():
            option_chain.set_live_mode(params)

    def get_option_chain(self, expiration: int):
        return self.__get__(expiration)
