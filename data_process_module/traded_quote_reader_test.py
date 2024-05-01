import unittest

import pandas as pd

from data_process_module.traded_quote_reader import TradedQuoteReader


class MyTestCase(unittest.TestCase):
    def test_traded_quote_reader(self):
        df = pd.read_csv("../tests/20240216_20240206.csv", index_col=0)
        df.sort_values(by="ms_of_day", inplace=True)
        df.to_csv("20240216_20240206_sorted.csv")

        quote_reader = TradedQuoteReader(
            path="../tests/20240216_20240206_sorted.csv",
            root="SPX",
            date=20240206,
            expiration=20240216,
            asset_type="option",
            max_row_reading_batch=1000,
        )
        quote_reader.open_stream(start_msd=0)
        header = quote_reader.get_header()
        records = quote_reader.read_until_msd(60 * 60 * 1000 * 15)
        # print(header)
        # print(records[0:1])
        print(dict(zip(header, records[0])))
        # print(len(records))
        next_records = quote_reader.read_until_msd(60 * 60 * 1000 * 16)
        # print(len(next_records))
        zero_records = quote_reader.read_until_msd(60 * 60 * 1000 * 16)

        quote_reader.open_stream(start_msd=0)
        # print(quote_reader.get_header())
        full_records = quote_reader.read_until_msd(60 * 60 * 1000 * 16)
        # print(len(full_records))
        self.assertEqual(len(full_records), len(records) + len(next_records))
        self.assertEqual(len(zero_records), 0)


if __name__ == "__main__":
    unittest.main()
