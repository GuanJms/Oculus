from datetime import datetime
from typing import Union

from time_system.utils._date_time_transformation import (
    msd_date_to_datetime,
    display_time,
    get_milliseconds,
    get_date,
)


class Time:
    def __init__(self, ms_of_day: Union[int, str], date: Union[int, str]):
        if not isinstance(ms_of_day, (int, str)):
            raise ValueError("Milliseconds of day must be an integer or a string")
        if isinstance(ms_of_day, str):
            ms_of_day = int(ms_of_day)

        if not isinstance(date, (int, str)):
            raise ValueError("Date must be an integer or a string")
        if isinstance(date, str):
            date = int(date)

        self._ms_of_day = ms_of_day
        self._date = date
        self._datetime = self.to_datetime()

    def __str__(self):
        return display_time(self._datetime)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.ms_of_day == other.ms_of_day and self.date == other.date

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if self.date < other.date:
            return True
        elif self.date == other.date:
            return self.ms_of_day < other.ms_of_day

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        if self.date > other.date:
            return True
        elif self.date == other.date:
            return self.ms_of_day > other.ms_of_day

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __hash__(self):
        return hash((self.ms_of_day, self.date))

    def to_datetime(self) -> datetime:
        if self._ms_of_day is None or self._date is None:
            raise ValueError("Time not set")
        return msd_date_to_datetime(self.ms_of_day, self.date)

    def set_datetime(self, date_time: datetime):
        self.ms_of_day = (
            date_time.hour * 3600000
            + date_time.minute * 60000
            + date_time.second * 1000
            + date_time.microsecond // 1000
        )
        self.date = get_date(date_time)

    def set_ms_of_day(self, ms_of_day: Union[int, str]):
        self.ms_of_day = get_milliseconds(ms_of_day)
        self._refresh_datetime()

    def set_date_time(self, ms_of_day: Union[int, str], date: Union[int, str]):
        self.ms_of_day = get_milliseconds(ms_of_day)
        self.date = get_date(date)
        self._refresh_datetime()

    def set_date(self, date: Union[int, str]):
        self.date = get_date(date)
        self._refresh_datetime()

    def _refresh_datetime(self):
        self._datetime = self.to_datetime()

    @property
    def ms_of_day(self):
        return self._ms_of_day

    @ms_of_day.setter
    def ms_of_day(self, ms_of_day):
        self._ms_of_day = ms_of_day

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date
