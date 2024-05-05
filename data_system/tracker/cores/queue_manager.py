from collections import deque


class QueueManager:
    def __init__(self, queue):
        self._queue = queue
        self._append_subs = deque()
        self._remove_subs = deque()
        self._state_change_subs = deque()
        self._tail_queues = deque()

    def subscribe_to_appends(self, calculator):
        self._append_subs.append(calculator)

    def subscribe_to_removals(self, calculator):
        self._remove_subs.append(calculator)

    def subscribe_to_state_change(self, calculator):
        self._state_change_subs.append(calculator)

    def add(self, data):
        for calculator in self._append_subs:
            calculator.add(data)
        dropped_data = self._queue.append(data)
        for datum in dropped_data:
            for calculator in self._remove_subs:
                calculator.remove(datum)
        for datum in dropped_data:
            for tail_q in self._tail_queues:
                tail_q.add(datum)
        for calculator in self._state_change_subs:
            calculator.state_change(self._queue)

    def add_tail_queue(self, tail_q):
        self._tail_queues.append(tail_q)

    def __display__(self, sequential=False):
        self._queue.set_display_sequential(sequential)
        print(f"Queue: {self._queue}")
