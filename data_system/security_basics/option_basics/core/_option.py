from typing import Optional, Any

from ...._enums import AssetDomain, EquityDomain, OptionDomain
from ..._asset import Asset
from ....domain_managers.greek_manager import GreekManager


class Option(Asset):
    def __init__(
        self,
        ticker: str,
        expiration: int,
        strike: int,
        underlying_asset: Asset = None,
        **kwargs,
    ):
        super().__init__()
        self._ticker = ticker
        self._underlying_asset = underlying_asset
        self._domains = [AssetDomain.EQUITY, EquityDomain.OPTION]
        self._option_type: Optional[OptionDomain] = None
        self._strike = strike
        self._expiration: int = expiration  # Remark: Add Date Time class if there is need for that in the future
        self._live_iv_mode = kwargs.get("live_iv_mode", False)
        self._live_greek_mode = kwargs.get("live_greek_mode", False)
        self._greek_manager: Optional[GreekManager] = None

    def __str__(self):
        return (
            super().__str__()
            + f"{self._option_type.name} {self._strike} {self._expiration}"
        )

    @property
    def greek_manager(self) -> GreekManager:
        return self._greek_manager

    def set_underlying_asset(self, asset: Asset | Any):
        self._underlying_asset = asset

    # def set_live_mode(self, params):
    #     super().set_live_mode(params)
    #     if "live_iv_mode" in params:
    #         self._live_iv_mode = params.get("live_iv_mode")
    #         self.volatility_manager.set_live_iv_mode(self._live_iv_mode)
    #     if "live_greek_mode" in params:
    #         self._live_greek_mode = params.get("live_greek_mode")
    #         self._greek_manager.set_live_greek_mode(self._live_greek_mode)

    def set_greek_manager(self, greek_manager: GreekManager = None):
        if greek_manager is not None:
            self._greek_manager = greek_manager
        else:
            # Create a new greek manager & greek manager should have access to the volatility manager for ivs
            # TODO: construct a time deque to store historical ivs for searching for historical ivs that needed for calculating the greeks
            if self._volatility_manager is None:
                self.set_volatility_manager()
            self._greek_manager = GreekManager(
                domains=self._domains,
                underlying_asset=self._underlying_asset,
                live_iv_mode=self._live_iv_mode,
            )
            self._greek_manager.set_volatility_manager(self._volatility_manager)
            greek_mode = {
                "delta": True,
                "gamma": True,
                "theta": True,
                "vega": True,
                "rho": False,
            }
            self._greek_manager.set_greek_mode(**greek_mode)  # TODO: implement function
            self.add_domain_manager(self._greek_manager)

    @property
    def option_type(self) -> OptionDomain:
        return self._option_type

    @property
    def strike(self) -> int:
        return self._strike

    @property
    def expiration(self) -> int:
        return self._expiration

    def get_last_traded_iv(self):
        return self.volatility_manager.get_last_trade_iv()

    def get_last_quote_iv(self):
        return self.volatility_manager.get_last_quote_iv()

    def live_greek_mode(self) -> bool:
        return self._live_greek_mode
