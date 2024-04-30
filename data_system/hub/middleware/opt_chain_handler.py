from typing import List

from .hub_ticker import HubTicker
from data_system.connection.api_request.stoculus import StoculusOptionRequester
from ...security_basics.factory.option_chain_factory import OptionChainFactory
from ...security_basics.option_basics import OptionChain


class HubOptionChainHandler:

    @staticmethod
    def create_option_chain(hub_tic: HubTicker, **kwargs) -> List[OptionChain]:
        HubOptionChainHandler._check_hub_ticker(hub_tic)
        ticker = hub_tic.ticker
        exp_strikes = HubOptionChainHandler.get_exp_strikes(hub_tic, **kwargs)
        opt_chains = []
        for expiration, strikes in exp_strikes.items():
            for strike in strikes:
                _opt_chain = OptionChainFactory.create_option_chain(ticker, expiration, strike)
                opt_chains.append(_opt_chain)
        return opt_chains

    @staticmethod
    def get_exp_strikes(hub_tic: HubTicker, **kwargs) -> dict[int, list[int]]:
        HubOptionChainHandler._check_hub_ticker(hub_tic)
        exp_strikes = {}
        expirations = kwargs.get('expirations', None)
        strikes = kwargs.get('strikes', None)
        strike_range = kwargs.get('strike_range', None)
        if expirations is None:
            expirations = HubOptionChainHandler.get_expirations(hub_tic)
        if strikes is None:
            for expiration in expirations:
                exp_strikes[expiration] = HubOptionChainHandler.get_strikes(hub_tic, expiration=expiration,
                                                                            strike_range=strike_range)
        return exp_strikes

    @staticmethod
    def get_expirations(hub_tic: HubTicker) -> list:
        requester = StoculusOptionRequester()
        try:
            expirations = requester.get_exps(hub_tic.ticker)
            # TODO: implement a ticker checker method (that visit the API) to check if the ticker is valid
            if expirations is None:
                return []
            return expirations
        except Exception as e:
            print("Error - get_expirations", e)
            return []

    @staticmethod
    def get_strikes(hub_tic: HubTicker, expiration: int, **kwargs) -> list:
        HubOptionChainHandler._check_hub_ticker(hub_tic)
        strike_range = kwargs.get('strike_range', None)  # type: tuple[int, int] | None
        # TODO: API to get strikes
        strikes = [1, 2, 3, 4, 5, 6]

        if strike_range is None:
            return strikes

        min_strike, max_strike = strike_range
        Ks = []
        for K in strikes:
            if min_strike <= K <= max_strike:
                Ks.append(K)
        return Ks

        raise NotImplementedError

    @staticmethod
    def _check_hub_ticker(hub_tic: HubTicker):
        if not isinstance(hub_tic, HubTicker):
            print(type(hub_tic))
            raise ValueError("Ticker must be a HubTicker")
