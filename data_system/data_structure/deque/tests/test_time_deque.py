import unittest
from data_system.data_structure.deque.time_deque import TimeDeque
import json
class MyTestCase(unittest.TestCase):

    def setUp(self):
        with open("/data_system/data_structure/testing_data/quote_data.json", "r") as f:
            self.data = json.load(f)
        self.header = self.data["header"]
        self.prices = self.data["data"]
        self.date = self.data['date']

    def test_load_data(self):
        print(self.header)
        print(self.prices)
        print(self.date)

        tdq = TimeDeque(60000, 'ms')





if __name__ == "__main__":
    unittest.main()
