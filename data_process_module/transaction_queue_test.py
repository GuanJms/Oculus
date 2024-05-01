import unittest
import pandas as pd

from quote_module.transaction._transaction import Transaction
from data_process_module.transaction_queue import TransactionQueue


class MyTestCase(unittest.TestCase):
    def test_transaction_queue_sort_order(self):
        csv_test_path = "/Users/jamesguan/Project/TemptDataHouse/SPX/raw_traded_quote/2024/02/20240216_20240206.csv"
        df = pd.read_csv(csv_test_path, index_col=0)
        df = df.sort_values(by="ms_of_day")
        records = df.to_dict("records")
        batch_size = 1000

        for i in range(0, len(records), batch_size):
            batch = records[i : i + batch_size]
            transactions = [Transaction(**record) for record in batch]
            transaction_queue1 = TransactionQueue()
            transaction_queue2 = TransactionQueue()
            transaction_queue1.add_transactions(transactions)
            transaction_queue2.add_transactions(transactions)
            pre_msd = -1
            for transaction1, transaction2 in zip(
                transaction_queue1, transaction_queue2
            ):
                current_msd = transaction1.ms_of_day
                self.assertGreaterEqual(current_msd, pre_msd)
                self.assertEqual(transaction1, transaction2)


if __name__ == "__main__":
    unittest.main()
