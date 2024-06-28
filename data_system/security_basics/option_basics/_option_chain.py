from typing import List, Dict, Any

from .._asset_collection import AssetCollection
from ..._enums import MultiAssetType, OptionDomain, AssetCollectionType
from .core import Option
from ._option_pair import OptionPair


class OptionChain(AssetCollection):
    def __init__(self, ticker: str, expiration: int, **kwargs):
        super().__init__()
        self._live_iv_mode = kwargs.get("live_iv_mode", False)
        self._live_greek_mode = kwargs.get("live_greek_mode", False)
        self._ticker = ticker
        self._asset_collection_type = AssetCollectionType.AssetCollection
        self._expiration = expiration
        self._assets: Dict[int, OptionPair] = {}  # key: strike, value: OptionPair

    def __str__(self):
        return f"OptionChain: {self._ticker} - {self._expiration} - {self._assets}"

    def __create__(self, key: str | int | Any):  # key: strike
        from ..factory.option_pair_factory import OptionPairFactory

        return OptionPairFactory.create_option_pair(
            ticker=self.ticker,
            expiration=self.expiration,
            strike=key,
            underlying_asset=self._underlying_asset,
            live_iv_mode=self._live_iv_mode,
            live_greek_mode=self._live_greek_mode,
        )

    def __check_inject_meta__(self, meta) -> bool:
        return "strike" in meta

    def __meta_key__(self, meta) -> Any:
        return meta["strike"]

    @property
    def ticker(self) -> str:
        return self._ticker

    @property
    def expiration(self) -> int:
        return self._expiration

    def add_asset(self, option: Option):
        if option.ticker != self.ticker:
            raise ValueError("Ticker does not match")
        if option.expiration != self.expiration:
            raise ValueError("Expiration does not match")

        strike = option.strike
        ticker = option.ticker
        # adding option to option chain
        option_pair: OptionPair = self.__get_not_create__(strike)
        option_pair.add_asset(option)

    def get_strike_options(self, strike: int) -> OptionPair:
        return self.__get_not_create__(strike)

    def get_option(self, strike: int, option_type: OptionDomain | str) -> Option:
        # Get and create if not exists
        option_pair: OptionPair = self.__get_not_create__(strike)
        return option_pair.get_option(option_type)

    def set_live_mode(self, params):
        # params should contain 'live_iv_mode' key
        if "live_iv_mode" in params:
            self._live_iv_mode = params.get("live_iv_mode")
        for option_pair in self._assets.values():
            option_pair.set_live_mode(params)

    def get_underlying_asset(self):
        return self._underlying_asset
