from datetime import datetime, timedelta
from typing import List, Optional

from market_data_system.data_process_module.transaction import Transaction
from global_component_id_generator import GlobalComponentIDGenerator
from sortedcontainers import SortedDict


def _update_strike_data(expiration_data: dict, strike: int, transaction: Transaction):
    if strike not in expiration_data:
        expiration_data[strike] = {}
    expiration_data[transaction.strike].update({transaction.type: (transaction.price, transaction.size,
                                                                   transaction.ms_of_day)})


class QuoteBoard:

    # _instnace_tracker = weakref.WeakSet()
    #
    # def __new__(cls, *args, **kwargs):
    #     instance = super(QuoteBoard, cls).__new__(cls)
    #     cls._instnace_tracker.add(instance)
    #     print(f"QuoteBoard init {len(cls._instnace_tracker)}")
    #     return instance

    def __init__(self, **kwargs):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._root = kwargs.get('root')
        self._last_msd: Optional[int] = None  # last msd of the quote board is kinda like current in a way but our
        # quote board is
        # discrete not real time
        self.expirations: Optional[List[int]] = None
        self._quote_date: Optional[
            int] = None  # current quote_date - which quote_date the quoteboard's number is displaying with
        self.strike_range: Optional[dict] = kwargs.get('strike_range', None)
        self.min_strike: Optional[int] = None
        self.max_strike: Optional[int] = None
        self.min_moneyness: Optional[float] = None
        self.max_moneyness: Optional[float] = None
        self.min_maturity: Optional[int] = None  # This should be a number like 4,5,6 for 4 days, 5 days, 6 days
        self.max_maturity: Optional[int] = None
        self._quote_expiration: dict[int, dict[str, SortedDict]] = {}
        self._quote_data: SortedDict = SortedDict()

        if self.strike_range is not None:
            self.min_strike = self.strike_range.get('min', None)
            self.max_strike = self.strike_range.get('max', None)
            self.min_moneyness = self.strike_range.get('minMoneyness', None)
            self.max_moneyness = self.strike_range.get('maxMoneyness', None)

        self.maturity_range: Optional[dict] = kwargs.get('maturity_range', None)
        if self.maturity_range is not None:
            self.min_maturity = self.maturity_range.get('min', None)
            self.max_maturity = self.maturity_range.get('max', None)

    @property
    def id(self):
        return self._id

    @property
    def root(self) -> str:
        return self._root

    @property
    def quote_date(self) -> int:
        return self._quote_date

    @property
    def last_msd(self) -> int:
        return self._last_msd

    def set_time(self, new_time: Optional[int] = None, new_date: Optional[int] = None):
        if new_time is not None:
            self._last_msd = new_time
        if new_date is not None:
            self._quote_date = new_date

    def get_expiration_params(self) -> dict:
        if self._quote_date is None:
            raise ValueError('quote_date has not been set - cannot get expiration params (at least for now)')

        current_date = self._quote_date
        min_expiration = self.min_maturity
        max_expiration = self.max_maturity
        if min_expiration is None:
            min_expiration_date = None
        else:
            min_expiration_date = datetime.strptime(str(current_date), '%Y%m%d') + timedelta(days=min_expiration)
            min_expiration_date = int(min_expiration_date.strftime('%Y%m%d'))
        if max_expiration is None:
            max_expiration_date = None
        else:
            max_expiration_date = datetime.strptime(str(current_date), '%Y%m%d') + timedelta(days=max_expiration)
            max_expiration_date = int(max_expiration_date.strftime('%Y%m%d'))

        expiration_date_params = {
            'min_expiration_date': min_expiration_date,
            'max_expiration_date': max_expiration_date
        }
        return expiration_date_params

    def get_expirations(self) -> List[int]:
        # DONE: quote board should know what expirations (quote_date, int) are available after initialization and
        # pathing
        if self.expirations is None:
            raise ValueError('Expirations have not been initialized')
        return self.expirations

    def set_expirations(self, expirations: List[int]):
        # This function is used by quote manager to set the expirations after pathing
        self.expirations = expirations

    def check_valid_to_initialize(self):
        if self.root is None:
            raise ValueError('root has not been initialized')
        # TODO: check if there exits root folder in the market_data_system source

    def is_initialized(self):
        if self.root is None or self.expirations is None or self._quote_date is None or self._last_msd is None:
            raise ValueError('QuoteBoard has not been initialized')

    def process_transaction(self, transaction: Transaction):
        right = transaction.right
        expiration = transaction.expiration
        expiration_data = self._get_expiration_data(expiration, right)
        _update_strike_data(expiration_data, transaction.strike, transaction)

    def get_quote(self, expiration: int, strike: int, transaction_type: str, right: str):
        expiration_data = self._get_expiration_data(expiration=expiration, right=right)
        if strike not in expiration_data:
            return None
        strike_data = expiration_data[strike]
        return strike_data.get(transaction_type, None)

    def _get_expiration_data(self, expiration: int, right: str) -> dict:
        if expiration not in self._quote_expiration:
            self._quote_expiration[expiration] = {'C': SortedDict(), 'P': SortedDict()}
        return self._quote_expiration[expiration].get(right)
