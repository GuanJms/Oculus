from enum import Enum, auto


class TimeType(Enum):
    MS_OF_DAY = auto()
    TIME_OF_DAY = auto()
    DATE = auto()
    DATETIME = auto()

    def is_time_of_day(self):
        return self == TimeType.TIME_OF_DAY or self == TimeType.MS_OF_DAY


class TimelineType(Enum):
    SIMULATION = auto()
    REALTIME = auto()
