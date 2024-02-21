"""
TradedQuoteDataManager manages the data from the quote manager. It will respond to the quote manager's request for data
and go to the data source to get the data. It will then process the data and return the data to the quote manager.
"""

import json
import os
from typing import List, Optional

from DataProcess.TradedQuoteReader import TradedQuoteReader
from utils.pathing import walk_in_process, _update_expiration_dict, _pathing_expirations, generate_path
from utils.process import split_path


class TradedQuoteDataManager:
    def __init__(self, config_file_path: str):
        from Backtest.QuoteManager import QuoteManager
        self.subscribed_quote_managers: List[QuoteManager] = []
        if not os.path.exists(config_file_path):
            raise ValueError('config file does not exist')
        self.config = self.load_config(config_file_path)
        self.root_system = self.config.get('root_system', None)
        self.quote_folder_name = self.config.get('quote_folder_name', None)
        if self.root_system is None:
            raise ValueError('root_system must be specified in the config file')
        self.quote_reader_dict: dict[
            (str, int, int, int), TradedQuoteReader] = {}  # key: root, date, expiration, quote_manager_id; value: TradedQuoteReader
        # self.roots_expiration_dict = {}  # key: root, date

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
        self._config()

    def add_subscription(self, quote_manager):
        self.subscribed_quote_managers.append(quote_manager)

    def remove_subscription(self, quote_manager):
        if quote_manager in self.subscribed_quote_managers:
            self.subscribed_quote_managers.remove(quote_manager)
        else:
            raise ValueError('quote_manager is not subscribed')

        # TODO: remove all the reading streams that are associated with the quote_manager

    def request_data(self, start_msd: int, end_msd: int,
                     root: str, date: int, expiration_params: Optional[dict]) -> dict:
        """
        TradedQuoteDataManager will return the data to the quote manager in dictionary format.
        It will first check if there is corresponding DataReader based on the root, date, and expiration_params
         (which contains the expiration date). If there is, it will read the data from the DataReader.

         Notice: start_msd should equal to last_msd in TradedQuoteReader. If it is not, there will be an inconsistency
         in the background running.
        """

        record_data_to_return = []

        # TODO: Based on the root, date, expiration_params, generate (root, date, expiration) key for next step.
        #   For expiration, we have condition of expiration_params, which contains the min_day and max_day as boundaries
        #   for the expiration date. Check the _update_expiration to first see if the expirations has been updated.
        #   If not, update the expirations first. Then, filter the expiration dates based on (min_date, max_date) and if
        #   the expiration_params is none, then just return all the expiration dates.

        # TODO: check if the needed raeding stream (i.e. if (root, date, expiration) exists in the quote_reader_dict)
        #  has been started in quote_readers; if not start the reading stream
        #  and store that reading stream into the quote_readers dictionary with key (root, date, expiration).
        #  Be careful here, if the reading stream doesnt exist, it means that the reading stream hasnt been started yet.
        #   Thne start_msd is important to pass in as a starting parameter for the reading stream.
        #  Now, we have all reading stream ready.

        # TODO: For each needed reading stream, get the data from the reading stream based on start_msd and end_msd.
        #   During which, check if the start_msd is equal to the last_msd in the reading stream. If not, there is an
        #   inconsistency. If there is an inconsistency, raise an error.
        #  If there is no inconsistency, then read the data from the reading stream up to the end_msd.

        # TODO: process the list return with its header and return the data in dictionary format. If the header is
        #  None ignore that data (that is prob just index, which is not needed). If the data is None, ignore the data
        #  as well. append the data in dictionary format to the record_data_to_return list.

        pass

    def _check_expiration(self, roots: List[str], date: int):
        """
        Check if the expiration dates for the roots and date are available in the expirations dictionary. If not
        available, update the expiration dates for the roots and date.
        """
        for root in roots:
            if (root, date) not in self.expiration_dict:
                self._update_expiration(root, date)

    # def _update_expiration(self, roots: List[str], date: int, quote_folder_name: str):
    #     """
    #     Update the dictionary of expirations with the root and date; Given the pair of root and date, there should be
    #     available expiration dates in the dictionary through checking up the data source.
    #
    #     TODO: write a function based on root and date. And check what is the available expiration dates. Basically
    #          just got to that SPX/raw_traeded_quote/2014/01/ folder and check based on the date, what is the available
    #          expirations dates: xxxxxxxx_20140101.csv. All xxxxxxxx should be put into a list that will be returned and stored
    #          into the self.expirations dictionary with key (root, date).
    #     """
    #     roots_expiration_dict = self.roots_expiration_dict
    #     expiration_dict = self.expiration_dict #expiration_dict = dict(zip(roots, [] * len(roots)))
    #     root_system = self.root_system
    #     year = str(date)[:4]
    #     month = str(date)[4:6]
    #     func = _update_expiration_dict
    #     func_params = dict(date=date, roots_expiration_dict=roots_expiration_dict, expiration_dict=expiration_dict)
    #     condition_params = {quote_folder_name: roots}
    #     walk_in_process(root_system, [quote_folder_name, year, month], func, func_params, condition_params)

    def get_expirations(self, root: str, date: int, expiration_date_params: dict, quote_manager_id: int):
        """
        Pathing the datasource to get the expiration dates for the quote board (root, date, expiration_date_params).
        """
        root_system = self.root_system
        quote_folder_name = self.quote_folder_name
        year = str(date)[:4]
        month = str(date)[4:6]
        func = _pathing_expirations
        func_params = dict(root=root, date=date, expiration_date_params=expiration_date_params)
        condition_params = {quote_folder_name: [root]}
        walk_in_process(root_system, [quote_folder_name, year, month], func, func_params, condition_params)

    def open_stream(self, root: str, date: int, expiration: int, quote_manager_id: int, last_mds: Optional[int] = None):
        """
        self.quote_reader_dict should have key (root, date, expiration, quote_manager_id) and value TradedQuoteReader
        """
        if (root, date, expiration, quote_manager_id) in self.quote_reader_dict:
            raise ValueError('reading stream already exists - use reset_reading_stream to reset the reading stream '
                             '- possible error in initialization of the reading stream')

        root_system = self.root_system
        path = generate_path(root_system=root_system, root=root, date=date,
                             expiration=expiration, quote_type_folder=self.quote_folder_name, extension='csv')
        quote_reader = TradedQuoteReader(path=path, root=root, date=date, expiration=expiration, asset_type='option',
                                         MSD_COL_NAME='ms_of_day')  # TODO: Modify for supporting other asset types
        quote_reader.reset_msd(last_mds) # set the quote_reader reading history to the last_mds
        self.quote_reader_dict[(root, date, expiration, quote_manager_id)] = quote_reader

    def close_stream(self, root: str, date: int, expiration: int, quote_manager_id: int):
        """
        Close the reading stream based on the key (root, date, expiration, quote_manager_id) in the quote_reader_dict.
        """
        if (root, date, expiration, quote_manager_id) not in self.quote_reader_dict:
            raise ValueError('reading stream does not exist')
        self.quote_reader_dict.pop((root, date, expiration, quote_manager_id)) # TODO: test the quote_reader is removed


    def reset_stream(self, root: str, date: int, expiration: int, quote_manager_id: int, sync_time: int):
        """
        Reset the reading stream based on the key (root, date, expiration, quote_manager_id) in the quote_reader_dict.
        """
        if (root, date, expiration, quote_manager_id) not in self.quote_reader_dict:
            raise ValueError('reading stream does not exist')
        quote_reader = self.quote_reader_dict.get((root, date, expiration, quote_manager_id))
        quote_reader.reset_msd(sync_time)


    def _config(self):
        # TODO: should configure the data manager based on the config file and subscribed quote managers
        self._config_roots_expiration_dict()
        raise NotImplementedError

    def _config_roots_expiration_dict(self):
        pass
