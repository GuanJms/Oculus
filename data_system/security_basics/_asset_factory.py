from typing import Optional

from data_system._enums import DomainEnum
from ..utils.domain_matcher import DomainMatcher
from ..utils.domain_operations import parse_domain
from ._asset import Asset


class AssetFactory:

    @staticmethod
    def create_asset(domain_chain_str: Optional[str] = None, domains: Optional[DomainEnum] = None, **kwargs) -> 'Asset':
        if domain_chain_str is None and domains is None:
            raise ValueError('domain_chain_str or domains is required')
        if domain_chain_str is not None:
            domains = parse_domain(domain_chain_str, asset_domain=True, equity_domain=True, price_domain=False)
            if len(domains) == 0:
                raise ValueError('domains cannot be empty')
        AssetClass = DomainMatcher.match_domain_asset(domains)
        return AssetClass(**kwargs)

