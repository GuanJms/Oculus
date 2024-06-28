from data_system._enums import OptionDomain
from data_system.security_basics import Asset
from data_system.security_basics.option_basics.core import Call, Put


class OptionFactory:
    @staticmethod
    def create_call(
        ticker: str,
        expiration: int,
        strike: int,
        underlying_asset: Asset = None,
        **kwargs,
    ) -> Call:
        c = Call(ticker, expiration, strike, **kwargs)
        c.set_underlying_asset(underlying_asset)
        c.set_price_manager(kwargs.get("price_manager", None))
        c.set_volatility_manager(kwargs.get("volatility_manager", None))
        if c.live_greek_mode:
            c.set_greek_manager(kwargs.get("greek_manager", None))
        return c

    @staticmethod
    def create_put(
        ticker: str,
        expiration: int,
        strike: int,
        underlying_asset: Asset = None,
        **kwargs,
    ) -> Put:
        p = Put(ticker, expiration, strike, **kwargs)
        p.set_underlying_asset(underlying_asset)
        p.set_price_manager(kwargs.get("price_manager", None))
        p.set_volatility_manager(kwargs.get("volatility_manager", None))
        return p

    @staticmethod
    def create_option(
        ticker: str,
        expiration: int,
        strike: int,
        right: OptionDomain | str,
        underlying_asset=None,
        **kwargs,
    ) -> Call | Put:

        if isinstance(right, str):
            right = OptionDomain.get_option_type(right)

        match right:
            case OptionDomain.CALL:
                return OptionFactory.create_call(
                    ticker,
                    expiration,
                    strike,
                    underlying_asset=underlying_asset,
                    price_manager=kwargs.get("price_manager", None),
                    live_iv_mode=kwargs.get("live_iv_mode", False),
                )
            case OptionDomain.PUT:
                return OptionFactory.create_put(
                    ticker,
                    expiration,
                    strike,
                    underlying_asset=underlying_asset,
                    price_manager=kwargs.get("price_manager", None),
                    live_iv_mode=kwargs.get("live_iv_mode", False),
                )
            case _:
                raise Exception(f"Right {right} not supported.")
