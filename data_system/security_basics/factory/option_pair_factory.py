from data_system.security_basics import Asset
from data_system.security_basics.option_basics.core import Call, Put


class OptionPairFactory:
    @staticmethod
    def create_option_pair(
        ticker: str,
        strike: int,
        expiration: int,
        put: Put = None,
        call: Call = None,
        underlying_asset: Asset = None,
        **kwargs
    ):
        from data_system.security_basics.factory.option_facotry import OptionFactory
        from data_system.security_basics.option_basics import OptionPair

        live_iv_mode = kwargs.get("live_iv_mode", False)
        live_greek_mode = kwargs.get("live_greek_mode", False)
        if put is None:
            put = OptionFactory.create_put(
                ticker,
                expiration,
                strike,
                underlying_asset=underlying_asset,
                live_iv_mode=live_iv_mode,
                live_greek_mode=live_greek_mode,
            )
        if call is None:
            call = OptionFactory.create_call(
                ticker,
                expiration,
                strike,
                underlying_asset=underlying_asset,
                live_iv_mode=live_iv_mode,
                live_greek_mode=live_greek_mode,
            )
        opt_pair = OptionPair(
            ticker,
            strike,
            expiration,
            live_iv_mode=live_iv_mode,
            live_greek_mode=live_greek_mode,
        )
        opt_pair.set_underlying_asset(underlying_asset)
        opt_pair.add_asset(put)
        opt_pair.add_asset(call)
        return opt_pair
