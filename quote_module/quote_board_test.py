import unittest

from utils.global_id.configuration.configuration_manager import ConfigurationManager
from data_process_module import TransactionFactory
from data_process_module import TransactionQueue
from quote_module.quote_board import QuoteBoard
from utils.process import CSVReader


class SimpleQuoteBoardTestCase(unittest.TestCase):

    def setUp(self):
        self.spy_quote_board_params = {'root': 'SPX'}
        self.uso_quote_board_params = {'root': 'USO'}
        self.transaction_queue = TransactionQueue(sort_key=ConfigurationManager.get_MSD_COL_NAME())
        self.batch_size = 100

    def test_quote_board_init(self):
        spy_quote_board = QuoteBoard(**self.spy_quote_board_params)
        uso_quote_board = QuoteBoard(**self.uso_quote_board_params)
        self.assertEqual(spy_quote_board.root, 'SPX')
        self.assertEqual(uso_quote_board.root, 'USO')

    def test_quote_board_process_transaction(self):
        # open the csv file and read the market_data_system
        csv_test_path = '../tests/20240216_20240206_sorted.csv'
        csvReader = CSVReader(csv_test_path)
        header = next(csvReader)
        raw_transaction_list = [row for row in csvReader]
        transaction_list = TransactionFactory.process_raw_transaction_list(header, raw_transaction_list)
        spy_quote_board = QuoteBoard(**self.spy_quote_board_params)
        for i in range(0, len(transaction_list), self.batch_size):
            self.transaction_queue.add_transactions(transaction_list[i: i + self.batch_size])
            for transaction in self.transaction_queue:
                spy_quote_board.process_transaction(transaction)



if __name__ == '__main__':
    unittest.main()
