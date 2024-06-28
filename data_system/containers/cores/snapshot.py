from data_system.containers.cores import QueueManager
from data_system.containers.cores._container import Container
from data_system.base_structure.deque import MaximumLengthDeque


class Snapshot(Container):
    def __init__(self, **kwargs):
        size = kwargs.get("size", 1)
        description = kwargs.get("description", "Snapshot container.")
        super().__init__(description=description)
        self.snapshot_queue = MaximumLengthDeque(size)
        self._snapshot_data = QueueManager(
            queue=self.snapshot_queue
        )  # This is for calculators

    def get_snapshot(self):
        N = self.snapshot_queue.size()
        data = [self.snapshot_queue.get(i) for i in range(N)]
        return data

    def inject(self, data, meta=None):
        self._snapshot_data.add(data)
        # print("Snapshot: ", data)