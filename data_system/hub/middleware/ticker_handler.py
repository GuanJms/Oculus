from typing import List

from data_system._enums import DomainEnum
from .hub_ticker import HubTicker


class HubTickerFactory:

    @staticmethod
    def create_ticker(ticker: str, domains: List[DomainEnum]) -> HubTicker:
        if HubTickerFactory._test_validate_ticker(ticker, domains):
            return HubTicker(ticker, domains)

    @staticmethod
    def _validate_ticker(ticker: str, domains: List[DomainEnum]) -> bool:
        raise NotImplementedError  # TODO: change this to a proper implementation

    @staticmethod
    def _test_validate_ticker(ticker: str, domains: List[DomainEnum]) -> bool:
        print(f" Warning : using testing function _test_validate_ticker for HubTickerFactory")
        return True
