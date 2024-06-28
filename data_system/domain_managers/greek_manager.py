from typing import Optional, Dict

from calculators.greek_calculator import GreekCalculator
from data_system._enums import PriceDomain, GreekDomain
from data_system.base_structure.nodes import TradeNode, QuoteNode
from data_system.containers.container_managers import (
    TimeLagQueueManager,
    SnapshotManager,
)
from data_system.domain_managers.domain_manager import DomainManager
from data_system.domain_managers.volatility_manager import VolatilityManager
from data_system.security_basics import Stock
from data_system.utils.time_operations import calculate_time_to_maturity


def calculate_inject_gamma(node, s, k, t, r, q, sigma, right):
    gamma = GreekCalculator.calculate_gamma(s, k, t, r, q, sigma, right)
    node.set_gamma(gamma)


class GreekManager(DomainManager):
    supported_greeks = ["delta", "gamma", "theta", "vega", "rho"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.greek_modes: Dict[str, bool] = {
            "delta": False,
            "gamma": False,
            "theta": False,
            "vega": False,
            "rho": False,
        }
        self._running_snapshot = False
        self._live_greek_mode = kwargs.get("live_greek_mode", False)
        self._underlying_asset = kwargs.get("underlying_asset", None)
        self._volatility_manager: Optional[VolatilityManager] = None
        self._size_limiter = None  # TODO: implement size limiter like frequency limiter
        self._traded_time_lag_queue_managers: Dict[
            GreekDomain, TimeLagQueueManager
        ] = {}
        self._quote_time_lag_queue_manager: Dict[GreekDomain, TimeLagQueueManager] = {}
        self._traded_snapshot_managers: Dict[GreekDomain, SnapshotManager] = {}
        self._quote_snapshot_managers: Dict[GreekDomain, SnapshotManager] = {}

        self.set_traded_time_lag_queue_managers()
        self.set_quote_time_lag_queue_managers()
        self.set_traded_snapshot_managers()
        self.set_quote_snapshot_managers()

    def inject(self, node, meta: dict = None):
        if self._live_greek_mode:
            self.calculate_inject_greeks(node, meta)
        raise NotImplementedError("Need to implement inject")

    def set_volatility_manager(self, volatility_manager: VolatilityManager):
        if volatility_manager is None:
            print("Greek Manager - Volatility manager is trying with None")
            return
        self._volatility_manager = volatility_manager

    def set_greek_mode(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.supported_greeks:
                self.greek_modes[key] = value
            else:
                print(f"Unsupported Greek: {key}")

    def set_traded_time_lag_queue_managers(self):
        for domain in GreekDomain:
            self._traded_time_lag_queue_managers[domain] = TimeLagQueueManager(
                domains=self._domains + [domain]
            )

    def set_quote_time_lag_queue_managers(self):
        for domain in GreekDomain:
            self._quote_time_lag_queue_manager[domain] = TimeLagQueueManager(
                domains=self._domains + [domain]
            )

    def set_traded_snapshot_managers(self):
        raise NotImplementedError("Need to implement set_traded_snapshot_managers")

    def set_quote_snapshot_managers(self):
        raise NotImplementedError("Need to implement set_quote_snapshot_managers")

    def calculate_inject_greeks(self, node: TradeNode | QuoteNode, meta):
        self._underlying_asset: Stock
        if self._volatility_manager is None:
            print("Greek Manager - Volatility manager is None")
            return
        sigma = self._volatility_manager.get_last_trade_iv()
        s = self._underlying_asset.get_last_traded_price()
        k = meta.get("strike") / 1000
        t = calculate_time_to_maturity(
            quote_date=meta.get("date"), expiration_date=meta.get("expiration")
        )
        r = 0.05
        q = 0.0
        right = meta.get("right")
        if sigma is None:
            print("Greek Manager - IV is None")
            return
        d1 = GreekCalculator.calculate_d1(s, k, t, r, q, sigma)
        d2 = GreekCalculator.calculate_d2(d1, sigma, t)
        if self.greek_modes["delta"]:
            self.calculate_inject_delta(node, d1, d2, s, k, t, r, q, sigma, right)
        if self.greek_modes["gamma"]:
            calculate_inject_gamma(node, d1, d2, s, k, t, r, q, sigma, right)
        if self.greek_modes["theta"]:
            self.calculate_inject_theta(node, d1, d2, s, k, t, r, q, sigma, right)
        if self.greek_modes["vega"]:
            self.calculate_inject_vega(node, d1, d2, s, k, t, r, q, sigma, right)
        if self.greek_modes["rho"]:
            self.calculate_inject_rho(node, d1, d2, s, k, t, r, q, sigma, right)

    @staticmethod
    def calculate_inject_delta(
        node: TradeNode | QuoteNode, d1, d2, s, k, t, r, q, sigma, right
    ):
        delta = GreekCalculator.calculate_delta(d1, d2, s, k, t, r, q, sigma, right)
        node.set_delta(delta)

    @staticmethod
    def calculate_inject_theta(
        node: TradeNode | QuoteNode, d1, d2, s, k, t, r, q, sigma, right
    ):
        theta = GreekCalculator.calculate_theta(d1, d2, s, k, t, r, q, sigma, right)
        node.set_theta(theta)
