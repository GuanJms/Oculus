from enum import Enum, auto


class TimeUnit(Enum):
    MILLISECOND = auto()
    SECOND = auto()
    MINUTE = auto()
    HOUR = auto()
    DAY = auto()
    WEEK = auto()
    MONTH = auto()

    def __str__(self):
        return self.name

    @classmethod
    def get(cls, unit):
        # if unit is str, then convert to TimeUnit
        if isinstance(unit, str):
            unit = unit.upper()
            if unit == "MILLISECOND" or unit == "MS":
                return cls.MILLISECOND
            elif unit == "SECOND":
                return cls.SECOND
            elif unit == "MINUTE":
                return cls.MINUTE
            elif unit == "HOUR":
                return cls.HOUR
            elif unit == "DAY":
                return cls.DAY
            elif unit == "WEEK":
                return cls.WEEK
            elif unit == "MONTH":
                return cls.MONTH
            else:
                raise ValueError("Invalid time unit")
        elif isinstance(unit, TimeUnit):
            # else if unit is TimeUnit, then return unit
            return unit
        else:
            raise ValueError("Invalid time unit")


class NodeType(Enum):
    QUOTE = auto()
    TRADE = auto()


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
