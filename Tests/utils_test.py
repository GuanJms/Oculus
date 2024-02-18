import unittest

import pandas as pd

from utils.process import CSVReader


class MyTestCase(unittest.TestCase):

    def test_read_csv(self):
        file_path = '20240216_20240206.csv'
        df = pd.read_csv(file_path)
        peekable_iter = CSVReader(file_path)
        i = -1 # excluding the header
        for _ in peekable_iter:
            i += 1
        self.assertEqual(i, len(df))

    def test_iterator(self):
        file_path = '20240216_20240206.csv'
        df = pd.read_csv(file_path)
        peekable_iter = CSVReader(file_path)
        header = next(peekable_iter)
        for j in range(len(df)):
            row = next(peekable_iter)
            # convert df.iloc[j].tolist() to string
            test_row = [str(x) for x in df.iloc[j].tolist()]
            self.assertEqual(row, test_row)

        with self.assertRaises(StopIteration):
            next(peekable_iter)

if __name__ == '__main__':
    unittest.main()
