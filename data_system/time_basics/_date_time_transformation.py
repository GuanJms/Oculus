from typing import Union, List, Type, Any
from datetime import datetime, timedelta


def msd_date_to_datetime(
    milliseconds_of_day: Union[int, str], date: Union[int, str]
) -> datetime:
    if isinstance(milliseconds_of_day, str):
        milliseconds_of_day = int(milliseconds_of_day)
    if not isinstance(milliseconds_of_day, int):
        raise ValueError("Milliseconds of day must be an integer")
    if isinstance(date, int):
        date = str(date)
    if not isinstance(date, str):
        raise ValueError("Date must be a string")

    seconds = milliseconds_of_day / 1000
    date = datetime.strptime(date, "%Y%m%d")
    return date + timedelta(seconds=seconds)


def msd_to_deltatime(milliseconds_of_day: Union[int, str]) -> timedelta:
    if isinstance(milliseconds_of_day, str):
        milliseconds_of_day = int(milliseconds_of_day)
    if not isinstance(milliseconds_of_day, int):
        raise ValueError("Milliseconds of day must be an integer")
    seconds = milliseconds_of_day / 1000
    return timedelta(seconds=seconds)


def time_of_day_to_ms_of_day(time: datetime) -> int:
    # Extracting time
    time = time.time()

    # Calculating total milliseconds
    milliseconds = (
        time.hour * 3600 + time.minute * 60 + time.second
    ) * 1000 + time.microsecond // 1000
    return milliseconds


def display_time(time: datetime) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S %f")


def date_to_int(time: datetime) -> int:
    return int(time.strftime("%Y%m%d"))


def get_milliseconds(ms_of_day: Any) -> int:
    if isinstance(ms_of_day, str):
        ms_of_day = int(ms_of_day)
    if isinstance(ms_of_day, float):
        ms_of_day = int(ms_of_day)
    if isinstance(ms_of_day, timedelta):
        ms_of_day = deltatime_to_milliseconds(ms_of_day)
    if isinstance(ms_of_day, int):
        if ms_of_day < 0 or ms_of_day > 86400000:
            raise ValueError("Milliseconds of day must be between 0 and 86400000")
        return ms_of_day
    else:
        raise NotImplementedError(f"type {type(ms_of_day)} not supported")


def get_date(date: Any) -> int:
    if isinstance(date, str):
        date = int(date)
    if isinstance(date, datetime):
        date = date_to_int(date)
    if isinstance(date, int):
        if date < 19700101 or date > 99991231:
            raise ValueError("Invalid date format. Must be in YYYYMMDD format")
        return date
    else:
        raise NotImplementedError(f"type {type(date)} not supported")


def get_datetime(date_time: Any) -> datetime:
    if isinstance(date_time, datetime):
        return date_time
    else:
        raise NotImplementedError(f"type {type(date_time)} not supported")


def check_valid_time_interval(time_interval: int):
    if time_interval <= 0:
        raise ValueError("Time interval must be a positive integer")


def deltatime_to_milliseconds(delta_time: timedelta) -> int:
    return int(delta_time.total_seconds() * 1000)
