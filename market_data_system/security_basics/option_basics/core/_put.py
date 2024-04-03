from ...._enums import OptionType
from ._option import Option


class Put(Option):
    def __init__(self, ticker: str, expiration: int, strike: int):
        super().__init__(ticker, expiration, strike)
        self._option_type = OptionType.PUT
