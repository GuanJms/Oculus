"""
PriceManager should many ContainerManagers, one for each price domain: Quote and Trade.
"""
from data_system._enums import PriceDomain, TimeUnit
from data_system.base_structure.nodes.trade_node import TradeNode
from data_system.containers.container_managers import SnapshotManager
from data_system.containers.container_managers.time_lag_queue_manager import (
    TimeLagQueueManager,
)
from data_system.domain_managers.domain_manager import DomainManager
from data_system.utils.domain_operations import parse_domain


class PriceManager(DomainManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._running_snapshot = False
        self._traded_time_lag_queue_manager = TimeLagQueueManager(
            domains=self._domains + [PriceDomain.TRADED]
        )
        self._quote_time_lag_queue_manager = TimeLagQueueManager(
            domains=self._domains + [PriceDomain.QUOTE]
        )
        self._quote_snapshot_manager = SnapshotManager(
            domains=self._domains + [PriceDomain.QUOTE]
        )
        self._trade_snapshot_manager = SnapshotManager(
            domains=self._domains + [PriceDomain.TRADED]
        )
        self._underlying_asset = kwargs.get("underlying_asset", None)
        self.run_live_snapshot(size=1)

    @property
    def quote_snapshot_manager(self) -> SnapshotManager:
        return self._quote_snapshot_manager

    @property
    def trade_snapshot_manager(self) -> SnapshotManager:
        return self._trade_snapshot_manager

    def run_live_snapshot(self, size=1):
        # Feature that capture one snapshot
        self._quote_snapshot_manager.run_live_snapshot(
            size, domains=self._domains + [PriceDomain.QUOTE]
        )
        self._trade_snapshot_manager.run_live_snapshot(
            size, domains=self._domains + [PriceDomain.TRADED]
        )
        self._running_snapshot = True

    def inject(self, node, domains: list = None, meta: dict = None):
        self._inject_time_lag_queue(node, domains, meta)
        if self._running_snapshot:
            self._inject_snapshot(node, domains, meta)

    def _inject_time_lag_queue(self, node, domains: list, meta: dict):

        if domains is None:
            domains = parse_domain(meta.get("domains", []))
            print("Error in PriceManager - domains from injection is None")

        if PriceDomain.QUOTE in domains:
            self._quote_time_lag_queue_manager.inject(node, domains, meta)
        elif PriceDomain.TRADED in domains:
            self._traded_time_lag_queue_manager.inject(node, domains, meta)
        else:
            print(f"Domain not found in PriceManager: {domains}")

    def _inject_snapshot(self, node, domains, meta: dict):
        if PriceDomain.QUOTE in domains:
            self._quote_snapshot_manager.inject(node, domains, meta)
        if PriceDomain.TRADED in domains:
            self._trade_snapshot_manager.inject(node, domains, meta)

    def add_lag_tracker(
        self,
        time_frame: int,
        time_unit: TimeUnit | str,
        lag=0,
        has_lag=False,
    ):
        self._quote_time_lag_queue_manager.add_lag_tracker(
            time_frame, time_unit, lag, has_lag
        )
        self._traded_time_lag_queue_manager.add_lag_tracker(
            time_frame, time_unit, lag, has_lag
        )

    def get_lag_tracker(
        self,
        time_frame: int,
        domains: list,
        lag: int,
        time_unit: TimeUnit | str,
    ):
        time_unit = TimeUnit.get(time_unit)  # Convert string to enum if necessary
        if time_unit != TimeUnit.SECOND:
            raise Exception("Only second time unit is supported for now")
        if PriceDomain.QUOTE in domains:
            return self._quote_time_lag_queue_manager.get_lag_tracker(time_frame, lag)
        if PriceDomain.TRADED in domains:
            return self._traded_time_lag_queue_manager.get_lag_tracker(time_frame, lag)
        print(
            f"Lag tracker time frame: {time_frame}, lag: {lag}, domains: {domains} not found in PriceManager."
        )
        return None

    def get_snapshot(self, domain=None):
        if domain is None:
            return {
                PriceDomain.QUOTE: self._quote_snapshot_manager.get_snapshot(),
                PriceDomain.TRADED: self._trade_snapshot_manager.get_snapshot(),
            }
        if domain == PriceDomain.QUOTE:
            return self._quote_snapshot_manager.get_snapshot()
        if domain == PriceDomain.TRADED:
            return self._trade_snapshot_manager.get_snapshot()
        return None

    def get_last_quote_price(self):
        nodes = self._quote_snapshot_manager.get_snapshot()
        if len(nodes) == 0:
            return None
        node: TradeNode = self._quote_snapshot_manager.get_snapshot()[0]
        raise NotImplementedError("Untested code")
        return node.get_price()

    def get_last_traded_price(self):
        nodes = self._trade_snapshot_manager.get_snapshot()
        if len(nodes) == 0:
            return None
        node: TradeNode = self._trade_snapshot_manager.get_snapshot()[0]
        return node.get_price()

    # def set_live_mode(self, params):
    #     pass
