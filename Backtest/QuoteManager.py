from Backtest.QuoteBoard import QuoteBoard
from DataProcess.Transaction import Transaction
from DataProcess.TransactionQueue import TransactionQueue
from DataProcess.TradedQuoteDataManager import TradedQuoteDataManager
from typing import List, Optional

"""
Queue manager is the class that manages the quote boards and the transaction queue
It takes in a data manager and a frequency to update the quote boards.
Based on the frequency, it will request data from the data manager and process the data stream and push the data to the 
subscribed quote boards with corresponding roots.
"""


def _aggregate_sync_request_params_to_list(sync_request_list: list, root: str, date: int, sync_time: int, expiration: int):
    # DONE: aggregate the sync request params to the sync_request_params with key (root, date)
    new_request_params = {'root': root,
                          'date': date,
                          'expiration': expiration,
                          'sync_time': sync_time}
    sync_request_list.append(new_request_params)


class QuoteManager:
    def __init__(self, MSD_COL_NAME: str,frequency: int = 60000):
        self.backtest_end_msd: Optional[int] = None
        self.backtest_start_msd: Optional[int] = None
        self.backtest_end_date: Optional[int] = None
        self.backtest_start_date: Optional[int] = None
        self.id = id(self)
        self.data_manager: Optional[TradedQuoteDataManager] = None
        self.quote_boards: List[QuoteBoard] = []
        self.frequency: int = frequency
        self.MSD_COL_NAME = MSD_COL_NAME
        self.transaction_queue: TransactionQueue = TransactionQueue(sort_key=MSD_COL_NAME)
        self.subscribed_quote_boards: List[QuoteBoard] = []
        self.qb_diclist: dict = {}
        # qb_diclist is a dictionary (key: root, value is List[QuoteBoard])
        self.qb_tree: dict = {}


        self.last_msd: Optional[int] = None
        self.quote_date: Optional[int] = None
        self.expiration_params: Optional[dict] = None
        self.subscribed_roots: Optional[List[str]] = None


    def is_connected(self) -> bool:
        if self.data_manager is None:
            return False
        elif not self.data_manager.is_connected():
            return False
        return True

    def connect_data_manager(self, data_manager: TradedQuoteDataManager):
        # Check if data_manager is TradedQuoteDataManager
        if not isinstance(data_manager, TradedQuoteDataManager):
            raise ValueError('data_manager must be TradedQuoteDataManager')
        self.data_manager = data_manager
        data_manager.connect(self)


    def set_quote_date(self, date: int):
        if not isinstance(date, int):
            raise ValueError('date must be int')
        self.quote_date = date

    def set_last_msd(self, msd: int):
        if not isinstance(msd, int):
            raise ValueError('msd must be int')
        self.last_msd = msd


    def set_frequency(self, frequency: int):
        self.frequency = frequency

    def _configure_subscribed_quote_boards(self):
        """
        All quote boards should have been initialized;
        Configure the subscribed quote boards to the same timeline just in case they are not;
        """
        # TODO: Setting all the quote boards to the same timeline in the data manager
        self._check_initialized()

        for quote_board in self.subscribed_quote_boards:
            try: quote_board.is_initailized()
            except: raise ValueError('quote board has not been initialized; cannot configure the quote board')

        self._sync_quote_board(sync_time=self.last_msd, sync_date=self.quote_date)
        # sync the quote board with the current date and last msd

        if self.subscribed_roots is None:
            self.subscribed_roots = list(self.qb_diclist.keys())
        if self.expiration_params is None:
            self.expiration_params = {}
            for quote_board in self.subscribed_quote_boards:

    def _configure(self):
        if not self.is_connected():
            raise ValueError('data manager is not connected')
        self._configure_subscribed_quote_boards()

    def run_once(self, delta_time_ms: int = None):

        if delta_time_ms is None:
            delta_time_ms = self.frequency
        start_msd = self.last_msd
        end_msd = start_msd + delta_time_ms

        transactions = []
        for root in self.subscribed_roots:
            root_expiration_params = self.expiration_params.get(root, None)
            transactions += self._request_data(start_msd=start_msd,
                                                end_msd=end_msd,
                                                root=root,
                                                date=self.quote_date, expiration_params = root_expiration_params)
        self.transaction_queue.add_transactions(transactions)

    def _request_data(self, start_msd: int, end_msd: int, root: str, date: int, expiration_params: Optional[dict]) \
            -> List[Transaction]:
        # TODO: request data from the data manager
        transactions_raw = self.data_manager.request_data(start_msd = start_msd,
                                                          end_msd = end_msd,
                                                          root = root,
                                                          date = date,
                                                          expiration_params = expiration_params)
        transactions = Transaction.process_raw_transactions(transactions_raw)
        return transactions

    def _get_transaction_queue(self) -> TransactionQueue:
        return self.transaction_queue

    def process_queue(self):
        while not self.transaction_queue.empty():
            transaction = self.transaction_queue.next()
            self._process_transaction(transaction)

    def _process_transaction(self, transaction: Transaction):
        root = transaction.get_root()
        quote_boards = self.qb_diclist.get(root, [])
        if len(quote_boards) == 0:
            return
        for quote_board in quote_boards:
            quote_board.update_quote(transaction)

    def add_quote_board(self, quote_board: QuoteBoard):

        try:self._check_initialized()
        except: raise ValueError('Make sure the data manager is connected before adding quote board')

        quote_board.check_valid_to_initialize()
        self.quote_boards.append(quote_board)
        self.subscribed_quote_boards.append(quote_board)
        root = quote_board.get_root()

        if not QuoteManager.check_existed_quote_board(quote_board, quote_boards=self.subscribed_quote_boards):
            self._initialize_quote_board(quote_board)
            self._add_qb_diclist(root, quote_board)
            expirations_to_add: List[int] = quote_board.get_expirations()
            self._add_exps_to_qb_tree(root, expirations_to_add, quote_board)

    def _add_qb_diclist(self, root: str, quote_board: QuoteBoard):
        root_qbs = self.qb_diclist.get(root, [])
        root_qbs.append(quote_board)
        self.qb_diclist[root] = root_qbs

    def _add_exps_to_qb_tree(self, root: str, expirations: List[int], quote_board: QuoteBoard):
        exp_links = self.qb_tree.get(root, {})
        for expiration in expirations:
            qb_list = exp_links.get(expiration, [])
            qb_list.append(quote_board)
            exp_links[expiration] = qb_list
        self.qb_tree[root] = exp_links

    def _remove_exps_from_qb_tree(self, root: str, expirations: List[int], quote_board: QuoteBoard):
        """Given a root and a list of expirations, remove the expirations from the qb_tree (key:root, value: dict(expiration - quote_board)"""
        exp_links = self.qb_tree.get(root, {})
        for expiration in expirations:
            qb_list = exp_links.get(expiration, [])
            if quote_board in qb_list:
                qb_list.remove(quote_board)
            exp_links[expiration] = qb_list
        self.qb_tree[root] = exp_links





    def get_subscribed_quote_boards(self):
        return self.subscribed_quote_boards
    def remove_quote_board(self, quote_board: QuoteBoard):
        # TODO: remove the quote board from the subscribed quote boards and quote boards list
        raise NotImplementedError

    @classmethod
    def check_existed_quote_board(cls, quote_board: QuoteBoard, quote_boards: List[QuoteBoard]):
        # TODO: assign unique ID to the quote board every time it is created, and check uniqueness based on the ID
        return quote_board in quote_boards

    def get_min_last_msd_in_quote_boards(self):
        # DONE: get the minimum ms_of_day in the ms_of_day_range of the quote boards
        min_msd = None
        for quote_board in self.quote_boards:
            last_msd = quote_board.get_last_msd()
            if min_msd is None or last_msd < min_msd:
                min_msd = last_msd
        return min_msd

    def get_min_date_in_quote_boards(self):
        min_date = None
        for quote_board in self.quote_boards:
            start_date = quote_board.get_date()
            if min_date is None or start_date < min_date:
                min_date = start_date
        return min_date

    def _sync_quote_board(self, sync_time: int , sync_date: int):
        # DONE: sync the quote board with the current date and last msd
        for quote_board in self.quote_boards:
            # Case1: quote board ran on a different date and needs to be synced
            if quote_board.get_date()!= sync_date:
                root = quote_board.get_root()
                old_expirations = quote_board.get_expirations()
                old_date = quote_board.get_date()

                self._initialize_quote_board(quote_board, reinitialize=True)
                # reinitialize the quote board
                new_expirations = quote_board.get_expirations()

                #DONE: delete old reading stream
                for expiration in old_expirations:
                    self.data_manager.close_stream(root, old_date, expiration, self.id)
                self._remove_exps_from_qb_tree(root, old_expirations, quote_board)

                #DONE: add new reading stream
                for expiration in new_expirations:
                    self.data_manager.open_stream(root, sync_date, expiration, self.id, last_mds=sync_time)
                self._add_exps_to_qb_tree(root, new_expirations, quote_board)

            # Case2: quote board ran on a different time and needs to be synced
            if quote_board.get_last_msd() != sync_time:
                quote_board.set_time(new_time=sync_time)
                root = quote_board.get_root()
                date = quote_board.get_date()
                expirations = quote_board.get_expirations()
                for expiration in expirations:
                    self.data_manager.reset_stream(root=root,date=date,expiration=expiration,
                                                   quote_manager_id=self.id, sync_time=sync_time)

    def _initialize_quote_board(self, quote_board: QuoteBoard, reinitialize: bool = False):
        # DONE: pathing the quote board to get the expirations and initialize the expirations in the quote board
        self._check_initialized()
        quote_board.check_valid_to_initialize()
        if not reinitialize and quote_board.get_date() is not None:
            raise ValueError('quote board date has been set - possible error in initialization')

        quote_board.set_time(new_time=self.last_msd, new_date=self.quote_date)
        root: str = quote_board.get_root()
        date: int = quote_board.get_date()
        expiration_date_params:dict = quote_board.get_expiration_params()
        self.data_manager.get_expirations(root, date, expiration_date_params, self.id)
        updated_expirations = expiration_date_params.get('expirations')
        if updated_expirations is None:
            raise ValueError('expiration dates have not been updated - error in function get_expirations in data manager')
        quote_board.set_expirations(updated_expirations)

        expirations = quote_board.get_expirations()
        for expiration in expirations:
            self.data_manager.open_stream(root, date, expiration, self.id, last_mds=self.last_msd)
            # data reader is opened for (root, date, expiration) and read up to the last msd


    def _check_initialized(self):
        if self.last_msd is None:
            raise ValueError('last msd has not been set')
        if self.quote_date is None:
            raise ValueError('quote date has not been set')
        if self.data_manager is None:
            raise ValueError('data manager has not been set')
        if not self.is_connected():
            raise ValueError('data manager is not connected')

    def set_backtest_params(self, backtest_setting_params: dict[str, int]):
        """" e.g. backtest_setting_params ={
            'backtest_start_date' : 20240101,
            'backtest_end_date': 20240201,
            'frequency' : 60000}
        """
        self.backtest_start_date = backtest_setting_params.get('backtest_start_date')
        self.backtest_end_date = backtest_setting_params.get('backtest_end_date')
        self.frequency = backtest_setting_params.get('frequency')
        self.backtest_start_msd = backtest_setting_params.get('backtest_start_msd')
        self.backtest_end_msd = backtest_setting_params.get('backtest_end_msd')

        if self.backtest_start_date is None:
            raise ValueError('backtest_start_date has not been set')
        if self.frequency is None:
            raise ValueError('frequency has not been set')


    def initialize(self):
        # TODO: initialize the quote manager with the backtest params epsecially with the start date and last_msd
        #  last_msd should comes the ms_of_day range from the backtest params
        self.set_quote_date(date=self.backtest_start_date)
        self.set_last_msd(msd = self.backtest_start_msd)




        








