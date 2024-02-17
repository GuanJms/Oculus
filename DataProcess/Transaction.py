from datetime import datetime
class Transaction:
    def __init__(self, **kwargs):
        self.root = kwargs.get('root', None)
        self.strike = kwargs.get('strike', None)
        self.right = kwargs.get('right', None)
        self.expiration = kwargs.get('expiration', None)
        self.price = kwargs.get('price', None)
        self.type = kwargs.get('type', None)
        self.ms_of_day = kwargs.get('ms_of_day', None)
        self.condition = kwargs.get('condition', None)
        self.exchange = kwargs.get('exchange', None)
        self.size = kwargs.get('size', None)
        self.condition_flags = kwargs.get('condition_flags', None)
        self.price_flags = kwargs.get('price_flags', None)
        self.volume_type = kwargs.get('volume_type', None)
        self.ms_of_day2 = kwargs.get('ms_of_day2', None)
        self.bid = kwargs.get('bid', None)
        self.bid_size = kwargs.get('bid_size', None)
        self.ask_size = kwargs.get('ask_size', None)
        self.bid_exchange = kwargs.get('bid_exchange', None)
        self.bid_condition = kwargs.get('bid_condition', None)
        self.ask_exchange = kwargs.get('ask_exchange', None)
        self.ask = kwargs.get('ask', None)
        self.ask_condition = kwargs.get('ask_condition', None)
        self.date = kwargs.get('date', None)
        self.DTE = None

        if self.expiration is not None and self.date is not None:
            # calculate DTE from expiration and date
            _expiration = datetime.strptime(str(self.expiration), '%Y%m%d')
            _date = datetime.strptime(str(self.date), '%Y%m%d')

    def get_params(self):
        return {
            'root': self.root,
            'strike': self.strike,
            'right': self.right,
            'expiration': self.expiration,
            'price': self.price,
            'type': self.type,
            'ms_of_day': self.ms_of_day,
            'condition': self.condition,
            'exchange': self.exchange,
            'size': self.size,
            'condition_flags': self.condition_flags,
            'price_flags': self.price_flags,
            'volume_type': self.volume_type,
            'ms_of_day2': self.ms_of_day2,
            'bid': self.bid,
            'bid_size': self.bid_size,
            'ask_size': self.ask_size,
            'bid_exchange': self.bid_exchange,
            'bid_condition': self.bid_condition,
            'ask_exchange': self.ask_exchange,
            'ask': self.ask,
            'ask_condition': self.ask_condition,
            'date': self.date,
            'DTE': self.DTE
        }

    def get_root(self):
        return self.root

    def get_DTE(self):
        return self.DTE

    def get_strike(self):
        return self.strike

    def get_right(self):
        return self.right

    def get_expiration(self):
        return self.expiration

    def get_price(self):
        return self.price

    def get_type(self):
        return self.type

    def get_ms_of_day(self):
        return self.ms_of_day

    def get_bid(self):
        return self.bid

    def get_ask(self):
        return self.ask

    def get_bid_size(self):
        return self.bid_size

    def get_ask_size(self):
        return self.ask_size

    def get_exchange(self):
        return self.exchange

    def get_date(self):
        return self.date

    def get_expirtion(self):
        return self.expiration
