from ._option import Option
from ...._enums import OptionDomain


class Call(Option):
    def __init__(self, ticker: str, expiration: int, strike: int):
        super().__init__(ticker, expiration, strike)
        self._option_type = OptionDomain.CALL
