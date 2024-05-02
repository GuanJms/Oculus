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