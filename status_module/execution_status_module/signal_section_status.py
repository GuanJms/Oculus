from enum import Enum, auto


class SignalSectionStatus(Enum):
    PENDING = auto()
    TRIGGERED = auto()
    REJECTED = auto()
