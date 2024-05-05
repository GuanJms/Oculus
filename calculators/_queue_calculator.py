from abc import ABC, abstractmethod
from collections import deque


class QueueCalculator:

    def __init__(self):
        self._queue = deque()

    def add(self, data):
        self._queue.append(data)

    def remove(self, data):
        self._queue.remove(data)
