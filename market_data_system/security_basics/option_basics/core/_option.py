from typing import Optional

from ...._enums import OptionDomain
from ..._asset import Asset


class Option(Asset):

    def __init__(self, ticker: str, expiration: int, strike: int):
        super().__init__()
        self._ticker = ticker
        self._type: AssetType.OPTION
        self._option_type: Optional[OptionDomain] = None
        self._strike = strike
        self._expiration = expiration  # Remark: Add Date Time class if there is need for that in the future

    @property
    def option_type(self) -> OptionDomain:
        return self._option_type

    @property
    def strike(self) -> int:
        return self._strike

    @property
    def expiration(self) -> int:
        return self._expiration
