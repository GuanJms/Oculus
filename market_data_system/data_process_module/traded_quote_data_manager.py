"""
TradedQuoteDataManager manages the market_data_system from the quote manager. It will respond to the quote manager's request for market_data_system
and go to the market_data_system source to get the market_data_system. It will then process the market_data_system and return the market_data_system to the quote manager.
"""

import json
import os
from typing import List, Optional, Tuple

from utils.global_id.configuration.configuration_manager import ConfigurationManager
from market_data_system.data_process_module.traded_quote_reader import TradedQuoteReader
from utils.pathing import walk_in_process, pathing_expirations, generate_path


class TradedQuoteDataManager:
    def __init__(self, config_file_path: str):
        from quote_module.quote_manager import QuoteManager
        self.subscribed_quote_managers: List[QuoteManager] = []
        if not os.path.exists(config_file_path):
            raise ValueError('config file does not exist')
        self.root_system: str = ConfigurationManager.get_root_system()
        self.quote_folder_name: str = ConfigurationManager.get_quote_folder_name()
        self.quote_reader_dict: dict[
            (str, int, int,
             str), TradedQuoteReader] = {}  # key: root, quote_date, expiration, quote_manager_id; value: TradedQuoteReader
        # self.roots_expiration_dict = {}  # key: root, quote_date

    def load_config(self, config_file: str) -> dict:
        with open(config_file, 'r') as file:
            return json.load(file)

    def get_file_path(self, relative_path: str) -> str:
        return os.path.join(self.root_system, relative_path)

    def is_connected(self) -> bool:
        if self.root_system is None or not os.path.exists(self.root_system):
            return False
        return True

    def connect(self, quote_manager):
        from quote_module.quote_manager import QuoteManager
        if not isinstance(quote_manager, QuoteManager):
            raise ValueError('quote_manager must be QuoteManager')
        if not self.is_connected():
            raise ValueError('market_data_system manager is not connected')
        self.add_subscription(quote_manager)

    def add_subscription(self, quote_manager):
        self.subscribed_quote_managers.append(quote_manager)

    def remove_subscription(self, quote_manager):
        if quote_manager in self.subscribed_quote_managers:
            self.subscribed_quote_managers.remove(quote_manager)
        else:
            raise ValueError('quote_manager is not subscribed')
        raise NotImplementedError
        # TODO: remove all the reading streams that are associated with the quote_manager

    def request_data(self, start_msd: int, end_msd: int,
                     root: str, date: int, expiration: int, quote_manager_id: str, status: str) \
            -> Tuple[List[str], List[List[str]], str]:
        """
        TradedQuoteDataManager will return the market_data_system to the quote manager in dictionary format.
        It will first check if there is corresponding DataReader based on the root, quote_date, and expiration_params
         (which contains the expiration quote_date). If there is, it will read the market_data_system from the DataReader.

         Notice: start_msd should equal to last_msd in TradedQuoteReader. If it is not, there will be an inconsistency
         in the background running.
         status = "DONE" (should not been passed in) , "ONGOING", "FIRST-RUN"
        """
        if (root, date, expiration, quote_manager_id) not in self.quote_reader_dict:
            raise ValueError('reading stream does not exist')
        quote_reader = self.quote_reader_dict.get((root, date, expiration, quote_manager_id))
        if start_msd != quote_reader.get_last_msd():
            raise ValueError('start_msd should equal to last_msd in TradedQuoteReader, unless you are jumping ahead '
                             'in time - if so do read_until_msd function in the future')
        header = quote_reader.get_header()
        # TODO: refactor and make a method for checking
        if quote_reader.get_next_msd() is None or quote_reader.get_next_msd() > end_msd:
            quote_reader.last_msd = end_msd # set the last_msd to the end_msd
            return header, [], "DONE"
        raw_data, status = quote_reader.read_until_msd(end_msd)
        return header, raw_data, status

    def update_expirations(self, root: str, date: int, expiration_date_params: dict):
        """
        Pathing the datasource to get the expiration dates for the quote board (root, quote_date, expiration_date_params).
        """
        root_system = self.root_system
        quote_folder_name = self.quote_folder_name
        year = str(date)[:4]
        month = str(date)[4:6]
        func = pathing_expirations
        func_params = dict(root=root, date=date, expiration_date_params=expiration_date_params)
        condition_params = {quote_folder_name: [root]}
        walk_in_process(root_system, [quote_folder_name, year, month], func, func_params, condition_params)

    def _open_stream(self, root: str, date: int, expiration: int, quote_manager_id: str, last_mds: Optional[int] = None):
        """
        self.quote_reader_dict should have key (root, quote_date, expiration, quote_manager_id) and value TradedQuoteReader
        """
        if self._check_stream_exist(root, date, expiration, quote_manager_id, soft_check=True):
            raise ValueError('reading stream already exists - use reset_reading_stream to reset the reading stream '
                             '- possible error in initialization of the reading stream')

        root_system = self.root_system
        path = generate_path(root_system=root_system, root=root, date=date,
                             expiration=expiration, quote_type_folder=self.quote_folder_name, extension='csv')
        quote_reader = TradedQuoteReader(path=path, root=root, date=date, expiration=expiration, asset_type='option',
                                         MSD_COL_NAME='ms_of_day')  # TODO: Modify for supporting other asset types
        quote_reader.reset_msd(last_mds)  # set the quote_reader reading history to the last_mds
        self.quote_reader_dict[(root, date, expiration, quote_manager_id)] = quote_reader

    def _close_stream(self, root: str, date: int, expiration: int, quote_manager_id: str):
        """
        Close the reading stream based on the key (root, quote_date, expiration, quote_manager_id) in the quote_reader_dict.
        """
        self._check_stream_exist(root, date, expiration, quote_manager_id)
        self.quote_reader_dict.pop((root, date, expiration, quote_manager_id))  # TODO: test the quote_reader is removed

    def request_close_stream(self, root: str, date: int, expiration: int, quote_manager_id: str):
        self._close_stream(root, date, expiration, quote_manager_id)

    def request_open_stream(self, root: str, date: int, expiration: int, quote_manager_id: str,
                            last_mds: Optional[int] = None):
        self._open_stream(root=root, date=date, expiration=expiration, quote_manager_id=quote_manager_id,
                          last_mds=last_mds)

    def reset_stream(self, root: str, date: int, expiration: int, quote_manager_id: str, sync_time: int):
        """
        Reset the reading stream based on the key (root, quote_date, expiration, quote_manager_id) in the quote_reader_dict.
        """
        self._check_stream_exist(root, date, expiration, quote_manager_id)
        quote_reader = self.quote_reader_dict.get((root, date, expiration, quote_manager_id))
        quote_reader.reset_msd(sync_time)

    def _check_stream_exist(self, root: str, date: int, expiration: int,
                            quote_manager_id: str, soft_check: bool = False) -> bool:
        if soft_check:
            return (root, date, expiration, quote_manager_id) in self.quote_reader_dict
        else:
            if (root, date, expiration, quote_manager_id) not in self.quote_reader_dict:
                raise ValueError('reading stream does not exist')
