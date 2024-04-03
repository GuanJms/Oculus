from typing import List, Dict

from .. import Asset
from ..._enums import MultiAssetType, OptionType
from .core import Option, Put, Call
from ._option_pair import OptionPair
from .._asset_collection import MultiAsset


class OptionChain(MultiAsset):

    def __init__(self, ticker: str, expiration: int):
        super().__init__()
        self._ticker = ticker
        self._type = MultiAssetType.OPTION_CHAIN
        self._expiration = expiration
        self._asset_list: Dict[int, OptionPair] = {}

    @property
    def ticker(self) -> str:
        return self._ticker

    @property
    def expiration(self) -> int:
        return self._expiration

    def add_asset(self, option: Option):
        strike = option.strike
        if strike not in self._asset_list:
            self._asset_list[strike] = OptionPair(strike=strike, expiration=self.expiration)
        if option.option_type == OptionType.PUT:
            self._asset_list[strike].put = option
        elif option.option_type == OptionType.CALL:
            self._asset_list[strike].call = option

    def get_strike_options(self, strike: int) -> OptionPair:
        return self._asset_list[strike]

    def get_option(self, strike: int, option_type: OptionType) -> Option:
        return self._asset_list[strike].get_option(option_type)

