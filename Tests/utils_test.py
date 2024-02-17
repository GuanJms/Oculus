import unittest
from utils.process import read_csv
class MyTestCase(unittest.TestCase):

    def test_read_csv(self):
        csv_name = '20240216_20240206.csv'

        i = 0
        for row in read_csv(csv_name):
            i+=1
            print(i , row)
            if i > 2:
                break




if __name__ == '__main__':
    unittest.main()
