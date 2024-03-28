from enum import Enum, auto


class OperationMode(Enum):
    LIVE_TRADING = auto()
    BACKTESTING = auto()
    PAPER_TRADING = auto()


class SimulationEventType(Enum):
    ADVANCE_MS_OF_DAY = auto()
    ADVANCE_DATE = auto()
    END = auto()
    START = auto()




