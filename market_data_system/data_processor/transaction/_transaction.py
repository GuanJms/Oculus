from typing import Optional, Any

from utils.global_id.configuration.configuration_manager import ConfigurationManager


class Transaction:
    MSD_COL_NAME = ConfigurationManager.get_MSD_COL_NAME()
    MSD_COL_NAME_SECONDARY = ConfigurationManager.get_MSD_COL_NAME_SECONDARY()
    traded_quote_transaction_attributes = ['root', 'type', 'strike', 'right', 'expiration', 'price', 'condition',
                                           'exchange', 'size', 'condition_flags', 'price_flags', 'volume_type',
                                           MSD_COL_NAME, MSD_COL_NAME_SECONDARY,
                                           'bid', 'bid_size', 'ask_size', 'bid_exchange', 'bid_condition',
                                           'ask_exchange',
                                           'ask', 'ask_condition', 'quote_date']

    def __init__(self, **kwargs):
        for attribute in Transaction.traded_quote_transaction_attributes:
            setattr(self, f"_{attribute}", kwargs.get(attribute, None))

    def get_params(self) -> dict[str, Optional]:
        # TODO: needs testing! Not sure if the code is correct
        all_params = {key: value for key, value in vars(self).items() if value is not None}
        return all_params

    def get_param(self, param: str) -> Optional[Any]:
        # check if the param exists
        if not param.startswith('_'):
            private = f"_{param}"
            if hasattr(self, private):
                return getattr(self, private)

        if hasattr(self, param):
            return getattr(self, param)

        return None

    def __str__(self):
        return str(self.get_params())

# {'': '3432', 'root': 'SPX', 'expiration': '20240216', 'strike': '5200000', 'right': 'C',
# 'ms_of_day': '3916031', 'sequence': '591691650', 'ext_condition1': '255', 'ext_condition2': '255',
# 'ext_condition3': '255', 'ext_condition4': '255', 'condition': '18', 'size': '1', 'exchange': '5',
# 'price': '0.35', 'condition_flags': '0', 'price_flags': '1', 'volume_type': '0', 'records_back': '0',
# 'ms_of_day2': '3916031', 'bid_size': '968', 'bid_exchange': '5', 'bid': '0.25', 'bid_condition': '50',
# 'ask_size': '100', 'ask_exchange': '5', 'ask': '0.35', 'ask_condition': '50', 'quote_date': '20240206'}


#
# self._root: str = kwargs.get('root')
# self._type: str = kwargs.get('type')
#
# self._strike: Optional[int] = kwargs.get('strike', None)
# self._right: Optional[str] = kwargs.get('right', None)
# self._expiration: Optional[int] = kwargs.get('expiration', None)
# self._price: Optional[float] = kwargs.get('price', None)
# self._ms_of_day: Optional[int] = kwargs.get(self.MSD_COL_NAME, None)
# self._condition: Optional[int] = kwargs.get('condition', None)
# self._exchange: Optional[int] = kwargs.get('exchange', None)
# self._size: Optional[int] = kwargs.get('size', None)
# self._condition_flags: Optional[int] = kwargs.get('condition_flags', None)
# self._price_flags: Optional[int] = kwargs.get('price_flags', None)
# self._volume_type: Optional[int] = kwargs.get('volume_type', None)
# self._ms_of_day2: Optional[int] = kwargs.get(self.MSD_COL_NAME_SECONDARY, None)
# self._bid: Optional[float] = kwargs.get('bid', None)
# self._bid_size: Optional[int] = kwargs.get('bid_size', None)
# self._ask_size: Optional[int] = kwargs.get('ask_size', None)
# self._bid_exchange: Optional[int] = kwargs.get('bid_exchange', None)
# self._bid_condition: Optional[int] = kwargs.get('bid_condition', None)
# self._ask_exchange: Optional[int] = kwargs.get('ask_exchange', None)
# self._ask: Optional[float] = kwargs.get('ask', None)
# self._ask_condition: Optional[int] = kwargs.get('ask_condition', None)
# self._date: Optional[int] = kwargs.get('quote_date', None)

# self.DTE: Optional[int] = None
#
# if self.expiration is not None and self.quote_date is not None:
#     # calculate DTE from expiration and quote_date
#     _expiration = datetime.strptime(str(self.expiration), '%Y%m%d')
#     _date = datetime.strptime(str(self.quote_date), '%Y%m%d')
