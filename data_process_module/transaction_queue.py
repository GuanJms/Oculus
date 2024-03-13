from collections import deque
from typing import Optional, List

from configuration_module.configuration_manager import ConfigurationManager
from data_process_module.transaction import Transaction


class _TransactionQueueIterator:
    def __init__(self, queue: deque):
        self.queue = queue

    def __next__(self):
        if not self.queue:  # If the deque is empty
            raise StopIteration
        return self.queue.popleft()


class TransactionQueue:
    def __init__(self, default_sort: bool, sort_key: Optional[str] = None):
        self.queue = deque()
        self.default_sort = default_sort
        self.sort_key = sort_key
        self.max_size = ConfigurationManager.get_max_transaction_queue_size()

    def __iter__(self):
        return _TransactionQueueIterator(self.queue)

    # TODO: verify if the iteration process clears the queue; or its just a copy of the queue

    def add_transactions(self, transactions: List[Transaction], message_request: Optional[bool] = False):
        for transaction in transactions:
            self.queue.append(transaction)
        if self.default_sort:
            self._sort_queue(sort_key=self.sort_key)
        if message_request:
            if len(self.queue) > self.max_size:
                return "PROCESS-QUEUE-REQUEST"
    def __len__(self):
        return len(self.queue)

    def sort(self):
        self._sort_queue(sort_key=self.sort_key)

    def _sort_queue(self, sort_key: str):
        if sort_key == ConfigurationManager.get_MSD_COL_NAME():
            self.queue = deque(sorted(self.queue, key=lambda x: x.ms_of_day))
        else:
            try:
                self.queue = deque(sorted(self.queue, key=lambda x: getattr(x, sort_key)))
            except AttributeError:
                raise ValueError('sort_key not supported')

    def empty(self) -> bool:
        return len(self.queue) == 0

    def next(self) -> Optional[Transaction]:
        return self.queue.popleft()
