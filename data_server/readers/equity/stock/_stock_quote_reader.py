from pathlib import Path
from typing import List, Optional, Tuple
from utils.process import CSVReader
from ..._time_data_reader import TimeDataStreamReader
from ...._enums import AssetDomain, EquityDomain
from ....path import PathManager

# TODO: Add metaclass if there is need to automate update Path process

class StockQuoteReader(TimeDataStreamReader):

    def __init__(self, date: int, root: str):
        super().__init__()
        self._domains = [AssetDomain.EQUITY, EquityDomain.STOCK]
        self._root = root
        self.set_date(date)

    @property
    def root(self) -> str:
        return self._root

    def set_root(self, root: str):
        self._root = root

    def update_file_path(self):
        file_path = PathManager.get_path(domains=self._domains, root=self._root, date=self._date)
        self.open_stream(file_path, has_header=True) # TODO: Add DataSchemaManager to get header
