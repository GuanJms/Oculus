from decimal import Decimal
from typing import Optional, Any

from ._asset import Asset
from .._enums import AssetType


class Stock(Asset):

    def __init__(self):
        super().__init__()
        self._type = AssetType.EQUITY
        self._company_name: Optional[str] = None
        self._sector: Optional[str] = None
        self._industry: Optional[str] = None
        self._country: Optional[str] = None
        self._market_cap: Optional[float] = None
        self._earning_per_share: Optional[Decimal] = None
        self._dividend: Optional[Decimal] = None

    def get_param(self, param: str) -> Optional[Any]:
        # check if the param exists
        if hasattr(self, param):
            return getattr(self, param)
        if not param.startswith('_'):
            private = f"_{param}"
            if hasattr(self, private):
                return getattr(self, private)
        return None
