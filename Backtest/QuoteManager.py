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

class QuoteManager:
    def __init__(self, MSD_COL_NAME: str = 'ms_of_day',frequency: int = 60000):
        self.data_manager: Optional[TradedQuoteDataManager] = None
        self.quote_boards: List[QuoteBoard] = []
        self.frequency: int = frequency
        self.MSD_COL_NAME = MSD_COL_NAME
        self.transaction_queue: TransactionQueue = TransactionQueue(sort_key=MSD_COL_NAME)
        self.subscribed_quote_boards: List[QuoteBoard] = []
        self.subscribed_quote_board_by_root: dict = {}
        self.last_msd: Optional[int] = None
        self.quote_date: Optional[int] = None
        self._ready_to_run: bool = False
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


    def set_current_date(self, date: int, reset_msd: bool=True, default_msd: int=34200000):
        """
        set the current date of the quote manager to the date
        and default the last msd run to the default msd if reset_msd is True
        Defualt msd is 9:30 am
        :param date: int
        :param reset_msd: bool
        :param default_msd: ms_of_day
        :return:
        """
        # check if date is int
        if not isinstance(date, int):
            # try to convert to int
            try:
                date = int(date)
            except:
                raise ValueError('date must be int')
        self.quote_date = date
        if reset_msd:
            self.last_msd = default_msd

    def set_frequency(self, frequency: int):
        self.frequency = frequency

    def configure_subscribed_quote_boards(self):
        if self.last_msd is None:
            self.last_msd = self.get_min_msd_in_quote_boards()
        if self.quote_date is None:
            self.quote_date = self.get_min_date_in_quote_boards()
        if self.subscribed_roots is None:
            self.subscribed_roots = list(self.subscribed_quote_board_by_root.keys())
        if self.expiration_params is None:
            self.expiration_params = {}
            for quote_board in self.subscribed_quote_boards:



        self._ready_to_run = True



    def run_once(self, delta_time_ms: int = None):
        if not self._ready_to_run:
            self.configure_subscribed_quote_boards()

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
        quote_boards = self.subscribed_quote_board_by_root.get(root, [])
        if len(quote_boards) == 0:
            return
        for quote_board in quote_boards:
            quote_board.update_quote(transaction)

    def add_quote_board(self, quote_board: QuoteBoard):
        self.quote_boards.append(quote_board)
        self.subscribed_quote_boards.append(quote_board)
        root = quote_board.get_root()
        root_quote_board = self.subscribed_quote_board_by_root.get(root, [])

        if not QuoteManager.check_existed_quote_board(quote_board, root_quote_board):
            root_quote_board.append(quote_board)
            self.subscribed_quote_board_by_root[root] = root_quote_board

    def get_subscribed_quote_boards(self):
        return self.subscribed_quote_boards
    def remove_quote_board(self, quote_board: QuoteBoard):
        # TODO: remove the quote board from the subscribed quote boards and quote boards list
        pass

    @classmethod
    def check_existed_quote_board(cls, quote_board: QuoteBoard, quote_boards: List[QuoteBoard]):
        for board in quote_boards:
            if board == quote_board:
                return True
        return False

    def get_min_msd_in_quote_boards(self):
        # TODO: get the minimum ms_of_day in the ms_of_day_range of the quote boards
        min_msd = None
        for quote_board in self.quote_boards:
            start_msd = quote_board.get_min_ms_of_day()
            if min_msd is None or start_msd < min_msd:
                min_msd = start_msd
        return min_msd

    def get_min_date_in_quote_boards(self):
        min_date = None
        for quote_board in self.quote_boards:
            start_date = quote_board.get_start_date()
            if min_date is None or start_date < min_date:
                min_date = start_date
        return min_date

