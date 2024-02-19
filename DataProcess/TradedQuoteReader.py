from collections import deque
from typing import List, Iterable, Optional

from utils.process import CSVReader


class TradedQuoteReader:
    def __init__(self, path: str, root: str, date: int, asset_type: str, expiration: int = None,
                 max_row_reading_batch: int = 1000, MSD_COL_NAME: str = 'ms_of_day'):
        """
        TradeQuoteReader is a class that reads the traded quote data from the csv file.
        It reads the data in batch and do processing in batch, that incldues return the header,
        read the data until a certain time, record the last ms_of_day read, and record the next ms_of_day to read.

        :param path: the path of the csv file
        :param root: the root of the traded quote, e.g. SPX
        :param date: the quote date of the traded quote
        :param expiration: the expiration date of option train in the traded quote
        :param reading_size: the size of the batch to read the data
        """

        if asset_type not in ['option', 'stock']:
            raise ValueError('Asset type not supported')
        if path.split('.')[-1] not in ['csv']:
            raise ValueError('File type not supported')
        if asset_type == 'option' and expiration is None:
            raise ValueError('Expiration date is required for option')

        self.path = path
        self.MSD_COL_NAME = MSD_COL_NAME
        self.asset_type = asset_type
        self.file_type = path.split('.')[-1]
        self.root = root
        self.date = date
        self.expiration = expiration
        self.max_row_reading_batch = max_row_reading_batch
        self.last_msd: int = 0
        self.next_msd: int = 0
        self.data_cache: deque = deque()
        self.stream: Optional[CSVReader] = None
        self.header:Optional[List[str]] = None
        self.MSD_COL_NAME_IX: Optional = None
        self.open_stream()

    def get_header(self):
        return self.header

    def read_until_msd(self, msd: int):
        record_to_return = []
        if self.peek_msd() is None:
            return record_to_return
        while self.peek_msd() <= msd:
            record_to_return.append(self.next())
            if self.peek_msd() is None:
                break
        if len(record_to_return) > 0:
            self.last_msd = int(record_to_return[-1][self.MSD_COL_NAME_IX])
            self.next_msd = self.peek_msd()
        return record_to_return

    def peek_msd(self):

        if len(self.data_cache) == 0:
            self._read_batch()
        if len(self.data_cache) == 0:
            return None
        return int(self.data_cache[0][self.MSD_COL_NAME_IX])

    def next(self):
        if len(self.data_cache) == 0:
            self._read_batch()
        if len(self.data_cache) == 0:
            return None
        else:
            return self.data_cache.popleft()

    def get_prev_msd(self):
        return self.last_msd

    def get_next_msd(self):
        return self.next_msd

    def _read_batch(self):
        """
        Read the batch of the data
        """
        for i in range(self.max_row_reading_batch):
            if self.stream.empty:
                break
            else:
                self.data_cache.append(next(self.stream))

    def reset_stream(self):
        self.open_stream()

    def open_stream(self):
        self.data_cache = deque()
        self.stream = CSVReader(self.path)
        self.header = next(self.stream)
        self.MSD_COL_NAME_IX = self.header.index(self.MSD_COL_NAME)
