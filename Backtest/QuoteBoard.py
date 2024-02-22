from datetime import datetime, timedelta
from typing import List, Optional


class QuoteBoard:

    def __init__(self, **kwargs):
        self.root = kwargs.get('root')
        self.quote_date: Optional[int] = kwargs.get('quote_date_range', None)
        self.last_msd: Optional[int] = None  # last msd of the quote board is kinda like current in a way but our
        # quote board is
        # discrete not real time
        self.expirations: Optional[List[int]] = None
        self.current_date: Optional[int] = None  # current date - which date the quoteboard's number is displaying with
        self.strike_range: Optional[dict] = kwargs.get('strike_range', None)
        self.min_strike: Optional[int] = None
        self.max_strike: Optional[int] = None
        self.min_moneyness: Optional[float] = None
        self.max_moneyness: Optional[float] = None
        self.min_maturity: Optional[int] = None  # This should be a number like 4,5,6 for 4 days, 5 days, 6 days
        self.max_maturity: Optional[int] = None

        if self.strike_range is not None:
            self.min_strike = self.strike_range.get('min', None)
            self.max_strike = self.strike_range.get('max', None)
            self.min_moneyness = self.strike_range.get('minMoneyness', None)
            self.max_moneyness = self.strike_range.get('maxMoneyness', None)

        self.maturity_range: Optional[dict] = kwargs.get('maturity_range', None)
        if self.maturity_range is not None:
            self.min_maturity = self.maturity_range.get('min', None)
            self.max_maturity = self.maturity_range.get('max', None)

    def get_root(self) -> str:
        return self.root

    def get_date(self) -> int:
        return self.current_date

    def get_last_msd(self) -> int:
        return self.last_msd

    def set_time(self, new_time: Optional[int] = None, new_date: Optional[int] = None):
        if not new_time:
            self.last_msd = new_time
        if not new_date:
            self.current_date = new_date

    def get_expiration_params(self) -> dict:
        if self.current_date is None:
            raise ValueError('current date has not been set - cannot get expiration params (at least for now)')

        current_date = self.current_date
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

    def get_expirations(self):
        # DONE: quote board should know what expirations (date, int) are available after initialization and pathing
        if self.expirations is None:
            raise ValueError('Expirations have not been initialized')
        return self.expirations

    def set_expirations(self, expirations: List[int]):
        # This function is used by quote manager to set the expirations after pathing
        self.expirations = expirations

    def check_valid_to_initialize(self):
        if self.root is None:
            raise ValueError('root has not been initialized')
        # TODO: check if there exits root folder in the data source

    def is_initailized(self):
        if self.root is None or self.expirations is None or self.current_date is None or self.last_msd is None:
            raise ValueError('QuoteBoard has not been initialized')
