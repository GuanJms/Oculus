from typing import List

from data_system._enums import *
from data_system.security_basics import Stock
from data_system.security_basics.option_basics import OptionChain
from data_system.security_basics.option_basics.core import Option


class TradeFlowData:
    def __init__(self, asset_data_hub):
        self.asset_data_hub = asset_data_hub
        self.assets = {}  # {ticker: Stock}
        self.traded_asset_time_queues = {}  # {ticker: {time_frame: QueueManager}}
        self.quote_asset_time_queues = {}  # {ticker: {time_frame: QueueManager}}

    def _request_lag_flow(
            self,
            ticker: str,
            time_frame: int,
            time_unit: TimeUnit | str,
            has_lag,
            lag: int,
            domains: List[DomainEnum],
    ):
        time_unit = TimeUnit.get(time_unit)
        if time_unit != TimeUnit.SECOND:
            raise Exception("Only second time unit is supported")
        flow_key = (time_frame, lag)
        if AssetDomain.EQUITY in domains:
            if EquityDomain.STOCK in domains:
                # Check if the asset is already in the system and create if not
                if ticker not in self.traded_asset_time_queues:
                    self.traded_asset_time_queues[ticker] = {}
                if ticker not in self.quote_asset_time_queues:
                    self.quote_asset_time_queues[ticker] = {}
                if ticker not in self.assets:
                    self.assets[ticker] = self.asset_data_hub.get_stock(ticker)

                stock: Stock = self.assets[ticker]
                # TODO: NO VOLATILITY DOMAIN IS IMPLEMENTED
                if PriceDomain.TRADED in domains:
                    stock.add_lag_tracker(time_frame, time_unit, lag, has_lag)
                    traded_price_tracker = stock.get_lag_tracker(
                        time_frame, lag, time_unit, domains=domains
                    )
                    self.traded_asset_time_queues[ticker][
                        flow_key
                    ] = traded_price_tracker
                if PriceDomain.QUOTE in domains:
                    stock.add_lag_tracker(time_frame, time_unit, lag, has_lag)
                    quote_price_tracker = stock.get_lag_tracker(
                        time_frame, lag, time_unit, domains=domains
                    )
                    self.quote_asset_time_queues[ticker][flow_key] = quote_price_tracker

    def get_lag_tracker(self, ticker, domains, time_frame, time_unit, lag):
        has_lag = False
        if lag:
            has_lag = True
        if EquityDomain.STOCK in domains:
            if ticker not in self.assets:
                self._request_lag_flow(ticker, time_frame, time_unit, has_lag, lag, domains)
            flow_key = (time_frame, lag)
            if PriceDomain.TRADED in domains:
                if flow_key not in self.traded_asset_time_queues[ticker]:
                    self._request_lag_flow(ticker, time_frame, time_unit, has_lag, lag, domains)
                return self.traded_asset_time_queues[ticker][flow_key]
            if PriceDomain.QUOTE in domains:
                if flow_key not in self.quote_asset_time_queues[ticker]:
                    self._request_lag_flow(ticker, time_frame, time_unit, has_lag, lag, domains)
                return self.quote_asset_time_queues[ticker][flow_key]
        raise ValueError(f"Unknown domain {domains}")

    def get_option_chain(self, ticker: str, expiration: int):
        option_chain: OptionChain = self.asset_data_hub.get_option_chain(ticker, expiration)
        if option_chain is None:
            print(f"Option chain for {ticker} with expiration {expiration} not found")
            return None
        return option_chain
