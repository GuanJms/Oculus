from typing import Optional, Dict, List

import numpy as np

from calculators.greek_calculator import GreekCalculator
from data_system._enums import (
    PriceDomain,
    GreekDomain,
    OptionDomain,
    ModelDomain,
    DomainEnum,
    TimeUnit,
)
from data_system.base_structure.factory import GreekNodeFactory
from data_system.base_structure.nodes import TradeNode, QuoteNode
from data_system.base_structure.nodes.greek_node import GreekNode
from data_system.containers.container_managers import (
    TimeLagQueueManager,
    SnapshotManager,
)
from data_system.domain_managers.domain_manager import DomainManager
from data_system.domain_managers.volatility_manager import VolatilityManager
from data_system.utils.domain_operations import fetch_domain
from data_system.utils.time_operations import calculate_time_to_maturity


class GreekManager(DomainManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from data_system.security_basics import Stock

        self.greek_modes: Dict[GreekDomain, bool] = {
            key: False for key in GreekDomain
        }  # TODO: modify the greek_modes such that it is a dictionary of ModelDomain of GreekDomain and boolean

        self.model_modes: Dict[ModelDomain, bool] = {key: False for key in ModelDomain}

        self._traded_time_lag_queue_managers: Dict[
            ModelDomain, TimeLagQueueManager
        ] = {}
        self._quote_time_lag_queue_managers: Dict[ModelDomain, TimeLagQueueManager] = {}
        self._traded_snapshot_managers: Dict[ModelDomain, SnapshotManager] = {}
        self._quote_snapshot_managers: Dict[ModelDomain, SnapshotManager] = {}

        self.set_greek_mode(kwargs.get("greek_modes", {}))
        self.set_model_modes(kwargs.get("model_modes", {}))

        self._option_type: Optional[OptionDomain] = kwargs.get("option_type", None)
        self._running_snapshot = kwargs.get("running_snapshot", False)
        self._live_greek_mode = kwargs.get("live_greek_mode", False)
        self._underlying_asset: Optional[Stock] = kwargs.get("underlying_asset", None)
        self._volatility_manager: Optional[VolatilityManager] = kwargs.get(
            "volatility_manager", None
        )

        self._size_limiter = None  # TODO: implement size limiter like frequency limiter

        self.set_lag_managers()
        if self._running_snapshot:
            self.set_snapshot_managers()

        self.run_live_snapshot(size=1)

    def inject(self, node, domains: list = None, meta: dict = None):
        if not any(self.model_modes.values()):
            print("Greek Manager - No model mode is set to True")
            return
        if self._live_greek_mode:
            # Check if any of the model modes are True
            self.calculate_inject_greeks(node, domains, meta)

    def delete_print(self):
        print(f"Greek Manager - Delete the function - {self._traded_snapshot_managers}")

    def set_volatility_manager(self, volatility_manager: VolatilityManager):
        if volatility_manager is None:
            print("Greek Manager - Volatility manager is trying with None")
            return
        self._volatility_manager = volatility_manager

    def run_live_snapshot(self, size=1):
        # Feature that capture one snapshot
        if not self._running_snapshot:
            self._running_snapshot = True
            self.set_traded_snapshot_managers()
            self.set_quote_snapshot_managers()

        for model in ModelDomain:
            if self.model_modes[model]:
                self._traded_snapshot_managers[model].run_live_snapshot(size)
                self._quote_snapshot_managers[model].run_live_snapshot(size)

    def set_greek_mode(self, setting_mode: Dict[GreekDomain, bool]):
        for key, value in setting_mode.items():
            if key in self.greek_modes:
                self.greek_modes[key] = value

    def set_model_modes(self, model_modes: Dict[ModelDomain, bool]):
        for key, value in model_modes.items():
            if key in self.model_modes:
                self.model_modes[key] = value
        self.set_lag_managers()

    def set_lag_managers(self):
        self.set_traded_time_lag_queue_managers()
        self.set_quote_time_lag_queue_managers()

    def set_traded_time_lag_queue_managers(self):
        for model in ModelDomain:
            if (
                self.model_modes[model]
                and model not in self._traded_time_lag_queue_managers
            ):
                self._traded_time_lag_queue_managers[model] = TimeLagQueueManager(
                    domains=self._domains + [PriceDomain.TRADED, model]
                )

    def set_quote_time_lag_queue_managers(self):
        for model in ModelDomain:
            if (
                self.model_modes[model]
                and model not in self._quote_time_lag_queue_managers
            ):
                self._quote_time_lag_queue_managers[model] = TimeLagQueueManager(
                    domains=self._domains + [PriceDomain.QUOTE, model]
                )

    def set_traded_snapshot_managers(self):
        for model in ModelDomain:
            if self.model_modes[model] and model not in self._traded_snapshot_managers:
                self._traded_snapshot_managers[model] = SnapshotManager(
                    domains=self._domains + [PriceDomain.TRADED, model]
                )

    def set_quote_snapshot_managers(self):
        for model in ModelDomain:
            if (
                self.model_modes[model] and model not in self._quote_snapshot_managers
            ):  # TODO: refactor all four set functions into one function
                self._quote_snapshot_managers[model] = SnapshotManager(
                    domains=self._domains + [PriceDomain.QUOTE, model]
                )

    def calculate_inject_greeks(
        self, node: TradeNode | QuoteNode, domains: list, meta: dict
    ):
        # TODO: add timestamp adjustment to time to maturity
        if self._volatility_manager is None:
            print("Greek Manager - Volatility manager is None")
            return

        k = meta.get("strike") / 1000
        t = calculate_time_to_maturity(
            quote_date=meta.get("date"), expiration_date=meta.get("expiration")
        )
        if self.model_modes[ModelDomain.BLACK_SCHOLES]:
            self._calculate_inject_greeks_black_scholes(node, domains, k, t)

        if self.model_modes[ModelDomain.HESTON]:
            self._calculate_inject_greeks_heston(node, domains, k, t)

    def _calculate_inject_greeks_black_scholes(
        self, node: TradeNode | QuoteNode, domains: List[DomainEnum], k, t
    ):  # k is strike price, t is time to maturity
        model = ModelDomain.BLACK_SCHOLES
        domains = domains.copy() + [model]
        sigma = self._volatility_manager.get_last_trade_iv()
        s = self._underlying_asset.get_last_traded_price()
        r = 0.05
        q = 0.0
        right: OptionDomain = self._option_type
        if sigma is None:
            return
        d1 = GreekCalculator.calculate_d1(s, k, t, r, q, sigma)
        d2 = GreekCalculator.calculate_d2(d1, sigma, t)
        greek_values = self.calculate_greeks(node, s, k, t, r, q, sigma, right, d1, d2)
        greek_node = self.greeks_process(node, greek_values, domains, model)
        self._inject_model_greeks(greek_node, domains, model)

    def _inject_model_greeks(
        self, node: GreekNode, domains: List[DomainEnum], model_domain: ModelDomain
    ):
        if node is None:
            return
        if PriceDomain.TRADED in domains:
            self._traded_time_lag_queue_managers[model_domain].inject(node, domains)
        elif PriceDomain.QUOTE in domains:
            self._quote_time_lag_queue_managers[model_domain].inject(node, domains)
        else:
            print(
                f"Error in Greek Manager - _inject_model_greeks - {domains} - {node}- {model_domain}"
            )
        if self._running_snapshot:
            self._inject_snapshot(node, domains, model_domain)

    def _inject_snapshot(
        self,
        node: GreekNode,
        domains: List[DomainEnum],
        model_domain: ModelDomain,
    ):
        if PriceDomain.QUOTE in domains:
            self._quote_snapshot_managers[model_domain].inject(node, domains)
        elif PriceDomain.TRADED in domains:
            self._traded_snapshot_managers[model_domain].inject(node, domains)
            _snapshot_manager: SnapshotManager = self._traded_snapshot_managers[
                model_domain
            ]
        else:
            print(f"Domain not found in GreekManager: {domains}")

    def add_lag_tracker(
        self,
        time_frame: int,
        time_unit: TimeUnit | str,
        model_domain: ModelDomain,
        lag=0,
        has_lag=False,
    ):
        if model_domain is None:
            print("Greek Manager - Model Domain is None.")
            return

        if model_domain not in self.model_modes or not self.model_modes[model_domain]:
            print("Greek Manager - Model Domain is not set to True.")
            return

        self._quote_time_lag_queue_managers[model_domain].add_lag_tracker(
            time_frame, time_unit, lag, has_lag
        )
        self._traded_time_lag_queue_managers[model_domain].add_lag_tracker(
            time_frame, time_unit, lag, has_lag
        )

    # TODO: Refactor this function with same function in PriceManager such that there is no redundant code in both
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
        try:
            model_domain = fetch_domain(ModelDomain, domains)
        except ValueError:
            print("Getting lag tracker - Model Domain not found in domains.")
            return None

        if model_domain not in self.model_modes or not self.model_modes[model_domain]:
            print("Getting lag tracker - Model Domain is not set to True.")
            return None

        if PriceDomain.QUOTE in domains:
            return self._quote_time_lag_queue_managers[model_domain].get_lag_tracker(
                time_frame, lag
            )
        if PriceDomain.TRADED in domains:
            return self._traded_time_lag_queue_managers[model_domain].get_lag_tracker(
                time_frame, lag
            )
        print(
            f"Lag tracker time frame: {time_frame}, lag: {lag}, domains: {domains} not found in GreekManager."
        )
        return None

    @staticmethod
    def calculate_delta(
        node: TradeNode | QuoteNode,
        s,
        k,
        t,
        r,
        q,
        sigma,
        right: OptionDomain,
        d1=None,
    ):
        delta = GreekCalculator.calculate_delta(s, k, t, r, q, sigma, right, d1=d1)

        if delta:
            node.set_delta(delta)

        return delta

    @staticmethod
    def calculate_gamma(node, s, k, t, r, q, sigma, d1=None):
        gamma = GreekCalculator.calculate_gamma(s, k, t, r, q, sigma, d1=d1)
        node.set_gamma(gamma)
        return gamma

    @staticmethod
    def calculate_vega(node, s, k, t, r, q, sigma, right, d1=None, d2=None):
        vega = GreekCalculator.calculate_vega(s, k, t, r, q, sigma, d1=d1)
        node.set_vega(vega)
        return vega

    @staticmethod
    def calculate_theta(
        node: TradeNode | QuoteNode,
        s,
        k,
        t,
        r,
        q,
        sigma,
        right: OptionDomain,
        d1=None,
        d2=None,
    ):
        theta = GreekCalculator.calculate_theta(
            s, k, t, r, q, sigma, right, d1=d1, d2=d2
        )
        node.set_theta(theta)
        return theta

    @staticmethod
    def calculate_rho(
        node: TradeNode | QuoteNode, s, k, t, r, q, sigma, right, d1=None, d2=None
    ):
        raise NotImplementedError("Need to implement calculate_inject_rho")

    @staticmethod
    def calculate_vomma(
        node: TradeNode | QuoteNode, s, k, t, r, q, sigma, d1=None, d2=None
    ):
        vomma = GreekCalculator.calculate_vomma(s, k, t, r, q, sigma, d1, d2)
        node.set_vomma(vomma)
        return vomma

    def calculate_greeks(self, node, s, k, t, r, q, sigma, right, d1, d2) -> dict:
        greek_values = {}
        if self.greek_modes[GreekDomain.DELTA]:
            greek_values[GreekDomain.DELTA] = self.calculate_delta(
                node, s, k, t, r, q, sigma, right, d1=d1
            )
        if self.greek_modes[GreekDomain.GAMMA]:
            greek_values[GreekDomain.GAMMA] = self.calculate_gamma(
                node, s, k, t, r, q, sigma, d1=d1
            )
        if self.greek_modes[GreekDomain.VEGA]:
            greek_values[GreekDomain.VEGA] = self.calculate_vega(
                node, s, k, t, r, q, sigma, right, d1=d1, d2=d2
            )
        if self.greek_modes[GreekDomain.THETA]:
            greek_values[GreekDomain.THETA] = self.calculate_theta(
                node, s, k, t, r, q, sigma, right, d1=d1, d2=d2
            )
        if self.greek_modes[GreekDomain.VOMMA]:
            greek_values[GreekDomain.VOMMA] = self.calculate_vomma(
                node, s, k, t, r, q, sigma, d1=d1, d2=d2
            )
        if self.greek_modes[GreekDomain.RHO]:
            greek_values[GreekDomain.RHO] = self.calculate_rho(
                node, s, k, t, r, q, sigma, right
            )
        return greek_values

    @staticmethod
    def greeks_process(
        node: TradeNode | QuoteNode,
        greek_values: Dict[GreekDomain, float | np.float32 | np.float64],
        domains: List[DomainEnum],
        model_domain: ModelDomain,
    ) -> GreekNode | None:
        """
        Process the dictionary of greek values and create a GreekNode object
        :param node: TradeNode or QuoteNode
        :param greek_values: dictionary of greek values
        :param domains: list of domains that includes the ModelDomain
        :param model_domain: ModelDomain
        :return: GreekNode
        """
        if not any(greek_values.values()):
            return None
        greek_node = GreekNodeFactory.create_greek_node(
            greek_values,
            node,
            timestamp=node.get("timestamp"),
            domains=domains,
            model_domain=model_domain,
        )
        return greek_node

    def _calculate_inject_greeks_heston(self, node, k, t):
        raise NotImplementedError("Need to implement _calculate_inject_greeks_heston")

    def set_snapshot_managers(self):
        self.set_traded_snapshot_managers()
        self.set_quote_snapshot_managers()
