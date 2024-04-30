from data_system._enums import OptionDomain
from data_system.security_basics.option_basics.core import Call, Put


class OptionFactory:
    @staticmethod
    def create_call(ticker: str, expiration: int, strike: int, **kwargs):
        return Call(ticker, expiration, strike)

    @staticmethod
    def create_put(ticker: str, expiration: int, strike: int, **kwargs):
        return Put(ticker, expiration, strike)
