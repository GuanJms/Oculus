"""
TradedQuoteDataManager manages the data from the quote manager. It will respond to the quote manager's request for data
and go to the data source to get the data. It will then process the data and return the data to the quote manager.
"""

import json
import os

from Backtest.QuoteManager import QuoteManager


class TradedQuoteDataManager:
    def __init__(self, config_file_path: str):
        self.subscribed_quote_managers = []
        if not os.path.exists(config_file_path):
            raise ValueError('config file does not exist')
        self.config = self.load_config(config_file_path)
        self.root_system = self.config.get('root_system', None)
        if self.root_system is None:
            raise ValueError('root_system must be specified in the config file')

    def load_config(self, config_file: str) -> dict:
        with open(config_file, 'r') as file:
            return json.load(file)

    def get_file_path(self, relative_path: str):
        return os.path.join(self.root_system, relative_path)

    def is_connected(self) -> bool:
        if self.root_system is None or not os.path.exists(self.root_system):
            return False
        return True

    def connect(self, quote_manager: QuoteManager):
        if not isinstance(quote_manager, QuoteManager):
            raise ValueError('quote_manager must be QuoteManager')
        if not self.is_connected():
            raise ValueError('data manager is not connected')
        self.add_subscription(quote_manager)

    def add_subscription(self, quote_manager: QuoteManager):
        self.subscribed_quote_managers.append(quote_manager)

    def remove_subscription(self, quote_manager: QuoteManager):
        if quote_manager in self.subscribed_quote_managers:
            self.subscribed_quote_managers.remove(quote_manager)
        else:
            raise ValueError('quote_manager is not subscribed')


