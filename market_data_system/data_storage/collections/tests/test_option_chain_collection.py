import unittest

from market_data_system.data_storage.collections._option_chain_collection import OptionChainCollection


class TestOptionChainCollection(unittest.TestCase):
    def setUp(self):
        self.option_chain_collection = OptionChainCollection()




if __name__ == '__main__':
    unittest.main()
