import unittest
from global_time_generator import GlobalTimeGenerator


class MyTestCase(unittest.TestCase):

    def test_next_business_day(self):
        from datetime import datetime, timedelta

        # Start date
        start_date = datetime.strptime("2010-01-01", "%Y-%m-%d")

        # Current date
        current_date = datetime.now()

        # Generate list of dates
        dates = []
        while start_date <= current_date:
            dates.append(int(start_date.strftime("%Y%m%d")))
            start_date += timedelta(days=1)
        dates.sort()
        calendar_dates = GlobalTimeGenerator.get_nasdaq_calendar()
        result = []
        for date in dates:
            for calendar_date in calendar_dates:
                if calendar_date > date:
                    result.append(calendar_date)
                    break

        result_next_business_day_list = []
        for date in dates:
            result_next_business_day_list.append(GlobalTimeGenerator.get_next_business_day(date))
        self.assertEqual(result, result_next_business_day_list)


if __name__ == '__main__':
    unittest.main()
