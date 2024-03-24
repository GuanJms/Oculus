import pandas_market_calendars as mcal
from global_utils.configuration.configuration_manager import ConfigurationManager
from bisect import bisect_right


class GlobalTimeGenerator:
    nasdaq_calendar = None

    @classmethod
    def get_current_timestamp(cls):
        from datetime import datetime
        return int(datetime.now().timestamp())

    @classmethod
    def convert_timestamp_to_datetime(cls, timestamp: int):
        from datetime import datetime
        return datetime.fromtimestamp(timestamp)

    @staticmethod
    def generate_current_date_integer():
        from datetime import datetime
        date = datetime.now()
        return int(date.strftime('%Y%m%d'))

    @classmethod
    def add_delta_date_to_date(cls, quote_date: int, delta_date: int):
        from datetime import datetime, timedelta
        date = datetime.strptime(str(quote_date), '%Y%m%d')
        date += timedelta(days=delta_date)
        return int(date.strftime('%Y%m%d'))

    @classmethod
    def get_nasdaq_calendar(cls):
        if cls.nasdaq_calendar is None:
            cls.load_calendar()
        return cls.nasdaq_calendar

    @classmethod
    def load_calendar(cls):
        import pandas as pd
        START_DATE = str(ConfigurationManager.START_DATE)
        START_DATE = f"{START_DATE[:4]}-{START_DATE[4:6]}-{START_DATE[6:]}"
        END_DATE = pd.Timestamp.today() + pd.Timedelta(days=30)
        END_DATE = END_DATE.strftime('%Y-%m-%d')
        nasdaq_calendar = mcal.get_calendar('NASDAQ')
        valid_days = nasdaq_calendar.valid_days(start_date=START_DATE, end_date=END_DATE)
        cls.nasdaq_calendar = valid_days.strftime('%Y%m%d').astype(int).tolist()
        cls.nasdaq_calendar.sort()

    @classmethod
    def get_next_business_day(cls, date: int):
        cls._check_nasdaq_calendar()
        index = bisect_right(cls.nasdaq_calendar, date)
        if index < len(cls.nasdaq_calendar):
            return cls.nasdaq_calendar[index]
        else:
            return None

    @classmethod
    def is_business_day(cls, start_date):
        cls._check_nasdaq_calendar()
        return start_date in cls.nasdaq_calendar

    @classmethod
    def _check_nasdaq_calendar(cls):
        if cls.nasdaq_calendar is None:
            cls.load_calendar()

    @classmethod
    def get_next_business_day_if_not_business_day(cls, date: int):
        if cls.is_business_day(date):
            return date
        else:
            return cls.get_next_business_day(date)
