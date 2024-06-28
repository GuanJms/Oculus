"""
Volatility Manager manages the volatility domain information for an asset including:
implied volatility, historical volatility, and other volatility metrics. It is a part of the Asset class.
"""

from typing import Optional, TYPE_CHECKING

from data_system.base_structure.nodes import TradeNode, QuoteNode, VolNode
from data_system.domain_managers.domain_manager import DomainManager
from data_system.utils.frequency_limiter import FrequencyLimiter

if TYPE_CHECKING:
    from data_system.security_basics._asset import Asset

from data_system._enums import VolatilityDomain, PriceDomain
from data_system.containers.container_managers import SnapshotManager
from data_system.utils.domain_operations import parse_domain
from data_system.utils.time_operations import calculate_time_to_maturity
from data_system.base_structure.factory import VolatilityNodeFactory

from calculators import ImpliedVolatilityCalculator


# TODO: Refactor this class with PriceManager


class VolatilityManager(DomainManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._underlying_asset: Optional["Asset"] = kwargs.get("underlying_asset", None)
        self._running_snapshot = False
        self._quote_snapshot_manager = SnapshotManager(
            domains=self._domains + [PriceDomain.QUOTE, VolatilityDomain.IMPLIED]
        )
        self._trade_snapshot_manager = SnapshotManager(
            domains=self._domains + [PriceDomain.TRADED, VolatilityDomain.IMPLIED]
        )
        self._live_iv_mode = kwargs.get("live_iv_mode", False)
        self._frequency_limiter: FrequencyLimiter = FrequencyLimiter()
        self.run_live_snapshot(size=1)

    def inject(self, node, meta: dict = None):
        if self._live_iv_mode:
            self.calculate_inject_iv(node, meta)

    def calculate_inject_iv(self, node: TradeNode | QuoteNode, meta: dict = None):
        if self._underlying_asset.get_last_traded_price() is None:
            return
        if self._frequency_limiter.is_limited(
            self.calculate_inject_iv.__name__, timestamp=node.get_timestamp()
        ):
            return
        else:
            self._frequency_limiter.update(
                self.calculate_inject_iv.__name__, timestamp=node.get_timestamp()
            )
        vol_node = self.iv_process(node, meta)
        if vol_node is None:
            # if meta.get("right") == "C":
            #     intrinsic = self._underlying_asset.get_last_traded_price() - meta.get("strike")/1000
            #     if intrinsic >= (node.get_price() + 0.02):
            #         print("Intrinsic value is higher than market price -- Arbitrage opportunity", intrinsic, node.get_price(), "Size: ", node.size, "Strike: ", meta.get("strike")/1000)
            #     else:
            #         print("Failed to calculate IV for node: ", node, "Meta: ", meta, "Underlying price: ", self._underlying_asset.get_last_traded_price(), "Last IV: ", self.get_last_trade_iv())
            # else:
            #     intrinsic = meta.get("strike")/1000 - self._underlying_asset.get_last_traded_price()
            #     if intrinsic >= (node.get_price() + 0.02):
            #         print("Intrinsic value is higher than market price -- Arbitrage opportunity", intrinsic, node.get_price(), "Size: ", node.size, "Strike: ", meta.get("strike")/1000)
            #     else:
            #         print("Failed to calculate IV for node: ", node, "Meta: ", meta, "Underlying price: ", self._underlying_asset.get_last_traded_price(), "Last IV: ", self.get_last_trade_iv())
            #
            # print("Different timestamps: ", node.get_timestamp() - self._underlying_asset._price_manager._trade_snapshot_manager.get_snapshot()[0].timestamp)
            return
        vol_domains = meta.get("domains", []) + [VolatilityDomain.IMPLIED]
        meta["domains"] = vol_domains
        if self._running_snapshot:
            self.inject_snapshot(vol_node, meta)

    def inject_snapshot(self, node, meta: dict = None):
        domains = parse_domain(meta.get("domains", []))
        if PriceDomain.QUOTE in domains:
            self._quote_snapshot_manager.inject(node, meta)
        if PriceDomain.TRADED in domains:
            self._trade_snapshot_manager.inject(node, meta)

    def run_live_snapshot(self, size=1):
        # Feature that capture one snapshot
        self._quote_snapshot_manager.run_live_snapshot(size)
        self._trade_snapshot_manager.run_live_snapshot(size)
        self._running_snapshot = True

    def _calculate_implied_volatility(
        self, node: TradeNode | QuoteNode, meta: dict = None, add_to_node=True
    ):
        s = self._underlying_asset.get_last_traded_price()
        k = meta.get("strike") / 1000
        t = calculate_time_to_maturity(
            quote_date=meta.get("date"), expiration_date=meta.get("expiration")
        )
        r = 0.05
        q = 0.0
        market_price = node.get_price()
        right = meta.get("right")
        iv = ImpliedVolatilityCalculator.calculate_iv(
            s, k, t, r, q, market_price, right, iv_guess=self.get_last_trade_iv()
        )
        if iv is None or iv < 0.0001:
            return None
        if add_to_node:
            node.set_iv(iv)
        # print(f"VolatilityManager calculate_implied_volatility - meta: {meta}")
        # print(f"VolatilityManager calculate_implied_volatility - data: {node}")
        # print(f"VolatilityManager - Underlying asset: {self._underlying_asset}")
        # print(f"VolatilityManager calculate_implied_volatility - s: {s}")
        # print(f"VolatilityManager calculate_implied_volatility - k: {k}")
        # print(f"VolatilityManager calculate_implied_volatility - t: {t}")
        # print(f"VolatilityManager calculate_implied_volatility - r: {r}")
        # print(f"VolatilityManager calculate_implied_volatility - q: {q}")
        # print(f"VolatilityManager calculate_implied_volatility - market_price: {market_price}")
        # print(f"VolatilityManager calculate_implied_volatility - right: {right}")
        # print(f"VolatilityManager calculate_implied_volatility - iv: {iv}")
        return iv

    def iv_process(
        self, node: TradeNode | QuoteNode, meta, add_to_node=True
    ) -> VolNode:
        sigma = self._calculate_implied_volatility(node, meta, add_to_node=add_to_node)
        if sigma is None:
            return None
        params = {
            "vol_domain": meta.get("domains", []) + [VolatilityDomain.IMPLIED],
        }
        node = VolatilityNodeFactory.create_volatility_node(
            sigma, timestamp=node.get("timestamp"), params=params
        )
        return node

    def get_last_trade_iv(self):
        nodes = self._trade_snapshot_manager.get_snapshot()
        if nodes:
            return nodes[0].get_value()
        return None

    def get_last_quote_iv(self):
        raise NotImplementedError

    def get_last_trade_vol_node(self):
        nodes = self._trade_snapshot_manager.get_snapshot()
        if nodes:
            return nodes[0]
        return None

    def set_live_iv_mode(self, on_off: bool):
        self._live_iv_mode = on_off
