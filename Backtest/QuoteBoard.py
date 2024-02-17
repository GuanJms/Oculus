class QuoteBoard:

    def __init__(self, **kwargs):
        self.root = kwargs.get('root', None)
        self.quote_date = kwargs.get('quote_date_range', None)
        if self.quote_date is not None:
            self.start_date = self.quote_date.get('start_date', None)
            self.end_date = self.quote_date.get('end_date', None)
            self.current_date = self.quote_date.get('current_date', None)
        else:
            self.start_date = None
            self.end_date = None
            self.current_date = None
        self.strike_range = kwargs.get('strike_range', None)
        if self.strike_range is not None:
            self.min_strike = self.strike_range.get('min', None)
            self.max_strike = self.strike_range.get('max', None)
            self.min_moneyness = self.strike_range.get('minMoneyness', None)
            self.max_moneyness = self.strike_range.get('maxMoneyness', None)
        else:
            self.min_strike = None
            self.max_strike = None
            self.min_moneyness = None
            self.max_moneyness = None
        self.maturity_range = kwargs.get('maturity_range', None)
        if self.maturity_range is not None:
            self.min_maturity = self.maturity_range.get('min', None)
            self.max_maturity = self.maturity_range.get('max', None)
        else:
            self.min_maturity = None
            self.max_maturity = None

    def get_root(self) -> str:
        return self.root



