from enum import Enum, auto


class StrategySectionStatus(Enum):
    OPEN_FAILURE = auto()
    OPEN_ORDER_PLACED = auto()
    AWAITING_EXECUTION = auto()
    MONITORING_POSITION = auto()
    CLOSE_ORDER_PLACED = auto()
    AWAITING_CLOSE_EXECUTION = auto()
