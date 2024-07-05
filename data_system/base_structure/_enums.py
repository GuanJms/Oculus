from enum import Enum, auto


class NodeType(Enum):
    QUOTE = auto()
    TRADE = auto()
    VOLATILITY = auto()
    GREEK = auto()


class VolType(Enum):
    IMPLIED = auto()


class QuoteType(Enum):
    BID = auto()
    ASK = auto()

    @classmethod
    def from_string(cls, quote_col):
        quote_col = quote_col.lower()
        if "bid" in quote_col:
            return cls.BID
        elif "ask" in quote_col:
            return cls.ASK
        else:
            raise ValueError("Invalid quote type")
