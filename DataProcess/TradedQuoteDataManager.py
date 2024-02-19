"""
TradedQuoteDataManager manages the data from the quote manager. It will respond to the quote manager's request for data
and go to the data source to get the data. It will then process the data and return the data to the quote manager.
"""

import json
import os
from typing import List, Optional

class TradedQuoteDataManager:
    def __init__(self, config_file_path: str):
        self.subscribed_quote_managers = []
        if not os.path.exists(config_file_path):
            raise ValueError('config file does not exist')
        self.config = self.load_config(config_file_path)
        self.root_system = self.config.get('root_system', None)
        if self.root_system is None:
            raise ValueError('root_system must be specified in the config file')
        self.quote_readers = {} # key: root, date, expiration
        self.expirations = {} # key: root, date

    def load_config(self, config_file: str) -> dict:
        with open(config_file, 'r') as file:
            return json.load(file)

    def get_file_path(self, relative_path: str):
        return os.path.join(self.root_system, relative_path)

    def is_connected(self) -> bool:
        if self.root_system is None or not os.path.exists(self.root_system):
            return False
        return True

    def connect(self, quote_manager):
        from Backtest.QuoteManager import QuoteManager
        if not isinstance(quote_manager, QuoteManager):
            raise ValueError('quote_manager must be QuoteManager')
        if not self.is_connected():
            raise ValueError('data manager is not connected')
        self.add_subscription(quote_manager)

    def add_subscription(self, quote_manager):
        self.subscribed_quote_managers.append(quote_manager)

    def remove_subscription(self, quote_manager):
        if quote_manager in self.subscribed_quote_managers:
            self.subscribed_quote_managers.remove(quote_manager)
        else:
            raise ValueError('quote_manager is not subscribed')


    def request_data(self, start_msd: int, end_msd: int,
                     root: str, date : int, expiration_params: Optional[dict]) -> dict:
        """
        TradedQuoteDataManager will return the data to the quote manager in dictionary format.
        It will first check if there is corresponding DataReader based on the root, date, and expiration_params
         (which contains the expiration date). If there is, it will read the data from the DataReader.

         Notice: start_msd should equal to last_msd in TradedQuoteReader. If it is not, there will be an inconsistency
         in the background running.
        """

        # TODO: Based on the root, date, expiration_params, generate (root, date, expiration) key for next step.
        #   For expiration, we have condition of expiration_params, which contains the min_day and max_day as boundaries
        #   for the expiration date. Check the _update_expiration to first see if the expirations has been updated.
        #   If not, update the expirations first. Then, filter the expiration dates based on (min_date, max_date) and if
        #   the expiration_params is none, then just return all the expiration dates.



        # TODO: check if the needed raeding stream has been started in quote_readers; if not start the reading stream
        #  and store that reading stream into the quote_readers dictionary with key (root, date, expiration)

        # TODO:




        pass

    def _update_expiration(self, root: str, date: int):
        """
        Update the dictionary of expirations with the root and date; Given the pair of root and date, there should be
        available expiration dates in the dictionary through checking up the data source.
        
        TODO: write a function based on root and date. And check what is the available expiration dates. Basically
             just got to that SPX/raw_traeded_quote/2014/01/ folder and check based on the date, what is the available
             expirations dates: xxxxxxxx_20140101.csv. All xxxxxxxx should be put into a list that will be returned and stored
             into the self.expirations dictionary with key (root, date).
        """
        pass






