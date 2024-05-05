import unittest
from data_system.tracker.builders import QueuePipelineBuilder
from data_system.tracker.cores import QueuePipeline

class TestQueuePipelineBuilder(unittest.TestCase):
    def test_build(self):
        builder = QueuePipelineBuilder()
        p = QueuePipeline()



if __name__ == "__main__":
    unittest.main()
