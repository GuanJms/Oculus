from typing import Optional, Any, List

from ._time import Time
from utils.global_id import GlobalComponentIDGenerator
from .._enums import TimeType


class Timeline:

    def __init__(self):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self.time = Time(0, 19700101)

    @property
    def id(self):
        return self._id

    def set_time(self, **kwargs):
        keys = kwargs.keys()
        match True:
            case _ if keys == {'ms_of_day', 'date'}:
                self.time = self.time.set_date_time(ms_of_day=kwargs['ms_of_day'], date=kwargs['date'])
            case _ if keys == {'ms_of_day'}:
                self.time = self.time.set_ms_of_day(kwargs['ms_of_day'])
            case _ if keys == {'date'}:
                self.time = self.time.set_date(kwargs['date'])
            case _ if keys == {'datetime'}:
                self.time = self.time.set_datetime(kwargs['datetime'])
            case _:
                raise ValueError(f"Invalid time setting{keys}")

    def get_time(self, time_type: TimeType):
        self._check_initiated()
        match time_type:
            case TimeType.MS_OF_DAY:
                return self.time.ms_of_day
            case TimeType.DATE:
                return self.time.date
            case TimeType.DATETIME:
                return self.time.to_datetime()
            case _:
                raise ValueError(f"Invalid time type: {time_type}")

    def _check_initiated(self):
        if self.time == Time(0, 1970):
            raise ValueError("Time not set")

    def __eq__(self, other):
        return self.time == other.timeline

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.time < other.timeline

    def __le__(self, other):
        return self.time <= other.timeline

    def __gt__(self, other):
        return self.time > other.timeline

    def __ge__(self, other):
        return self.time >= other.timeline
