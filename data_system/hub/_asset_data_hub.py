"""
This collection class contains OptionChainCollection, EquityCollection and IndexCollection (and possibly more in the future)
Each DataSession should contain one MarketDataCollection object. All oject on the MarketDataCollection should be updated
with same Timeline manner.
"""
from typing import Optional

from .middleware import HubTickerFactory
from .middleware.opt_chain_handler import HubOptionChainHandler
from ..utils._id_operations import generate_unique_uuid
from .collections import OptionChainCollectionHub, StockCollectionHub
from ..security_basics import Asset
from ..time_basics import Timeline
from .._enums import *


class AssetDataHub:
    option_domains = [AssetDomain.EQUITY, EquityDomain.OPTION]

    def __init__(self):
        self._id: str = generate_unique_uuid()
        self._option_chain_collection: OptionChainCollectionHub = OptionChainCollectionHub()
        self._equity_collection: StockCollectionHub = StockCollectionHub()
        self._timeline: Optional[Timeline] = None
        self._public_token: str | None = None
        self._private_key: str | None = None
        self._failed_tickers: list[str] = []
        self._connection_errors: list[str] = []

    @property
    def id(self) -> str:
        return self._id

    def get_timeline_id(self) -> str:
        return self._timeline.id

    def set_timeline(self, timeline: Timeline):
        self._timeline = timeline

    def get_timeline(self) -> Timeline:
        if self._timeline is None:
            raise ValueError("Timeline is not set")
        return self._timeline

    def set_time(self, **kwargs):
        """
        Set time of the timeline
        :param kwargs:
            'ms_of_day': int
            'date': int
            'datetime': datetime
        """
        self._timeline.set_time(**kwargs)

    def add_asset(self, asset: Asset):
        domains = set(asset.domains)
        if domains == {AssetDomain.EQUITY, EquityDomain.STOCK}:
            self._equity_collection.add(asset)
        elif domains == {AssetDomain.EQUITY, EquityDomain.OPTION}:
            self._option_chain_collection.add(asset)
        else:
            raise ValueError(f"Asset domains {asset.domains} is not supported")

    def get_assets(self) -> list[Asset]:
        return self._equity_collection.get_assets() + self._option_chain_collection.get_assets()

    @property
    def public_token(self) -> str:
        if self._public_token is None:
            raise ValueError("Public token is not set")
        return self._public_token

    @public_token.setter
    def public_token(self, public_token: str):
        self._public_token = public_token

    @property
    def private_key(self) -> str:
        if self._private_key is None:
            raise ValueError("Key is not set")
        return self._private_key

    @private_key.setter
    def private_key(self, key: str):
        self._private_key = key

    def set_failed_tickers(self, failed_tickers: list[str]):
        self._failed_tickers = failed_tickers

    def get_failed_tickers(self) -> list[str]:
        return self._failed_tickers

    def set_connection_errors(self, errors: list[str]):
        self._connection_errors = errors

    def get_connection_errors(self) -> list[str]:
        return self._connection_errors

    def add_option_chain(self, ticker: str):
        hub_ticker = HubTickerFactory.create_ticker(ticker=ticker, domains=self.option_domains)
        option_chain_list = HubOptionChainHandler.create_option_chain(hub_tic=hub_ticker)
        for option_chain in option_chain_list:
            self._option_chain_collection.add(option_chain)

    def has_token_key(self):
        return self._public_token is not None and self._private_key is not None
