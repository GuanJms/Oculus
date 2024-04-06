from pathlib import Path
from typing import List, Optional, Tuple
from utils.process import CSVReader
from data_server.reader import TimeDataStreamReader
from data_server._enums import AssetDomain, EquityDomain, PriceDomain
from data_server.path import PathManager
from data_server.configuration import ConfigurationManager


# TODO: Add metaclass if there is need to automate update Path process

class StockQuoteReader(TimeDataStreamReader):

    def __init__(self, date: int, root: str):
        super().__init__()
        self._domains = [AssetDomain.EQUITY, EquityDomain.STOCK, PriceDomain.QUOTE]
        self._root = root
        self.set_date(date)

    @property
    def root(self) -> str:
        return self._root

    def set_root(self, root: str):
        self._root = root

    def configure_file(self):
        # Setting file reading type
        domain_config = ConfigurationManager.get_domain_config(domains=self._domains) # type: dict
        self._file_type = domain_config.get("FILE_TYPE", None)
        self._intraday_time_column = domain_config.get("TIME_COLUMN", None)
        self._encoding = domain_config.get("ENCODING", 'utf-8')
        self._delimiter = domain_config.get("DELIMITER", ',')
        if domain_config['HAS_HEADER'] is not None:
            self._has_header = True if domain_config['HAS_HEADER'] == 'True' else False

        # Setting Path
        new_path = PathManager.get_path(domains=self._domains, root=self._root,
                                        date=self._date, file_type=self._file_type)
        self.set_path(new_path)
