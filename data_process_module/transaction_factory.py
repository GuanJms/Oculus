from typing import List

from data_process_module.transaction import Transaction


class TransactionFactory:
    headers = []
    header_indices = {}

    @classmethod
    def update_header(cls, new_header):
        cls.headers.append(new_header)
        cls.header_indices[new_header] = dict(zip(new_header, range(len(new_header))))

    @staticmethod
    def find_header_index(header) -> dict[str, int]:
        header = tuple(header)
        if header in TransactionFactory.header_indices:
            return TransactionFactory.header_indices[header]
        else:
            TransactionFactory.update_header(header)
            return TransactionFactory.header_indices[header]

    @classmethod
    def process_transaction(cls, header: List[str], raw_transaction: List[str], header_index: dict) -> List[Transaction]:
        root = raw_transaction[header_index['root']]
        strike = int(raw_transaction[header_index['strike']])
        right = raw_transaction[header_index['right']]
        expiration = int(raw_transaction[header_index['expiration']])
        date = int(raw_transaction[header_index['date']])
        transaction_list = []

        if 'price' in header:
            transaction_type = 'traded_quote'
            price = float(raw_transaction[header_index['price']])
            ms_of_day = int(raw_transaction[header_index['ms_of_day']])
            exchange = int(raw_transaction[header_index['exchange']])
            size = int(raw_transaction[header_index['size']])
            condition = int(raw_transaction[header_index['condition']])
            price_flags = int(raw_transaction[header_index['price_flags']])
            new_transaction = Transaction(root=root, strike=strike, right=right, expiration=expiration, price=price,
                                          type=transaction_type, ms_of_day=ms_of_day, exchange=exchange, size=size,
                                          condition=condition, price_flags=price_flags)
            transaction_list.append(new_transaction)

        if 'bid' in header:
            transaction_type = 'bid'
            bid = float(raw_transaction[header_index['bid']])
            bid_size = int(raw_transaction[header_index['bid_size']])
            bid_exchange = int(raw_transaction[header_index['bid_exchange']])
            bid_condition = int(raw_transaction[header_index['bid_condition']])
            ms_of_day2 = int(raw_transaction[header_index['ms_of_day2']])
            new_transaction = Transaction(root=root, strike=strike, right=right, expiration=expiration, bid=bid,
                                          bid_size=bid_size, bid_exchange=bid_exchange, bid_condition=bid_condition,
                                          ms_of_day2=ms_of_day2, type=transaction_type)
            transaction_list.append(new_transaction)

        if 'ask' in header:
            transaction_type = 'ask'
            ask = float(raw_transaction[header_index['ask']])
            ask_size = int(raw_transaction[header_index['ask_size']])
            ask_exchange = int(raw_transaction[header_index['ask_exchange']])
            ask_condition = int(raw_transaction[header_index['ask_condition']])
            ms_of_day2 = int(raw_transaction[header_index['ms_of_day2']])
            new_transaction = Transaction(root=root, strike=strike, right=right, expiration=expiration, ask=ask,
                                          ask_size=ask_size, ask_exchange=ask_exchange, ask_condition=ask_condition,
                                          ms_of_day2=ms_of_day2, type=transaction_type)
            transaction_list.append(new_transaction)

        return transaction_list

    @classmethod
    def process_raw_transaction_list(cls, header: List[str], raw_transaction_list: List[List[str]]) -> List[Transaction]:
        """TODO: definity need to be make it more genric in the future. Now it is hard coded for the transaction"""
        header_index = cls.find_header_index(header)
        transaction_list = []
        for raw_transaction in raw_transaction_list:
            transaction_list += cls.process_transaction(header, raw_transaction, header_index)
        return transaction_list
