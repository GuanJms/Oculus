import datetime
import pytz


def get_timestamp(date: str | int, data_timezone: str, _format="%Y%m%d") -> int:
    if isinstance(date, int):
        date = str(date)
    # Parse the date string into a datetime object
    dt = datetime.datetime.strptime(date, _format)
    # Attach the data timezone to the datetime
    data_tz = pytz.timezone(data_timezone)
    dt = data_tz.localize(dt)
    return int(dt.timestamp() * 1000)


# # Example usage
# data_timezone1 = "US/Eastern"
# print(get_timestamp("20240501", data_timezone1))
