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
        c = OptionFactory.configure_option(c, underlying_asset, **kwargs)
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
        p = OptionFactory.configure_option(p, underlying_asset, **kwargs)
        return p

    @staticmethod
    def configure_option(option, underlying_asset, **kwargs):
        option.set_underlying_asset(underlying_asset)
        option.set_price_manager(kwargs.get("price_manager", None))
        option.set_volatility_manager(kwargs.get("volatility_manager", None))
        if option.live_greek_mode:
            option.set_greek_manager(kwargs.get("greek_manager", None))
        return option

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

        option_params = {
            "underlying_asset": underlying_asset,
            "price_manager": kwargs.get("price_manager", None),
            "live_iv_mode": kwargs.get("live_iv_mode", False),
            "live_greek_mode": kwargs.get("live_greek_mode", False),
        }

        match right:
            case OptionDomain.CALL:
                return OptionFactory.create_call(
                    ticker, expiration, strike, **option_params
                )
            case OptionDomain.PUT:
                return OptionFactory.create_put(
                    ticker,
                    expiration,
                    strike,
                    **option_params,
                )
            case _:
                raise Exception(f"Right {right} not supported.")
