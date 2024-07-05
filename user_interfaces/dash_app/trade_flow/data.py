from typing import List, Tuple, Dict

from data_system._enums import *
from data_system.containers.cores import QueueManager
from data_system.hub import AssetDataHub
from data_system.security_basics import Stock, Asset
from data_system.security_basics.option_basics import OptionChain
from data_system.security_basics.option_basics.core import Option
from data_system.utils import DomainMatcher
from data_system.utils.domain_operations import parse_domain, fetch_domain, domain_to_chains


class TradeFlowData:
    def __init__(self, asset_data_hub):
        self.asset_data_hub: AssetDataHub = asset_data_hub
        self.assets = []  # {ticker: Stock}
        # self.traded_asset_time_queues = {}  # {ticker: {time_frame: QueueManager}}
        # self.quote_asset_time_queues = {}  # {ticker: {time_frame: QueueManager}}
        self.asset_time_queues: Dict[Asset, Dict[tuple, QueueManager]] = {}

    def _request_lag_flow(
            self,
            ticker: str,
            time_frame: int,
            time_unit: TimeUnit | str,
            has_lag,
            lag: int,
            domains: List[DomainEnum],
            **kwargs,
    ):
        time_unit = TimeUnit.get(time_unit)
        if time_unit != TimeUnit.SECOND:
            raise Exception("Only second time unit is supported")

        asset = self.get_asset(ticker, domains, **kwargs)
        if asset is None:
            return None
        flow_key = self._get_flow_key(time_frame, lag, domains)

        if flow_key in self.asset_time_queues[asset]:
            print(f"Flow key {flow_key} already exists in asset time queues")
            return

        if isinstance(asset, Stock):
            asset.add_lag_tracker(time_frame, time_unit, PriceDomain, lag, has_lag)
            price_tracker = asset.get_lag_tracker(
                time_frame, lag, time_unit, domains=domains, domain_type=PriceDomain
            )
            self.asset_time_queues[asset][flow_key] = price_tracker

        if isinstance(asset, Option):
            if OptionDomain.GREEK in domains:
                asset: Option
                model_domain = fetch_domain(ModelDomain, domains)
                asset.add_lag_tracker(time_frame, time_unit, OptionDomain.GREEK, lag, has_lag,
                                      model_domain=model_domain)
                greek_tracker = asset.get_lag_tracker(
                    time_frame, lag, time_unit, domains=domains ,domain_type=OptionDomain.GREEK
                )
                self.asset_time_queues[asset][flow_key] = greek_tracker

    def get_lag_tracker(self, ticker, domains, time_frame, time_unit, lag, **kwargs):
        time_unit = TimeUnit.get(time_unit)
        if time_unit != TimeUnit.SECOND:
            raise Exception("Only second time unit is supported for now")

        has_lag = True if lag else False
        flow_key = self._get_flow_key(time_frame, lag, domains)
        asset = self.get_asset(ticker, domains, **kwargs)
        _queues = self.asset_time_queues[asset]
        if flow_key not in _queues:
            self._request_lag_flow(
                ticker, time_frame, time_unit, has_lag, lag, domains, **kwargs
            )
        return _queues[flow_key]

    def get_option_chain(self, ticker: str, expiration: int):
        option_chain: OptionChain = self.asset_data_hub.get_option_chain(
            ticker, expiration
        )
        if option_chain is None:
            print(f"Option chain for {ticker} with expiration {expiration} not found")
            return None
        return option_chain

    @staticmethod
    def _get_flow_key(time_frame: int, lag: int, domains: List[DomainEnum]):
        domains_str = domain_to_chains(domains)
        flow_key = (time_frame, lag, domains_str)
        return flow_key

    def get_asset(self, ticker, domains, **kwargs):
        domains = parse_domain(
            domains,
            asset_domain=True,
            equity_domain=True,
            price_domain=False,
        )
        domains = [domain for domain in domains if type(domain) in [EquityDomain, AssetDomain]]
        asset_type = DomainMatcher.match_domain_asset(domains)
        if asset_type is Stock:
            stock = self.asset_data_hub.get_stock(ticker)
            self.__register_asset(stock)
            return stock
        if asset_type is Option:
            expiration = kwargs.get("expiration")
            strike = kwargs.get("strike")
            right = kwargs.get("right")
            option = self.asset_data_hub.get_option(ticker, expiration, strike, right)
            self.__register_asset(option)
            return option

    def __register_asset(self, asset):
        if asset is None:
            return
        if asset not in self.assets:
            self.assets.append(asset)
        if asset not in self.asset_time_queues:
            self.asset_time_queues[asset] = {}
