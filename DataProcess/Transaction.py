from datetime import datetime
from typing import Optional, List, TypeVar

class Transaction:
    headers = []
    header_indices = {}
    def __init__(self, **kwargs):
        self.root: str = kwargs.get('root')
        self.type: str = kwargs.get('type')

        self.strike: Optional[int] = kwargs.get('strike', None)
        self.right: Optional[str] = kwargs.get('right', None)
        self.expiration: Optional[int] = kwargs.get('expiration', None)
        self.price: Optional[float] = kwargs.get('price', None)
        self.ms_of_day: Optional[int] = kwargs.get('ms_of_day', None)
        self.condition: Optional[int] = kwargs.get('condition', None)
        self.exchange: Optional[int] = kwargs.get('exchange', None)
        self.size: Optional[int] = kwargs.get('size', None)
        self.condition_flags: Optional[int] = kwargs.get('condition_flags', None)
        self.price_flags: Optional[int] = kwargs.get('price_flags', None)
        self.volume_type: Optional[int] = kwargs.get('volume_type', None)
        self.ms_of_day2: Optional[int] = kwargs.get('ms_of_day2', None)
        self.bid: Optional[float] = kwargs.get('bid', None)
        self.bid_size: Optional[int] = kwargs.get('bid_size', None)
        self.ask_size: Optional[int] = kwargs.get('ask_size', None)
        self.bid_exchange: Optional[int] = kwargs.get('bid_exchange', None)
        self.bid_condition: Optional[int] = kwargs.get('bid_condition', None)
        self.ask_exchange: Optional[int] = kwargs.get('ask_exchange', None)
        self.ask: Optional[float] = kwargs.get('ask', None)
        self.ask_condition: Optional[int] = kwargs.get('ask_condition', None)
        self.date: Optional[int] = kwargs.get('date', None)

        # self.DTE: Optional[int] = None
        #
        # if self.expiration is not None and self.date is not None:
        #     # calculate DTE from expiration and date
        #     _expiration = datetime.strptime(str(self.expiration), '%Y%m%d')
        #     _date = datetime.strptime(str(self.date), '%Y%m%d')

    def get_params(self)-> dict[str, Optional]:
        # TODO: needs testing! Not sure if the code is correct
        exisiting_params = {key: value for key, value in vars(self).items() if value is not None}
        return exisiting_params

    def get_root(self) -> str:
        return self.root

    # def get_DTE(self):
    #     return self.DTE

    def get_strike(self) -> Optional[int]:
        return self.strike

    def get_right(self) -> Optional[str]:
        return self.right

    def get_expiration(self) -> Optional[int]:
        return self.expiration

    def get_price(self) -> Optional[float]:
        return self.price

    def get_type(self) -> Optional[str]:
        return self.type

    def get_ms_of_day(self) -> Optional[int]:
        return self.ms_of_day

    def get_bid(self) -> Optional[float]:
        return self.bid

    def get_ask(self) -> Optional[float]:
        return self.ask

    def get_bid_size(self) -> Optional[int]:
        return self.bid_size

    def get_ask_size(self) -> Optional[int]:
        return self.ask_size

    def get_exchange(self) -> Optional[int]:
        return self.exchange

    def get_date(self) -> Optional[int]:
        return self.date

    def get_expirtion(self) -> Optional[int]:
        return self.expiration

    @classmethod
    def update_header(cls, new_header):
        cls.headers.append(new_header)
        cls.header_indices[new_header] = dict(zip(new_header, range(len(new_header))))

    @staticmethod
    def find_header_index(header) -> dict[str, int]:
        if header in Transaction.header_indices:
            return Transaction.header_indices[header]
        else:
            Transaction.update_header(header)
            return Transaction.header_indices[header]

    @classmethod
    def process_raw_transactions(cls, header: List[str], transactions_raw: List[List[str]]):
        """TODO: definity need to be make it more genric in the future. Now it is hard coded for the transaction"""
        header_index = cls.find_header_index(header)
        transactions = []
        for transaction in transactions_raw:
            root = transaction[header_index['root']]
            strike = int(transaction[header_index['strike']])
            right = transaction[header_index['right']]
            expiration = int(transaction[header_index['expiration']])
            date = int(transaction[header_index['date']])

            if 'price' in header:
                transaction_type = 'traded_quote'
                price = float(transaction[header_index['price']])
                ms_of_day = int(transaction[header_index['ms_of_day']])
                exchange = int(transaction[header_index['exchange']])
                size = int(transaction[header_index['size']])
                condition = int(transaction[header_index['condition']])
                price_flags = int(transaction[header_index['price_flags']])
                new_transaction = cls(root=root, strike=strike, right=right, expiration=expiration, price=price,
                                      type=transaction_type, ms_of_day=ms_of_day, exchange=exchange, size=size,
                                      condition=condition, price_flags=price_flags)
                transactions.append(new_transaction)
            if 'bid' in header:
                transaction_type = 'bid'
                bid = transaction[header_index['bid']]
                bid_size = transaction[header_index['bid_size']]
                bid_exchange = transaction[header_index['bid_exchange']]
                bid_condition = transaction[header_index['bid_condition']]
                ms_of_day2 = transaction[header_index['ms_of_day2']]
                new_transaction = cls(root=root, strike=strike, right=right, expiration=expiration, bid=bid,
                                      ask_size=bid_size, bid_exchange=bid_exchange, bid_condition=bid_condition,
                                      ms_of_day2=ms_of_day2, type=transaction_type)
                transactions.append(new_transaction)
            if 'ask' in header:
                transaction_type = 'ask'
                ask = transaction[header_index['ask']]
                ask_size = transaction[header_index['ask_size']]
                ask_exchange = transaction[header_index['ask_exchange']]
                ask_condition = transaction[header_index['ask_condition']]
                ms_of_day2 = transaction[header_index['ms_of_day2']]
                new_transaction = cls(root=root, strike=strike, right=right, expiration=expiration, ask=ask,
                                      ask_size=ask_size, ask_exchange=ask_exchange, ask_condition=ask_condition,
                                      ms_of_day2=ms_of_day2, type=transaction_type)
                transactions.append(new_transaction)
        return transactions

# {'': '3432', 'root': 'SPX', 'expiration': '20240216', 'strike': '5200000', 'right': 'C',
# 'ms_of_day': '3916031', 'sequence': '591691650', 'ext_condition1': '255', 'ext_condition2': '255',
# 'ext_condition3': '255', 'ext_condition4': '255', 'condition': '18', 'size': '1', 'exchange': '5',
# 'price': '0.35', 'condition_flags': '0', 'price_flags': '1', 'volume_type': '0', 'records_back': '0',
# 'ms_of_day2': '3916031', 'bid_size': '968', 'bid_exchange': '5', 'bid': '0.25', 'bid_condition': '50',
# 'ask_size': '100', 'ask_exchange': '5', 'ask': '0.35', 'ask_condition': '50', 'date': '20240206'}

