from enum import Enum, auto


class SimulationEventType(Enum):
    ADVANCE_MS_OF_DAY = auto()
    ADVANCE_DATE = auto()
    END = auto()
    START = auto()




