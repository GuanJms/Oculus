from collections import deque
class TransactionQueue:
    def __init__(self, default_sort = True):
        self.queue = deque()
        self.default_sort = default_sort

    class _TransactionQueueIterator:
        def __init__(self, queue):
            self.queue = queue

        def __next__(self):
            if not self.queue:  # If the deque is empty
                raise StopIteration
            return self.queue.popleft()

    def __iter__(self):
        return TransactionQueue._TransactionQueueIterator(self.queue)

    def add_transactions(self, transactions):
        for transaction in transactions:
            self.queue.append(transaction)
        if self.default_sort:
            self._sort_queue()

    def __len__(self):
        return len(self.queue)

    def _sort_queue(self, sort_key = 'ms_of_day'):
        if sort_key == 'ms_of_day':
            self.queue = deque(sorted(self.queue, key = lambda x: getattr(x, sort_key)))
        else:
            raise ValueError('sort_key not supported')

    def empty(self):
        return len(self.queue) == 0

    def next(self):
        return self.queue.popleft()




    


