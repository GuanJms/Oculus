from typing import Optional, Any

from .core import Option
from .. import AssetCollection, Asset
from ..._enums import OptionDomain, AssetCollectionType


class OptionPair(AssetCollection):
    def __init__(self, ticker: str, strike: int, expiration: int, **kwargs):
        super().__init__()
        self._ticker = ticker
        self._asset_collection_type = AssetCollectionType.Asset
        self._live_iv_mode = kwargs.get("live_iv_mode", False)
        self._live_greek_mode = kwargs.get("live_greek_mode", False)

        # validate strike and expiration
        if not isinstance(strike, int):
            raise ValueError(f"Strike must be an integer - received {strike} of type {type(strike)}")
        if not isinstance(expiration, int):
            raise ValueError(f"Expiration must be an integer - received {expiration} of type {type(expiration)}")

        self._strike = strike
        self._expiration = expiration

    def __str__(self):
        return f"OptionPair: {self._ticker} - {self._strike} - {self._expiration} - {self._assets}"

    def __repr__(self):
        return self.__str__()

    def __create__(self, right: OptionDomain):
        from ..factory.option_facotry import OptionFactory

        return OptionFactory.create_option(
            self._ticker,
            self._expiration,
            self._strike,
            right,
            underlying_asset=self._underlying_asset,
            live_iv_mode=self._live_iv_mode,
            live_greek_mode=self._live_greek_mode,
        )

    def __get__(self, key: OptionDomain | str) -> Asset | AssetCollection:
        if isinstance(key, str):
            key = OptionDomain.get_option_type(key)  # convert string to OptionDomain
        return super().__get__(key)

    def __check_inject_meta__(self, meta) -> bool:
        return "right" in meta

    def __meta_key__(self, meta) -> Any:
        return meta["right"]

    @property
    def ticker(self):
        return self._ticker

    @property
    def put(self):
        return self.__get_not_create__(OptionDomain.PUT)

    @property
    def call(self):
        return self.__get_not_create__(OptionDomain.CALL)

    @property
    def strike(self):
        return self._strike

    def add_asset(self, asset: Option):
        if asset.strike != self.strike:
            raise ValueError("Strike does not match")
        if asset.expiration != self._expiration:
            raise ValueError("Expiration does not match")
        if asset.ticker != self._ticker:
            raise ValueError("Ticker does not match")

        if asset.option_type == OptionDomain.PUT:
            self.__add__(OptionDomain.PUT, asset)
        elif asset.option_type == OptionDomain.CALL:
            self.__add__(OptionDomain.CALL, asset)

    def get_option(self, option_type: OptionDomain | str):
        return self.__get__(option_type)
