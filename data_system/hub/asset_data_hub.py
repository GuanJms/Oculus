"""
This collection class contains OptionChainCollection, EquityCollection and IndexCollection (and possibly more in the future)
Each DataSession should contain one MarketDataCollection object. All oject on the MarketDataCollection should be updated
with same Timeline manner.
"""
import threading
from typing import Optional, List

from .middleware import HubTickerFactory
from ..utils.domain_operations import parse_domain
from ..utils.id_operations import generate_unique_uuid
from .collections import OptionChainCollectionHub, StockCollectionHub
from ..security_basics import Asset
from ..time_basics import Timeline
from .._enums import *
from .instrument_finder import InstrumentFinder
from .hub_lock import HubLock


class AssetDataHub:
    _option_chain_collection_hub: OptionChainCollectionHub
    _stock_collection_hub: StockCollectionHub
    option_domains = [AssetDomain.EQUITY, EquityDomain.OPTION]

    _instance = None

    def __new__(cls, **kwargs):
        if cls._instance is None:
            hublock = HubLock()
            with hublock.get_lock():
                if cls._instance is None:
                    cls._instance = super(AssetDataHub, cls).__new__(cls)
                    cls._instance.__init__(**kwargs)
        return cls._instance

    def __init__(self, **kwargs):
        self._live_iv_mode: bool = kwargs.get("live_iv_mode", False)
        self._live_greek_mode: bool = kwargs.get("live_greek_mode", False)
        self._id: str = generate_unique_uuid()
        self._option_chain_collection_hub: OptionChainCollectionHub = (
            OptionChainCollectionHub(live_iv_mode=self._live_iv_mode,
                                     live_greek_mode=self._live_greek_mode)
        )
        self._stock_collection_hub: StockCollectionHub = StockCollectionHub()
        self._timeline: Optional[Timeline] = None
        self._public_token: str | None = None
        self._private_key: str | None = None
        self._failed_tickers: list[str] = []
        self._connection_errors: list[str] = []

        # initialize instrument finder
        self._instrument_finder = InstrumentFinder()
        self._instrument_finder.add_hub(self._option_chain_collection_hub)
        self._instrument_finder.add_hub(self._stock_collection_hub)

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
            self._stock_collection_hub.add_asset(asset)
        elif domains == {AssetDomain.EQUITY, EquityDomain.OPTION}:
            self._option_chain_collection_hub.add_asset(asset)
        else:
            raise ValueError(f"Asset domains {asset.domains} is not supported")

    def get_assets(self) -> list[Asset]:
        return (
            self._stock_collection_hub.get_assets()
            + self._option_chain_collection_hub.get_assets()
        )

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

    def has_token_key(self):
        return self._public_token is not None and self._private_key is not None

    def inject(self, data, meta: dict[str, any] = None):
        if meta is None:
            print("Meta not found")
            return
        if len(meta) == 0:
            return
        domains = parse_domain(meta.get("domains", []))
        if EquityDomain.STOCK in domains:
            collection = self._stock_collection_hub
        elif EquityDomain.OPTION in domains:
            collection = self._option_chain_collection_hub
        else:
            raise ValueError("Unsupported domain")
        collection.inject(
            data, meta=meta
        )  # type: StockCollectionHub | OptionChainCollectionHub

    def get_asset(self, meta):
        # Find the corresponding asset with meta data (which should contain contract details)
        # If the asset is not found, the collection hub will construct for it and return the asset
        if any(map(lambda x: x not in meta, ["ticker", "domains"])):
            raise ValueError("Meta data is missing crucial information")
        ticker = meta.get("ticker")
        domains = parse_domain(meta.get("domains"))
        if EquityDomain.STOCK in domains:
            return self._stock_collection_hub.get_stock(ticker)
        elif EquityDomain.OPTION in domains:
            if any(map(lambda x: x not in meta, ["expiration", "strike", "right"])):
                raise ValueError("Option meta data is missing crucial information")
            expiration = meta.get("expiration")
            strike = meta.get("strike")
            right = meta.get("right")
            return self._option_chain_collection_hub.get_option(
                ticker=ticker, expiration=expiration, strike=strike, right=right
            )

        else:
            raise ValueError("Unsupported domain")

    def run_live_snapshot(self):
        self._stock_collection_hub.run_live_snapshot()  # type: StockCollectionHub
        self._option_chain_collection_hub.run_live_snapshot()

    def set_live_mode(self, params):
        # params should contain 'live_iv_mode' key
        if "live_iv_mode" in params:
            self._live_iv_mode = params.get("live_iv_mode")

    # def add_option_chain(self, ticker: str):
    #     from .middleware.opt_chain_handler import HubOptionChainHandler
    #     hub_ticker = HubTickerFactory.create_ticker(
    #         ticker=ticker, domains=self.option_domains
    #     )
    #     option_chain_list = HubOptionChainHandler.create_option_chain(
    #         hub_tic=hub_ticker
    #     )
    #     for option_chain in option_chain_list:
    #         self._option_chain_collection_hub.add_asset(option_chain)

    def get_option_chain(self, ticker: str, expiration: int):
        return self._option_chain_collection_hub.get_option_chain(
            ticker, expiration
        )  # type: OptionChainCollectionHub

    def get_stock(self, ticker):
        return self._stock_collection_hub.get_stock(ticker)
