from typing import Optional, List, Any, Dict, Type
from abc import ABC

from data_system.domain_managers.price_manager import PriceManager
from .._enums import DomainEnum, PriceDomain, TimeUnit, VolatilityDomain, OptionDomain
from utils.global_id import GlobalComponentIDGenerator
from ..domain_managers import DomainManager, VolatilityManager
from ..utils.domain_operations import parse_domain


# TODO: each asset collection should have one container manager
# TODO: Add price manager and take the price, bid, ask, and other price related into the price manager rather than the asset itself
class Asset(ABC):
    def __init__(self):
        self._id = GlobalComponentIDGenerator.generate_unique_id(
            self.__class__.__name__, id(self)
        )
        self._ticker: Optional[str] = None
        self._domains: Optional[List[DomainEnum]] = None
        self._underlying_asset: Optional["Asset"] = None
        self._price_manager: Optional[PriceManager] = None
        self._volatility_manager: Optional[VolatilityManager] = None
        self._domain_managers: List[DomainManager] = []  # managers of all other kinds

        # Option specific attributes
        self._underlying_asset: Optional["Asset"] = None
        self._live_iv_mode: Optional[bool] = None

    def __str__(self):
        return f"{self.__class__.__name__} {self._ticker}, snapshot: \033[94m{self.price_manager.get_snapshot()}\033[0m"

    def __repr__(self):
        return self.__str__()

    @property
    def id(self) -> str:
        return self._id

    @property
    def ticker(self) -> str:
        return self._ticker

    @property
    def domains(self) -> List[DomainEnum]:
        return self._domains

    @property
    def price_manager(self) -> PriceManager:
        return self._price_manager

    @property
    def volatility_manager(self) -> VolatilityManager:
        return self._volatility_manager

    def set_price_manager(self, price_manager: PriceManager = None):
        if price_manager is not None:
            self._price_manager = price_manager
        else:
            self._price_manager = PriceManager(
                domains=self._domains,
                underlying_asset=self._underlying_asset,
            )

    def set_volatility_manager(self, volatility_manager: VolatilityManager = None):
        if volatility_manager is not None:
            self._volatility_manager = volatility_manager
            self._volatility_manager.set_live_iv_mode(
                self._live_iv_mode
            )  # TODO: check if this is correct, make sure there is no conflict
        else:
            if self._volatility_manager is None:
                self._volatility_manager = VolatilityManager(
                    domains=self._domains,
                    underlying_asset=self._underlying_asset,
                    live_iv_mode=self._live_iv_mode,
                )
            else:
                print("Volatility manager already exists")

    def set_underlying_asset(self, asset: "Asset"):
        self._underlying_asset = asset

    def set_tick(self, tick: str):
        self._ticker = tick

    def get_param(self, param: str) -> Optional[Any]:
        # check if the param exists
        if hasattr(self, param):
            return getattr(self, param)
        if not param.startswith("_"):
            private = f"_{param}"
            if hasattr(self, private):
                return getattr(self, private)
        return None

    def get_params(self) -> dict[str, Optional]:
        # TODO: needs testing! Not sure if the code is correct
        all_params = {
            key: value for key, value in vars(self).items() if value is not None
        }
        return all_params

    def get_domain_chain_str(self, price_domain: PriceDomain | None = None) -> str:
        from ..utils.domain_operations import domain_to_chains

        domains = self._domains.copy()
        if price_domain is not None and not isinstance(price_domain, PriceDomain):
            raise ValueError("price_domain must be a PriceDomain enum")
        if price_domain is not None and isinstance(price_domain, PriceDomain):
            domains.append(price_domain)
        return domain_to_chains(domains=domains)

    def inject(self, data, meta: Dict[str, Any] | None = None):
        domains = parse_domain(meta.get("domains", []))
        self._price_manager.inject(data, domains=domains, meta=meta)
        if self._volatility_manager:
            self._volatility_manager.inject(data, domains=domains, meta=meta)

        for manager in self._domain_managers:
            manager.inject(data, domains=domains, meta=meta)

    def add_domain_manager(self, manager: DomainManager):
        self._domain_managers.append(manager)

    def add_lag_tracker(
        self,
        time_frame: int,
        time_unit: TimeUnit | str,
        domain_type: Type[DomainEnum],
        lag=0,
        has_lag=False,
        **kwargs,
    ):
        if domain_type == PriceDomain:
            self._price_manager.add_lag_tracker(time_frame, time_unit, lag, has_lag)

    def get_lag_tracker(
        self,
        time_frame: int,
        lag: int = 0,
        time_unit: TimeUnit | str = TimeUnit.SECOND,
        domains: List[DomainEnum] = None,
        domain_type=None,
    ):
        if domains is None:
            return None
        if domain_type == PriceDomain:
            return self._price_manager.get_lag_tracker(time_frame, domains, lag, time_unit)
        elif domain_type == VolatilityDomain:
            raise NotImplementedError("Implied volatility lag tracker not implemented")
        return None



    def get_last_traded_price(self):
        return self._price_manager.get_last_traded_price()

    def get_last_quote_price(self):
        return self._price_manager.get_last_quote_price()

    # def set_live_mode(self, params):
    #     if self._volatility_manager:
    #         self._volatility_manager.set_live_mode(params)
    #     if self._price_manager:
    #         self._price_manager.set_live_mode(params)
