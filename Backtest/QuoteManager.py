from DataProcess.TransactionQueue import TransactionQueue

"""
Queue manager is the class that manages the quote boards and the transaction queue
It takes in a data manager and a frequency to update the quote boards.
Based on the frequency, it will request data from the data manager and process the data stream and push the data to the 
subscribed quote boards with corresponding roots.
"""

class QuoteManager:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.quote_boards = []
        self.frequency = 60000
        self.transaction_queue = TransactionQueue()
        self.subscribed_quote_boards = []
        self.subscribed_quote_board_by_root = {}
        self.last_msd = None
        self.quote_date = None

    def set_current_date(self, date, reset_msd=True, default_msd=34200000):
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

    def set_frequency(self, frequency):
        self.frequency = frequency

    def test_once(self, total=None):
        if total is None:
            total = self.frequency
        start_msd = self.last_msd
        transactions = self._request_data(start_msd=start_msd,
                                          end_msd=start_msd + total,
                                          roots=self.subscribed_quote_board_by_root.keys(),
                                          date=self.quote_date)
        self.transaction_queue.add_transactions(transactions)

    def _request_data(self, start_msd, end_msd, roots, date):
        # TODO: request data from the data manager
        transactions = self.data_manager.request_data(start_msd, end_msd, roots, date)
        return transactions

    def _get_transaction_queue(self):
        return self.transaction_queue

    def process_queue(self):
        while not self.transaction_queue.empty():
            transaction = self.transaction_queue.next()
            self._process_transaction(transaction)

    def _process_transaction(self, transaction):
        root = transaction.get_root()
        quote_boards = self.subscribed_quote_board_by_root.get(root, [])
        if len(quote_boards) == 0:
            return
        for quote_board in quote_boards:
            quote_board.update_quote(transaction)

    def add_quote_board(self, quote_board):
        self.quote_boards.append(quote_board)
        self.subscribed_quote_boards.append(quote_board)
        root = quote_board.get_root()
        root_quote_board = self.subscribed_quote_board_by_root.get(root, [])

        if not QuoteManager.check_existed_quote_board(quote_board, root_quote_board):
            root_quote_board.append(quote_board)
            self.subscribed_quote_board_by_root[root] = root_quote_board

    def remove_quote_board(self, quote_board):
        # TODO: remove the quote board from the subscribed quote boards and quote boards list
        pass

    @classmethod
    def check_existed_quote_board(cls, quote_board, quote_boards):
        for board in quote_boards:
            if board == quote_board:
                return True
        return False
