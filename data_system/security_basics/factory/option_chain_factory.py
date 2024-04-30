from data_system.security_basics.factory.option_facotry import OptionFactory
from data_system.security_basics.option_basics import OptionChain


class OptionChainFactory:
    @staticmethod
    def create_option_chain(ticker: str, expiration: int, strikes: list[int]):
        opt_chain = OptionChain(ticker, expiration)
        for strike in strikes:
            put = OptionFactory.create_put(ticker, expiration, strike)
            call = OptionFactory.create_call(ticker, expiration, strike)
            opt_chain.add_asset(put)
            opt_chain.add_asset(call)
        return opt_chain
