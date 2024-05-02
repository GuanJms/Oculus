import unittest
from data_system.data_structure.factory.stoculus_data.stoculus_option_data_quote_node_factory import StoculusOptionQuoteNodeFactory
import json

class MyTestCase(unittest.TestCase):
    def test_stoculus_option_data_factory(self):
        with open("/Users/jamesguan/Project/Oculus/data_system/data_structure/testing_data/quote_data.json", "r") as f:
            data = json.load(f)

        header = data["header"]
        prices = data["data"]
        date = data['date']

        factory = StoculusOptionQuoteNodeFactory(header)
        nodes = factory.create_nodes(prices)
        print(nodes)





if __name__ == "__main__":
    unittest.main()
