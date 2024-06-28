from collections import deque
from typing import Optional

from data_system.containers.cores._container import Container
from data_system.containers.cores.queue_manager import QueueManager
from data_system.base_structure.deque.acc_deque import AccDeque

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
        self._asset = kwargs.get("asset", None)

    @property
    def pipeline(self):
        return self._pipeline

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

    def inject(self, data, meta=None):  # v is the data being injected
        # if self._accumulated:
        #     self._accumulator.append(data)
        if len(self._pipeline) == 0:
            return
        self._pipeline[0].append(data)

    def __display__(self, sequential=False):
        for i, q in enumerate(self._pipeline):
            print(f"Queue {i}: {self._meta[q]}")
            q.__display__(sequential=sequential)
        print("End of Pipeline")

    def get_last_queue(self):
        if len(self._pipeline) == 0:
            return None
        return self._pipeline[-1]

    # def get_accumulated_size(self):
    #     if self._accumulator:
    #         return self._accumulator.size()
    #     print(self._accumulator)
    #     return 0

    # def print_acc_data(self):
    #     if self._accumulator:
    #         self._accumulator.set_display_sequential(True)
    #         print(self._accumulator)

    # def construct_accumulator(self):
    #     accumulator_queue = AccDeque()
    #     self._accumulator = accumulator_queue

    # @property
    # def accumulated(self):
    #     return self._accumulated
    #
    # @accumulated.setter
    # def accumulated(self, value):
    #     self._accumulated = value

    # @property
    # def accumulator(self):
    #     return self._accumulator
