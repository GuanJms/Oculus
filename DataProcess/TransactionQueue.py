from collections import deque
from typing import Optional, List

from DataProcess.Transaction import Transaction


class TransactionQueue:
    def __init__(self, default_sort: bool = True, sort_key: Optional[str] = None):
        self.queue = deque()
        self.default_sort = default_sort
        self.sort_key = sort_key

    class _TransactionQueueIterator:
        def __init__(self, queue):
            self.queue = queue

        def __next__(self):
            if not self.queue:  # If the deque is empty
                raise StopIteration
            return self.queue.popleft()

    def __iter__(self):
        return TransactionQueue._TransactionQueueIterator(self.queue)

    def add_transactions(self, transactions: List[Transaction]):
        for transaction in transactions:
            self.queue.append(transaction)
        if self.default_sort:
            self._sort_queue(sort_key = self.sort_key)

    def __len__(self):
        return len(self.queue)

    def _sort_queue(self, sort_key: str):
        try:
            self.queue = deque(sorted(self.queue, key = lambda x: getattr(x, sort_key)))
        except AttributeError:
            raise ValueError('sort_key not supported')

    def empty(self):
        return len(self.queue) == 0

    def next(self):
        return self.queue.popleft()




    


