from typing import List

from ._transaction import Transaction
from market_data_system._enums import TransactionType
from decimal import Decimal


class TransactionFactory:
    headers = []
    header_indices = {}
    HEADERS_FROM_TRADED_QUOTE_DATA_SOURCE = {
        'ALL': {'STRING': ['root', 'right'], 'INTEGER': ['expiration', 'date', 'strike']},
        'TRADED': {'DECIMAL': ['price'],
                   'INTEGER': ['ms_of_day', 'exchange', 'size', 'condition', 'price_flags']},
        'BID': {'DECIMAL': ['bid'],
                'INTEGER': ['bid_size', 'bid_exchange', 'bid_condition', 'ms_of_day2']},
        'ASK': {'DECIMAL': ['ask'],
                'INTEGER': ['ask_size', 'ask_exchange', 'ask_condition', 'ms_of_day2']}
    }

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
    def _add_header(cls, params: dict, raw_transaction: List[str], header_index: dict, header_setting: dict) -> dict:
        type_keys = header_setting.keys()
        if 'STRING' in type_keys:
            for key in header_setting['STRING']:
                params[key] = raw_transaction[header_index[key]]
        if 'DECIMAL' in type_keys:
            for key in header_setting['DECIMAL']:
                str_value = str(raw_transaction[header_index[key]])
                params[key] = Decimal(str_value)
        if 'INTEGER' in type_keys:
            for key in header_setting['INTEGER']:
                params[key] = int(raw_transaction[header_index[key]])
        return params

    @classmethod
    def create_transaction_from_traded_quote_data_source(cls, raw_transaction: List[str], header_index: dict,
                                                         transaction_type: TransactionType) -> Transaction:
        params = {}
        cls._add_header(params, raw_transaction, header_index, cls.HEADERS_FROM_TRADED_QUOTE_DATA_SOURCE['ALL'])
        cls._add_header(params, raw_transaction, header_index,
                        cls.HEADERS_FROM_TRADED_QUOTE_DATA_SOURCE[transaction_type.value])
        return Transaction(type=transaction_type, **params)

    @classmethod
    def find_transaction_types(cls, header: List[str]) -> List[TransactionType]:
        types = []
        if 'price' in header:
            types.append(TransactionType.TRADED)
        if 'bid' in header:
            types.append(TransactionType.BID)
        if 'ask' in header:
            types.append(TransactionType.ASK)
        return types

    @classmethod
    def process_transaction(cls, header: List[str], raw_transaction: List[str], header_index: dict) -> List[
        Transaction]:
        required_types = cls.find_transaction_types(header)
        transaction_list = []
        for transaction_type in required_types:
            new_transaction = cls.create_transaction_from_traded_quote_data_source(raw_transaction, header_index,
                                                                                   transaction_type)
            transaction_list.append(new_transaction)
        return transaction_list

    @classmethod
    def process_raw_transaction_list(cls, header: List[str], raw_transaction_list: List[List[str]]) -> List[
        Transaction]:
        """TODO: definity need to be make it more genric in the future. Now it is hard coded for the price"""
        header_index = cls.find_header_index(header)
        transaction_list = []
        for raw_transaction in raw_transaction_list:
            transaction_list += cls.process_transaction(header, raw_transaction, header_index)
        return transaction_list
