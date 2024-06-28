from enum import Enum, auto


class SimulationEventType(Enum):
    ADVANCE_MS_OF_DAY = auto()
    ADVANCE_DATE = auto()
    END = auto()
    START = auto()


class OperationMode(Enum):
    LIVE = auto()
    BACKTEST = auto()
    PAPER = auto()


class TimelineType(Enum):
    SIMULATION = auto()
    REALTIME = auto()


class DomainEnum(Enum):
    def to_string(self):
        return self.name.upper()


class StructureDomain(DomainEnum):
    STRUCTURED = auto()
    SEMI_STRUCTURED = auto()
    UNSTRUCTURED = auto()

    def to_string(self):
        return self.name.upper()


class AssetDomain(DomainEnum):
    EQUITY = auto()


class EquityDomain(DomainEnum):
    STOCK = auto()
    OPTION = auto()


class PriceDomain(DomainEnum):
    TRADED = auto()
    QUOTE = auto()
    # TRADED_QUOTE = auto()


class GreekDomain(DomainEnum):
    DELTA = auto()
    GAMMA = auto()
    VEGA = auto()
    THETA = auto()
    RHO = auto()


class VolatilityDomain(DomainEnum):
    IMPLIED = auto()


class AssetCollectionType(Enum):
    Asset = auto()
    AssetCollection = auto()


class OptionDomain(Enum):
    CALL = auto()
    PUT = auto()

    @classmethod
    def get_option_type(cls, option_type):
        if option_type.upper() in ["CALL", "C"]:
            return cls.CALL
        elif option_type.upper() in ["PUT", "P"]:
            return cls.PUT
        else:
            raise ValueError("Invalid option type")


class MultiAssetType(Enum):
    OPTION_CHAIN = auto()
    OPTION_PAIR = auto()

    def get_domains(self):
        if self in [MultiAssetType.OPTION_CHAIN, MultiAssetType.OPTION_PAIR]:
            return [AssetDomain.EQUITY, EquityDomain.OPTION]
        else:
            raise ValueError(f"{self} has not being signed into domains")


class SingleAssetType(Enum):
    OPTION = auto()
    STOCK = auto()

    def get_domains(self):
        if self == SingleAssetType.OPTION:
            return [AssetDomain.EQUITY, EquityDomain.OPTION]
        elif self == SingleAssetType.STOCK:
            return [AssetDomain.EQUITY, EquityDomain.STOCK]
        else:
            raise ValueError(f"{self} has not being signed into domains")


class TimeType(Enum):
    MS_OF_DAY = auto()
    TIME_OF_DAY = auto()
    DATE = auto()
    DATETIME = auto()

    def is_time_of_day(self):
        return self == TimeType.TIME_OF_DAY or self == TimeType.MS_OF_DAY


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


__all__ = [
    "SimulationEventType",
    "OperationMode",
    "TimelineType",
    "OptionDomain",
    "AssetCollectionType",
    "TimeType",
    "DomainEnum",
    "StructureDomain",
    "AssetDomain",
    "EquityDomain",
    "PriceDomain",
    "MultiAssetType",
    "SingleAssetType",
    "TimeUnit",
    "VolatilityDomain",
]
