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


class AssetType(Enum):
    EQUITY = auto()
    BOND = auto()
    OPTION = auto()
    INDEX = auto()


class AssetCollectionType(Enum):
    SingleAsset = auto()
    MultiAsset = auto()


class OptionType(Enum):
    CALL = auto()
    PUT = auto()

    @classmethod
    def get_option_type(cls, option_type):
        if option_type.upper() in ["CALL", 'C']:
            return cls.CALL
        elif option_type.upper() in ["PUT", 'P']:
            return cls.PUT
        else:
            raise ValueError("Invalid option type")


class MultiAssetType(Enum):
    OPTION_CHAIN = auto()


class TimeType(Enum):
    MS_OF_DAY = auto()
    TIME_OF_DAY = auto()
    DATE = auto()
    DATETIME = auto()

    def is_time_of_day(self):
        return self == TimeType.TIME_OF_DAY or self == TimeType.MS_OF_DAY


class DomainEnum(Enum):
    def to_string(self):
        return self.name.upper()


class StructureDomainTag(DomainEnum):
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
    TRADED_QUOTE = auto()


__all__ = ["SimulationEventType", "OperationMode", "TimelineType", "AssetType", "OptionType", "AssetCollectionType",
           "TimeType", "TransactionType"]
