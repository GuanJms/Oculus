from typing import List, Dict

from .. import Asset
from ..._enums import MultiAssetType, OptionDomain
from .core import Option, Put, Call
from ._option_pair import OptionPair
from .._asset_collection import AssetCollection


class OptionChain(AssetCollection):

    def __init__(self, ticker: str, expiration: int):
        super().__init__()
        self._ticker = ticker
        self._asset_type = MultiAssetType.OPTION_CHAIN
        self._expiration = expiration
        self._assets: Dict[int, OptionPair] = {}  # key: strike, value: OptionPair

    @property
    def ticker(self) -> str:
        return self._ticker

    @property
    def expiration(self) -> int:
        return self._expiration

    def add_asset(self, option: Option):
        strike = option.strike
        if strike not in self._assets:
            self._assets[strike] = OptionPair(strike=strike, expiration=self.expiration)
        if option.option_type == OptionDomain.PUT:
            self._assets[strike].put = option
        elif option.option_type == OptionDomain.CALL:
            self._assets[strike].call = option

    def get_strike_options(self, strike: int) -> OptionPair:
        return self._assets[strike]

    def get_option(self, strike: int, option_type: OptionDomain) -> Option:
        return self._assets[strike].get_option(option_type)

