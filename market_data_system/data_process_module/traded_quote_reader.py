from collections import deque
from typing import List, Optional, Tuple
from utils.global_id.configuration.configuration_manager import ConfigurationManager
from utils.process import CSVReader


class TradedQuoteReader:

    #
    # _instnace_tracker = weakref.WeakSet()
    #
    # def __new__(cls, *args, **kwargs):
    #     instance = super(TradedQuoteReader, cls).__new__(cls)
    #     cls._instnace_tracker.add(instance)
    #     print(f"TradedQuoteReader init {len(cls._instnace_tracker)}")
    #     return instance


    def __init__(self, path: str, root: str, date: int, asset_type: str,
                 MSD_COL_NAME: str, expiration: int = None, max_row_reading_batch: int = 1000, ):
        """
        TradeQuoteReader is a class that reads the traded quote market_data_system from the csv file.
        It reads the market_data_system in batch and do processing in batch, that incldues return the header,
        read the market_data_system until a certain time, record the last ms_of_day read, and record the next ms_of_day to read.

        :param path: the path of the csv file
        :param root: the root of the traded quote, e.g. SPX
        :param date: the quote quote_date of the traded quote
        :param expiration: the expiration quote_date of option train in the traded quote
        :param reading_size: the size of the batch to read the market_data_system
        """

        if asset_type not in ['option', 'stock']:
            raise ValueError('Asset type not supported')
        if path.split('.')[-1] not in ['csv']:
            raise ValueError('File type not supported')
        if asset_type == 'option' and expiration is None:
            raise ValueError('Expiration quote_date is required for option')

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
        self.header: Optional[List[str]] = None
        self.MSD_COL_NAME_IX: Optional[int] = None
        self.open_status: bool = False
        self._max_reading_batch = ConfigurationManager.get_max_reading_batch()

    def get_last_msd(self) -> int:
        return self.last_msd

    def reset_msd(self, msd: int):
        # TODO: reset the msd to the given msd (i.e. reopen the stream and read until the given msd)
        self.open_stream(msd)

    def get_header(self):
        if self.header is not None:
            return self.header
        else:
            raise ValueError('Stream is not open')

    def read_until_msd(self, msd: int) -> Tuple[List[List[str]], str]:
        record_to_return = []
        status = "DONE"
        if self.peek_msd() is None:
            self.last_msd = msd
            return record_to_return, status
        while self.peek_msd() <= msd:
            record_to_return.append(self.next())
            if self.peek_msd() is None:
                break
            if len(record_to_return) >= self._max_reading_batch:
                status = "ONGOING"
                break
        if len(record_to_return) > 0:
            # self.last_msd = int(record_to_return[-1][self.MSD_COL_NAME_IX])
            self.next_msd = self.peek_msd()
        if status == "DONE":
            self.last_msd = msd
        # DONE: write a function to check if the stream is empty and close the stream if it is empty
        if self.stream.is_empty() and len(self.data_cache) == 0:
            self.open_status = False
        else:
            self.open_status = True
        return record_to_return, status

    def peek_msd(self) -> Optional[int]:
        if len(self.data_cache) == 0:
            self._read_batch()
        if len(self.data_cache) == 0:
            return None
        return int(self.data_cache[0][self.MSD_COL_NAME_IX])

    def next(self) -> Optional[List[str]]:
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
        Read the batch of the market_data_system
        """
        for i in range(self.max_row_reading_batch):
            if self.stream.empty:
                break
            else:
                self.data_cache.append(next(self.stream))

    # def reset_stream(self):
    #     self._open_stream()

    def open_stream(self, start_msd: int):
        self.data_cache = deque()
        self.stream = CSVReader(self.path)
        self.header = next(self.stream)
        self.MSD_COL_NAME_IX: int = self.header.index(self.MSD_COL_NAME)

        _, reading_status = self.read_until_msd(start_msd)
        while reading_status == "ONGOING":
            _, reading_status = self.read_until_msd(start_msd)


    # TODO: modify the functions such at the end of the file, the stream will be closed automatically and marked as
    #  closed. So it wont allow to read the market_data_system again.
