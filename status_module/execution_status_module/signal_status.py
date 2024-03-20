from enum import Enum, auto


class SignalStatus(Enum):
    PENDING = auto()
    TRIGGERED = auto()
    REJECTED = auto()
