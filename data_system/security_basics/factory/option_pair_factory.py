from data_system.security_basics.factory.option_facotry import OptionFactory
from data_system.security_basics.option_basics import OptionPair


class OptionPairFactory:

    @staticmethod
    def create_option_pair(ticker: str, strike: int, expiration: int, **kwargs):
        put = kwargs.get('put', None)
        call = kwargs.get('call', None)
        if put is None:
            put = OptionFactory.create_put(ticker, expiration, strike)
        if call is None:
            call = OptionFactory.create_call(ticker, expiration, strike)
        return OptionPair(ticker, strike, expiration, put, call)
