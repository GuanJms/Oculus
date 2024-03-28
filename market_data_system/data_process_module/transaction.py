from typing import Optional

from utils.global_id.configuration.configuration_manager import ConfigurationManager


class Transaction:

    # _instnace_tracker = weakref.WeakSet()
    #
    # def __new__(cls, *args, **kwargs):
    #     instance = super(Transaction, cls).__new__(cls)
    #     cls._instnace_tracker.add(instance)
    #     if len(cls._instnace_tracker) % 2000 == 0:
    #         print(f"Transaction init {len(cls._instnace_tracker)}")
    #     return instance

    MSD_COL_NAME = ConfigurationManager.get_MSD_COL_NAME()
    MSD_COL_NAME_SECONDARY = ConfigurationManager.get_MSD_COL_NAME_SECONDARY()

    def __init__(self, **kwargs):
        self._root: str = kwargs.get('root')
        self._type: str = kwargs.get('type')

        self._strike: Optional[int] = kwargs.get('strike', None)
        self._right: Optional[str] = kwargs.get('right', None)
        self._expiration: Optional[int] = kwargs.get('expiration', None)
        self._price: Optional[float] = kwargs.get('price', None)
        self._ms_of_day: Optional[int] = kwargs.get(self.MSD_COL_NAME, None)
        self._condition: Optional[int] = kwargs.get('condition', None)
        self._exchange: Optional[int] = kwargs.get('exchange', None)
        self._size: Optional[int] = kwargs.get('size', None)
        self._condition_flags: Optional[int] = kwargs.get('condition_flags', None)
        self._price_flags: Optional[int] = kwargs.get('price_flags', None)
        self._volume_type: Optional[int] = kwargs.get('volume_type', None)
        self._ms_of_day2: Optional[int] = kwargs.get(self.MSD_COL_NAME_SECONDARY, None)
        self._bid: Optional[float] = kwargs.get('bid', None)
        self._bid_size: Optional[int] = kwargs.get('bid_size', None)
        self._ask_size: Optional[int] = kwargs.get('ask_size', None)
        self._bid_exchange: Optional[int] = kwargs.get('bid_exchange', None)
        self._bid_condition: Optional[int] = kwargs.get('bid_condition', None)
        self._ask_exchange: Optional[int] = kwargs.get('ask_exchange', None)
        self._ask: Optional[float] = kwargs.get('ask', None)
        self._ask_condition: Optional[int] = kwargs.get('ask_condition', None)
        self._date: Optional[int] = kwargs.get('quote_date', None)

        # self.DTE: Optional[int] = None
        #
        # if self.expiration is not None and self.quote_date is not None:
        #     # calculate DTE from expiration and quote_date
        #     _expiration = datetime.strptime(str(self.expiration), '%Y%m%d')
        #     _date = datetime.strptime(str(self.quote_date), '%Y%m%d')

    def get_params(self)-> dict[str, Optional]:
        # TODO: needs testing! Not sure if the code is correct
        exisiting_params = {key: value for key, value in vars(self).items() if value is not None}
        return exisiting_params

    def __str__(self):
        return str(self.get_params())

    @property
    def root(self) -> str:
        return self._root

    # def get_DTE(self):
    #     return self.DTE

    @property
    def type(self) -> str:
        return self._type

    @property
    def strike(self) -> Optional[int]:
        return self._strike

    @property
    def right(self) -> Optional[str]:
        return self._right

    @property
    def expiration(self) -> Optional[int]:
        return self._expiration

    @property
    def price(self) -> Optional[float]:
        if self.type == 'traded_quote':
            return self._price
        if self.type == 'bid':
            return self._bid
        if self.type == 'ask':
            return self._ask
        return self._price

    @property
    def ms_of_day(self) -> Optional[int]:
        if self.type == 'bid' or self.type == 'ask':
            return self._ms_of_day2
        return self._ms_of_day

    @property
    def condition(self) -> Optional[int]:
        return self._condition

    @property
    def exchange(self) -> Optional[int]:
        return self._exchange

    @property
    def size(self) -> Optional[int]:
        if self.type == 'traded_quote':
            return self._size
        if self.type == 'bid':
            return self._bid_size
        if self.type == 'ask':
            return self._ask_size
        return self._size

    @property
    def condition_flags(self) -> Optional[int]:
        return self._condition_flags

    @property
    def price_flags(self) -> Optional[int]:
        return self._price_flags

    @property
    def volume_type(self) -> Optional[int]:
        return self._volume_type

    @property
    def ms_of_day2(self) -> Optional[int]:
        return self._ms_of_day2

    @property
    def bid(self) -> Optional[float]:
        return self._bid

    @property
    def bid_size(self) -> Optional[int]:
        return self._bid_size

    @property
    def ask_size(self) -> Optional[int]:
        return self._ask_size

    @property
    def bid_exchange(self) -> Optional[int]:
        return self._bid_exchange

    @property
    def bid_condition(self) -> Optional[int]:
        return self._bid_condition

    @property
    def ask_exchange(self) -> Optional[int]:
        return self._ask_exchange

    @property
    def ask(self) -> Optional[float]:
        return self._ask

    @property
    def ask_condition(self) -> Optional[int]:
        return self._ask_condition

    @property
    def date(self) -> Optional[int]:
        return self._date




# {'': '3432', 'root': 'SPX', 'expiration': '20240216', 'strike': '5200000', 'right': 'C',
# 'ms_of_day': '3916031', 'sequence': '591691650', 'ext_condition1': '255', 'ext_condition2': '255',
# 'ext_condition3': '255', 'ext_condition4': '255', 'condition': '18', 'size': '1', 'exchange': '5',
# 'price': '0.35', 'condition_flags': '0', 'price_flags': '1', 'volume_type': '0', 'records_back': '0',
# 'ms_of_day2': '3916031', 'bid_size': '968', 'bid_exchange': '5', 'bid': '0.25', 'bid_condition': '50',
# 'ask_size': '100', 'ask_exchange': '5', 'ask': '0.35', 'ask_condition': '50', 'quote_date': '20240206'}

