from typing import Optional, Any, List

from ._time import Time
from utils.global_id import GlobalComponentIDGenerator
from .._enums import TimeType


class Timeline:
    def __init__(self):
        self._id = GlobalComponentIDGenerator.generate_unique_id(
            self.__class__.__name__, id(self)
        )
        self.time = Time(0, 19700101)

    @property
    def id(self):
        return self._id

    def set_time(self, **kwargs):
        """
        Set time of the timeline
        :param kwargs:
            'ms_of_day': int
            'date': int
            'datetime': datetime
        :return:
        """
        keys = kwargs.keys()
        match True:
            case _ if keys == {"ms_of_day", "date"}:
                self.time.set_date_time(
                    ms_of_day=kwargs["ms_of_day"], date=kwargs["date"]
                )
            case _ if keys == {"ms_of_day"}:
                self.time.set_ms_of_day(kwargs["ms_of_day"])
            case _ if keys == {"date"}:
                self.time.set_date(kwargs["date"])
            case _ if keys == {"datetime"}:
                self.time.set_datetime(kwargs["datetime"])
            case _:
                raise ValueError(f"Invalid time setting{keys}")

    def __str__(self):
        return f"Timeline: {self.time}"

    def __repr__(self):
        return self.__str__() + f" ID: {self.id}"

    def get_time(self, time_type: TimeType | None | str):
        """
        Get time of the timeline
        :param time_type: TimeType
        :return:
        """
        print(self)
        self._check_initiated()
        if time_type is None:
            return self.time
        if isinstance(time_type, str):
            time_type = time_type.upper()
        match time_type:
            case TimeType.MS_OF_DAY | "MS_OF_DAY":
                return self.time.ms_of_day
            case TimeType.DATE | "DATE":
                return self.get_date()
            case TimeType.DATETIME | "DATETIME":
                return self.time.to_datetime()
            case _:
                raise ValueError(f"Invalid time type: {time_type}")

    def get_date(self):
        return self.time.date

    def _check_initiated(self):
        if self.time == Time(0, 19700101):
            raise ValueError("Time not set")

    def __eq__(self, other):
        return self.time == other.time

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.time < other.time

    def __le__(self, other):
        return self.time <= other.time

    def __gt__(self, other):
        return self.time > other.time

    def __ge__(self, other):
        return self.time >= other.time
