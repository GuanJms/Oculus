from enum import Enum
from typing import List, Any, Type

from data_system._enums import *
from data_system.security_basics import Stock, Asset
from data_system.security_basics.option_basics.core import Option

DOMAIN_MAP = {
    AssetDomain.EQUITY: {
        EquityDomain.STOCK: {
            PriceDomain.TRADED: "get_stock_traded",
            PriceDomain.QUOTE: "get_stock_quote",
        },
        EquityDomain.OPTION: {
            PriceDomain.TRADED: "get_option_traded",
            PriceDomain.QUOTE: "get_option_quote",
        },
    }
}

DOMAIN_ASSET_MAP = {
    AssetDomain.EQUITY: {EquityDomain.STOCK: Stock, EquityDomain.OPTION: Option}
}


class DomainMatcher:
    @staticmethod
    def get_domain_iterator(domains: List[DomainEnum]):
        # TODO: sort the domains
        return iter(domains)

    @staticmethod
    def match_domain(
        domains: List[DomainEnum | AssetDomain], domain_map: dict = None, **kwargs
    ):
        if domain_map is None:
            domain_map = DOMAIN_MAP
        if (
            isinstance(domain_map, str) or len(domains) == 0
        ):  # TODO: check if "len(domains) == 0" changes anything
            return domain_map
        domains = domains.copy()
        if domains[0] in domain_map:
            domain_map = domain_map[domains[0]]
            return DomainMatcher.match_domain(domains[1:], domain_map, **kwargs)
        else:
            raise ValueError(f"Invalid Asset Domain {domains[0]}")

    @staticmethod
    def match_domain_asset(
        domains: List[DomainEnum | AssetDomain], domain_map=None, **kwargs
    ):
        if domain_map is None:
            domain_map = DOMAIN_ASSET_MAP
        if not domains:
            if issubclass(domain_map, Asset):
                return domain_map
            else:
                raise ValueError(f"Invalid Asset Domain")
        domains = domains.copy()  # protect the original list
        if domains[0] in domain_map:
            domain_map = domain_map[domains[0]]
            return DomainMatcher.match_domain_asset(domains[1:], domain_map, **kwargs)
        else:
            raise ValueError(f"Invalid Asset Domain {domains[0]}")
