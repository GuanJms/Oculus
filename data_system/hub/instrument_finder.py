"""
This class is for finding entities in the data system. The entity can be an asset or a collection of assets.
"""
import threading
from typing import List, Dict

from data_system._enums import (
    SingleAssetType,
    MultiAssetType,
    DomainEnum,
    EquityDomain,
    AssetDomain,
)
from data_system.hub.hub_lock import HubLock

from data_system.utils.domain_operations import parse_domain, fetch_domain

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data_system.hub.collections.asset_collection_hub import AssetCollectionHub


class InstrumentFinder:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            hublock = HubLock()
            with hublock.get_lock():
                if not cls._instance:
                    cls._instance = super(InstrumentFinder, cls).__new__(cls)
                    if kwargs.get("hubs", None):
                        for hub in kwargs["hubs"]:
                            cls._instance.add_hub(hub)
        return cls._instance

    def __init__(self):
        # Ensure _hubs is only initialized once
        if not hasattr(self, "_hubs_initialized"):
            self._hubs_initialized = True
            self._hubs: Dict[EquityDomain, "AssetCollectionHub"] = {}

    def add_hub(self, hub: "AssetCollectionHub"):
        hub_domains = hub.get_domains()
        if EquityDomain.OPTION in hub_domains:
            self._hubs[EquityDomain.OPTION] = hub
        elif EquityDomain.STOCK in hub_domains:
            self._hubs[EquityDomain.STOCK] = hub
        else:
            raise ValueError(f"unsupported hub domains {hub_domains}")

    def find_asset(self, meta=None, ticker=None, asset_type: SingleAssetType = None):
        # TODO: ticker and asset_type is semi-supported
        hub: AssetCollectionHub = self._find_hub(meta=meta, asset_type=asset_type)
        if meta is None:
            print("Instrument Finder - find_asset - Overwrite meta with ticker -- Warning: This is not recommended")
        meta = {"ticker": ticker} if ticker else meta  # ticker overwrites meta
        asset = hub.get_asset(params=meta)
        return asset

    def find_collection(self, meta, collection_type: MultiAssetType = None):
        raise NotImplementedError("Not implemented yet")

    def _find_hub(self, meta=None, collection_type=None, asset_type=None):
        if meta is None and collection_type is None and asset_type is None:
            raise ValueError(
                "Meta and Collection type should not be empty at same time"
            )
        # find_hub_meta
        domains = None
        if collection_type:
            domains = collection_type.get_domains()
        elif asset_type:
            domains = asset_type.get_domains()
        elif meta:
            if "domains" not in meta:
                raise ValueError("Illegal meta without domains")
            domains = meta.get("domains")
        print(f"Domains: {domains}")
        return self._find_hub_domains(domains)

    def _find_hub_domains(self, domains: List[DomainEnum]):
        if not domains:
            raise ValueError("Domains should not be empty")
        domains: List[DomainEnum] = (
            parse_domain(domains) if isinstance(domains, str) else domains
        )
        if AssetDomain.EQUITY in domains:
            try:
                key_domain = fetch_domain(domain_type=EquityDomain, domains=domains)
            except Exception as e:
                print(e)
                return
            return self._hubs.get(key_domain)
        else:
            raise ValueError(f"Unsupported domains - {domains}")
