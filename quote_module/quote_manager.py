import weakref

from data_process_module.transaction_factory import TransactionFactory
from global_component_id_generator import GlobalComponentIDGenerator
from global_time_generator import GlobalTimeGenerator
from quote_module.quote_board import QuoteBoard
from data_process_module.transaction import Transaction
from data_process_module.transaction_queue import TransactionQueue
from data_process_module.traded_quote_data_manager import TradedQuoteDataManager
from typing import List, Optional, Tuple

"""
Queue manager is the class that manages the quote boards and the transaction queue
It takes in a data manager and a frequency to update the quote boards.
Based on the frequency, it will request data from the data manager and process the data stream and push the data to the 
subscribed quote boards with corresponding roots.
"""


def _aggregate_sync_request_params_to_list(sync_request_list: list, root: str, date: int, sync_time: int,
                                           expiration: int):
    # DONE: aggregate the sync request params to the sync_request_params with key (root, quote_date)
    new_request_params = {'root': root,
                          'quote_date': date,
                          'expiration': expiration,
                          'sync_time': sync_time}
    sync_request_list.append(new_request_params)


class QuoteManager:
    #
    # _instnace_tracker = weakref.WeakSet()
    #
    # def __new__(cls, *args, **kwargs):
    #     instance = super(QuoteManager, cls).__new__(cls)
    #     cls._instnace_tracker.add(instance)
    #     print(f"TradedQuoteReader init {len(cls._instnace_tracker)}")
    #     return instance

    def __init__(self, MSD_COL_NAME: str, frequency: int = 60000):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self.data_manager: Optional[TradedQuoteDataManager] = None
        self.frequency: int = frequency
        self.MSD_COL_NAME: str = MSD_COL_NAME
        self._transaction_queue: TransactionQueue = TransactionQueue(default_sort=False, sort_key=MSD_COL_NAME)
        self._quote_board_list: List[QuoteBoard] = []
        self._root_quote_board_list_dict: dict[str, List[QuoteBoard]] = {}  # key: root, value: list of quote boards
        self._quote_board_dict: dict[(str, int), QuoteBoard] = {}  # key: (root, expiration), value: QuoteBoard
        self._last_msd: Optional[int] = None
        self._quote_date: Optional[int] = None
        self._on_process: bool = False

    @property
    def id(self):
        return self._id

    @property
    def last_msd(self):
        return self._last_msd

    @property
    def quote_date(self):
        return self._quote_date

    def initialize(self, data_manager: TradedQuoteDataManager, quote_date: int, msd: int):
        self.connect_data_manager(data_manager)
        self._set_date_and_time(date=quote_date, msd=msd)

    def is_connected(self) -> bool:
        if self.data_manager is None:
            return False
        elif not self.data_manager.is_connected():
            return False
        return True

    def _delete_quote_board_from_list(self, quote_board: QuoteBoard):
        if quote_board in self._quote_board_list:
            self._quote_board_list.remove(quote_board)

    def delete_all_quote_board_list(self):
        # TODO: maybe make it asynchronous in the future
        for quote_board in self._quote_board_list:
            self._delete_quote_board(quote_board)

    def _request_delete_quote_board_stream(self, quote_board: QuoteBoard):
        root = quote_board.root
        date = quote_board.quote_date
        expirations = quote_board.get_expirations()
        quote_manager_id = self.id
        for expiration in expirations:
            self.data_manager.request_close_stream(root, date, expiration, quote_manager_id)

    def connect_data_manager(self, data_manager: TradedQuoteDataManager):
        # Check if data_manager is TradedQuoteDataManager
        if not isinstance(data_manager, TradedQuoteDataManager):
            raise ValueError('data_manager must be TradedQuoteDataManager')
        self.data_manager = data_manager
        data_manager.connect(self)

    def _set_quote_date(self, date: int):
        if not isinstance(date, int):
            raise ValueError('quote_date must be int')
        self._quote_date = date

    def _set_last_msd(self, msd: int):
        if not isinstance(msd, int):
            raise ValueError('msd must be int')
        self._last_msd = msd

    def set_frequency(self, frequency: int):
        self.frequency = frequency

    def _configure(self):
        if not self.is_connected():
            raise ValueError('data manager is not connected')
        self._configure_subscribed_quote_boards()

    def _advance_time_quote_board(self, quote_board: QuoteBoard, start_msd: int, end_msd: int):
        root = quote_board.root
        date = quote_board.quote_date
        expirations = quote_board.get_expirations()
        for expiration in expirations:
            status = 'FIRST-RUN'
            while status == 'ONGOING' or status == 'FIRST-RUN':
                new_transactions, status = self._request_data(start_msd=start_msd, end_msd=end_msd, root=root, date=date,
                                                              expiration=expiration, status=status)
                process_request = self._transaction_queue.add_transactions(new_transactions, message_request=True)
                if process_request == "PROCESS-QUEUE-REQUEST":
                    self._process_queue()

    def _advance_time(self, delta_time_ms: int):
        self._turn_on_process()
        start_msd = self._last_msd
        end_msd = start_msd + delta_time_ms
        quote_board_to_advance = self._quote_board_list
        for quote_board in quote_board_to_advance:
            self._advance_time_quote_board(quote_board, start_msd, end_msd)
        self._process_queue()
        if self._transaction_queue.empty():
            self._set_last_msd(end_msd)

    def request_advance_time(self, delta_time_ms: int = None):
        """
        :param delta_time_ms: milliseconds to advance the time; default is the frequency and for most cases it should be
        None
        :return:
        """
        if delta_time_ms is None:
            delta_time_ms = self.frequency
        self._advance_time(delta_time_ms)

    def request_advance_date(self, quote_date: int, start_ms_of_day: int):
        self._turn_on_process()
        self._set_date_and_time(date=quote_date, msd=start_ms_of_day)

    def get_process_status(self) -> str:
        if self._get_on_process():
            return 'ON'
        else:
            return 'OFF'

    def _request_data(self, start_msd: int, end_msd: int, root: str, date: int, expiration: int, status: str) \
            -> Tuple[List[Transaction], str]:
        # TODO: check test for this function
        # print(self.__class__.__name__, 'request_data', f"start_msd: {start_msd}, end_msd: {end_msd}, "
        #                                                f"root: {root}, date: {date}, expiration: {expiration}"
        #       f"quote_manager_id: {self.id}")
        header, transactions_raw, status = self.data_manager.request_data(start_msd=start_msd,
                                                                          end_msd=end_msd,
                                                                          root=root,
                                                                          date=date,
                                                                          expiration=expiration,
                                                                          quote_manager_id=self.id,
                                                                          status=status)
        transaction_list = TransactionFactory.process_raw_transaction_list(header, transactions_raw)
        return transaction_list, status

    def _get_transaction_queue(self) -> TransactionQueue:
        return self._transaction_queue

    def _process_queue(self):
        self._transaction_queue.sort()
        while not self._transaction_queue.empty():
            transaction = self._transaction_queue.next()
            self._process_transaction(transaction)

    def _process_transaction(self, transaction: Transaction):
        root = transaction.root
        quote_boards = self._root_quote_board_list_dict.get(root, [])
        if len(quote_boards) == 0:
            return
        for quote_board in quote_boards:
            quote_board.process_transaction(transaction)

    def add_quote_board(self, quote_board: QuoteBoard):
        self._check_initialized()
        quote_board.check_valid_to_initialize()
        if not QuoteManager.check_existed_quote_board(quote_board, quote_boards=self._quote_board_list):
            self.initialize_quote_board(quote_board)

    def get_quote_board_list(self) -> List[QuoteBoard]:
        return self._quote_board_list

    def get_quote_board_list_by_root(self, root: str) -> List[QuoteBoard]:
        return self._root_quote_board_list_dict.get(root, [])

    def _delete_quote_board(self, quote_board: QuoteBoard):
        self._request_delete_quote_board_stream(quote_board)
        self._remove_quote_board_from_dict(quote_board)
        self._remove_quote_board_from_root_quote_board_list_dict(quote_board)
        self._delete_quote_board_from_list(quote_board)

    @classmethod
    def check_existed_quote_board(cls, quote_board: QuoteBoard, quote_boards: List[QuoteBoard]) -> bool:
        # TODO: assign unique ID to the quote board every time it is created, and check uniqueness based on the ID
        return quote_board in quote_boards

    def get_min_last_msd_in_quote_boards(self) -> int:
        # DONE: get the minimum ms_of_day in the ms_of_day_range of the quote boards
        min_msd = None
        for quote_board in self._quote_board_list:
            last_msd = quote_board.last_msd
            if min_msd is None or last_msd < min_msd:
                min_msd = last_msd
        return min_msd

    def get_min_date_in_quote_boards(self):
        min_date = None
        for quote_board in self._quote_board_list:
            start_date = quote_board.quote_date
            if min_date is None or start_date < min_date:
                min_date = start_date
        return min_date

    def initialize_quote_board(self, quote_board: QuoteBoard, reinitialize: bool = False):
        # DONE: pathing the quote board to get the expirations and initialize the expirations in the quote board
        self._check_initialized()
        quote_board.check_valid_to_initialize()
        if not reinitialize and quote_board.quote_date is not None:
            raise ValueError('quote board quote_date has been set - possible error in initialization')

        quote_board.set_time(new_time=self._last_msd, new_date=self._quote_date)
        self._quote_board_list.append(quote_board)
        root: str = quote_board.root
        date: int = quote_board.quote_date
        expiration_date_params: dict = quote_board.get_expiration_params()
        self.data_manager.update_expirations(root, date, expiration_date_params)
        updated_expirations = expiration_date_params.get('expirations')
        if updated_expirations is None:
            raise ValueError(
                'expiration dates have not been updated - error in function get_expirations in data manager')
        quote_board.set_expirations(updated_expirations)

        expirations = quote_board.get_expirations()
        for expiration in expirations:
            self.data_manager.request_open_stream(root, date, expiration, self.id, last_mds=self._last_msd)
            # data reader is opened for (root, quote_date, expiration) and read up to the last msd

        self._add_quote_board_to_root_quote_board_list_dict(root, quote_board)
        self._add_quote_board_to_dictionary(quote_board)

    def _check_initialized(self):
        if self._last_msd is None:
            raise ValueError('last msd has not been set')
        if self._quote_date is None:
            raise ValueError('quote quote_date has not been set')
        if self.data_manager is None:
            raise ValueError('data manager has not been set')
        if not self.is_connected():
            raise ValueError('data manager is not connected')

    # TODO: move this functionality to BacktestManager, which will be done in the future

    def _set_date_and_time(self, date: int, msd: int):
        self._set_quote_date(date)
        self._set_last_msd(msd)

    def _add_quote_board_to_root_quote_board_list_dict(self, root: str, quote_board: QuoteBoard):
        quote_board_list = self._root_quote_board_list_dict.get(root, [])
        quote_board_list.append(quote_board)
        self._root_quote_board_list_dict[root] = quote_board_list

    def _add_quote_board_to_dictionary(self, quote_board: QuoteBoard):
        root = quote_board.root
        expirations = quote_board.get_expirations()
        for expiration in expirations:
            self._quote_board_dict[(root, expiration)] = quote_board

    def _remove_quote_board_from_dict(self, quote_board: QuoteBoard):
        """Given a root and a list of expirations, remove the expirations from the qb_tree (key:root, value: dict(
        expiration - quote_board)"""
        root = quote_board.root
        expirations = quote_board.get_expirations()
        for expiration in expirations:
            self._quote_board_dict.pop((root, expiration))

    def _remove_quote_board_from_root_quote_board_list_dict(self, quote_board: QuoteBoard):
        root = quote_board.root
        quote_board_list = self._root_quote_board_list_dict.get(root, [])
        if quote_board in quote_board_list:
            quote_board_list.remove(quote_board)
            self._root_quote_board_list_dict[root] = quote_board_list

    def _sync_quote_board(self, sync_time: int, sync_date: int):
        # DONE: sync the quote board with the current quote_date and last msd
        for quote_board in self._quote_board_list:
            # Case1: quote board ran on a different quote_date and needs to be synced
            if quote_board.quote_date != sync_date:
                root = quote_board.root
                old_expirations = quote_board.get_expirations()
                old_date = quote_board.quote_date

                self.initialize_quote_board(quote_board, reinitialize=True)
                # reinitialize the quote board
                new_expirations = quote_board.get_expirations()

                # DONE: delete old reading stream
                for expiration in old_expirations:
                    self.data_manager.request_close_stream(root, old_date, expiration, self.id)
                self._remove_quote_board_from_dict(quote_board)

                # DONE: add new reading stream
                for expiration in new_expirations:
                    self.data_manager.request_open_stream(root, sync_date, expiration, self.id, last_mds=sync_time)
                self._add_quote_board_to_dictionary(quote_board)

            # Case2: quote board ran on a different time and needs to be synced
            if quote_board.last_msd != sync_time:
                quote_board.set_time(new_time=sync_time)
                root = quote_board.root
                date = quote_board.quote_date
                expirations = quote_board.get_expirations()
                for expiration in expirations:
                    self.data_manager.reset_stream(root=root, date=date, expiration=expiration,
                                                   quote_manager_id=self.id, sync_time=sync_time)

    def _configure_subscribed_quote_boards(self):
        """
        All quote boards should have been initialized;
        Configure the subscribed quote boards to the same timeline just in case they are not;
        """
        # TODO: Setting all the quote boards to the same timeline in the data manager
        self._check_initialized()

        for quote_board in self._quote_board_list:
            try:
                quote_board.is_initialized()
            except:
                raise ValueError('quote board has not been initialized; cannot configure the quote board')

        self._sync_quote_board(sync_time=self._last_msd, sync_date=self._quote_date)
        # sync the quote board with the current quote_date and last msd

    def _set_on_process(self, on_process: bool):
        self._on_process = on_process

    def _turn_on_process(self):
        self._set_on_process(True)

    def _done_process(self):
        self._set_on_process(False)

    def _get_on_process(self) -> bool:
        return self._on_process
