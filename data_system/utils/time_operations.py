from datetime import datetime

import pytz
import numpy as np


def get_timestamp(date: str | int, data_timezone: str, _format="%Y%m%d") -> int:
    if isinstance(date, int):
        date = str(date)
    # Parse the date string into a datetime object
    dt = datetime.strptime(date, _format)
    # Attach the data timezone to the datetime
    data_tz = pytz.timezone(data_timezone)
    dt = data_tz.localize(dt)
    return int(dt.timestamp() * 1000)  # timestamp unit is in milliseconds


def calculate_time_to_maturity(quote_date: int, expiration_date: int) -> float:
    """
    This function calculates the time to maturity in year per unit and weekends are included.
    :param quote_date: int
    :param expiration_date:int
    :return: T (time to maturity in years)
    """
    t1 = datetime.strptime(str(quote_date), "%Y%m%d")
    t2 = datetime.strptime(str(expiration_date), "%Y%m%d")
    return (t2 - t1).days / 365 + 1 / 365


def convert_timestamp_to_datetime(timestamp_ms):
    # Convert milliseconds to seconds and then to a numpy datetime64 object
    datetime_np = np.datetime64(timestamp_ms, "ms")
    return datetime_np


def current_date_as_int():
    return int(datetime.now().strftime('%Y%m%d'))

# # Example usage
# data_timezone1 = "US/Eastern"
# print(get_timestamp("20240501", data_timezone1))
# test_msd = 60*60*1000*10
# print(timestamp := get_timestamp("20240501", data_timezone1) + test_msd)
# print(pd.to_datetime(timestamp, unit='ms', utc=True).tz_convert('US/Eastern'))
# converted = datetime.datetime.fromtimestamp(timestamp/1000, pytz.timezone('US/Eastern'))
# print(converted)
