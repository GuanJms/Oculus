from data_system.security_basics.option_basics import OptionChain


class OptionChainFactory:
    @staticmethod
    def create_option_chain(
        ticker: str,
        expiration: int,
        strikes: list[int] = None,
        underlying_asset=None,
        live_iv_mode: bool = False,
        live_greek_mode: bool = False,
    ) -> OptionChain:
        from data_system.security_basics.factory.option_facotry import OptionFactory
        opt_chain = OptionChain(ticker, expiration, live_iv_mode=live_iv_mode, live_greek_mode=live_greek_mode)
        opt_chain.set_underlying_asset(underlying_asset)
        for strike in strikes:
            put = OptionFactory.create_put(
                ticker,
                expiration,
                strike,
                underlying_asset=underlying_asset,
                live_iv_mode=live_iv_mode,
                live_greek_mode=live_greek_mode,
            )
            call = OptionFactory.create_call(
                ticker,
                expiration,
                strike,
                underlying_asset=underlying_asset,
                live_iv_mode=live_iv_mode,
                live_greek_mode=live_greek_mode,
            )
            opt_chain.add_asset(put)
            opt_chain.add_asset(call)
        return opt_chain
