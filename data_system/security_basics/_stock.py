from decimal import Decimal
from typing import Optional, Any

from ._asset import Asset
from .._enums import AssetDomain, EquityDomain, SingleAssetType


class Stock(Asset):

    def __init__(self, **kwargs):
        super().__init__()
        self._domains = [AssetDomain.EQUITY, EquityDomain.STOCK]

        if 'ticker' not in kwargs:
            raise ValueError('ticker is required')

        self._ticker: Optional[str] = kwargs.get('ticker')
        self._company_name: Optional[str] = kwargs.get('company_name', None)
        self._sector: Optional[str] = kwargs.get('sector', None)
        self._industry: Optional[str] = kwargs.get('industry', None)
        self._country: Optional[str] = kwargs.get('country', None)
        self._market_cap: Optional[float] = kwargs.get('market_cap', None)
        self._earning_per_share: Optional[Decimal] = kwargs.get('earning_per_share', None)
        self._dividend: Optional[Decimal] = kwargs.get('dividend', None)


