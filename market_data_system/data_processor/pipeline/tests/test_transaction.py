import unittest
from quote_module.transaction._transaction import Transaction


class TransactionTest(unittest.TestCase):
    def test_class_attribute(self):
        transaction = Transaction()
        transaction2 = Transaction()
        print(id(transaction.traded_quote_transaction_attributes))
        print(id(transaction2.traded_quote_transaction_attributes))

    def test_init(self):
        test_input = {'root': 'SPX', 'expiration': '20240216', 'strike': '5200000', 'right': 'C',
                      'ms_of_day': '3916031', 'sequence': '591691650', 'ext_condition1': '255', 'ext_condition2': '255',
                      'ext_condition3': '255', 'ext_condition4': '255', 'condition': '18', 'size': '1', 'exchange': '5',
                      'price': '0.35', 'condition_flags': '0', 'price_flags': '1', 'volume_type': '0',
                      'records_back': '0',
                      'ms_of_day2': '3916031', 'bid_size': '968', 'bid_exchange': '5', 'bid': '0.25',
                      'bid_condition': '50',
                      'ask_size': '100', 'ask_exchange': '5', 'ask': '0.35', 'ask_condition': '50',
                      'quote_date': '20240206'}

        test_attributes = ['root', 'strike', 'right', 'expiration', 'price', 'condition',
                                               'exchange', 'size', 'condition_flags', 'price_flags', 'volume_type',
                                               'ms_of_day', 'ms_of_day2'
                                               'bid', 'bid_size', 'ask_size', 'bid_exchange', 'bid_condition',
                                               'ask_exchange',
                                               'ask', 'ask_condition', 'quote_date']

        transaction = Transaction(type = 'traded_quote',**test_input)
        print(transaction.get_params())
        for attribute in test_attributes:
            self.assertEqual(transaction.get_param(attribute), test_input.get(attribute, None))
        print(transaction.get_param('type'))




if __name__ == '__main__':
    unittest.main()
