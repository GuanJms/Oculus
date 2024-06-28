from ...._enums import OptionDomain
from ._option import Option


class Put(Option):
    def __init__(self, ticker: str, expiration: int, strike: int, **kwargs):
        super().__init__(ticker, expiration, strike, **kwargs)
        self._option_type = OptionDomain.PUT
