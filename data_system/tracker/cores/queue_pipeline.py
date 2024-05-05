from collections import deque

from data_system.tracker.cores._container import Container
from data_system.tracker.cores.queue_manager import QueueManager

"""
This class is composed of multiple queue that is attached to each other. 
Base functionality should include 
    - Add and delete the queue.
    - Managing between the queue (tail structure)
"""


class QueuePipeline(Container):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._pipeline = deque()
        self._meta = {}

    def add_queue_manager(self, q_manager, meta=None):
        if meta is None:
            meta = {}
        prev_q: QueueManager = self._pipeline[-1] if len(self._pipeline) != 0 else None
        self._pipeline.append(q_manager)
        if prev_q:
            prev_q.add_tail_queue(q_manager)
        self._meta[q_manager] = meta

    def remove_queue_manager(self, q_manager):
        try:
            self._pipeline.remove(q_manager)
        except ValueError:
            print("Value not found in the deque")

    def inject(self, data):  # v is the data being injected
        self._pipeline[0].add(data)

    def __display__(self, sequential=False):
        for i, q in enumerate(self._pipeline):
            print(f"Queue {i}: {self._meta[q]}")
            q.__display__(sequential=sequential)
        print("End of Pipeline")

