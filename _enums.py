from enum import Enum, auto

from time_system._enums import TimelineType


class OperationMode(Enum):
    LIVE = auto()
    BACKTEST = auto()
    PAPER = auto()
