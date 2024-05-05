import unittest
from data_system.tracker.cores import QueuePipeline, QueueManager
from data_system.base_structure.deque import TimeDeque
from .test_time_node import TestTimeNode


class MyTestCase(unittest.TestCase):
    def test_pipeline(self):
        pipeline = QueuePipeline()
        q1 = TimeDeque(max_time=10)
        qm1 = QueueManager(q1)
        q1_meta = {
            "description": "This is the first queue",
            "domain": "test",
            "type": "time_deque",
            "max_time": 10,
        }
        q2 = TimeDeque(max_time=20)
        qm2 = QueueManager(q2)
        q2_meta = {
            "description": "This is the second queue",
            "domain": "test",
            "type": "time_deque",
            "max_time": 20,
        }
        pipeline.add_queue_manager(q_manager=qm1, meta=q1_meta)
        pipeline.add_queue_manager(q_manager=qm2, meta=q2_meta)

        for i in range(30):
            pipeline.inject(TestTimeNode.generate_random(i))
            pipeline.__display__(sequential=True)



if __name__ == "__main__":
    unittest.main()
