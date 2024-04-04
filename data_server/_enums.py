from enum import Enum, auto


class ReadingStatus(Enum):
    DONE = auto()
    ONGOING = auto()


class ReaderStatus(Enum):
    OPEN = auto()
    CLOSED = auto()
    ERROR = auto()


class AssetDomain(Enum):
    EQUITY = auto()


class EquityDomain(Enum):
    STOCK = auto()
    OPTION = auto()


class PriceDomain(Enum):
    TRADED = auto()
    QUOTE = auto()
    TRADED_QUOTE = auto()